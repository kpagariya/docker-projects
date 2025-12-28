@echo off
REM User Management Application - Local Startup (No Docker)
REM This script starts both backend and frontend locally

echo ================================================
echo   User Management - Local Development
echo ================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.11+ from https://python.org
    pause
    exit /b 1
)
echo   Python is installed

REM Check MySQL
sc query MySQL80 | findstr "RUNNING" >nul 2>&1
if errorlevel 1 (
    echo   MySQL is not running. Starting MySQL...
    net start MySQL80
    if errorlevel 1 (
        echo   WARNING: Could not start MySQL automatically
        echo   Please start MySQL manually
        pause
    )
) else (
    echo   MySQL is running
)

echo.
echo ================================================
echo   Configuration
echo ================================================
echo.

REM Check if backend .env exists
if not exist "backend\.env" (
    echo WARNING: backend\.env file not found!
    echo.
    echo Creating .env file...
    (
        echo SECRET_KEY=django-insecure-local-dev-key-12345
        echo DEBUG=True
        echo ALLOWED_HOSTS=localhost,127.0.0.1
        echo DB_NAME=user_management_db
        echo DB_USER=root
        echo DB_PASSWORD=password
        echo DB_HOST=localhost
        echo DB_PORT=3306
        echo CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
        echo CORS_ALLOW_ALL_ORIGINS=True
    ) > backend\.env
    echo   Created backend\.env file
    echo   Please update DB_PASSWORD with your MySQL password
    echo.
    pause
)

echo   Configuration ready
echo.

REM Check database exists
echo Checking database...
mysql -u root -p -e "USE user_management_db;" 2>nul
if errorlevel 1 (
    echo   WARNING: Database 'user_management_db' not found
    echo   Please create it manually:
    echo   mysql -u root -p
    echo   CREATE DATABASE user_management_db;
    echo.
    pause
)

echo.
echo ================================================
echo   Starting Application
echo ================================================
echo.

REM Start backend in new window
echo Starting Django Backend...
start "Django Backend (Port 8000)" cmd /k "cd backend && python manage.py runserver"
timeout /t 3 /nobreak >nul

REM Start frontend in new window
echo Starting Frontend Server...
start "Frontend Server (Port 3000)" cmd /k "cd frontend && python -m http.server 3000"
timeout /t 2 /nobreak >nul

echo.
echo ================================================
echo   Application Started Successfully!
echo ================================================
echo.
echo   Two windows opened:
echo   1. Django Backend (port 8000)
echo   2. Frontend Server (port 3000)
echo.
echo   Access the application:
echo   Frontend:  http://localhost:3000
echo   Backend:   http://localhost:8000/api/users/
echo   Login:     admin / admin
echo.
echo   Press Ctrl+C in each window to stop
echo.
echo ================================================

REM Wait and open browser
timeout /t 3 /nobreak >nul
start http://localhost:3000

pause

