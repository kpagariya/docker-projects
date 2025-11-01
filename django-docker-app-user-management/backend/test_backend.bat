@echo off
REM Quick Backend Test Script for Windows
REM This script tests if the backend is running and responding correctly

echo ==================================
echo   Backend API Health Check
echo ==================================
echo.

set BASE_URL=http://localhost:8000

REM Check if server is running
echo 1. Checking if backend server is running...
curl -s -o nul -w "%%{http_code}" %BASE_URL%/admin/ > temp_status.txt
set /p STATUS=<temp_status.txt
del temp_status.txt

if "%STATUS%"=="200" (
    echo    Backend server is running
) else if "%STATUS%"=="302" (
    echo    Backend server is running
) else (
    echo    Backend server is NOT running
    echo    Start with: docker-compose up backend db
    echo    Or: python manage.py runserver
    pause
    exit /b 1
)

echo.
echo 2. Testing API endpoint...
curl -s %BASE_URL%/api/users/ > response.json
if errorlevel 0 (
    echo    API is responding
    type response.json
    del response.json
) else (
    echo    API is not responding
)

echo.
echo 3. Testing user creation...
curl -s -X POST %BASE_URL%/api/users/ ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Test User\",\"email\":\"test@example.com\",\"phone\":\"+1234567890\"}" ^
  > create_response.json

if errorlevel 0 (
    echo    User creation test completed
    type create_response.json
    del create_response.json
) else (
    echo    User creation test failed
)

echo.
echo ==================================
echo   Test Summary
echo ==================================
echo.
echo Backend API is accessible at:
echo   - API:         %BASE_URL%/api/users/
echo   - Admin:       %BASE_URL%/admin/
echo.
echo Try the Python test script for detailed testing:
echo   pip install requests
echo   python test_api.py
echo.
pause

