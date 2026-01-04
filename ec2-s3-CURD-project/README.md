# S3 Image Manager

A Flask web application for uploading, managing, and organizing images in AWS S3. This project includes a complete CI/CD pipeline using Jenkins.

![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![AWS](https://img.shields.io/badge/AWS-S3-orange)
![Jenkins](https://img.shields.io/badge/CI/CD-Jenkins-red)

## Features

- 📤 **Upload Images** - Drag & drop or click to upload images to S3
- 📋 **List Images** - View all images in your S3 bucket with metadata
- ⬇️ **Download Images** - Download images directly from the browser
- 🗑️ **Delete Images** - Remove images from S3 with confirmation
- 🔍 **Image Preview** - Click to view full-size images in a modal
- 🔌 **REST API** - Full API endpoints for programmatic access
- 🏥 **Health Checks** - Built-in health endpoints for monitoring
- 🚀 **CI/CD Pipeline** - Complete Jenkins pipeline for automated deployment

## Project Structure

```
s3-ec2-project/
├── app.py                 # Main Flask application
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── Jenkinsfile           # Jenkins CI/CD pipeline
├── templates/
│   └── index.html        # Web UI template
├── tests/
│   ├── __init__.py
│   └── test_app.py       # Unit tests
└── scripts/
    ├── deploy.sh         # Deployment script
    ├── start.sh          # Start application
    ├── stop.sh           # Stop application
    └── setup-ec2.sh      # EC2 instance setup
```

## Prerequisites

- Python 3.11+
- AWS Account with S3 bucket
- EC2 instance (for deployment)
- Jenkins server (for CI/CD)

## Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd s3-ec2-project
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file in the project root:

```env
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-bucket-name
SECRET_KEY=your-secret-key
FLASK_DEBUG=True
PORT=5000
```

### 5. Run the Application

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web UI home page |
| POST | `/upload` | Upload image (form) |
| GET | `/download/<key>` | Download image |
| GET | `/delete/<key>` | Delete image |
| GET | `/api/images` | List all images (JSON) |
| POST | `/api/upload` | Upload image (API) |
| DELETE | `/api/delete/<key>` | Delete image (API) |
| GET | `/health` | Application health check |
| GET | `/health/s3` | S3 connectivity check |

### API Examples

**List Images:**
```bash
curl http://localhost:5000/api/images
```

**Upload Image:**
```bash
curl -X POST -F "file=@image.jpg" http://localhost:5000/api/upload
```

**Delete Image:**
```bash
curl -X DELETE http://localhost:5000/api/delete/image-key.jpg
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Jenkins CI/CD Pipeline

### Pipeline Stages

1. **Checkout** - Clone source code from repository
2. **Setup Python Environment** - Create virtual environment and install dependencies
3. **Lint & Code Quality** - Run flake8, black, and isort
4. **Unit Tests** - Run pytest with coverage reporting
5. **Integration Tests** - Test application endpoints (main/develop branches)
6. **File Upload Test** - Test S3 upload functionality (main/develop branches)
7. **Build Artifact** - Create deployment package
8. **Deploy to EC2** - Deploy to production (main branch only)

### Jenkins Setup

#### 1. Create Jenkins Credentials

Add these credentials in Jenkins (Manage Jenkins → Credentials):

| ID | Type | Description |
|----|------|-------------|
| `aws-access-key-id` | Secret text | AWS Access Key ID |
| `aws-secret-access-key` | Secret text | AWS Secret Access Key |
| `s3-bucket-name` | Secret text | S3 Bucket Name |
| `test-s3-bucket-name` | Secret text | Test S3 Bucket Name |

#### 2. Configure EC2 Node

1. Launch an EC2 instance (Amazon Linux 2 recommended)
2. Run the setup script:
   ```bash
   chmod +x scripts/setup-ec2.sh
   sudo ./scripts/setup-ec2.sh
   ```
3. In Jenkins, go to **Manage Jenkins → Nodes → New Node**
4. Configure:
   - Node name: `ec2-node`
   - Remote root directory: `/var/lib/jenkins`
   - Launch method: Launch agents via SSH
   - Host: Your EC2 public IP
   - Credentials: EC2 SSH key

#### 3. Create Pipeline Job

1. New Item → Pipeline
2. Configure:
   - Pipeline: Pipeline script from SCM
   - SCM: Git
   - Repository URL: Your repo URL
   - Script Path: `Jenkinsfile`

## Deployment

### Manual Deployment

```bash
# On EC2 instance
sudo chmod +x scripts/deploy.sh
sudo ./scripts/deploy.sh
```

### Service Management

```bash
# Start
sudo systemctl start s3-image-manager

# Stop
sudo systemctl stop s3-image-manager

# Restart
sudo systemctl restart s3-image-manager

# View logs
sudo journalctl -u s3-image-manager -f
```

## AWS Configuration

### S3 Bucket Policy

Ensure your S3 bucket has appropriate permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::your-bucket-name",
                "arn:aws:s3:::your-bucket-name/*"
            ]
        }
    ]
}
```

### IAM User Policy

Create an IAM user with the following policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:DeleteObject",
                "s3:ListBucket",
                "s3:HeadBucket"
            ],
            "Resource": [
                "arn:aws:s3:::your-bucket-name",
                "arn:aws:s3:::your-bucket-name/*"
            ]
        }
    ]
}
```

## Security Considerations

- Never commit `.env` files or AWS credentials
- Use IAM roles for EC2 instances when possible
- Enable S3 bucket versioning for data protection
- Configure HTTPS in production (use nginx/ALB)
- Regularly rotate AWS access keys

## Troubleshooting

### Common Issues

**1. S3 Access Denied**
- Verify AWS credentials in `.env`
- Check IAM user permissions
- Ensure bucket name is correct

**2. Module Not Found**
- Activate virtual environment
- Run `pip install -r requirements.txt`

**3. Port Already in Use**
- Check if another process is using port 5000
- Change PORT in `.env` file

**4. Jenkins Build Fails**
- Verify EC2 node is online
- Check Jenkins credentials are configured
- Review console output for specific errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest tests/ -v`
5. Submit a pull request

## License

MIT License - feel free to use this project for learning and production.

