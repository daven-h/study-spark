# Study Spark AI Attention Tracking - FastAPI Server

This is the FastAPI version of the Study Spark AI Attention Tracking server, providing better performance, automatic API documentation, and easier deployment compared to Flask.

## Features

- **FastAPI Framework**: High-performance async web framework
- **Automatic API Documentation**: Swagger UI and ReDoc available
- **Type Safety**: Pydantic models for request/response validation
- **Better Error Handling**: Structured error responses
- **Production Ready**: Optimized for deployment

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start Development Server
```bash
python start_server.py
```
Or directly:
```bash
python fastapi_server.py
```

### 3. Access the API
- **API Base URL**: http://localhost:8765
- **Swagger UI**: http://localhost:8765/docs
- **ReDoc**: http://localhost:8765/redoc

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/ping` | Health check |
| GET | `/api/status` | Server status |
| POST | `/api/start_tracking` | Start attention tracking |
| POST | `/api/stop_tracking` | Stop attention tracking |
| GET | `/api/attention_data` | Get real-time attention data |

## Production Deployment

### Using the Production Server
```bash
python production_server.py
```

### Using Docker (Optional)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8765

CMD ["python", "production_server.py"]
```

### Using Gunicorn with Uvicorn Workers
```bash
pip install gunicorn
gunicorn fastapi_server:app -w 1 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8765
```

## Environment Variables

- `HOST`: Server host (default: localhost)
- `PORT`: Server port (default: 8765)
- `WORKERS`: Number of workers (default: 1)
- `LOG_LEVEL`: Logging level (default: info)

## API Response Examples

### Start Tracking Response
```json
{
  "success": true,
  "message": "YOUR ADVANCED MediaPipe-based algorithm started",
  "timestamp": 1703123456.789,
  "algorithm_features": [
    "MediaPipe Face Mesh (478 landmarks)",
    "MediaPipe Hands Detection",
    "MediaPipe Pose Detection",
    "Advanced Eye Aspect Ratio (EAR)",
    "Mouth Aspect Ratio (MAR) for Yawning",
    "Head Pose Estimation (Yaw/Pitch/Roll)",
    "Flexible Phone Detection",
    "Hand Near Face Detection",
    "Posture Analysis",
    "Enhanced Focus Scoring"
  ],
  "camera_params": {
    "width": 640,
    "height": 480,
    "fps": 30
  }
}
```

### Attention Data Response
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
    "timestamp": 1703123456.789,
    "focus_status": "focused",
    "session_active": true,
    "camera_active": true,
    "face_visible": true,
    "orientation_good": true,
    "yaw": 2.1,
    "pitch": -1.5,
    "roll": 0.8,
    "eye_closed": false,
    "yawning": false,
    "hand_near_face": false,
    "phone_confidence": 0.0,
    "posture_stable": true,
    "status_messages": {}
  },
  "timestamp": 1703123456.789
}
```

## Troubleshooting

### Camera Access Issues
- Ensure camera is not being used by another application
- Check camera permissions on your system
- Try different camera indices (0, 1, 2, etc.)

### Performance Issues
- Use production server configuration for better performance
- Monitor CPU usage during tracking
- Adjust frame rate in the algorithm if needed

### Deployment Issues
- Ensure all dependencies are installed
- Check firewall settings for port 8765
- Use environment variables for configuration

## Migration from Flask

The FastAPI version maintains the same API endpoints and response format as the Flask version, making migration seamless. The main differences are:

1. **Better Performance**: FastAPI is significantly faster
2. **Automatic Documentation**: Built-in Swagger UI and ReDoc
3. **Type Safety**: Pydantic models for validation
4. **Async Support**: Better handling of concurrent requests
5. **Production Ready**: Better deployment options

## Support

For issues or questions, please check the API documentation at `/docs` endpoint or refer to the FastAPI documentation.

