#!/bin/bash

# FPL AI Model - Quick Start Script

echo "🚀 FPL AI Model - Quick Start"
echo "=============================="
echo ""

# Check if we're in the project root
if [ ! -f "README.md" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists python3; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js is not installed"
    exit 1
fi

if ! command_exists npm; then
    echo "❌ npm is not installed"
    exit 1
fi

echo "✅ All prerequisites met"
echo ""

# Setup backend
echo "🔧 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
fi

echo "Creating necessary directories..."
mkdir -p logs uploads models

echo "✅ Backend setup complete"
echo ""

cd ..

# Setup frontend
echo "🎨 Setting up frontend..."
cd frontend

echo "Installing npm dependencies..."
npm install --silent

echo "✅ Frontend setup complete"
echo ""

cd ..

# Start services
echo "🚀 Starting services..."
echo ""
echo "Starting backend on http://localhost:8000"
echo "Starting frontend on http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Start backend in background
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

# Start frontend
cd ../frontend
npm run dev &
FRONTEND_PID=$!

# Wait for Ctrl+C
trap "echo ''; echo '🛑 Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT

wait
