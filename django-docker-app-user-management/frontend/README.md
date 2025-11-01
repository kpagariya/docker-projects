# User Management Frontend - JavaScript Application

This is a JavaScript-based frontend for the User Management application with OAuth2 Microsoft Entra (Azure AD) authentication.

## Features

- Modern responsive UI using Bootstrap 5
- OAuth2 authentication with Microsoft Entra (Azure AD)
- CRUD operations for user management
- Clean and intuitive user interface
- Real-time form validation
- Alert notifications for user feedback

## Technologies Used

- HTML5
- CSS3
- JavaScript (ES6+)
- Bootstrap 5.3.2
- Bootstrap Icons
- Microsoft Authentication Library (MSAL) 2.30.0

## Setup Instructions

### 1. Authentication Configuration

The application supports two authentication modes:

#### **Simple Login (Default - No Setup Required)**

By default, the application uses simple authentication. Just run the application and login with:
- **Username:** `admin`
- **Password:** `admin`

#### **Microsoft Entra (Azure AD) OAuth2 (Optional)**

To enable Microsoft Entra ID authentication:

1. **Register your application in Azure Portal:**
   - Go to [Azure Portal](https://portal.azure.com)
   - Navigate to **Azure Active Directory** > **App registrations**
   - Click **New registration**
   - Enter application name (e.g., "User Management App")
   - Select supported account types
   - Add redirect URI: `http://localhost:3000` (or your application URL)
   - Click **Register**
   - Note down the **Application (client) ID** and **Directory (tenant) ID**
   - Go to **Authentication** section:
     - Add redirect URI: `http://localhost:3000`
     - Enable **Access tokens** and **ID tokens**
     - Save changes
   - Go to **API permissions**:
     - Ensure **User.Read** permission is granted

2. **Update Configuration** in `js/config.js`:

```javascript
const AUTH_CONFIG = {
    USE_ENTRA_ID: true,  // Change from false to true
    // ...
};

const MSAL_CONFIG = {
    auth: {
        clientId: 'YOUR_CLIENT_ID', // Replace with your Application (client) ID
        authority: 'https://login.microsoftonline.com/YOUR_TENANT_ID', // Replace with your Tenant ID
        redirectUri: window.location.origin,
    },
    // ...
};
```

### 2. Update API Configuration (if needed)

If your backend is running on a different host, update the API base URL in `js/config.js`:

```javascript
const API_CONFIG = {
    BASE_URL: 'http://localhost:8000/api',
    // ...
};
```

### 3. Local Development

#### Option 1: Using Python HTTP Server

```bash
python -m http.server 3000
```

#### Option 2: Using Node.js HTTP Server

```bash
npx http-server -p 3000
```

#### Option 3: Using Live Server (VS Code Extension)

Install Live Server extension and click "Go Live" button.

Access the application at `http://localhost:3000`

### 4. Docker Deployment

See the main project README for Docker deployment instructions.

## Application Structure

```
frontend/
├── index.html          # Main HTML file
├── css/
│   └── styles.css      # Custom styles
├── js/
│   ├── config.js       # Configuration (API & OAuth2)
│   ├── auth.js         # Authentication logic
│   └── app.js          # Application logic (CRUD operations)
├── Dockerfile          # Docker configuration
├── nginx.conf          # Nginx configuration
└── README.md           # This file
```

## Features Overview

### Authentication
- Login with Microsoft account (OAuth2)
- Secure token-based authentication
- Automatic token refresh
- Logout functionality

### User Management
- **List Users**: View all users in a table
- **Create User**: Add new users with form validation
- **Update User**: Edit existing user information
- **Delete User**: Remove users with confirmation dialog

### UI/UX Features
- Responsive design (mobile-friendly)
- Loading indicators
- Success/error notifications
- Form validation
- Confirmation dialogs for destructive actions
- Clean and modern interface

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Security Considerations

1. **OAuth2 Authentication**: Uses Microsoft Entra for secure authentication
2. **XSS Protection**: HTML escaping for user-generated content
3. **HTTPS**: Use HTTPS in production for secure communication
4. **Token Storage**: Tokens stored securely in localStorage
5. **CORS**: Configure CORS properly in the backend

## Troubleshooting

### Login Issues
- Verify CLIENT_ID and TENANT_ID in `config.js`
- Check redirect URI matches Azure AD configuration
- Ensure browser allows pop-ups

### API Connection Issues
- Verify backend is running
- Check API_BASE_URL in `config.js`
- Ensure CORS is properly configured in backend

### Browser Console Errors
- Open browser DevTools (F12)
- Check Console tab for error messages
- Verify network requests in Network tab

