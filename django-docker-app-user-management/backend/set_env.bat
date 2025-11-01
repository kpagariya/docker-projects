@echo off
REM This script sets environment variables for the current session
REM Run this before executing Django commands manually

echo Setting Django environment variables...
echo.

REM Django Settings
set SECRET_KEY=django-insecure-change-this-in-production
set DEBUG=True
set ALLOWED_HOSTS=localhost,127.0.0.1

REM Database Settings
set DB_NAME=user_management_db
set DB_USER=root
set DB_PASSWORD=password
set DB_HOST=localhost
set DB_PORT=3306

REM CORS Settings
set CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

echo Environment variables set successfully!
echo.
echo You can now run Django commands like:
echo   python manage.py runserver
echo   python manage.py migrate
echo   python manage.py createsuperuser
echo.
echo Note: These variables are only set for this command prompt window.
echo.

