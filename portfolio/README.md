# SSH Portfolio

A terminal-based portfolio served over SSH. Connect and navigate through sections to learn about me.

## Quick Start

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the TUI directly (for testing)
python app.py

# Run the SSH server
python ssh_server.py
```

Then connect:
```bash
ssh localhost -p 2222
```

### Docker Deployment

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Connect
ssh your-server -p 2222
```

## Navigation

| Key | Action |
|-----|--------|
| ← → | Switch tabs |
| ↑ ↓ | Scroll content |
| Tab | Next tab |
| Shift+Tab | Previous tab |
| q | Quit |

## Project Structure

```
portfolio/
├── app.py              # Textual TUI application
├── ssh_server.py       # SSH server wrapper
├── screens/
│   └── portfolio.py    # Main portfolio screen
├── content/            # Markdown content files
│   ├── about.md
│   ├── backend.md
│   ├── devops.md
│   ├── frontend.md
│   ├── security.md
│   └── others.md
├── styles.tcss         # Textual CSS styles
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Security

This portfolio is designed with security in mind:

- **No shell access**: The SSH server only handles PTY requests for the TUI
- **No command execution**: Only navigation keys are processed
- **Rate limiting**: Prevents connection flooding
- **Connection limits**: Max 50 concurrent connections
- **Idle timeout**: Sessions expire after 5 minutes of inactivity
- **Docker isolation**: Read-only filesystem, dropped capabilities
- **Non-root**: Runs as unprivileged user

## Customization

### Content

Edit the markdown files in `content/` to update your portfolio content:

- `about.md` - Personal introduction
- `backend.md` - Backend development skills
- `devops.md` - DevOps and infrastructure
- `frontend.md` - Frontend development
- `security.md` - Security expertise
- `others.md` - Other interests

### Styling

Modify `styles.tcss` to customize the appearance. See the [Textual CSS documentation](https://textual.textualize.io/guide/CSS/).

### Configuration

Environment variables:
- `SSH_PORT` - Port to listen on (default: 2222)

In `ssh_server.py`:
- `MAX_CONNECTIONS` - Maximum concurrent connections
- `CONNECTIONS_PER_IP_PER_MINUTE` - Rate limit
- `IDLE_TIMEOUT` - Session idle timeout (seconds)
- `MAX_SESSION_DURATION` - Maximum session length (seconds)

## Firewall Setup

```bash
# Allow SSH portfolio port with rate limiting
sudo ufw allow 2222/tcp
sudo ufw limit 2222/tcp
```

## Fail2ban (Optional)

Create `/etc/fail2ban/jail.d/portfolio.conf`:

```ini
[portfolio-ssh]
enabled = true
port = 2222
filter = sshd
logpath = /var/log/portfolio/ssh.log
maxretry = 10
bantime = 600
```

## License

MIT
