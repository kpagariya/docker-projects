/**
 * Main application logic for User Management
 */

let deleteUserId = null;
let isEditMode = false;

// Bootstrap modal instances
let userModal;
let deleteModal;

// Initialize modals when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    userModal = new bootstrap.Modal(document.getElementById('userModal'));
    deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
});

/**
 * Show alert message
 */
function showAlert(type, message) {
    const alertContainer = document.getElementById('alertContainer');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    alertContainer.appendChild(alert);
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        alert.remove();
    }, 5000);
}

/**
 * Load all users
 */
async function loadUsers() {
    const tableBody = document.getElementById('usersTableBody');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const noDataMessage = document.getElementById('noDataMessage');
    
    try {
        loadingSpinner.classList.remove('d-none');
        tableBody.innerHTML = '';
        noDataMessage.classList.add('d-none');
        
        const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.USERS}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch users');
        }
        
        const result = await response.json();
        const users = result.data || [];
        
        loadingSpinner.classList.add('d-none');
        
        if (users.length === 0) {
            noDataMessage.classList.remove('d-none');
            return;
        }
        
        users.forEach(user => {
            const row = createUserRow(user);
            tableBody.appendChild(row);
        });
        
    } catch (error) {
        console.error('Error loading users:', error);
        loadingSpinner.classList.add('d-none');
        showAlert('danger', 'Failed to load users. Please try again.');
    }
}

/**
 * Create table row for a user
 */
function createUserRow(user) {
    const row = document.createElement('tr');
    const createdDate = new Date(user.created_at).toLocaleDateString();
    
    row.innerHTML = `
        <td>${user.id}</td>
        <td>${escapeHtml(user.name)}</td>
        <td>${escapeHtml(user.email)}</td>
        <td>${escapeHtml(user.phone)}</td>
        <td>${createdDate}</td>
        <td class="action-buttons">
            <button class="btn btn-sm btn-primary" onclick="openEditModal(${user.id})" title="Edit">
                <i class="bi bi-pencil"></i>
            </button>
            <button class="btn btn-sm btn-danger" onclick="openDeleteModal(${user.id})" title="Delete">
                <i class="bi bi-trash"></i>
            </button>
        </td>
    `;
    
    return row;
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Open create modal
 */
function openCreateModal() {
    isEditMode = false;
    document.getElementById('userModalTitle').textContent = 'Add New User';
    document.getElementById('userForm').reset();
    document.getElementById('userId').value = '';
    
    // Remove validation classes
    const form = document.getElementById('userForm');
    form.classList.remove('was-validated');
}

/**
 * Open edit modal
 */
async function openEditModal(userId) {
    isEditMode = true;
    document.getElementById('userModalTitle').textContent = 'Edit User';
    
    try {
        const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.USERS}${userId}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch user details');
        }
        
        const result = await response.json();
        const user = result.data;
        
        document.getElementById('userId').value = user.id;
        document.getElementById('userName').value = user.name;
        document.getElementById('userEmail').value = user.email;
        document.getElementById('userPhone').value = user.phone;
        
        userModal.show();
        
    } catch (error) {
        console.error('Error loading user details:', error);
        showAlert('danger', 'Failed to load user details. Please try again.');
    }
}

/**
 * Save user (create or update)
 */
async function saveUser() {
    const form = document.getElementById('userForm');
    
    // Validate form
    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return;
    }
    
    const userId = document.getElementById('userId').value;
    const userData = {
        name: document.getElementById('userName').value,
        email: document.getElementById('userEmail').value,
        phone: document.getElementById('userPhone').value
    };
    
    try {
        let url = `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.USERS}`;
        let method = 'POST';
        
        if (isEditMode && userId) {
            url += `${userId}/`;
            method = 'PUT';
        }
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        });
        
        const result = await response.json();
        
        if (!response.ok) {
            let errorMessage = 'Failed to save user. ';
            if (result.errors) {
                errorMessage += Object.values(result.errors).flat().join(' ');
            }
            throw new Error(errorMessage);
        }
        
        userModal.hide();
        showAlert('success', result.message || 'User saved successfully!');
        loadUsers();
        form.reset();
        form.classList.remove('was-validated');
        
    } catch (error) {
        console.error('Error saving user:', error);
        showAlert('danger', error.message);
    }
}

/**
 * Open delete confirmation modal
 */
function openDeleteModal(userId) {
    deleteUserId = userId;
    deleteModal.show();
}

/**
 * Confirm and delete user
 */
async function confirmDelete() {
    if (!deleteUserId) return;
    
    try {
        const response = await fetch(
            `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.USERS}${deleteUserId}/`,
            {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                }
            }
        );
        
        if (!response.ok) {
            throw new Error('Failed to delete user');
        }
        
        const result = await response.json();
        
        deleteModal.hide();
        showAlert('success', result.message || 'User deleted successfully!');
        loadUsers();
        deleteUserId = null;
        
    } catch (error) {
        console.error('Error deleting user:', error);
        showAlert('danger', 'Failed to delete user. Please try again.');
    }
}

