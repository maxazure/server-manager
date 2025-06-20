#!/bin/bash

# Deploy script for project1
# Arguments: $1=repository_name, $2=ref, $3=commit_id

PROJECT_NAME="project1"
REPO_URL="https://github.com/username/project1.git"
BRANCH="main"  
DEPLOY_DIR="/var/www/project1"
LOG_DIR="/opt/deploy/logs"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
LOG_FILE="${LOG_DIR}/${PROJECT_NAME}_${TIMESTAMP}.log"

# Create log directory if not exists
mkdir -p "$LOG_DIR"

# Function to log with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Function to log and update database
log_and_update_db() {
    local status=$1
    local message=$2
    log "$message"
    python3 "$(dirname "$(dirname "$0")")/log_writer.py" --project-name "$PROJECT_NAME" --status "$status" --log-path "$LOG_FILE"
}

log "========== Starting deployment for $PROJECT_NAME =========="
log "Repository: $1, Ref: $2, Commit: $3"

# Update database with deployment start
log_and_update_db "started" "Deployment started"

# Change to deployment directory
cd "$DEPLOY_DIR" || {
    log_and_update_db "failed" "Failed to change to deployment directory: $DEPLOY_DIR"
    exit 1
}

# Run pre-deployment script if exists
if [ -f "/opt/deploy/scripts/pre_deploy.sh" ]; then
    log "Running pre-deployment script..."
    if bash /opt/deploy/scripts/pre_deploy.sh "$PROJECT_NAME" 2>&1 | tee -a "$LOG_FILE"; then
        log "Pre-deployment script completed successfully"
    else
        log_and_update_db "failed" "Pre-deployment script failed"
        exit 1
    fi
fi

# Git pull
log "Pulling latest changes from $BRANCH branch..."
if git pull origin "$BRANCH" 2>&1 | tee -a "$LOG_FILE"; then
    log "Git pull completed successfully"
else
    log_and_update_db "failed" "Git pull failed"
    exit 1
fi

# Install/update dependencies if package.json exists
if [ -f "package.json" ]; then
    log "Installing npm dependencies..."
    if npm install 2>&1 | tee -a "$LOG_FILE"; then
        log "npm install completed successfully"
    else
        log_and_update_db "failed" "npm install failed"
        exit 1
    fi
fi

# Build if build script exists
if [ -f "package.json" ] && npm run build --silent 2>/dev/null; then
    log "Building project..."
    if npm run build 2>&1 | tee -a "$LOG_FILE"; then
        log "Build completed successfully"
    else
        log_and_update_db "failed" "Build failed"
        exit 1
    fi
fi

# Restart services if needed
if systemctl is-active --quiet "${PROJECT_NAME}.service"; then
    log "Restarting ${PROJECT_NAME} service..."
    if sudo systemctl restart "${PROJECT_NAME}.service" 2>&1 | tee -a "$LOG_FILE"; then
        log "Service restarted successfully"
    else
        log_and_update_db "failed" "Service restart failed"
        exit 1
    fi
fi

# Run post-deployment script if exists
if [ -f "/opt/deploy/scripts/post_deploy.sh" ]; then
    log "Running post-deployment script..."
    if bash /opt/deploy/scripts/post_deploy.sh "$PROJECT_NAME" 2>&1 | tee -a "$LOG_FILE"; then
        log "Post-deployment script completed successfully"
    else
        log_and_update_db "failed" "Post-deployment script failed"
        exit 1
    fi
fi

log_and_update_db "success" "Deployment completed successfully"
log "========== Deployment finished =========="

exit 0