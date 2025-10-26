#!/bin/bash
# Startup script for Study Spark Attention Tracking

echo "🚀 Starting Study Spark Attention Tracking Server..."
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    exit 1
fi

# Navigate to the correct directory
cd "$(dirname "$0")"

# Check if we're in the right directory
if [ ! -f "advanced_server.py" ]; then
    echo "❌ advanced_server.py not found. Please check the file location"
    exit 1
fi

# Check if dependencies are installed
echo "🔍 Checking dependencies..."
python3 -c "import mediapipe, cv2, flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Required dependencies not installed."
    echo "📦 Installing dependencies from requirements.txt..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        echo "💡 Try running: pip3 install mediapipe opencv-python flask flask-cors numpy scipy"
        exit 1
    fi
    echo "✅ Dependencies installed successfully"
else
    echo "✅ All dependencies are installed"
fi

echo ""
echo "🎯 Starting HTTP API server on localhost:8765"
echo "📱 Make sure your camera is connected and accessible"
echo "🌐 The Next.js frontend will connect automatically"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python3 advanced_server.py
