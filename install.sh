#!/bin/bash

# Auto Deployment System Installation Script
# For Ubuntu 20.04/22.04 LTS

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   error "This script should not be run as root. Please run as a regular user with sudo privileges."
fi

# Check Ubuntu version
if ! lsb_release -d | grep -q "Ubuntu"; then
    error "This script is designed for Ubuntu. Other distributions are not supported."
fi

log "Starting Auto Deployment System installation..."

# Update system packages
log "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required system packages
log "Installing system dependencies..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    nginx \
    git \
    curl \
    wget \
    sqlite3 \
    systemd \
    certbot \
    python3-certbot-nginx

# Install webhook
log "Installing webhook..."
if ! command -v webhook &> /dev/null; then
    sudo apt install -y webhook
else
    log "Webhook is already installed"
fi

# Create users
log "Creating system users..."
sudo useradd -r -s /bin/bash -d /opt/deploy -m webhook || log "User webhook already exists"
sudo useradd -r -s /bin/bash -d /home/deploy -m deploy || log "User deploy already exists"

# Create directories
log "Creating directory structure..."
sudo mkdir -p /opt/deploy/{scripts,logs}
sudo mkdir -p /etc/webhook
sudo mkdir -p /var/log/flask-deploy
sudo mkdir -p /home/deploy/server-manager

# Set permissions
log "Setting up permissions..."
sudo chown -R webhook:webhook /opt/deploy
sudo chown -R deploy:deploy /home/deploy
sudo chown -R deploy:deploy /var/log/flask-deploy

# Copy files to their destinations
log "Copying configuration files..."

# Copy webhook configuration
sudo cp webhook/hooks.json /etc/webhook/
sudo chown webhook:webhook /etc/webhook/hooks.json

# Copy deployment scripts
sudo cp deploy/scripts/* /opt/deploy/scripts/
sudo chown -R webhook:webhook /opt/deploy/scripts
sudo chmod +x /opt/deploy/scripts/*.sh

# Copy Flask application
sudo cp -r flask_app/* /home/deploy/server-manager/
sudo cp deploy/init_db.py /home/deploy/server-manager/
sudo cp deploy/log_writer.py /home/deploy/server-manager/
sudo cp requirements.txt /home/deploy/server-manager/
sudo chown -R deploy:deploy /home/deploy/server-manager

# Install Python dependencies
log "Installing Python dependencies..."
sudo -u deploy bash -c "cd /home/deploy/server-manager && python3 -m pip install --user -r requirements.txt"

# Copy systemd service files
log "Installing systemd services..."
sudo cp config/webhook.service /etc/systemd/system/
sudo cp config/flask-deploy.service /etc/systemd/system/

# Copy nginx configuration
log "Configuring Nginx..."
sudo cp config/nginx-deploy.conf /etc/nginx/sites-available/deploy
if [ ! -L /etc/nginx/sites-enabled/deploy ]; then
    sudo ln -s /etc/nginx/sites-available/deploy /etc/nginx/sites-enabled/deploy
fi

# Initialize database
log "Initializing database..."
sudo -u deploy python3 /home/deploy/server-manager/init_db.py

# Reload systemd and enable services
log "Enabling and starting services..."
sudo systemctl daemon-reload
sudo systemctl enable webhook.service
sudo systemctl enable flask-deploy.service
sudo systemctl enable nginx

# Start services
log "Starting services..."
sudo systemctl start webhook.service
sudo systemctl start flask-deploy.service
sudo systemctl restart nginx

# Check service status
log "Checking service status..."
if sudo systemctl is-active --quiet webhook.service; then
    log "Webhook service is running"
else
    warn "Webhook service failed to start"
fi

if sudo systemctl is-active --quiet flask-deploy.service; then
    log "Flask service is running"
else
    warn "Flask service failed to start"
fi

if sudo systemctl is-active --quiet nginx; then
    log "Nginx service is running"
else
    warn "Nginx service failed to start"
fi

# Configure firewall (if ufw is available)
if command -v ufw &> /dev/null; then
    log "Configuring firewall..."
    sudo ufw allow 22/tcp
    sudo ufw allow 80/tcp
    sudo ufw allow 443/tcp
    sudo ufw allow 9000/tcp  # Webhook port
    echo "y" | sudo ufw enable || true
fi

# Display installation summary
echo ""
echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}  Installation Complete!${NC}"
echo -e "${BLUE}================================${NC}"
echo ""
echo "Services:"
echo "  - Webhook Server: http://localhost:9000"
echo "  - Flask Application: http://localhost:5000"
echo "  - Nginx Proxy: http://localhost"
echo ""
echo "Default Login:"
echo "  - Username: admin"
echo "  - Password: admin123"
echo ""
echo "Configuration Files:"
echo "  - Webhook: /etc/webhook/hooks.json"
echo "  - Database: /home/deploy/server-manager/data/deploy.db"
echo "  - Logs: /opt/deploy/logs/"
echo ""
echo "Next Steps:"
echo "  1. Update domain name in /etc/nginx/sites-available/deploy"
echo "  2. Obtain SSL certificate: sudo certbot --nginx -d your-domain.com"
echo "  3. Configure GitHub webhooks in your repositories"
echo "  4. Change default admin password"
echo ""
echo "Management Commands:"
echo "  - View webhook logs: sudo journalctl -u webhook.service -f"
echo "  - View flask logs: sudo journalctl -u flask-deploy.service -f"
echo "  - Restart services: sudo systemctl restart webhook flask-deploy nginx"
echo ""

log "Installation completed successfully!"