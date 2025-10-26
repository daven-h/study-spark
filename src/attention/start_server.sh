#!/bin/bash
# Startup script for Study Spark Attention Tracking

echo "🚀 Starting Study Spark Attention Tracking Server..."
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "websocket_server.py" ]; then
    echo "❌ websocket_server.py not found. Please run this script from the src/attention directory"
    exit 1
fi

# Check if dependencies are installed
echo "🔍 Checking dependencies..."
python3 -c "import mediapipe, cv2, websockets" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Required dependencies not installed. Installing now..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
    echo "✅ Dependencies installed successfully"
else
    echo "✅ All dependencies are installed"
fi

echo ""
echo "🎯 Starting WebSocket server on localhost:8765"
echo "📱 Make sure your camera is connected and accessible"
echo "🌐 The Next.js frontend will connect automatically"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python3 advanced_server.py
