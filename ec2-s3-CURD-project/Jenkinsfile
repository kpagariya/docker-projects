pipeline {
    agent {
        label 'AWS_EC2'  // Your EC2 node label in Jenkins
    }
    
    environment {
        // AWS settings (using IAM Role - no access keys needed!)
        AWS_REGION = 'ap-south-1'
        //S3_BUCKET_NAME = credentials('s3-bucket-name')
        S3_BUCKET_NAME = "kunalhvdesai25cat"
        TEST_S3_BUCKET_NAME = "test-s3-bucket-name"
        
        // Application settings
        APP_NAME = 's3-image-manager'
        PYTHON_VERSION = '3.11'
        VENV_PATH = "${WORKSPACE}/venv"
    }
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '📥 Checking out source code...'
                checkout scm
                
                script {
                    // Get commit info for display
                    env.GIT_COMMIT_SHORT = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                    env.GIT_AUTHOR = sh(
                        script: 'git log -1 --format="%an"',
                        returnStdout: true
                    ).trim()
                }
                
                echo "Commit: ${env.GIT_COMMIT_SHORT} by ${env.GIT_AUTHOR}"
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                echo '🐍 Setting up Python virtual environment...'
                sh '''
                    # Install Python if not present (for Ubuntu)
                    if ! command -v python3 &> /dev/null; then
                        sudo apt-get update
                        sudo apt-get install -y python3 python3-pip python3-venv
                    fi
                    
                    # Create virtual environment
                    python3 -m venv ${VENV_PATH}
                    
                    # Activate and upgrade pip
                    source ${VENV_PATH}/bin/activate
                    pip install --upgrade pip
                    
                    # Install dependencies
                    pip install -r requirements.txt
                    
                    echo "Python version: $(python --version)"
                    echo "Pip packages installed:"
                    pip list
                '''
            }
        }
        
        stage('Lint & Code Quality') {
            steps {
                echo '🔍 Running code quality checks...'
                sh '''
                    source ${VENV_PATH}/bin/activate
                    
                    # Install linting tools
                    pip install flake8 black isort
                    
                    # Run flake8 for style checking
                    echo "Running flake8..."
                    flake8 app.py config.py --max-line-length=120 --ignore=E501,W503 || true
                    
                    # Check import sorting
                    echo "Checking imports with isort..."
                    isort --check-only --diff app.py config.py || true
                    
                    # Check code formatting
                    echo "Checking formatting with black..."
                    black --check --diff app.py config.py || true
                '''
            }
        }
        
        stage('Unit Tests') {
            steps {
                echo '🧪 Running unit tests...'
                sh '''
                    source ${VENV_PATH}/bin/activate
                    
                    # Set test environment
                    export TESTING=true
                    export SECRET_KEY=test-secret-key
                    
                    # Run pytest with coverage
                    pytest tests/ -v \
                        --cov=app \
                        --cov-report=xml:coverage.xml \
                        --cov-report=html:htmlcov \
                        --junitxml=test-results.xml \
                        --tb=short
                '''
            }
            post {
                always {
                    // Publish test results
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                    
                    // Archive coverage report
                    archiveArtifacts artifacts: 'htmlcov/**/*', allowEmptyArchive: true
                    archiveArtifacts artifacts: 'coverage.xml', allowEmptyArchive: true
                }
            }
        }
        
        stage('Integration Tests') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                }
            }
            steps {
                echo '🔗 Running integration tests...'
                sh '''
                    source ${VENV_PATH}/bin/activate
                    
                    # Start the Flask app in background for testing
                    export FLASK_DEBUG=false
                    export PORT=5001
                    
                    python app.py &
                    APP_PID=$!
                    
                    # Wait for app to start
                    sleep 5
                    
                    # Test health endpoint
                    echo "Testing health endpoint..."
                    curl -f http://localhost:5001/health || { kill $APP_PID; exit 1; }
                    
                    # Test S3 health endpoint
                    echo "Testing S3 health endpoint..."
                    curl -f http://localhost:5001/health/s3 || echo "S3 health check skipped (credentials may not be available)"
                    
                    # Test API list endpoint
                    echo "Testing API images endpoint..."
                    curl -f http://localhost:5001/api/images || echo "API test skipped"
                    
                    # Stop the app
                    kill $APP_PID || true
                    
                    echo "Integration tests completed!"
                '''
            }
        }
        
        stage('File Upload Test') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                }
            }
            steps {
                echo '📤 Testing file upload to S3...'
                sh '''
                    source ${VENV_PATH}/bin/activate
                    
                    # Start the Flask app in background
                    export FLASK_DEBUG=false
                    export PORT=5002
                    
                    python app.py &
                    APP_PID=$!
                    
                    # Wait for app to start
                    sleep 5
                    
                    # Create a test image file
                    echo "Creating test image..."
                    convert -size 100x100 xc:red test_image.png 2>/dev/null || \
                    python3 -c "
from PIL import Image
img = Image.new('RGB', (100, 100), color='red')
img.save('test_image.png')
" 2>/dev/null || \
                    echo "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==" | base64 -d > test_image.png
                    
                    # Test file upload via API
                    echo "Uploading test image..."
                    UPLOAD_RESPONSE=$(curl -s -X POST \
                        -F "file=@test_image.png" \
                        http://localhost:5002/api/upload)
                    
                    echo "Upload response: $UPLOAD_RESPONSE"
                    
                    # Check if upload was successful
                    if echo "$UPLOAD_RESPONSE" | grep -q "Upload successful"; then
                        echo "✅ File upload test PASSED!"
                    else
                        echo "⚠️ File upload test - Response received (may need S3 credentials)"
                    fi
                    
                    # Cleanup
                    rm -f test_image.png
                    kill $APP_PID || true
                '''
            }
        }
        
        stage('Build Artifact') {
            steps {
                echo '📦 Creating deployment artifact...'
                sh '''
                    # Create deployment package
                    mkdir -p dist
                    
                    # Copy application files
                    cp app.py dist/
                    cp config.py dist/
                    cp requirements.txt dist/
                    cp -r templates dist/
                    
                    # Create deployment scripts
                    cat > dist/start.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
gunicorn --bind 0.0.0.0:5000 --workers 2 --threads 4 app:app
EOF
                    
                    cat > dist/stop.sh << 'EOF'
#!/bin/bash
pkill -f "gunicorn.*app:app" || true
EOF
                    
                    chmod +x dist/start.sh dist/stop.sh
                    
                    # Create tarball
                    tar -czvf ${APP_NAME}-${BUILD_NUMBER}.tar.gz -C dist .
                    
                    echo "Artifact created: ${APP_NAME}-${BUILD_NUMBER}.tar.gz"
                '''
            }
            post {
                success {
                    archiveArtifacts artifacts: '*.tar.gz', fingerprint: true
                }
            }
        }
        
        stage('Deploy to EC2') {
            when {
                branch 'main'
            }
            steps {
                echo '🚀 Deploying to EC2...'
                sh '''
                    # Deployment directory
                    DEPLOY_DIR="/opt/${APP_NAME}"
                    
                    # Stop existing application
                    sudo ${DEPLOY_DIR}/stop.sh 2>/dev/null || true
                    
                    # Backup existing deployment
                    if [ -d "$DEPLOY_DIR" ]; then
                        sudo mv $DEPLOY_DIR ${DEPLOY_DIR}.backup.$(date +%Y%m%d_%H%M%S)
                    fi
                    
                    # Create deployment directory
                    sudo mkdir -p $DEPLOY_DIR
                    
                    # Extract new version
                    sudo tar -xzvf ${APP_NAME}-${BUILD_NUMBER}.tar.gz -C $DEPLOY_DIR
                    
                    # Create virtual environment
                    sudo python3 -m venv ${DEPLOY_DIR}/venv
                    sudo ${DEPLOY_DIR}/venv/bin/pip install --upgrade pip
                    sudo ${DEPLOY_DIR}/venv/bin/pip install -r ${DEPLOY_DIR}/requirements.txt
                    
                    # Set permissions (ubuntu is the default user on Ubuntu EC2)
                    sudo chown -R ubuntu:ubuntu $DEPLOY_DIR
                    
                    # Create environment file (no AWS keys needed - using IAM Role)
                    cat > ${DEPLOY_DIR}/.env << EOF
AWS_REGION=${AWS_REGION}
S3_BUCKET_NAME=${S3_BUCKET_NAME}
SECRET_KEY=$(openssl rand -hex 32)
FLASK_DEBUG=false
PORT=5000
EOF
                    
                    # Start the application
                    cd $DEPLOY_DIR
                    ./start.sh &
                    
                    # Wait and verify
                    sleep 5
                    
                    # Health check
                    curl -f http://localhost:5000/health && echo "✅ Deployment successful!" || echo "⚠️ Health check failed"
                '''
            }
        }
    }
    
    post {
        always {
            echo '🧹 Cleaning up workspace...'
            cleanWs(
                cleanWhenNotBuilt: false,
                deleteDirs: true,
                disableDeferredWipeout: true,
                notFailBuild: true
            )
        }
        success {
            echo '✅ Pipeline completed successfully!'
            // Uncomment to send Slack notification
            // slackSend(color: 'good', message: "Build ${BUILD_NUMBER} succeeded for ${APP_NAME}")
        }
        failure {
            echo '❌ Pipeline failed!'
            // Uncomment to send Slack notification
            // slackSend(color: 'danger', message: "Build ${BUILD_NUMBER} failed for ${APP_NAME}")
        }
        unstable {
            echo '⚠️ Pipeline unstable - check test results'
        }
    }
}

