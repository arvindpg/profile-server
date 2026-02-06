FROM python:3.11-slim

# Security: Create non-root user
RUN groupadd -r portfolio && useradd -r -g portfolio portfolio

# Install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create keys directory and set ownership
RUN mkdir -p /app/keys && chown -R portfolio:portfolio /app

# Switch to non-root user
USER portfolio

# Expose SSH port
EXPOSE 2222

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import socket; s=socket.socket(); s.settimeout(5); s.connect(('localhost', 2222)); s.close()"

# Run SSH server
CMD ["python", "ssh_server.py"]
