#!/bin/bash
# Start the S3 Image Manager application

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(dirname "$SCRIPT_DIR")"

cd "$APP_DIR"

# Activate virtual environment
source venv/bin/activate

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Start with gunicorn
exec gunicorn \
    --bind 0.0.0.0:${PORT:-5000} \
    --workers 2 \
    --threads 4 \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log \
    --capture-output \
    --enable-stdio-inheritance \
    app:app

