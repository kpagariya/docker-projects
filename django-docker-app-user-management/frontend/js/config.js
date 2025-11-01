/**
 * Configuration file for the User Management application
 */

// API Configuration
const API_CONFIG = {
    // Update this URL to your Django backend URL
    BASE_URL: 'http://localhost:8000/api',
    ENDPOINTS: {
        USERS: '/users/'
    }
};

// Authentication Configuration
const AUTH_CONFIG = {
    // Set to true to use Microsoft Entra (Azure AD) OAuth2
    // Set to false to use simple login (username: admin, password: admin)
    USE_ENTRA_ID: false,
    
    // Simple login credentials (used when USE_ENTRA_ID = false)
    SIMPLE_LOGIN: {
        USERNAME: 'admin',
        PASSWORD: 'admin'
    }
};

// Microsoft Entra (Azure AD) OAuth2 Configuration
// Only used when AUTH_CONFIG.USE_ENTRA_ID = true
const MSAL_CONFIG = {
    auth: {
        clientId: 'YOUR_CLIENT_ID', // Replace with your Microsoft Entra Application (client) ID
        authority: 'https://login.microsoftonline.com/YOUR_TENANT_ID', // Replace YOUR_TENANT_ID with your tenant ID or 'common'
        redirectUri: window.location.origin, // Current application URL
    },
    cache: {
        cacheLocation: 'localStorage', // This configures where your cache will be stored
        storeAuthStateInCookie: false, // Set to true for IE11 or Edge
    },
};

// Scopes for OAuth2 authentication
const LOGIN_REQUEST = {
    scopes: ['User.Read'], // Microsoft Graph API scopes
};

// Token request configuration
const TOKEN_REQUEST = {
    scopes: ['User.Read'],
    forceRefresh: false
};

