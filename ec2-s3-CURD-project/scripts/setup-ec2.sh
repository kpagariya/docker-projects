#!/bin/bash
# ===========================================
# EC2 Instance Setup Script
# Run this on a fresh EC2 instance (Amazon Linux 2)
# ===========================================

set -e

echo "=========================================="
echo "Setting up EC2 instance for S3 Image Manager"
echo "=========================================="

# Update system
echo "Updating system packages..."
sudo yum update -y

# Install Python 3 and development tools
echo "Installing Python and tools..."
sudo yum install -y python3 python3-pip python3-devel gcc git

# Install Java (required for Jenkins agent)
echo "Installing Java..."
sudo amazon-linux-extras install -y java-openjdk11
java -version

# Create application user (if needed)
if ! id "appuser" &>/dev/null; then
    echo "Creating application user..."
    sudo useradd -m -s /bin/bash appuser
fi

# Create application directories
echo "Creating application directories..."
sudo mkdir -p /opt/s3-image-manager
sudo mkdir -p /opt/s3-image-manager/logs
sudo chown -R ec2-user:ec2-user /opt/s3-image-manager

# Install pip packages globally (for convenience)
echo "Installing global pip packages..."
sudo pip3 install --upgrade pip
sudo pip3 install virtualenv gunicorn

# Configure firewall (if using)
echo "Configuring firewall..."
if command -v firewall-cmd &> /dev/null; then
    sudo firewall-cmd --permanent --add-port=5000/tcp
    sudo firewall-cmd --reload
fi

# Setup Jenkins agent directory (optional)
echo "Setting up Jenkins workspace..."
sudo mkdir -p /var/lib/jenkins
sudo chown -R ec2-user:ec2-user /var/lib/jenkins

echo "=========================================="
echo "EC2 Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Configure AWS credentials in /opt/s3-image-manager/.env"
echo "2. Configure Jenkins to connect to this EC2 instance"
echo "3. Run the deployment script or Jenkins pipeline"
echo "=========================================="

