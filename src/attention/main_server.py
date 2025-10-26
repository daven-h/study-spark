#!/usr/bin/env python3
"""
Main HTTP Server for Study Spark AI Attention Tracking
Uses the updated AdvancedAttentionTracker class
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import cv2
import time
import threading
import json
import numpy as np

# Import the updated AdvancedAttentionTracker
from advanced_attention_tracker import AdvancedAttentionTracker

app = Flask(__name__)
CORS(app)  # Enable CORS for Next.js frontend

# Global state
tracking_active = False
tracker = None
tracker_thread = None
current_data = {
    'attention_score': 0.0,
    'eye_ar': 0.0,
    'mouth_ar': 0.0,
    'head_tilt': 0.0,
    'phone_detected': False,
    'fps': 0,
    'timestamp': time.time(),
    'focus_status': 'idle',
    'session_active': False
}

def run_tracking_loop():
    """Background thread for continuous tracking using AdvancedAttentionTracker"""
    global current_data, tracking_active, tracker

    print("🎥 Starting tracking loop...")

    while tracking_active and tracker:
        try:
            # Capture frame from camera
            ret, frame = tracker.cap.read()
            if not ret:
                print("❌ Failed to read frame from camera")
                time.sleep(0.1)
                continue

            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)

            # Process frame with AdvancedAttentionTracker
            metrics = tracker.process_frame(frame)

            # Convert to API format (ensure all values are JSON serializable)
            current_data.update({
                'attention_score': float(metrics.get('focus_score', 0.0)),
                'eye_ar': float(metrics.get('ear', 0.0)),
                'mouth_ar': float(metrics.get('mar', 0.0)),
                'head_tilt': float(metrics.get('head_tilt', 0.0)),
                'phone_detected': bool(metrics.get('phone_near_face', False)),
                'fps': int(metrics.get('fps', 0)),
                'timestamp': time.time(),
                'focus_status': 'focused' if metrics.get('focused', False) else 'distracted',
                'session_active': tracking_active,
                # Additional detailed metrics
                'face_visible': bool(metrics.get('face_visible', False)),
                'orientation_good': bool(metrics.get('orientation_good', True)),
                'eye_closed': bool(metrics.get('eye_closed', False)),
                'yawning': bool(metrics.get('yawning', False)),
                'hand_near_face': bool(metrics.get('hand_near_face', False)),
                'yaw': float(metrics.get('yaw', 0.0)),
                'pitch': float(metrics.get('pitch', 0.0)),
                'roll': float(metrics.get('roll', 0.0))
            })

        except Exception as e:
            print(f"❌ Error in tracking loop: {e}")
            import traceback
            traceback.print_exc()
            time.sleep(0.1)

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get server status"""
    return jsonify({
        'status': 'running',
        'tracking_active': tracking_active,
        'tracker_initialized': tracker is not None,
        'timestamp': time.time()
    })

@app.route('/api/start_tracking', methods=['POST'])
def start_tracking():
    """Start attention tracking"""
    global tracking_active, tracker, tracker_thread

    try:
        if tracking_active:
            return jsonify({
                'success': True,
                'message': 'Tracking already active',
                'timestamp': time.time()
            })

        # Initialize tracker if not already done
        if tracker is None:
            print("🚀 Initializing AdvancedAttentionTracker...")
            tracker = AdvancedAttentionTracker(camera_index=0, frame_width=640, frame_height=480)
            print("✅ Tracker initialized successfully")

        # Start tracking
        tracking_active = True

        # Start background thread
        if tracker_thread is None or not tracker_thread.is_alive():
            tracker_thread = threading.Thread(target=run_tracking_loop, daemon=True)
            tracker_thread.start()
            print("✅ Tracking thread started")

        return jsonify({
            'success': True,
            'message': 'Tracking started successfully',
            'timestamp': time.time()
        })

    except Exception as e:
        print(f"❌ Error starting tracking: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': time.time()
        }), 500

@app.route('/api/stop_tracking', methods=['POST'])
def stop_tracking():
    """Stop attention tracking"""
    global tracking_active, tracker

    try:
        tracking_active = False

        # Give thread time to stop
        time.sleep(0.2)

        # Release camera
        if tracker and hasattr(tracker, 'cap'):
            tracker.cap.release()
            print("📷 Camera released")

        return jsonify({
            'success': True,
            'message': 'Tracking stopped',
            'timestamp': time.time()
        })

    except Exception as e:
        print(f"❌ Error stopping tracking: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': time.time()
        }), 500

@app.route('/api/attention_data', methods=['GET'])
def get_attention_data():
    """Get current attention data"""
    return jsonify({
        'success': True,
        'data': current_data,
        'timestamp': time.time()
    })

@app.route('/api/ping', methods=['GET'])
def ping():
    """Ping endpoint to check if server is alive"""
    return jsonify({
        'success': True,
        'message': 'pong',
        'timestamp': time.time()
    })

if __name__ == '__main__':
    print("=" * 60)
    print("🧠 STUDY SPARK AI ATTENTION TRACKING SERVER")
    print("=" * 60)
    print("📡 Starting HTTP API server on http://localhost:8765")
    print("")
    print("📋 API Endpoints:")
    print("   GET  /api/ping              - Health check")
    print("   GET  /api/status            - Get server status")
    print("   POST /api/start_tracking    - Start camera and tracking")
    print("   POST /api/stop_tracking     - Stop tracking")
    print("   GET  /api/attention_data    - Get real-time metrics")
    print("")
    print("🎯 Features:")
    print("   • MediaPipe Face Mesh Detection")
    print("   • Eye Aspect Ratio (EAR) Analysis")
    print("   • Mouth Aspect Ratio (MAR) for Yawning")
    print("   • Head Pose Estimation (Yaw/Pitch/Roll)")
    print("   • Phone Detection Near Face")
    print("   • Hand Tracking Near Face")
    print("   • Posture Analysis")
    print("")
    print("⚠️  Make sure to grant camera permissions when prompted")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 60)

    try:
        app.run(host='localhost', port=8765, debug=False, threaded=True)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down server...")
        tracking_active = False
        if tracker and hasattr(tracker, 'cap'):
            tracker.cap.release()
        print("✅ Server stopped cleanly")
