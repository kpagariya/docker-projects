#!/bin/bash
# Stop local development servers

echo "================================================"
echo "  Stopping Local Servers"
echo "================================================"
echo ""

# Stop using saved PIDs
if [ -f /tmp/backend.pid ]; then
    BACKEND_PID=$(cat /tmp/backend.pid)
    echo "Stopping Backend (PID: $BACKEND_PID)..."
    kill $BACKEND_PID 2>/dev/null
    rm /tmp/backend.pid
    echo "✓ Backend stopped"
fi

if [ -f /tmp/frontend.pid ]; then
    FRONTEND_PID=$(cat /tmp/frontend.pid)
    echo "Stopping Frontend (PID: $FRONTEND_PID)..."
    kill $FRONTEND_PID 2>/dev/null
    rm /tmp/frontend.pid
    echo "✓ Frontend stopped"
fi

# Kill any remaining processes on ports
echo ""
echo "Checking for remaining processes on ports..."
lsof -ti:8000 | xargs kill -9 2>/dev/null && echo "✓ Killed process on port 8000"
lsof -ti:3000 | xargs kill -9 2>/dev/null && echo "✓ Killed process on port 3000"

echo ""
echo "✓ All servers stopped"
echo ""

