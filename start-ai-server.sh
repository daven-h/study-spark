#!/bin/bash

echo "🧠 Starting Study Spark AI Attention Tracking Server..."
echo ""
echo "📋 Prerequisites:"
echo "  1. Python 3.8+ installed"
echo "  2. Webcam connected"
echo "  3. Python dependencies installed"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  No virtual environment found. Creating one..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
echo "📦 Checking dependencies..."
if ! python -c "import flask" 2>/dev/null; then
    echo "📥 Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies already installed"
fi

echo ""
echo "🚀 Starting AI server on http://localhost:8765"
echo "   Press Ctrl+C to stop"
echo ""

cd src/attention
python3 main_server.py
