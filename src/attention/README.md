# Study Spark - AI-Powered Focus Tracking

This project integrates computer vision-based attention tracking with a Next.js frontend to provide real-time focus monitoring during study sessions.

## Features

- **Real-time Attention Tracking**: Uses MediaPipe and OpenCV to track eye movement, head pose, and facial expressions
- **Phone Detection**: Detects when users are distracted by their phones
- **WebSocket Communication**: Real-time data streaming between Python backend and Next.js frontend
- **Session Analytics**: Stores attention scores and metrics for each study session
- **Visual Feedback**: Live indicators showing focus status, eye aspect ratio, and attention score

## Setup Instructions

### 1. Install Python Dependencies

```bash
cd src/attention
pip3 install -r requirements.txt
```

### 2. Start the AI Server

```bash
cd src/attention
./start_server.sh
```

Or manually:
```bash
cd src/attention
python3 http_server.py
```

The server will start on `http://localhost:8765`

### 3. Start the Next.js Frontend

```bash
# From project root
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 4. Using the Focus Session

1. Navigate to the Focus page (`/focus`)
2. Ensure the AI server is running (you'll see "🔗 AI Connected" status)
3. Allow camera permissions when prompted
4. Click "Start Session" to begin tracking
5. The AI will monitor your attention in real-time
6. Click "Stop Session" to end and save the session data

## Technical Details

### Attention Tracking Metrics

- **Eye Aspect Ratio (EAR)**: Measures eye openness to detect drowsiness
- **Mouth Aspect Ratio (MAR)**: Detects yawning or talking
- **Head Pose**: Tracks head orientation to detect distraction
- **Phone Detection**: Uses YOLO to detect phones in the camera view
- **Attention Score**: Combined metric (0-1) indicating overall focus level

### HTTP API Protocol

The server communicates with the frontend using HTTP REST API:

**API Endpoints:**
- `GET /api/ping` - Check server status
- `POST /api/start_tracking` - Start attention tracking
- `POST /api/stop_tracking` - Stop attention tracking
- `GET /api/attention_data` - Get current attention data
- `GET /api/status` - Get server status

**Response Format:**
```json
{
  "success": true,
  "data": {
    "attention_score": 0.85,
    "eye_ar": 0.25,
    "mouth_ar": 0.12,
    "head_tilt": 5.2,
    "phone_detected": false,
    "fps": 30,
    "timestamp": 1234567890,
    "focus_status": "focused",
    "session_active": true
  },
  "timestamp": 1234567890
}
```

### File Structure

```
src/attention/
├── precise_attention_tracker.py    # Main attention tracking logic
├── flexible_phone_detector.py      # Phone detection using YOLO
├── websocket_server.py            # WebSocket server for frontend communication
├── start_server.sh                # Convenient startup script
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Troubleshooting

### Camera Issues
- Ensure camera permissions are granted
- Check if another application is using the camera
- Try refreshing the page

### WebSocket Connection Issues
- Verify the Python server is running on port 8765
- Check browser console for connection errors
- Ensure no firewall is blocking the connection

### Performance Issues
- Close other applications using the camera
- Reduce video resolution in browser settings
- Check system resources (CPU/Memory usage)

## Development

### Adding New Metrics
1. Modify `precise_attention_tracker.py` to calculate new metrics
2. Update the `AttentionData` interface in `page.tsx`
3. Add UI elements to display the new metrics

### Customizing Detection Thresholds
Edit the thresholds in `precise_attention_tracker.py`:
```python
self.eye_ar_threshold = 0.20      # Eye aspect ratio threshold
self.mouth_ar_threshold = 0.88    # Mouth aspect ratio threshold
self.head_tilt_threshold = 180.0  # Head tilt threshold
```

## License

This project is part of Study Spark - an AI-powered study companion.