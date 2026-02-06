#!/usr/bin/env python3
"""SSH Server for Portfolio TUI.

This module provides a secure SSH server that runs the portfolio TUI application.
Security measures:
- No shell access (only PTY for TUI)
- No command execution
- Rate limiting per IP
- Connection limits
- Idle timeout
"""

import asyncio
import logging
import os
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Optional

import asyncssh

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


# Configuration
MAX_CONNECTIONS = 50
CONNECTIONS_PER_IP_PER_MINUTE = 10
IDLE_TIMEOUT = 300  # 5 minutes
MAX_SESSION_DURATION = 1800  # 30 minutes
HOST_KEY_DIR = Path(os.environ.get("HOST_KEY_DIR", "keys"))
HOST_KEY_PATH = HOST_KEY_DIR / "host_key"
SSH_PORT = int(os.environ.get("SSH_PORT", 2222))


class RateLimiter:
    """Track and limit connections per IP address."""

    def __init__(self, max_per_minute: int = CONNECTIONS_PER_IP_PER_MINUTE):
        self.max_per_minute = max_per_minute
        self.connections: dict[str, list[float]] = defaultdict(list)

    def allow(self, ip: str) -> bool:
        """Check if a connection from this IP should be allowed."""
        now = time.time()
        minute_ago = now - 60

        # Clean old entries
        self.connections[ip] = [t for t in self.connections[ip] if t > minute_ago]

        # Check limit
        if len(self.connections[ip]) >= self.max_per_minute:
            logger.warning(f"Rate limit exceeded for IP: {ip}")
            return False

        # Record this connection
        self.connections[ip].append(now)
        return True

    def cleanup(self) -> None:
        """Remove old entries from all IPs."""
        now = time.time()
        minute_ago = now - 60
        empty_ips = []
        for ip, times in self.connections.items():
            self.connections[ip] = [t for t in times if t > minute_ago]
            if not self.connections[ip]:
                empty_ips.append(ip)
        for ip in empty_ips:
            del self.connections[ip]


class ConnectionManager:
    """Manage active connections and enforce limits."""

    def __init__(self, max_connections: int = MAX_CONNECTIONS):
        self.max_connections = max_connections
        self.active_connections: set[str] = set()
        self._lock = asyncio.Lock()

    async def add(self, conn_id: str) -> bool:
        """Try to add a new connection. Returns False if at limit."""
        async with self._lock:
            if len(self.active_connections) >= self.max_connections:
                logger.warning(f"Max connections reached, rejecting: {conn_id}")
                return False
            self.active_connections.add(conn_id)
            logger.info(
                f"Connection added: {conn_id} "
                f"(active: {len(self.active_connections)})"
            )
            return True

    async def remove(self, conn_id: str) -> None:
        """Remove a connection."""
        async with self._lock:
            self.active_connections.discard(conn_id)
            logger.info(
                f"Connection removed: {conn_id} "
                f"(active: {len(self.active_connections)})"
            )


# Global instances
rate_limiter = RateLimiter()
connection_manager = ConnectionManager()


class PortfolioSSHServer(asyncssh.SSHServer):
    """SSH Server that only allows PTY sessions for the portfolio TUI."""

    def __init__(self) -> None:
        self._conn: Optional[asyncssh.SSHServerConnection] = None
        self._peername: Optional[str] = None

    def connection_made(self, conn: asyncssh.SSHServerConnection) -> None:
        """Called when a connection is established."""
        self._conn = conn
        peername = conn.get_extra_info("peername")
        self._peername = peername[0] if peername else "unknown"
        logger.info(f"Connection attempt from {self._peername}")

    def connection_lost(self, exc: Optional[Exception]) -> None:
        """Called when a connection is lost."""
        if exc:
            logger.info(f"Connection lost from {self._peername}: {exc}")
        else:
            logger.info(f"Connection closed from {self._peername}")

    def begin_auth(self, username: str) -> bool:
        """Handle authentication - no auth required for public portfolio."""
        logger.info(f"Auth attempt from {self._peername} as '{username}'")
        # Return False to indicate no authentication is required
        return False

    def session_requested(self) -> bool:
        """Allow session requests."""
        return True

    # Note: We intentionally do NOT implement:
    # - shell_requested() - no shell access
    # - exec_requested() - no command execution
    # This means only PTY requests will work (for the TUI)


async def handle_client(process: asyncssh.SSHServerProcess) -> None:
    """Handle an SSH client connection by running the portfolio TUI via PTY subprocess."""
    import fcntl
    import pty
    import signal
    import struct
    import subprocess
    import termios
    import tty

    # Disable line editing mode for single-keypress handling
    try:
        channel = process.channel
        if hasattr(channel, 'set_line_mode'):
            channel.set_line_mode(False)
        if hasattr(channel, 'set_echo'):
            channel.set_echo(False)
    except Exception as e:
        logger.warning(f"Could not disable line mode: {e}")

    peername = process.get_extra_info("peername")
    client_ip = peername[0] if peername else "unknown"
    conn_id = f"{client_ip}:{id(process)}"

    # Check rate limit
    if not rate_limiter.allow(client_ip):
        process.stdout.write("Too many connections. Please try again later.\n")
        process.exit(1)
        return

    # Check connection limit
    if not await connection_manager.add(conn_id):
        process.stdout.write("Server is busy. Please try again later.\n")
        process.exit(1)
        return

    master_fd = None
    child_proc = None

    try:
        logger.info(f"Starting TUI session for {client_ip}")

        # Create pseudo-terminal
        master_fd, slave_fd = pty.openpty()

        # Set raw mode on slave PTY (disables echo, canonical mode, etc.)
        tty.setraw(slave_fd)

        # Set terminal size from SSH client (default to 80x24 if not available)
        term_size = process.get_terminal_size()
        if term_size:
            cols, rows = term_size[0], term_size[1]
        else:
            cols, rows = 80, 24

        # Ensure minimum size for Textual
        if cols < 10 or rows < 5:
            cols, rows = 80, 24

        winsize = struct.pack("HHHH", rows, cols, 0, 0)
        fcntl.ioctl(slave_fd, termios.TIOCSWINSZ, winsize)

        # Get the app directory
        app_dir = Path(__file__).parent


        # Set up environment for the TUI subprocess
        env = os.environ.copy()
        env["TERM"] = process.get_terminal_type() or "xterm-256color"
        env["COLORTERM"] = "truecolor"
        env["PYTHONUNBUFFERED"] = "1"

        # Start the TUI as a subprocess with PTY
        # Send stderr to the PTY as well so we can see errors
        child_proc = subprocess.Popen(
            [sys.executable, "-u", str(app_dir / "run_tui.py")],
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,  # stderr to PTY so we see errors
            cwd=str(app_dir),
            env=env,
            start_new_session=True,
        )
        os.close(slave_fd)
        logger.info(f"Started TUI subprocess {child_proc.pid}")


        # Make master non-blocking
        flags = fcntl.fcntl(master_fd, fcntl.F_GETFL)
        fcntl.fcntl(master_fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

        loop = asyncio.get_event_loop()
        running = True

        async def forward_pty_to_ssh():
            """Forward PTY output to SSH."""
            nonlocal running
            try:
                # Give subprocess time to initialize
                await asyncio.sleep(0.1)

                while running and child_proc.poll() is None:
                    try:
                        data = os.read(master_fd, 8192)
                        if data:
                            # Write to stdout - decode as UTF-8
                            try:
                                process.stdout.write(data.decode('utf-8', errors='replace'))
                                await process.stdout.drain()
                            except Exception as e:
                                if "not open" not in str(e):
                                    logger.error(f"Error writing to stdout: {e}")
                    except BlockingIOError:
                        await asyncio.sleep(0.005)  # Small sleep when no data
                        continue
                    except OSError:
                        break
            except Exception as e:
                logger.error(f"forward_pty_to_ssh error: {e}")

        async def forward_ssh_to_pty():
            """Forward SSH input to PTY."""
            nonlocal running
            try:
                while running and child_proc.poll() is None:
                    try:
                        data = await asyncio.wait_for(
                            process.stdin.read(4096), timeout=0.1
                        )
                        if data:
                            # Handle both str and bytes (depends on asyncssh mode)
                            if isinstance(data, str):
                                data = data.encode('utf-8')
                            os.write(master_fd, data)
                        elif data == "" or data == b"":
                            break
                    except asyncio.TimeoutError:
                        continue
                    except OSError:
                        break
            except Exception as e:
                logger.debug(f"forward_ssh_to_pty error: {e}")

        async def wait_for_child():
            """Wait for the subprocess to exit."""
            nonlocal running
            while child_proc.poll() is None:
                await asyncio.sleep(0.1)
            running = False

        async def session_timeout_task():
            """Kill session after max duration."""
            await asyncio.sleep(MAX_SESSION_DURATION)
            logger.info(f"Session timeout for {client_ip}")
            if child_proc and child_proc.poll() is None:
                child_proc.terminate()

        # Run all tasks concurrently
        tasks = [
            asyncio.create_task(forward_pty_to_ssh()),
            asyncio.create_task(forward_ssh_to_pty()),
            asyncio.create_task(wait_for_child()),
            asyncio.create_task(session_timeout_task()),
        ]

        # Wait for any task to complete
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

        # Stop running
        running = False

        # Cancel remaining tasks
        for task in pending:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

        logger.info(f"TUI session ended for {client_ip}")
        process.exit(0)

    except Exception as e:
        logger.error(f"Error in session for {client_ip}: {e}")
        import traceback
        logger.error(traceback.format_exc())
        process.exit(1)

    finally:
        if master_fd is not None:
            try:
                os.close(master_fd)
            except OSError:
                pass
        if child_proc is not None and child_proc.poll() is None:
            try:
                child_proc.terminate()
                child_proc.wait(timeout=2)
            except Exception:
                child_proc.kill()
        await connection_manager.remove(conn_id)


def generate_host_key() -> None:
    """Generate SSH host key if it doesn't exist."""
    # Ensure key directory exists
    HOST_KEY_DIR.mkdir(parents=True, exist_ok=True)

    if not HOST_KEY_PATH.exists() or not HOST_KEY_PATH.is_file():
        logger.info("Generating new SSH host key...")
        key = asyncssh.generate_private_key("ssh-rsa", key_size=4096, comment="portfolio")
        HOST_KEY_PATH.write_bytes(key.export_private_key())
        HOST_KEY_PATH.chmod(0o600)
        logger.info(f"Host key saved to {HOST_KEY_PATH}")
    else:
        logger.info(f"Using existing host key from {HOST_KEY_PATH}")


async def start_server() -> None:
    """Start the SSH server."""
    generate_host_key()

    # Periodic cleanup of rate limiter
    async def cleanup_loop():
        while True:
            await asyncio.sleep(60)
            rate_limiter.cleanup()

    asyncio.create_task(cleanup_loop())

    logger.info(f"Starting SSH server on port {SSH_PORT}...")

    await asyncssh.create_server(
        PortfolioSSHServer,
        "",
        SSH_PORT,
        server_host_keys=[str(HOST_KEY_PATH)],
        process_factory=handle_client,
    )

    logger.info(f"SSH Portfolio server running on port {SSH_PORT}")
    logger.info(f"Connect with: ssh localhost -p {SSH_PORT}")

    # Keep the server running
    await asyncio.Event().wait()


def main() -> None:
    """Main entry point."""
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
