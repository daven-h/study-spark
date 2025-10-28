#!/usr/bin/env python3
"""
FastAPI HTTP server using YOUR ADVANCED ATTENTION TRACKER (MediaPipe-based)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import cv2
import time
import threading
import json
import numpy as np
import asyncio
from typing import Dict, Any, Optional
from pydantic import BaseModel

# Import YOUR ADVANCED Attention Tracker class
from advanced_attention_tracker import AdvancedAttentionTracker

def convert_numpy_types(obj):
    """Convert NumPy types to native Python types for JSON serialization"""
    if isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    else:
        return obj

# Pydantic models for request/response validation
class TrackingResponse(BaseModel):
    success: bool
    message: str
    timestamp: float
    algorithm_features: Optional[list] = None
    camera_params: Optional[dict] = None

class StatusResponse(BaseModel):
    status: str
    tracking_active: bool
    camera_active: bool
    timestamp: float

class AttentionDataResponse(BaseModel):
    success: bool
    data: Dict[str, Any]
    timestamp: float

# Initialize FastAPI app
app = FastAPI(
    title="Study Spark AI Attention Tracking API",
    description="Advanced MediaPipe-based attention tracking system",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
tracking_active = False
tracker: Optional[AdvancedAttentionTracker] = None
tracker_thread: Optional[threading.Thread] = None
current_data = {
    'attention_score': 0.85,
    'eye_ar': 0.25,
    'mouth_ar': 0.12,
    'head_tilt': 5.2,
    'phone_detected': False,
    'fps': 30,
    'timestamp': time.time(),
    'focus_status': 'focused',
    'session_active': False
}

def run_your_advanced_algorithm():
    """Background thread using YOUR ADVANCED MediaPipe-based algorithm"""
    global current_data, tracking_active, tracker

    while tracking_active and tracker:
        try:
            # Use YOUR ADVANCED algorithm - capture frame
            ret, frame = tracker.cap.read()
            if not ret:
                print("❌ Failed to read frame from camera")
                continue

            # Flip frame for mirror effect
            frame = cv2.flip(frame, 1)

            # Use YOUR COMPLETE process_frame algorithm
            metrics = tracker.process_frame(frame)

            # Convert NumPy types to native Python types
            metrics = convert_numpy_types(metrics)

            # Convert YOUR algorithm results to API format
            current_data.update({
                'attention_score': metrics.get('focus_score', 0.0),
                'eye_ar': metrics.get('ear', 0.0),
                'mouth_ar': metrics.get('mar', 0.0),
                'head_tilt': metrics.get('head_tilt', 0.0),
                'phone_detected': metrics.get('phone_near_face', False),
                'fps': metrics.get('fps', 30),
                'timestamp': time.time(),
                'focus_status': 'focused' if metrics.get('focused', False) else 'distracted',
                'session_active': tracking_active,
                'camera_active': True,
                'frame_width': tracker.frame_width,
                'frame_height': tracker.frame_height,
                # YOUR ADVANCED algorithm data
                'face_visible': metrics.get('face_visible', False),
                'orientation_good': metrics.get('orientation_good', False),
                'yaw': metrics.get('yaw', 0.0),
                'pitch': metrics.get('pitch', 0.0),
                'roll': metrics.get('roll', 0.0),
                'eye_closed': metrics.get('eye_closed', False),
                'yawning': metrics.get('yawning', False),
                'hand_near_face': metrics.get('hand_near_face', False),
                'phone_confidence': metrics.get('phone_confidence', 0.0),
                'posture_stable': metrics.get('posture_stable', False),
                'status_messages': metrics.get('status_messages', {})
            })

            # Small delay to prevent overwhelming
            time.sleep(0.033)  # ~30 FPS

        except Exception as e:
            print(f"Error in YOUR ADVANCED algorithm: {e}")
            import traceback
            traceback.print_exc()
            time.sleep(0.1)

@app.get("/api/status", response_model=StatusResponse)
async def get_status():
    """Get server status"""
    return StatusResponse(
        status='running',
        tracking_active=tracking_active,
        camera_active=tracker is not None and tracker.cap is not None and tracker.cap.isOpened(),
        timestamp=time.time()
    )

@app.post("/api/start_tracking", response_model=TrackingResponse)
async def start_tracking():
    """Start tracking using YOUR ADVANCED MediaPipe-based algorithm"""
    global tracking_active, tracker_thread, tracker

    if not tracking_active:
        try:
            # Use YOUR ADVANCED Attention Tracker class
            tracker = AdvancedAttentionTracker(camera_index=0, frame_width=640, frame_height=480)
            print("✅ YOUR ADVANCED Attention Tracker algorithm initialized")

            tracking_active = True
            tracker_thread = threading.Thread(target=run_your_advanced_algorithm)
            tracker_thread.daemon = True
            tracker_thread.start()

            return TrackingResponse(
                success=True,
                message='YOUR ADVANCED MediaPipe-based algorithm started',
                timestamp=time.time(),
                algorithm_features=[
                    'MediaPipe Face Mesh (478 landmarks)',
                    'MediaPipe Hands Detection',
                    'MediaPipe Pose Detection',
                    'Advanced Eye Aspect Ratio (EAR)',
                    'Mouth Aspect Ratio (MAR) for Yawning',
                    'Head Pose Estimation (Yaw/Pitch/Roll)',
                    'YOLOv11 Phone Detection',
                    'Hand Near Face Detection',
                    'Posture Analysis',
                    'Enhanced Focus Scoring'
                ],
                camera_params={
                    'width': tracker.frame_width,
                    'height': tracker.frame_height,
                    'fps': 30
                }
            )

        except Exception as e:
            print(f"❌ Failed to initialize YOUR ADVANCED algorithm: {e}")
            import traceback
            traceback.print_exc()
            raise HTTPException(
                status_code=500,
                detail=f'Failed to initialize algorithm: {str(e)}'
            )
    else:
        return TrackingResponse(
            success=True,
            message='Tracking already active',
            timestamp=time.time()
        )

@app.post("/api/stop_tracking", response_model=TrackingResponse)
async def stop_tracking():
    """Stop tracking using YOUR algorithm cleanup"""
    global tracking_active, tracker

    tracking_active = False

    # Use YOUR algorithm cleanup
    if tracker:
        try:
            tracker.cap.release()
            tracker = None
            print("✅ YOUR ADVANCED Attention Tracker stopped")
        except Exception as e:
            print(f"Error stopping YOUR algorithm: {e}")

    return TrackingResponse(
        success=True,
        message='YOUR ADVANCED Attention Tracker stopped',
        timestamp=time.time()
    )

@app.get("/api/attention_data", response_model=AttentionDataResponse)
async def get_attention_data():
    """Get data from YOUR ADVANCED algorithm"""
    return AttentionDataResponse(
        success=True,
        data=convert_numpy_types(current_data),
        timestamp=time.time()
    )

@app.get("/api/ping")
async def ping():
    """Ping endpoint"""
    return JSONResponse({
        'success': True,
        'message': 'pong',
        'camera_active': tracker is not None and tracker.cap is not None and tracker.cap.isOpened(),
        'timestamp': time.time()
    })

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Study Spark AI Attention Tracking API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "GET /api/ping": "Health check",
            "GET /api/status": "Server status",
            "POST /api/start_tracking": "Start advanced algorithm",
            "POST /api/stop_tracking": "Stop algorithm",
            "GET /api/attention_data": "Get algorithm data"
        }
    }

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    print("=" * 70)
    print("🧠 STUDY SPARK AI ATTENTION TRACKING SERVER (FastAPI)")
    print("=" * 70)
    print("Starting FastAPI HTTP API server using YOUR ADVANCED MediaPipe-based Tracker")
    print("")
    print("🎯 YOUR ADVANCED Algorithm Features:")
    print("  ✅ MediaPipe Face Mesh (478 landmarks)")
    print("  ✅ MediaPipe Hands Detection")
    print("  ✅ MediaPipe Pose Detection")
    print("  ✅ Advanced Eye Aspect Ratio (EAR)")
    print("  ✅ Mouth Aspect Ratio (MAR) for Yawning")
    print("  ✅ Head Pose Estimation (Yaw/Pitch/Roll)")
    print("  ✅ YOLOv11 Phone Detection")
    print("  ✅ Hand Near Face Detection")
    print("  ✅ Posture Analysis")
    print("  ✅ Enhanced Focus Scoring")
    print("")
    print("📡 API endpoints on http://localhost:8765:")
    print("  GET  /api/ping              - Health check")
    print("  GET  /api/status            - Server status")
    print("  POST /api/start_tracking    - Start YOUR ADVANCED algorithm")
    print("  POST /api/stop_tracking     - Stop YOUR algorithm")
    print("  GET  /api/attention_data    - Get algorithm data")
    print("  GET  /docs                  - Swagger UI documentation")
    print("  GET  /redoc                 - ReDoc documentation")
    print("")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 70)

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global tracking_active, tracker
    print("🛑 Shutting down Study Spark AI Attention Tracking Server...")
    
    tracking_active = False
    
    if tracker:
        try:
            tracker.cap.release()
            tracker = None
            print("✅ Camera resources released")
        except Exception as e:
            print(f"Error during cleanup: {e}")
    
    print("✅ Server shutdown complete")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        "fastapi_server:app",
        host="localhost",
        port=8765,
        reload=False,  # Set to True for development
        log_level="info"
    )

