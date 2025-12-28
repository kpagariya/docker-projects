#!/bin/bash
# User Management Application - Local Startup (No Docker)
# This script starts both backend and frontend locally

echo "================================================"
echo "  User Management - Local Development"
echo "================================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python is not installed!"
    echo "Please install Python 3.11+ from https://python.org"
    exit 1
fi
echo "✓ Python is installed"

# Check MySQL (Linux/Mac)
if command -v mysql &> /dev/null; then
    if mysql -e "SELECT 1" &> /dev/null; then
        echo "✓ MySQL is running"
    else
        echo "⚠ MySQL might not be running"
        echo "  Start it with: sudo service mysql start"
    fi
else
    echo "⚠ MySQL command not found"
fi

echo ""
echo "================================================"
echo "  Configuration"
echo "================================================"
echo ""

# Check if backend .env exists
if [ ! -f "backend/.env" ]; then
    echo "⚠ WARNING: backend/.env file not found!"
    echo ""
    echo "Creating .env file..."
    cat > backend/.env << EOF
SECRET_KEY=django-insecure-local-dev-key-12345
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=user_management_db
DB_USER=root
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=3306
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CORS_ALLOW_ALL_ORIGINS=True
EOF
    echo "✓ Created backend/.env file"
    echo "  Please update DB_PASSWORD with your MySQL password"
    echo ""
    read -p "Press Enter to continue..."
fi

echo "✓ Configuration ready"
echo ""

# Check database exists
if mysql -u root -p -e "USE user_management_db;" 2>/dev/null; then
    echo "✓ Database exists"
else
    echo "⚠ WARNING: Database 'user_management_db' not found"
    echo "  Create it with:"
    echo "  mysql -u root -p"
    echo "  CREATE DATABASE user_management_db;"
    echo ""
fi

echo ""
echo "================================================"
echo "  Starting Application"
echo "================================================"
echo ""

# Kill any existing processes on ports 8000 and 3000
echo "Checking for existing processes..."
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null

# Start backend
echo "Starting Django Backend..."
cd backend
python3 manage.py runserver > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend
echo "Starting Frontend Server..."
cd frontend
python3 -m http.server 3000 > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Wait for services to start
sleep 2

echo ""
echo "================================================"
echo "  Application Started Successfully! 🎉"
echo "================================================"
echo ""
echo "  Process IDs:"
echo "  Backend:  $BACKEND_PID"
echo "  Frontend: $FRONTEND_PID"
echo ""
echo "  Access the application:"
echo "  Frontend:  http://localhost:3000"
echo "  Backend:   http://localhost:8000/api/users/"
echo "  Login:     admin / admin"
echo ""
echo "  Logs:"
echo "  Backend:   tail -f /tmp/backend.log"
echo "  Frontend:  tail -f /tmp/frontend.log"
echo ""
echo "  To stop:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo "  or run: ./stop_local.sh"
echo ""
echo "================================================"

# Save PIDs for stopping
echo $BACKEND_PID > /tmp/backend.pid
echo $FRONTEND_PID > /tmp/frontend.pid

# Open browser (Mac/Linux)
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:3000 2>/dev/null &
elif command -v open &> /dev/null; then
    open http://localhost:3000 2>/dev/null &
fi

