@echo off
REM User Management Application - Startup Script for Windows

echo ================================================
echo   User Management Application - Docker Setup
echo ================================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not installed.
    echo Please install Docker from https://www.docker.com/
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo Error: Docker Compose is not installed.
    echo Please install Docker Compose from https://docs.docker.com/compose/install/
    pause
    exit /b 1
)

echo Docker is installed
echo Docker Compose is installed
echo.

REM Check if .env file exists
if not exist "backend\.env" (
    echo Warning: backend\.env file not found.
    echo Creating .env from .env.example...
    copy backend\.env.example backend\.env
    echo Created backend\.env file
    echo.
)

REM Remind user about authentication
echo Authentication Configuration:
echo The application uses SIMPLE LOGIN by default (admin/admin)
echo.
echo To enable Microsoft Entra (Azure AD) OAuth2 (optional):
echo 1. Register app at https://portal.azure.com
echo 2. Update frontend\js\config.js:
echo    - Set USE_ENTRA_ID: true
echo    - Add CLIENT_ID and TENANT_ID
echo.
echo Press any key to continue with Docker deployment...
pause >nul

REM Stop any existing containers
echo Stopping existing containers...
docker-compose down

REM Build and start containers
echo Building and starting containers...
docker-compose up --build -d

REM Wait for services to be ready
echo Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Check if services are running
echo.
echo Checking service status...
docker-compose ps

echo.
echo ================================================
echo   Application Started Successfully!
echo ================================================
echo.
echo Access the application at:
echo    Frontend:      http://localhost:3000
echo    Backend API:   http://localhost:8000/api/
echo    Django Admin:  http://localhost:8000/admin/
echo.
echo Next Steps:
echo 1. Open http://localhost:3000 in your browser
echo 2. Sign in with Microsoft account
echo 3. Start managing users!
echo.
echo Useful Commands:
echo    View logs:           docker-compose logs -f
echo    Stop application:    docker-compose down
echo    Restart:             docker-compose restart
echo    Create superuser:    docker exec -it user_management_backend python manage.py createsuperuser
echo.
echo ================================================
pause

