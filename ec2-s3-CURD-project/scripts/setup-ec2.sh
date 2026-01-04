#!/bin/bash
# ===========================================
# EC2 Instance Setup Script (Ubuntu)
# Run this on a fresh Ubuntu EC2 instance
# ===========================================

set -e

echo "=========================================="
echo "Setting up Ubuntu EC2 instance for S3 Image Manager"
echo "=========================================="

# Update system
echo "Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y

# Install Python 3 and development tools
echo "Installing Python and tools..."
sudo apt-get install -y python3 python3-pip python3-venv python3-dev build-essential git curl

# Install Java (required for Jenkins agent)
echo "Installing Java..."
sudo apt-get install -y openjdk-11-jdk
java -version

# Create application directories
echo "Creating application directories..."
sudo mkdir -p /opt/s3-image-manager
sudo mkdir -p /opt/s3-image-manager/logs
sudo chown -R ubuntu:ubuntu /opt/s3-image-manager

# Install pip packages globally (for convenience)
echo "Installing global pip packages..."
sudo pip3 install --upgrade pip
sudo pip3 install virtualenv gunicorn

# Configure firewall (if using ufw)
echo "Configuring firewall..."
if command -v ufw &> /dev/null; then
    sudo ufw allow 5000/tcp
    sudo ufw allow 22/tcp
    echo "Firewall rules added (run 'sudo ufw enable' if not already enabled)"
fi

# Setup Jenkins agent directory (optional)
echo "Setting up Jenkins workspace..."
sudo mkdir -p /var/lib/jenkins
sudo chown -R ubuntu:ubuntu /var/lib/jenkins

echo "=========================================="
echo "EC2 Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Attach IAM Role with S3 permissions to this EC2 instance"
echo "2. Update S3_BUCKET_NAME in /opt/s3-image-manager/.env"
echo "3. Configure Jenkins to connect to this EC2 instance"
echo "4. Run the deployment script or Jenkins pipeline"
echo "=========================================="
