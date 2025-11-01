#!/bin/bash

# User Management Application - Startup Script

echo "================================================"
echo "  User Management Application - Docker Setup"
echo "================================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed."
    echo "Please install Docker from https://www.docker.com/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: Docker Compose is not installed."
    echo "Please install Docker Compose from https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker is installed"
echo "✅ Docker Compose is installed"
echo ""

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  Warning: backend/.env file not found."
    echo "Creating .env from .env.example..."
    cp backend/.env.example backend/.env
    echo "✅ Created backend/.env file"
    echo ""
fi

# Remind user about authentication
echo "📝 Authentication Configuration:"
echo "The application uses SIMPLE LOGIN by default (admin/admin)"
echo ""
echo "To enable Microsoft Entra (Azure AD) OAuth2 (optional):"
echo "1. Register app at https://portal.azure.com"
echo "2. Update frontend/js/config.js:"
echo "   - Set USE_ENTRA_ID: true"
echo "   - Add CLIENT_ID and TENANT_ID"
echo ""
echo "Press Enter to continue with Docker deployment..."
read

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Build and start containers
echo "🔨 Building and starting containers..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
echo ""
echo "📊 Checking service status..."
docker-compose ps

echo ""
echo "================================================"
echo "  Application Started Successfully! 🎉"
echo "================================================"
echo ""
echo "🌐 Access the application at:"
echo "   Frontend:      http://localhost:3000"
echo "   Backend API:   http://localhost:8000/api/"
echo "   Django Admin:  http://localhost:8000/admin/"
echo ""
echo "📝 Next Steps:"
echo "1. Open http://localhost:3000 in your browser"
echo "2. Sign in with Microsoft account"
echo "3. Start managing users!"
echo ""
echo "🔧 Useful Commands:"
echo "   View logs:           docker-compose logs -f"
echo "   Stop application:    docker-compose down"
echo "   Restart:             docker-compose restart"
echo "   Create superuser:    docker exec -it user_management_backend python manage.py createsuperuser"
echo ""
echo "================================================"

