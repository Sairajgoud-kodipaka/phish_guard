#!/bin/bash

echo "================================================================"
echo "🚀 PHISHGUARD - AI-Powered Email Security Platform"
echo "================================================================"
echo "🔒 Backend: FastAPI + ML Models"
echo "🎨 Frontend: Next.js + React"
echo "🤖 AI: Spam Detection & Threat Analysis"
echo "================================================================"

echo ""
echo "🔍 Checking system requirements..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.8+"
    exit 1
fi
echo "✅ Python3 found"

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js"
    exit 1
fi
echo "✅ Node.js found"

# Check if npm is available
if ! command -v npm &> /dev/null; then
    echo "❌ npm not found. Please install npm"
    exit 1
fi
echo "✅ npm found"

echo ""
echo "📦 Installing dependencies..."

# Install backend dependencies
echo "🔧 Installing backend dependencies..."
cd backend
python3 -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install backend dependencies"
    exit 1
fi
echo "✅ Backend dependencies installed"

# Install frontend dependencies
echo "🔧 Installing frontend dependencies..."
cd ../frontend
npm install
if [ $? -ne 0 ]; then
    echo "❌ Failed to install frontend dependencies"
    exit 1
fi
echo "✅ Frontend dependencies installed"

echo ""
echo "🚀 Starting PhishGuard services..."

# Start backend in background
echo "🔒 Starting backend service..."
cd ../backend
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 5

# Start frontend in background
echo "🎨 Starting frontend service..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

# Wait a bit for frontend to start
sleep 8

echo ""
echo "⏳ Waiting for services to be ready..."

# Wait for services to be ready
BACKEND_READY=false
FRONTEND_READY=false

for i in {1..30}; do
    if [ "$BACKEND_READY" = false ]; then
        if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
            BACKEND_READY=true
            echo "✅ Backend service is ready"
        fi
    fi
    
    if [ "$FRONTEND_READY" = false ]; then
        if curl -s http://localhost:3000 > /dev/null 2>&1; then
            FRONTEND_READY=true
            echo "✅ Frontend service is ready"
        fi
    fi
    
    if [ "$BACKEND_READY" = true ] && [ "$FRONTEND_READY" = true ]; then
        break
    fi
    
    echo "   Waiting... ($i/30)"
    sleep 1
done

echo ""
echo "================================================================"
echo "📊 PHISHGUARD STATUS"
echo "================================================================"
echo "🔒 Backend: ✅ RUNNING (http://localhost:8000)"
echo "🎨 Frontend: ✅ RUNNING (http://localhost:3000)"
echo ""
echo "🎯 Your PhishGuard application is ready!"
echo "🔍 Access your application at: http://localhost:3000"
echo "📚 API documentation at: http://localhost:8000/docs"
echo ""
echo "💡 Press Ctrl+C to stop all services"
echo "================================================================"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down PhishGuard services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Services stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Open the application in browser
echo ""
echo "🌐 Opening PhishGuard application..."
if command -v xdg-open &> /dev/null; then
    # Linux
    xdg-open http://localhost:3000 &
    xdg-open http://localhost:8000/docs &
elif command -v open &> /dev/null; then
    # macOS
    open http://localhost:3000
    open http://localhost:8000/docs
else
    echo "💡 Please manually open:"
    echo "   Frontend: http://localhost:3000"
    echo "   API Docs: http://localhost:8000/docs"
fi

echo ""
echo "🎉 PhishGuard started successfully!"
echo "Services are running in the background."
echo "Press Ctrl+C to stop all services."

# Keep the script running
while true; do
    sleep 1
done
