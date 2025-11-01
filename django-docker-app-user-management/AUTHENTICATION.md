# Authentication Configuration Guide

This application supports two authentication modes that can be easily switched via configuration.

## Authentication Modes

### 1. Simple Login (Default) ✅

**Status:** Enabled by default - No setup required!

**Credentials:**
- Username: `admin`
- Password: `admin`

**How it works:**
- Simple username/password form
- Credentials validated against config file
- Session stored in browser localStorage
- Perfect for development and testing

**Configuration:**
```javascript
// frontend/js/config.js
const AUTH_CONFIG = {
    USE_ENTRA_ID: false,  // ← Default
    SIMPLE_LOGIN: {
        USERNAME: 'admin',
        PASSWORD: 'admin'
    }
};
```

### 2. Microsoft Entra (Azure AD) OAuth2

**Status:** Available but requires setup

**How it works:**
- Redirects to Microsoft login page
- OAuth2 authentication flow
- Access tokens for secure API calls
- Enterprise-grade security

**Setup Steps:**

1. **Register Application in Azure Portal:**
   ```
   Portal: https://portal.azure.com
   Path: Azure Active Directory → App registrations → New registration
   ```

2. **Configure Application:**
   - Name: "User Management App"
   - Redirect URI: `http://localhost:3000`
   - Enable: Access tokens & ID tokens
   - API Permissions: User.Read

3. **Get Credentials:**
   - Copy: Application (client) ID
   - Copy: Directory (tenant) ID

4. **Update Configuration:**
   ```javascript
   // frontend/js/config.js
   const AUTH_CONFIG = {
       USE_ENTRA_ID: true,  // ← Change to true
       // ...
   };

   const MSAL_CONFIG = {
       auth: {
           clientId: 'YOUR_CLIENT_ID',      // ← Paste your Client ID
           authority: 'https://login.microsoftonline.com/YOUR_TENANT_ID',  // ← Add Tenant ID
           redirectUri: 'http://localhost:3000',
       },
       // ...
   };
   ```

5. **Restart the application**

## Switching Between Modes

Simply change the `USE_ENTRA_ID` flag in `frontend/js/config.js`:

```javascript
// Simple Login
const AUTH_CONFIG = {
    USE_ENTRA_ID: false,
    // ...
};

// Microsoft Entra ID
const AUTH_CONFIG = {
    USE_ENTRA_ID: true,
    // ...
};
```

**No code changes needed!** Just update the config and refresh the page.

## Customizing Simple Login Credentials

You can change the default admin credentials:

```javascript
// frontend/js/config.js
const AUTH_CONFIG = {
    USE_ENTRA_ID: false,
    SIMPLE_LOGIN: {
        USERNAME: 'myusername',  // ← Change this
        PASSWORD: 'mypassword'   // ← Change this
    }
};
```

## Security Notes

### Simple Login
- ⚠️ **For development only** - not suitable for production
- Credentials are stored in plain text in config file
- No encryption or secure token handling
- Use only in trusted environments

### Microsoft Entra ID
- ✅ **Production-ready** - enterprise-grade security
- OAuth2 standard authentication
- Secure token management
- Single Sign-On (SSO) support
- Multi-factor authentication support

## Troubleshooting

### Simple Login Issues

**Problem:** Login not working
- **Solution:** Verify credentials in `config.js` match what you're entering
- **Solution:** Check browser console for JavaScript errors

**Problem:** Logged out unexpectedly
- **Solution:** Check if localStorage is cleared
- **Solution:** Browser may have cleared storage

### Entra ID Issues

**Problem:** Popup blocked
- **Solution:** Allow popups for your site

**Problem:** Login fails
- **Solution:** Verify CLIENT_ID and TENANT_ID are correct
- **Solution:** Check redirect URI matches Azure configuration

**Problem:** "User.Read permission not granted" error
- **Solution:** Grant User.Read permission in Azure Portal

## Quick Start

### Development (Simple Login)
```bash
# No setup needed!
docker-compose up --build

# Login with: admin/admin
```

### Production (Microsoft Entra ID)
```bash
# 1. Setup Azure AD app
# 2. Update frontend/js/config.js
# 3. Set USE_ENTRA_ID: true
# 4. Add CLIENT_ID and TENANT_ID

docker-compose up --build
```

## FAQ

**Q: Can I use both authentication methods simultaneously?**  
A: No, you must choose one mode at a time via `USE_ENTRA_ID` flag.

**Q: Will my users need to re-login when I switch modes?**  
A: Yes, switching authentication modes will require all users to login again.

**Q: Can I add multiple admin users to simple login?**  
A: Currently it supports one set of credentials. You can extend `auth.js` to support multiple users.

**Q: Is simple login secure enough for production?**  
A: No, use Microsoft Entra ID or implement a proper authentication backend for production.

**Q: Can I use other OAuth providers (Google, GitHub)?**  
A: The code structure supports it, but you'll need to modify `auth.js` to add other providers.

## Summary

| Feature | Simple Login | Microsoft Entra ID |
|---------|-------------|-------------------|
| Setup Required | ❌ None | ✅ Azure Portal |
| Security Level | 🔸 Basic | 🔒 Enterprise |
| Use Case | Development | Production |
| SSO Support | ❌ No | ✅ Yes |
| MFA Support | ❌ No | ✅ Yes |
| Cost | Free | Free (Azure AD) |

---

**Default Mode:** Simple Login (admin/admin)  
**Recommended for Production:** Microsoft Entra ID

