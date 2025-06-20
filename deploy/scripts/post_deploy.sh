#!/bin/bash

# Post-deployment script template  
# Arguments: $1=project_name

PROJECT_NAME=$1
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] Running post-deployment tasks for $PROJECT_NAME"

# Example: Application-specific post-deployment tasks
case "$PROJECT_NAME" in
    "project1")
        echo "[$TIMESTAMP] Warming up application cache..."
        # curl -s http://localhost:3000/health > /dev/null
        echo "[$TIMESTAMP] Starting nginx..."
        # sudo systemctl start nginx
        ;;
    "project2")
        echo "[$TIMESTAMP] Running post-deployment tests..."
        # cd /var/www/project2 && python3 manage.py test
        echo "[$TIMESTAMP] Clearing application cache..."
        # redis-cli FLUSHDB
        ;;
    *)
        echo "[$TIMESTAMP] No specific post-deployment tasks for $PROJECT_NAME"
        ;;
esac

# Common post-deployment tasks
echo "[$TIMESTAMP] Checking service status..."
if systemctl is-active --quiet "${PROJECT_NAME}.service"; then
    echo "[$TIMESTAMP] $PROJECT_NAME service is running"
else
    echo "[$TIMESTAMP] Warning: $PROJECT_NAME service is not running"
fi

echo "[$TIMESTAMP] Checking application health..."
# Add health check commands here

echo "[$TIMESTAMP] Sending deployment notification..."
# curl -X POST -H 'Content-type: application/json' \
#   --data '{"text":"Deployment completed for '$PROJECT_NAME'"}' \
#   YOUR_SLACK_WEBHOOK_URL

echo "[$TIMESTAMP] Post-deployment tasks completed for $PROJECT_NAME"
exit 0