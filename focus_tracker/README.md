# Python Attention Tracking Engine

A real-time attention tracking system using MediaPipe and OpenCV that detects face, hands, and torso to compute focus scores and distraction detection.

## Features

- **Real-time Face Detection**: Uses MediaPipe FaceMesh for precise face landmark detection
- **Hand Tracking**: Detects hands and identifies when they're near the face (phone usage)
- **Posture Analysis**: Monitors torso position to detect slouching
- **Focus Scoring**: Computes real-time focus scores based on multiple factors
- **Attention Ring**: Visual overlay showing focus state with color-coded ring
- **WebSocket Server**: Optional real-time data streaming to web frontend
- **Privacy-Safe**: All processing happens on-device, no cloud dependencies

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure you have a working webcam connected to your system.

## Usage

### Basic Attention Tracking

Run the main attention tracker with webcam feed:

```bash
python main.py
```

**Controls:**
- `q` - Quit
- `r` - Reset focus history
- `s` - Save screenshot
- `l` - Toggle landmark display
- `g` - Toggle focus grid

### WebSocket Server

Start the WebSocket server for frontend integration:

```bash
python server.py
```

The server will run on `ws://localhost:8765` and stream real-time focus data.

### Command Line Options

**Main Script:**
```bash
python main.py --camera 0 --width 640 --height 480 --no-landmarks --no-grid --no-json
```

**Server Script:**
```bash
python server.py --host localhost --port 8765 --camera 0
```

## Output Format

The system outputs JSON data with the following structure:

```json
{
  "timestamp": "2025-10-24T19:10:22Z",
  "focused": true,
  "focus_score": 0.93,
  "yaw": 0.03,
  "pitch": 0.05,
  "hand_near_face": false,
  "posture_stable": true,
  "fps": 28.7
}
```

## Focus Evaluation

The system evaluates focus based on:

1. **Face Visibility**: Is the face detected and visible?
2. **Face Orientation**: Is the person looking straight ahead?
3. **Hand Position**: Are hands away from the face?
4. **Posture**: Is the person sitting upright?
5. **Face Centering**: Is the face centered in the frame?

## WebSocket Integration

Connect from your Next.js frontend:

```javascript
const ws = new WebSocket('ws://localhost:8765');

ws.onmessage = (event) => {
  const focusData = JSON.parse(event.data);
  updateAttentionRing(focusData);
};

// Send commands
ws.send(JSON.stringify({ type: 'start_stream' }));
ws.send(JSON.stringify({ type: 'get_latest' }));
```

## Architecture

```
focus_tracker/
├── main.py              # Main application with webcam loop
├── tracker.py           # MediaPipe detection (face, hands, pose)
├── focus_logic.py       # Focus evaluation and scoring
├── visualizer.py        # Attention ring and overlay rendering
├── server.py            # WebSocket server for real-time streaming
├── utils.py             # Geometry and analysis utilities
└── requirements.txt     # Python dependencies
```

## Performance

- **Target FPS**: 20-30 FPS
- **Latency**: <50ms processing time
- **CPU Usage**: Moderate (MediaPipe optimized)
- **Memory**: Low footprint

## Troubleshooting

**Camera Issues:**
- Ensure camera is not being used by other applications
- Try different camera indices: `--camera 1`, `--camera 2`
- Check camera permissions

**Performance Issues:**
- Reduce frame resolution: `--width 320 --height 240`
- Disable landmarks: `--no-landmarks`
- Close other applications using the camera

**WebSocket Connection Issues:**
- Check firewall settings
- Ensure port 8765 is available
- Verify WebSocket client implementation

## Privacy & Security

- All processing happens locally on your device
- No data is sent to external servers
- Camera feed is processed in real-time and not stored
- WebSocket server only runs locally by default
