# User Management Application

A complete user management system with Django REST API backend, JavaScript frontend, and OAuth2 Microsoft Entra authentication.

## 🚀 Features

### Backend (Django)
- RESTful API with CRUD operations
- MySQL database integration
- Django REST Framework
- CORS enabled
- Docker support

### Frontend (JavaScript)
- Modern responsive UI with Bootstrap 5
- OAuth2 authentication with Microsoft Entra (Azure AD)
- Real-time form validation
- CRUD operations interface
- Clean and intuitive design

### User Model
- Name
- Email (unique)
- Phone
- Timestamps (created_at, updated_at)

## 📋 Prerequisites

- Docker and Docker Compose
- Microsoft Entra (Azure AD) account for OAuth2 setup

### For Local Development (without Docker)
- Python 3.11+
- MySQL 8.0+
- Modern web browser

## 🛠️ Quick Start with Docker

### 1. Clone the Repository

```bash
cd user-management-app
```

### 2. Authentication Configuration

> 📖 **Detailed Guide:** See [AUTHENTICATION.md](AUTHENTICATION.md) for complete authentication setup guide.

The application supports two authentication modes:

#### **Option A: Simple Login (Default)**
By default, the application uses simple authentication with credentials: **admin/admin**

No additional configuration needed! Just start the application and login with:
- Username: `admin`
- Password: `admin`

#### **Option B: Microsoft Entra (Azure AD) OAuth2**

To enable Microsoft Entra ID authentication:

1. **Register app in Azure Portal:**
   - Go to [Azure Portal](https://portal.azure.com)
   - Navigate to **Azure Active Directory** > **App registrations**
   - Click **New registration**
   - Enter application details and redirect URI: `http://localhost:3000`
   - Note down **Application (client) ID** and **Directory (tenant) ID**
   - Enable required API permissions: `User.Read`

2. **Update configuration** in `frontend/js/config.js`:

```javascript
const AUTH_CONFIG = {
    USE_ENTRA_ID: true,  // Change to true
    // ...
};

const MSAL_CONFIG = {
    auth: {
        clientId: 'YOUR_CLIENT_ID',        // Add your Client ID
        authority: 'https://login.microsoftonline.com/YOUR_TENANT_ID',  // Add your Tenant ID
        redirectUri: 'http://localhost:3000',
    },
    // ...
};
```

### 3. Start the Application

```bash
docker-compose up --build
```

This will start:
- MySQL database on port 3306
- Django backend on port 8000
- Frontend on port 3000

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/

### 5. Login

**Default Credentials:**
- Username: `admin`
- Password: `admin`

### 6. Create Django Superuser (Optional)

```bash
docker exec -it user_management_backend python manage.py createsuperuser
```

## 🏗️ Project Structure

```
user-management-app/
├── backend/                    # Django Backend
│   ├── user_management/        # Django project
│   │   ├── settings.py         # Settings
│   │   └── urls.py             # URL configuration
│   ├── users/                  # Users app
│   │   ├── models.py           # User model
│   │   ├── serializers.py      # DRF serializers
│   │   ├── views.py            # API views
│   │   └── urls.py             # App URLs
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile              # Backend Docker config
│   └── README.md               # Backend documentation
│
├── frontend/                   # JavaScript Frontend
│   ├── index.html              # Main HTML
│   ├── css/
│   │   └── styles.css          # Custom styles
│   ├── js/
│   │   ├── config.js           # Configuration
│   │   ├── auth.js             # Authentication
│   │   └── app.js              # Main app logic
│   ├── Dockerfile              # Frontend Docker config
│   ├── nginx.conf              # Nginx configuration
│   └── README.md               # Frontend documentation
│
├── docker-compose.yml          # Docker Compose config
└── README.md                   # This file
```

## 🔌 API Endpoints

All endpoints are prefixed with `/api/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/` | List all users |
| POST | `/api/users/` | Create a new user |
| GET | `/api/users/{id}/` | Get user details |
| PUT | `/api/users/{id}/` | Update user |
| PATCH | `/api/users/{id}/` | Partial update user |
| DELETE | `/api/users/{id}/` | Delete user |

### Example API Request

**Create User:**
```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890"
  }'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "created_at": "2025-10-30T10:00:00Z",
    "updated_at": "2025-10-30T10:00:00Z"
  },
  "message": "User created successfully"
}
```

## 🔧 Local Development (without Docker)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Update .env with your MySQL credentials

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Frontend Setup

```bash
cd frontend

# Serve with Python
python -m http.server 3000

# Or with Node.js
npx http-server -p 3000
```

## 🐳 Docker Commands

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Rebuild and start
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Execute commands in backend
docker exec -it user_management_backend python manage.py migrate
docker exec -it user_management_backend python manage.py createsuperuser

# Access MySQL
docker exec -it user_management_db mysql -uroot -ppassword user_management_db
```

## 🔒 Security Notes

1. **Change Default Passwords**: Update MySQL and Django secret keys in production
2. **Use HTTPS**: Deploy with SSL/TLS certificates
3. **Environment Variables**: Use secure environment variable management
4. **CORS**: Restrict CORS origins to your actual domains
5. **OAuth2**: Keep client secrets secure, never commit to version control

## 📝 Environment Variables

### Backend (.env)

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DB_NAME=user_management_db
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=db
DB_PORT=3306
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

### Frontend (config.js)

```javascript
clientId: 'YOUR_AZURE_CLIENT_ID'
authority: 'https://login.microsoftonline.com/YOUR_TENANT_ID'
BASE_URL: 'https://api.yourdomain.com/api'
```

## 🧪 Testing the Application

1. **Login**: Click "Sign in with Microsoft" and authenticate
2. **Create User**: Click "Add New User" and fill the form
3. **View Users**: All users are displayed in the table
4. **Edit User**: Click edit icon, modify details, and save
5. **Delete User**: Click delete icon and confirm

## 🐛 Troubleshooting

### Backend Issues

**Database Connection Error:**
- Ensure MySQL is running
- Check database credentials in `.env`
- Wait for database to be ready (use healthcheck)

**CORS Error:**
- Update `CORS_ALLOWED_ORIGINS` in settings
- Restart backend server

### Frontend Issues

**Authentication Error:**
- Verify Azure AD configuration
- Check CLIENT_ID and TENANT_ID in `config.js`
- Ensure redirect URI matches

**API Connection Error:**
- Verify backend is running
- Check API_BASE_URL in `config.js`
- Check browser console for errors

### Docker Issues

**Container Won't Start:**
```bash
docker-compose logs backend
docker-compose logs db
```

**Reset Everything:**
```bash
docker-compose down -v
docker-compose up --build
```

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [Microsoft Identity Platform](https://docs.microsoft.com/azure/active-directory/develop/)
- [MSAL.js Documentation](https://github.com/AzureAD/microsoft-authentication-library-for-js)

## 📄 License

This project is created for educational purposes.

## 👥 Contributing

Feel free to submit issues and enhancement requests!

## 📧 Support

For questions and support, please refer to the individual README files in the `backend/` and `frontend/` directories.

