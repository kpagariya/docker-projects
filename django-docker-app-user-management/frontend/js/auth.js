/**
 * Authentication module
 * Supports both Microsoft Entra (Azure AD) OAuth2 and Simple Login
 */

// Initialize MSAL (only if using Entra ID)
let msalInstance = null;
if (AUTH_CONFIG.USE_ENTRA_ID && typeof msal !== 'undefined') {
    msalInstance = new msal.PublicClientApplication(MSAL_CONFIG);
}

// Account object
let currentAccount = null;

/**
 * Initialize authentication
 */
async function initAuth() {
    if (AUTH_CONFIG.USE_ENTRA_ID) {
        // Use Microsoft Entra ID authentication
        await initEntraAuth();
    } else {
        // Use simple login authentication
        await initSimpleAuth();
    }
}

/**
 * Initialize Microsoft Entra ID authentication
 */
async function initEntraAuth() {
    await msalInstance.initialize();
    
    // Check if user is already signed in
    const accounts = msalInstance.getAllAccounts();
    
    if (accounts.length > 0) {
        currentAccount = accounts[0];
        showMainPage();
    } else {
        showLoginPage();
    }
}

/**
 * Initialize simple authentication
 */
async function initSimpleAuth() {
    // Check if user is already logged in (stored in localStorage)
    const loggedInUser = localStorage.getItem('simpleAuthUser');
    
    if (loggedInUser) {
        currentAccount = { name: loggedInUser, username: loggedInUser };
        showMainPage();
    } else {
        showLoginPage();
    }
}

/**
 * Handle login button click
 */
async function handleLogin() {
    if (AUTH_CONFIG.USE_ENTRA_ID) {
        await handleEntraLogin();
    } else {
        await handleSimpleLogin();
    }
}

/**
 * Handle Microsoft Entra ID login
 */
async function handleEntraLogin() {
    try {
        const loginResponse = await msalInstance.loginPopup(LOGIN_REQUEST);
        currentAccount = loginResponse.account;
        showMainPage();
    } catch (error) {
        console.error('Login error:', error);
        showError('loginError', 'Failed to login: ' + error.message);
    }
}

/**
 * Handle simple login
 */
async function handleSimpleLogin() {
    const username = document.getElementById('simpleUsername').value;
    const password = document.getElementById('simplePassword').value;
    
    // Clear any previous errors
    document.getElementById('loginError').classList.add('d-none');
    
    // Validate credentials
    if (username === AUTH_CONFIG.SIMPLE_LOGIN.USERNAME && 
        password === AUTH_CONFIG.SIMPLE_LOGIN.PASSWORD) {
        // Store login state
        localStorage.setItem('simpleAuthUser', username);
        currentAccount = { name: username, username: username };
        showMainPage();
    } else {
        showError('loginError', 'Invalid username or password. Use admin/admin');
    }
}

/**
 * Handle logout button click
 */
async function handleLogout() {
    if (AUTH_CONFIG.USE_ENTRA_ID) {
        await handleEntraLogout();
    } else {
        await handleSimpleLogout();
    }
}

/**
 * Handle Microsoft Entra ID logout
 */
async function handleEntraLogout() {
    try {
        await msalInstance.logoutPopup({
            account: currentAccount,
            postLogoutRedirectUri: window.location.origin
        });
        currentAccount = null;
        showLoginPage();
    } catch (error) {
        console.error('Logout error:', error);
        showAlert('danger', 'Failed to logout: ' + error.message);
    }
}

/**
 * Handle simple logout
 */
async function handleSimpleLogout() {
    localStorage.removeItem('simpleAuthUser');
    currentAccount = null;
    showLoginPage();
    // Clear form
    document.getElementById('simpleUsername').value = '';
    document.getElementById('simplePassword').value = '';
}

/**
 * Get access token for API calls (only for Entra ID)
 */
async function getAccessToken() {
    if (!AUTH_CONFIG.USE_ENTRA_ID) {
        return null; // No token needed for simple auth
    }
    
    if (!currentAccount) {
        throw new Error('No user is signed in');
    }

    try {
        const response = await msalInstance.acquireTokenSilent({
            ...TOKEN_REQUEST,
            account: currentAccount
        });
        return response.accessToken;
    } catch (error) {
        console.error('Token acquisition error:', error);
        
        // If silent token acquisition fails, try interactive method
        if (error instanceof msal.InteractionRequiredAuthError) {
            const response = await msalInstance.acquireTokenPopup(TOKEN_REQUEST);
            return response.accessToken;
        }
        throw error;
    }
}

/**
 * Show login page
 */
function showLoginPage() {
    const loginPage = document.getElementById('loginPage');
    const mainPage = document.getElementById('mainPage');
    
    loginPage.classList.remove('d-none');
    mainPage.classList.add('d-none');
    
    // Show appropriate login form
    const entraLoginForm = document.getElementById('entraLoginForm');
    const simpleLoginForm = document.getElementById('simpleLoginForm');
    
    if (AUTH_CONFIG.USE_ENTRA_ID) {
        entraLoginForm.classList.remove('d-none');
        simpleLoginForm.classList.add('d-none');
    } else {
        entraLoginForm.classList.add('d-none');
        simpleLoginForm.classList.remove('d-none');
    }
}

/**
 * Show main application page
 */
function showMainPage() {
    document.getElementById('loginPage').classList.add('d-none');
    document.getElementById('mainPage').classList.remove('d-none');
    
    // Display user name
    if (currentAccount) {
        document.getElementById('userDisplayName').textContent = 
            currentAccount.name || currentAccount.username;
    }
    
    // Load users
    loadUsers();
}

/**
 * Show error message on login page
 */
function showError(elementId, message) {
    const errorElement = document.getElementById(elementId);
    errorElement.textContent = message;
    errorElement.classList.remove('d-none');
    
    setTimeout(() => {
        errorElement.classList.add('d-none');
    }, 5000);
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    initAuth();
    
    // Entra ID login button
    const entraLoginBtn = document.getElementById('loginBtn');
    if (entraLoginBtn) {
        entraLoginBtn.addEventListener('click', handleLogin);
    }
    
    // Simple login form
    const simpleLoginBtn = document.getElementById('simpleLoginBtn');
    if (simpleLoginBtn) {
        simpleLoginBtn.addEventListener('click', (e) => {
            e.preventDefault();
            handleLogin();
        });
    }
    
    // Allow Enter key to submit simple login form
    const simplePassword = document.getElementById('simplePassword');
    if (simplePassword) {
        simplePassword.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                handleLogin();
            }
        });
    }
    
    // Logout button
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }
});

