#!/bin/bash
# ===========================================
# Deployment Script for S3 Image Manager
# ===========================================

set -e  # Exit on error

# Configuration
APP_NAME="s3-image-manager"
DEPLOY_DIR="/opt/${APP_NAME}"
SERVICE_NAME="s3-image-manager"
PORT=5000

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root or with sudo
check_permissions() {
    if [ "$EUID" -ne 0 ]; then
        log_error "Please run as root or with sudo"
        exit 1
    fi
}

# Install system dependencies
install_dependencies() {
    log_info "Installing system dependencies..."
    
    # Ubuntu / Debian
    apt-get update
    apt-get install -y python3 python3-pip python3-venv python3-dev build-essential
}

# Create application directory
setup_directories() {
    log_info "Setting up directories..."
    
    # Backup existing deployment
    if [ -d "$DEPLOY_DIR" ]; then
        BACKUP_DIR="${DEPLOY_DIR}.backup.$(date +%Y%m%d_%H%M%S)"
        log_info "Backing up existing deployment to $BACKUP_DIR"
        mv "$DEPLOY_DIR" "$BACKUP_DIR"
    fi
    
    mkdir -p "$DEPLOY_DIR"
    mkdir -p "$DEPLOY_DIR/logs"
}

# Copy application files
copy_files() {
    log_info "Copying application files..."
    
    cp app.py "$DEPLOY_DIR/"
    cp config.py "$DEPLOY_DIR/"
    cp requirements.txt "$DEPLOY_DIR/"
    cp -r templates "$DEPLOY_DIR/"
    
    # Copy scripts
    mkdir -p "$DEPLOY_DIR/scripts"
    cp scripts/*.sh "$DEPLOY_DIR/scripts/" 2>/dev/null || true
}

# Setup Python virtual environment
setup_venv() {
    log_info "Setting up Python virtual environment..."
    
    python3 -m venv "$DEPLOY_DIR/venv"
    source "$DEPLOY_DIR/venv/bin/activate"
    
    pip install --upgrade pip
    pip install -r "$DEPLOY_DIR/requirements.txt"
    
    deactivate
}

# Create environment file
create_env_file() {
    log_info "Creating environment configuration..."
    
    if [ ! -f "$DEPLOY_DIR/.env" ]; then
        cat > "$DEPLOY_DIR/.env" << EOF
# AWS Configuration (using IAM Role - no access keys needed!)
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-bucket-name

# Flask Configuration
SECRET_KEY=$(openssl rand -hex 32)
FLASK_DEBUG=false
PORT=${PORT}
EOF
        
        log_warn "Please update $DEPLOY_DIR/.env with your S3 bucket name"
    else
        log_info "Environment file already exists, skipping..."
    fi
}

# Create systemd service
create_systemd_service() {
    log_info "Creating systemd service..."
    
    cat > "/etc/systemd/system/${SERVICE_NAME}.service" << EOF
[Unit]
Description=S3 Image Manager Flask Application
After=network.target

[Service]
Type=simple
User=ubuntu
Group=ubuntu
WorkingDirectory=${DEPLOY_DIR}
Environment="PATH=${DEPLOY_DIR}/venv/bin"
EnvironmentFile=${DEPLOY_DIR}/.env
ExecStart=${DEPLOY_DIR}/venv/bin/gunicorn --bind 0.0.0.0:${PORT} --workers 2 --threads 4 --access-logfile ${DEPLOY_DIR}/logs/access.log --error-logfile ${DEPLOY_DIR}/logs/error.log app:app
ExecReload=/bin/kill -s HUP \$MAINPID
ExecStop=/bin/kill -s TERM \$MAINPID
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl enable "$SERVICE_NAME"
}

# Set permissions
set_permissions() {
    log_info "Setting permissions..."
    
    chown -R ubuntu:ubuntu "$DEPLOY_DIR"
    chmod -R 755 "$DEPLOY_DIR"
    chmod 600 "$DEPLOY_DIR/.env"
}

# Start the service
start_service() {
    log_info "Starting the service..."
    
    systemctl start "$SERVICE_NAME"
    sleep 3
    
    if systemctl is-active --quiet "$SERVICE_NAME"; then
        log_info "Service started successfully!"
    else
        log_error "Service failed to start. Check logs:"
        journalctl -u "$SERVICE_NAME" -n 20
        exit 1
    fi
}

# Health check
health_check() {
    log_info "Running health check..."
    
    for i in {1..5}; do
        if curl -sf "http://localhost:${PORT}/health" > /dev/null; then
            log_info "Health check passed!"
            return 0
        fi
        log_warn "Health check attempt $i failed, retrying..."
        sleep 2
    done
    
    log_error "Health check failed after 5 attempts"
    return 1
}

# Main deployment function
main() {
    log_info "Starting deployment of $APP_NAME..."
    
    check_permissions
    install_dependencies
    setup_directories
    copy_files
    setup_venv
    create_env_file
    create_systemd_service
    set_permissions
    start_service
    health_check
    
    log_info "=========================================="
    log_info "Deployment completed successfully!"
    log_info "Application URL: http://$(hostname -I | awk '{print $1}'):${PORT}"
    log_info "=========================================="
}

# Run main function
main "$@"

