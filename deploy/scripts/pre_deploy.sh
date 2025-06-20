#!/bin/bash

# Pre-deployment script template
# Arguments: $1=project_name

PROJECT_NAME=$1
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] Running pre-deployment tasks for $PROJECT_NAME"

# Example: Stop application services before deployment
case "$PROJECT_NAME" in
    "project1")
        echo "[$TIMESTAMP] Stopping nginx for maintenance page..."
        # sudo systemctl stop nginx
        ;;
    "project2")  
        echo "[$TIMESTAMP] Creating database backup..."
        # mysqldump -u user -p database > /backup/db_backup_$(date +%Y%m%d_%H%M%S).sql
        ;;
    *)
        echo "[$TIMESTAMP] No specific pre-deployment tasks for $PROJECT_NAME"
        ;;
esac

# Common pre-deployment tasks
echo "[$TIMESTAMP] Checking disk space..."
df -h

echo "[$TIMESTAMP] Checking system load..."
uptime

echo "[$TIMESTAMP] Pre-deployment checks completed for $PROJECT_NAME"
exit 0