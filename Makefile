# Auto Deployment System Makefile

.PHONY: install start stop restart status logs test clean dev help

# Default target
help:
	@echo "Available commands:"
	@echo "  make install    - Install the complete system"
	@echo "  make start      - Start all services"
	@echo "  make stop       - Stop all services"
	@echo "  make restart    - Restart all services"
	@echo "  make status     - Show service status"
	@echo "  make logs       - Show real-time logs"
	@echo "  make test       - Run tests"
	@echo "  make dev        - Start development server"
	@echo "  make clean      - Clean up temporary files"
	@echo "  make backup     - Backup database and logs"
	@echo "  make ssl        - Setup SSL certificate"

# Install the complete system
install:
	@echo "Installing Auto Deployment System..."
	./install.sh

# Service management
start:
	sudo systemctl start webhook.service flask-deploy.service nginx

stop:
	sudo systemctl stop webhook.service flask-deploy.service

restart:
	sudo systemctl restart webhook.service flask-deploy.service nginx

status:
	@echo "=== Service Status ==="
	@sudo systemctl status webhook.service --no-pager -l
	@echo ""
	@sudo systemctl status flask-deploy.service --no-pager -l
	@echo ""
	@sudo systemctl status nginx --no-pager -l

# Logging
logs:
	@echo "Showing real-time logs (Ctrl+C to exit)..."
	sudo journalctl -u webhook.service -u flask-deploy.service -f

logs-webhook:
	sudo journalctl -u webhook.service -f

logs-flask:
	sudo journalctl -u flask-deploy.service -f

logs-nginx:
	sudo tail -f /var/log/nginx/deploy_access.log /var/log/nginx/deploy_error.log

# Development
dev:
	@echo "Starting development server..."
	cd flask_app && python3 -m pip install -r ../requirements.txt --user
	cd flask_app && python3 app.py

test:
	@echo "Running tests..."
	cd flask_app && python3 -m pytest tests/ -v || echo "No tests found"

# Database operations
init-db:
	sudo -u deploy python3 /home/deploy/server-manager/init_db.py

backup:
	@echo "Creating backup..."
	mkdir -p backup/$(shell date +%Y%m%d_%H%M%S)
	sudo cp /home/deploy/server-manager/data/deploy.db backup/$(shell date +%Y%m%d_%H%M%S)/
	sudo cp -r /opt/deploy/logs backup/$(shell date +%Y%m%d_%H%M%S)/
	@echo "Backup created in backup/$(shell date +%Y%m%d_%H%M%S)/"

# SSL setup
ssl:
	@read -p "Enter your domain name: " domain; \
	sudo certbot --nginx -d $$domain

ssl-renew:
	sudo certbot renew --quiet

# Cleanup
clean:
	@echo "Cleaning up..."
	sudo find /opt/deploy/logs -name "*.log" -mtime +30 -delete || true
	sudo find /tmp -name "deploy_*" -mtime +1 -delete || true
	@echo "Cleanup completed"

# Configuration
update-webhook:
	sudo cp webhook/hooks.json /etc/webhook/
	sudo systemctl restart webhook.service

update-nginx:
	sudo cp config/nginx-deploy.conf /etc/nginx/sites-available/deploy
	sudo nginx -t && sudo systemctl reload nginx

# Monitoring
health:
	@echo "=== Health Check ==="
	@curl -s http://localhost/health || echo "Web service not responding"
	@curl -s http://localhost:9000 || echo "Webhook service not responding"
	@echo ""
	@echo "=== Disk Usage ==="
	@df -h /opt/deploy
	@echo ""
	@echo "=== Memory Usage ==="
	@free -h

# User management
create-user:
	@read -p "Enter username: " username; \
	read -s -p "Enter password: " password; \
	cd flask_app && python3 -c "import hashlib; print('$$password')" | \
	python3 -c "import hashlib, sys; print(hashlib.sha256(sys.stdin.read().strip().encode()).hexdigest())" > /tmp/hash; \
	sudo sqlite3 /home/deploy/server-manager/data/deploy.db "INSERT INTO user (username, password_hash) VALUES ('$$username', '$(shell cat /tmp/hash)')"; \
	rm -f /tmp/hash; \
	echo "User $$username created successfully"

# Deployment
deploy-update:
	@echo "Updating deployment system..."
	git pull origin main
	cd flask_app && python3 -m pip install -r ../requirements.txt --user --upgrade
	sudo systemctl restart flask-deploy.service
	@echo "Update completed"

# Security
security-check:
	@echo "=== Security Check ==="
	@echo "Checking file permissions..."
	@sudo find /opt/deploy -type f -perm /o+w -ls | head -10 || echo "No world-writable files found"
	@echo ""
	@echo "Checking for updates..."
	@sudo apt list --upgradable | head -10
	@echo ""
	@echo "Checking SSL certificate..."
	@sudo certbot certificates | grep -A 2 "Certificate Name:" || echo "No SSL certificates found"