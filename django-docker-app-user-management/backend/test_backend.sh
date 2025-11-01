#!/bin/bash

# Quick Backend Test Script
# This script tests if the backend is running and responding correctly

echo "=================================="
echo "  Backend API Health Check"
echo "=================================="
echo ""

BASE_URL="http://localhost:8000"

# Check if server is running
echo "1. Checking if backend server is running..."
if curl -s -o /dev/null -w "%{http_code}" $BASE_URL/admin/ | grep -q "200\|302"; then
    echo "   ✓ Backend server is running"
else
    echo "   ✗ Backend server is NOT running"
    echo "   Start with: docker-compose up backend db"
    echo "   Or: python manage.py runserver"
    exit 1
fi

echo ""
echo "2. Testing API endpoint..."
RESPONSE=$(curl -s -w "\n%{http_code}" $BASE_URL/api/users/)
STATUS_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$STATUS_CODE" = "200" ]; then
    echo "   ✓ API is responding (Status: 200)"
    echo "   Response: $BODY"
else
    echo "   ✗ API returned status: $STATUS_CODE"
    echo "   Response: $BODY"
fi

echo ""
echo "3. Testing user creation..."
CREATE_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","phone":"+1234567890"}')

CREATE_STATUS=$(echo "$CREATE_RESPONSE" | tail -n1)
CREATE_BODY=$(echo "$CREATE_RESPONSE" | sed '$d')

if [ "$CREATE_STATUS" = "201" ]; then
    echo "   ✓ User created successfully (Status: 201)"
    USER_ID=$(echo "$CREATE_BODY" | grep -o '"id":[0-9]*' | grep -o '[0-9]*')
    echo "   Created User ID: $USER_ID"
    
    # Clean up - delete the test user
    if [ ! -z "$USER_ID" ]; then
        DELETE_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE $BASE_URL/api/users/$USER_ID/)
        if [ "$DELETE_STATUS" = "200" ]; then
            echo "   ✓ Test user cleaned up (Status: 200)"
        fi
    fi
else
    echo "   ✗ User creation failed (Status: $CREATE_STATUS)"
    echo "   Response: $CREATE_BODY"
fi

echo ""
echo "=================================="
echo "  Test Summary"
echo "=================================="
echo ""
echo "Backend API is accessible at:"
echo "  - API:         $BASE_URL/api/users/"
echo "  - Admin:       $BASE_URL/admin/"
echo ""
echo "Try the Python test script for detailed testing:"
echo "  pip install requests"
echo "  python test_api.py"
echo ""

