# Running Backend Standalone

This guide shows how to run just the Django backend independently for development and testing.

## Prerequisites

- Python 3.11+
- MySQL 8.0+ (running locally or accessible)
- pip (Python package manager)

## Quick Start

### Option 1: With Docker (Backend + MySQL only)

```bash
# From project root directory
docker-compose up backend db

# Or in detached mode
docker-compose up -d backend db
```

**Access:**
- API: http://localhost:8000/api/users/
- Admin: http://localhost:8000/admin/

---

### Option 2: Local Development (No Docker)

#### Step 1: Setup MySQL Database

Make sure MySQL is running and create a database:

```sql
CREATE DATABASE user_management_db;
CREATE USER 'appuser'@'localhost' IDENTIFIED BY 'apppassword';
GRANT ALL PRIVILEGES ON user_management_db.* TO 'appuser'@'localhost';
FLUSH PRIVILEGES;
```

#### Step 2: Navigate to Backend Directory

```bash
cd backend
```

#### Step 3: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 4: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 5: Configure Environment

Create `.env` file:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edit `.env` with your local MySQL settings:

```env
SECRET_KEY=django-insecure-your-secret-key-for-development
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Update these for local MySQL
DB_NAME=user_management_db
DB_USER=appuser
DB_PASSWORD=apppassword
DB_HOST=localhost
DB_PORT=3306

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

#### Step 6: Run Migrations

```bash
python manage.py migrate
```

#### Step 7: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

Follow prompts to create an admin account.

#### Step 8: Start Development Server

```bash
python manage.py runserver
```

**Server starts at:** http://localhost:8000/

---

## Testing the Backend

### 1. Check if Server is Running

Open browser: http://localhost:8000/

You should see a Django error page (normal - no root URL defined).

### 2. Test API Endpoints

#### List All Users (GET)

```bash
curl http://localhost:8000/api/users/
```

**Expected Response:**
```json
{
  "success": true,
  "data": [],
  "message": "Users retrieved successfully"
}
```

#### Create a User (POST)

```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "created_at": "2025-11-01T10:00:00Z",
    "updated_at": "2025-11-01T10:00:00Z"
  },
  "message": "User created successfully"
}
```

#### Get a Specific User (GET)

```bash
curl http://localhost:8000/api/users/1/
```

#### Update a User (PUT)

```bash
curl -X PUT http://localhost:8000/api/users/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith",
    "email": "john.smith@example.com",
    "phone": "+1234567890"
  }'
```

#### Delete a User (DELETE)

```bash
curl -X DELETE http://localhost:8000/api/users/1/
```

### 3. Test with Postman or Thunder Client

Import these settings:

**Base URL:** `http://localhost:8000/api`

**Endpoints:**
- GET `/users/` - List all users
- POST `/users/` - Create user
- GET `/users/{id}/` - Get user
- PUT `/users/{id}/` - Update user
- DELETE `/users/{id}/` - Delete user

### 4. Access Django Admin

1. Go to: http://localhost:8000/admin/
2. Login with superuser credentials
3. Manage users through admin interface

### 5. Using Python Requests Library

Create a test script `test_api.py`:

```python
import requests
import json

BASE_URL = "http://localhost:8000/api"

# Test 1: List users
response = requests.get(f"{BASE_URL}/users/")
print("List Users:", response.json())

# Test 2: Create user
data = {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "+9876543210"
}
response = requests.post(f"{BASE_URL}/users/", json=data)
print("Create User:", response.json())
user_id = response.json()['data']['id']

# Test 3: Get user
response = requests.get(f"{BASE_URL}/users/{user_id}/")
print("Get User:", response.json())

# Test 4: Update user
data['name'] = "Jane Smith"
response = requests.put(f"{BASE_URL}/users/{user_id}/", json=data)
print("Update User:", response.json())

# Test 5: Delete user
response = requests.delete(f"{BASE_URL}/users/{user_id}/")
print("Delete User:", response.json())
```

Run:
```bash
pip install requests
python test_api.py
```

---

## Troubleshooting

### Database Connection Error

**Error:** `django.db.utils.OperationalError: (2003, "Can't connect to MySQL server...")`

**Solutions:**
- Verify MySQL is running
- Check credentials in `.env` file
- For Docker: Use `DB_HOST=db`
- For local: Use `DB_HOST=localhost`

### Port Already in Use

**Error:** `Error: That port is already in use.`

**Solutions:**
```bash
# Use different port
python manage.py runserver 8001

# Find and kill process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -i :8000
kill -9 <PID>
```

### Migration Errors

**Error:** `django.db.utils.ProgrammingError: (1146, "Table doesn't exist")`

**Solution:**
```bash
python manage.py migrate --run-syncdb
```

### CORS Errors (when testing with frontend)

**Error:** `Access to XMLHttpRequest has been blocked by CORS policy`

**Solution:**
- Add frontend URL to `CORS_ALLOWED_ORIGINS` in `.env`
- Restart the server

---

## Development Tools

### Django Shell

Interactive Python shell with Django context:

```bash
python manage.py shell
```

```python
from users.models import User

# Create user
user = User.objects.create(
    name="Test User",
    email="test@example.com",
    phone="+1234567890"
)

# List users
User.objects.all()

# Filter users
User.objects.filter(email__contains="example.com")

# Delete user
user.delete()
```

### Database Shell

Direct MySQL access:

```bash
python manage.py dbshell
```

### Run Tests (if you add them later)

```bash
python manage.py test
```

---

## API Testing with curl - Complete Examples

### Windows PowerShell

```powershell
# List users
Invoke-WebRequest -Uri http://localhost:8000/api/users/ -Method GET

# Create user
$body = @{
    name = "John Doe"
    email = "john@example.com"
    phone = "+1234567890"
} | ConvertTo-Json

Invoke-WebRequest -Uri http://localhost:8000/api/users/ `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

### Linux/Mac bash

```bash
# List users
curl http://localhost:8000/api/users/

# Create user
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","phone":"+1234567890"}'
```

---

## Monitoring and Logs

### View Server Logs

The development server outputs logs to console. Watch for:
- Request logs: `GET /api/users/ HTTP/1.1" 200`
- Error logs: Any 4xx or 5xx status codes
- SQL queries (if `DEBUG=True`)

### Enable SQL Query Logging

Add to `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

---

## Performance Testing

### Using Apache Bench (ab)

```bash
# Install (if needed)
# Ubuntu: sudo apt-get install apache2-utils
# Mac: pre-installed

# Test list endpoint
ab -n 100 -c 10 http://localhost:8000/api/users/
```

### Using wrk

```bash
# Install wrk
# Linux: sudo apt-get install wrk
# Mac: brew install wrk

# Run load test
wrk -t4 -c100 -d30s http://localhost:8000/api/users/
```

---

## Production Considerations

This setup uses Django's development server (`runserver`), which is **NOT** for production.

For production, use:
- **Gunicorn** or **uWSGI** as WSGI server
- **Nginx** as reverse proxy
- **PostgreSQL** instead of MySQL (recommended)
- Environment-based configuration
- SSL/TLS certificates

Example production command:
```bash
gunicorn user_management.wsgi:application --bind 0.0.0.0:8000
```

---

## Summary

**Docker (Easiest):**
```bash
docker-compose up backend db
```

**Local Development:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Test:**
```bash
curl http://localhost:8000/api/users/
```

✅ Backend is now running independently!

