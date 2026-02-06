#!/usr/bin/env python3
"""Simple TUI for portfolio using Rich with scrollable content."""
import os
import sys
from pathlib import Path
from io import StringIO

# Change to the app directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
import tty
import termios

CONTENT_DIR = Path(__file__).parent / "content"
TABS = ["about", "backend", "devops", "frontend", "security", "others"]
TAB_NAMES = ["About", "Backend", "DevOps", "Frontend", "Security", "Others"]


def load_content(name: str) -> str:
    """Load markdown content from file."""
    content_file = CONTENT_DIR / f"{name}.md"
    if content_file.exists():
        return content_file.read_text()
    return f"# {name.title()}\n\nContent coming soon..."


def render_content_to_lines(console: Console, content: str) -> list[str]:
    """Render markdown content to a list of lines."""
    # Create a string buffer to capture output
    string_io = StringIO()
    temp_console = Console(file=string_io, width=console.width - 4, force_terminal=True)
    md = Markdown(content)
    temp_console.print(md)
    rendered = string_io.getvalue()
    return rendered.split('\n')


def render_screen(console: Console, current_tab: int, scroll_pos: int, content_lines: list[str]) -> int:
    """Render the full screen with scrollable content. Returns max scroll position."""
    console.clear()

    width = console.width
    height = console.height

    # Fixed header (3 lines: panel top, text, panel bottom)
    header = Text("Arvind's Portfolio", style="bold white on blue", justify="center")
    console.print(Panel(header, style="blue"))

    # Tab bar (1 line)
    tab_line = Text()
    for i, name in enumerate(TAB_NAMES):
        if i == current_tab:
            tab_line.append(f" [{name}] ", style="bold white on green")
        else:
            tab_line.append(f"  {name}  ", style="white on dark_blue")
    console.print(tab_line)
    console.print()

    # Calculate content area height
    # Header panel: 3 lines, tab bar: 1 line, empty line: 1, footer panel: 3 lines, scroll indicator: 1
    fixed_lines = 9
    content_height = max(height - fixed_lines, 5)

    # Calculate max scroll
    total_content_lines = len(content_lines)
    max_scroll = max(0, total_content_lines - content_height)

    # Clamp scroll position
    scroll_pos = max(0, min(scroll_pos, max_scroll))

    # Render visible content lines (use Text.from_ansi to interpret ANSI codes)
    visible_lines = content_lines[scroll_pos:scroll_pos + content_height]
    for line in visible_lines:
        console.print(Text.from_ansi(line))

    # Pad remaining lines if content is shorter than viewport
    lines_printed = len(visible_lines)
    for _ in range(content_height - lines_printed):
        console.print()

    # Scroll indicator
    if total_content_lines > content_height:
        scroll_pct = int((scroll_pos / max_scroll) * 100) if max_scroll > 0 else 0
        scroll_info = f"Lines {scroll_pos + 1}-{min(scroll_pos + content_height, total_content_lines)} of {total_content_lines} ({scroll_pct}%)"
        console.print(Text(f"  ↑↓ Scroll | {scroll_info}", style="dim"))
    else:
        console.print()

    # Footer
    footer = Text("← → Navigate Tabs  |  ↑ ↓ Scroll  |  q Quit", style="dim")
    console.print(Panel(footer, style="dim"))

    return max_scroll


def setup_terminal():
    """Set up terminal for raw input without echo. Returns old settings."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setraw(fd)
    return old_settings


def restore_terminal(old_settings):
    """Restore terminal settings."""
    fd = sys.stdin.fileno()
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def get_key() -> str:
    """Read a single keypress. Terminal must be set up with setup_terminal() first."""
    fd = sys.stdin.fileno()
    ch = os.read(fd, 1).decode('utf-8', errors='replace')
    if ch == '\x1b':  # Escape sequence
        ch2 = os.read(fd, 1).decode('utf-8', errors='replace')
        if ch2 == '[':
            ch3 = os.read(fd, 1).decode('utf-8', errors='replace')
            if ch3 == 'D':  # Left arrow
                return 'left'
            elif ch3 == 'C':  # Right arrow
                return 'right'
            elif ch3 == 'A':  # Up arrow
                return 'up'
            elif ch3 == 'B':  # Down arrow
                return 'down'
        return 'escape'
    elif ch == '\t':  # Tab key
        return 'tab'
    return ch


def main():
    console = Console()
    current_tab = 0
    scroll_pos = 0
    old_settings = None

    # Pre-render content for current tab
    content = load_content(TABS[current_tab])
    content_lines = render_content_to_lines(console, content)

    try:
        # Set up terminal for raw input without echo
        old_settings = setup_terminal()

        # Initial render
        max_scroll = render_screen(console, current_tab, scroll_pos, content_lines)

        while True:
            key = get_key()

            if key in ('q', 'Q', '\x03'):  # q or Ctrl+C
                console.clear()
                break
            elif key == 'left':
                current_tab = (current_tab - 1) % len(TABS)
                scroll_pos = 0  # Reset scroll on tab change
                content = load_content(TABS[current_tab])
                content_lines = render_content_to_lines(console, content)
                max_scroll = render_screen(console, current_tab, scroll_pos, content_lines)
            elif key in ('right', 'tab'):  # Right arrow or Tab
                current_tab = (current_tab + 1) % len(TABS)
                scroll_pos = 0  # Reset scroll on tab change
                content = load_content(TABS[current_tab])
                content_lines = render_content_to_lines(console, content)
                max_scroll = render_screen(console, current_tab, scroll_pos, content_lines)
            elif key == 'up':
                if scroll_pos > 0:
                    scroll_pos -= 3  # Scroll 3 lines at a time
                    scroll_pos = max(0, scroll_pos)
                    render_screen(console, current_tab, scroll_pos, content_lines)
            elif key == 'down':
                if scroll_pos < max_scroll:
                    scroll_pos += 3  # Scroll 3 lines at a time
                    scroll_pos = min(scroll_pos, max_scroll)
                    render_screen(console, current_tab, scroll_pos, content_lines)
            elif key == '':
                # EOF received, exit
                break
    finally:
        # Restore terminal settings on exit
        if old_settings is not None:
            restore_terminal(old_settings)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
