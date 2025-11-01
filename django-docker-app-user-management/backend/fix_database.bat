@echo off
REM Database Fix Script
REM This script will fix common database and migration issues

echo ================================================
echo   Database Fix Script
echo ================================================
echo.

REM Step 1: Run diagnostics
echo Step 1: Running diagnostics...
python diagnose_db.py
if errorlevel 1 (
    echo.
    echo Diagnostics found issues. Please fix them first.
    pause
    exit /b 1
)

echo.
echo ================================================
echo   Applying Fixes
echo ================================================
echo.

REM Step 2: Create migrations
echo Step 2: Creating migrations for users app...
python manage.py makemigrations users

REM Step 3: Apply migrations
echo.
echo Step 3: Applying migrations...
python manage.py migrate

REM Step 4: Check if it worked
echo.
echo Step 4: Verifying fix...
python -c "from django.db import connection; cursor = connection.cursor(); cursor.execute('SHOW TABLES LIKE \"users\"'); print('SUCCESS: users table exists!' if cursor.fetchone() else 'FAILED: users table still missing')"

echo.
echo ================================================
echo   Fix Complete
echo ================================================
echo.
echo Try accessing the API now:
echo   http://localhost:8000/api/users/
echo.
pause

