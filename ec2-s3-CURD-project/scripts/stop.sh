#!/bin/bash
# Stop the S3 Image Manager application

echo "Stopping S3 Image Manager..."

# Kill gunicorn processes
pkill -f "gunicorn.*app:app" 2>/dev/null && echo "Application stopped" || echo "No running process found"

