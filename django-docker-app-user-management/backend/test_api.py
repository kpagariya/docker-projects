#!/usr/bin/env python3
"""
Simple script to test the User Management API endpoints
Usage: python test_api.py
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000/api"
HEADERS = {"Content-Type": "application/json"}

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_test(test_name):
    """Print test name"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"TEST: {test_name}")
    print(f"{'='*60}{Colors.RESET}")

def print_success(message):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")

def print_error(message):
    """Print error message"""
    print(f"{Colors.RED}✗ {message}{Colors.RESET}")

def print_response(response):
    """Pretty print response"""
    print(f"\n{Colors.YELLOW}Status Code: {response.status_code}{Colors.RESET}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

def test_list_users():
    """Test GET /api/users/ - List all users"""
    print_test("List All Users")
    try:
        response = requests.get(f"{BASE_URL}/users/", headers=HEADERS)
        print_response(response)
        
        if response.status_code == 200:
            print_success("Successfully retrieved users list")
            return True
        else:
            print_error(f"Failed with status code {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_create_user():
    """Test POST /api/users/ - Create a new user"""
    print_test("Create New User")
    
    user_data = {
        "name": f"Test User {datetime.now().strftime('%H:%M:%S')}",
        "email": f"test_{datetime.now().timestamp()}@example.com",
        "phone": "+1234567890"
    }
    
    print(f"Creating user with data: {json.dumps(user_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/users/",
            headers=HEADERS,
            json=user_data
        )
        print_response(response)
        
        if response.status_code == 201:
            user_id = response.json()['data']['id']
            print_success(f"Successfully created user with ID: {user_id}")
            return user_id
        else:
            print_error(f"Failed with status code {response.status_code}")
            return None
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return None

def test_get_user(user_id):
    """Test GET /api/users/{id}/ - Get specific user"""
    print_test(f"Get User (ID: {user_id})")
    
    try:
        response = requests.get(f"{BASE_URL}/users/{user_id}/", headers=HEADERS)
        print_response(response)
        
        if response.status_code == 200:
            print_success(f"Successfully retrieved user {user_id}")
            return True
        else:
            print_error(f"Failed with status code {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_update_user(user_id):
    """Test PUT /api/users/{id}/ - Update user"""
    print_test(f"Update User (ID: {user_id})")
    
    update_data = {
        "name": f"Updated User {datetime.now().strftime('%H:%M:%S')}",
        "email": f"updated_{datetime.now().timestamp()}@example.com",
        "phone": "+9876543210"
    }
    
    print(f"Updating user with data: {json.dumps(update_data, indent=2)}")
    
    try:
        response = requests.put(
            f"{BASE_URL}/users/{user_id}/",
            headers=HEADERS,
            json=update_data
        )
        print_response(response)
        
        if response.status_code == 200:
            print_success(f"Successfully updated user {user_id}")
            return True
        else:
            print_error(f"Failed with status code {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_delete_user(user_id):
    """Test DELETE /api/users/{id}/ - Delete user"""
    print_test(f"Delete User (ID: {user_id})")
    
    try:
        response = requests.delete(f"{BASE_URL}/users/{user_id}/", headers=HEADERS)
        print_response(response)
        
        if response.status_code == 200:
            print_success(f"Successfully deleted user {user_id}")
            return True
        else:
            print_error(f"Failed with status code {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_validation():
    """Test validation - try to create user with invalid data"""
    print_test("Test Validation (Invalid Email)")
    
    invalid_data = {
        "name": "Invalid User",
        "email": "not-an-email",  # Invalid email
        "phone": "+1234567890"
    }
    
    print(f"Attempting to create user with invalid data: {json.dumps(invalid_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/users/",
            headers=HEADERS,
            json=invalid_data
        )
        print_response(response)
        
        if response.status_code == 400:
            print_success("Validation working correctly - rejected invalid email")
            return True
        else:
            print_error("Validation not working as expected")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    print(f"\n{Colors.BLUE}")
    print("=" * 60)
    print("  USER MANAGEMENT API - TEST SUITE")
    print("=" * 60)
    print(f"{Colors.RESET}")
    print(f"Base URL: {BASE_URL}")
    print(f"Testing started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test 1: List users (initial state)
    test_list_users()
    
    # Test 2: Create user
    user_id = test_create_user()
    
    if user_id:
        # Test 3: Get the created user
        test_get_user(user_id)
        
        # Test 4: Update the user
        test_update_user(user_id)
        
        # Test 5: List users (should include our user)
        test_list_users()
        
        # Test 6: Delete the user
        test_delete_user(user_id)
        
        # Test 7: Try to get deleted user (should fail)
        print_test(f"Verify User Deletion (ID: {user_id})")
        response = requests.get(f"{BASE_URL}/users/{user_id}/", headers=HEADERS)
        if response.status_code == 404:
            print_success("User successfully deleted (404 Not Found)")
        else:
            print_error("User still exists after deletion")
    
    # Test 8: Validation
    test_validation()
    
    # Summary
    print(f"\n{Colors.BLUE}")
    print("=" * 60)
    print("  TEST SUITE COMPLETED")
    print("=" * 60)
    print(f"{Colors.RESET}")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n{Colors.GREEN}All tests completed! Check results above.{Colors.RESET}\n")

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Tests interrupted by user{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Fatal error: {str(e)}{Colors.RESET}")

