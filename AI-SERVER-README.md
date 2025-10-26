# AI Attention Tracking Server

## Overview
The AI server provides real-time attention tracking using computer vision and MediaPipe. It analyzes:
- Eye aspect ratio (EAR) - detects if eyes are open/closed
- Mouth aspect ratio (MAR) - detects yawning
- Head tilt - tracks head position
- Phone detection - detects if phone is near face
- Overall attention score - 0-100%

## Quick Start

### Option 1: Use the startup script (Recommended)
```bash
./start-ai-server.sh
```

### Option 2: Manual setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
cd src/attention
python3 complete_algorithm_server.py
```

## Requirements
- Python 3.8 or higher
- Webcam connected to your computer
- ~500MB disk space for dependencies

## API Endpoints

Once running on `http://localhost:8765`:

- `GET /api/ping` - Check if server is running
- `POST /api/start_tracking` - Start camera and tracking
- `POST /api/stop_tracking` - Stop tracking and release camera
- `GET /api/attention_data` - Get current attention metrics
- `GET /api/status` - Get server status

## Troubleshooting

### Server won't start
- Make sure port 8765 is not already in use
- Check if Python 3.8+ is installed: `python3 --version`

### Camera not working
- Grant camera permissions to Terminal/iTerm
- Check if another app is using the camera
- Try unplugging and replugging webcam

### Dependencies fail to install
- Make sure you have pip installed: `python3 -m pip --version`
- Try upgrading pip: `pip install --upgrade pip`
- On Mac, you may need: `brew install cmake` for opencv

### AI not detecting properly
- Ensure good lighting in your environment
- Position camera at eye level
- Sit 1-2 feet away from camera

## Development

The main tracking algorithm is in:
- `src/attention/main_server.py` - HTTP server (LATEST)
- `src/attention/advanced_attention_tracker.py` - Core tracking algorithm (LATEST)
- `src/attention/flexible_phone_detector.py` - Phone detection

## Notes
- The server must be running locally before starting a focus session
- It uses your webcam to track attention in real-time
- All processing is done locally - no data is sent to external servers
