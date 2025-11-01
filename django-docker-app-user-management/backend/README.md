# User Management Backend - Django REST API

This is a Django REST API backend for User Management application with MySQL database.

## Features

- User CRUD operations (Create, Read, Update, Delete)
- RESTful API endpoints
- MySQL database integration
- CORS enabled for frontend integration
- Docker support

## User Model

- Name (CharField)
- Email (EmailField, unique)
- Phone (CharField)
- Created At (DateTimeField)
- Updated At (DateTimeField)

## API Endpoints

All endpoints are prefixed with `/api/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/` | List all users |
| POST | `/api/users/` | Create a new user |
| GET | `/api/users/{id}/` | Get a specific user |
| PUT | `/api/users/{id}/` | Update a user |
| PATCH | `/api/users/{id}/` | Partially update a user |
| DELETE | `/api/users/{id}/` | Delete a user |

## Quick Start - Backend Only

### Option 1: Docker (Recommended)

Run just the backend and database:

```bash
# From project root
docker-compose up backend db

# Or in detached mode
docker-compose up -d backend db
```

**Access:**
- API: http://localhost:8000/api/users/
- Admin: http://localhost:8000/admin/

### Option 2: Quick Test

```bash
# Windows
cd backend
test_backend.bat

# Linux/Mac
cd backend
chmod +x test_backend.sh
./test_backend.sh
```

---

## Detailed Setup Instructions

📖 **For comprehensive standalone setup:** See [RUN_STANDALONE.md](RUN_STANDALONE.md)

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file from `.env.example`:
```bash
cp .env.example .env
```

3. Update `.env` with your MySQL credentials

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser (optional):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

### Docker Deployment

See the main project README for Docker deployment instructions.

---

## Testing the Backend

### Quick Health Check

**Windows:**
```bash
cd backend
test_backend.bat
```

**Linux/Mac:**
```bash
cd backend
chmod +x test_backend.sh
./test_backend.sh
```

### Comprehensive API Testing

```bash
cd backend

# Install requests library
pip install requests

# Run test suite
python test_api.py
```

This will test all CRUD operations:
- ✓ List users
- ✓ Create user
- ✓ Get user
- ✓ Update user
- ✓ Delete user
- ✓ Validation

### Manual Testing with curl

```bash
# List all users
curl http://localhost:8000/api/users/

# Create a user
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","phone":"+1234567890"}'

# Get specific user (replace 1 with actual ID)
curl http://localhost:8000/api/users/1/

# Update user
curl -X PUT http://localhost:8000/api/users/1/ \
  -H "Content-Type: application/json" \
  -d '{"name":"John Smith","email":"john.smith@example.com","phone":"+1234567890"}'

# Delete user
curl -X DELETE http://localhost:8000/api/users/1/
```

### Using Browser

Open in your browser:
- API Root: http://localhost:8000/api/users/
- Django Admin: http://localhost:8000/admin/

Django REST Framework provides a browsable API interface!

## Environment Variables

- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DB_NAME`: MySQL database name
- `DB_USER`: MySQL username
- `DB_PASSWORD`: MySQL password
- `DB_HOST`: MySQL host
- `DB_PORT`: MySQL port
- `CORS_ALLOWED_ORIGINS`: Comma-separated list of allowed CORS origins

