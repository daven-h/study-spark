#!/usr/bin/env python3
"""
HTTP server using YOUR ADVANCED ATTENTION TRACKER (MediaPipe-based)
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import cv2
import time
import threading
import json
import numpy as np

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

app = Flask(__name__)
CORS(app)

# Global state
tracking_active = False
tracker = None
tracker_thread = None
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

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get server status"""
    return jsonify({
        'status': 'running',
        'tracking_active': tracking_active,
        'camera_active': tracker is not None and tracker.cap is not None and tracker.cap.isOpened(),
        'timestamp': time.time()
    })

@app.route('/api/start_tracking', methods=['POST'])
def start_tracking():
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

            return jsonify({
                'success': True,
                'message': 'YOUR ADVANCED MediaPipe-based algorithm started',
                'algorithm_features': [
                    'MediaPipe Face Mesh (478 landmarks)',
                    'MediaPipe Hands Detection',
                    'MediaPipe Pose Detection',
                    'Advanced Eye Aspect Ratio (EAR)',
                    'Mouth Aspect Ratio (MAR) for Yawning',
                    'Head Pose Estimation (Yaw/Pitch/Roll)',
                    'Flexible Phone Detection',
                    'Hand Near Face Detection',
                    'Posture Analysis',
                    'Enhanced Focus Scoring'
                ],
                'camera_params': {
                    'width': tracker.frame_width,
                    'height': tracker.frame_height,
                    'fps': 30
                },
                'timestamp': time.time()
            })

        except Exception as e:
            print(f"❌ Failed to initialize YOUR ADVANCED algorithm: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'success': False,
                'message': f'Failed to initialize algorithm: {str(e)}',
                'timestamp': time.time()
            }), 500
    else:
        return jsonify({
            'success': True,
            'message': 'Tracking already active',
            'timestamp': time.time()
        })

@app.route('/api/stop_tracking', methods=['POST'])
def stop_tracking():
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

    return jsonify({
        'success': True,
        'message': 'YOUR ADVANCED Attention Tracker stopped',
        'timestamp': time.time()
    })

@app.route('/api/attention_data', methods=['GET'])
def get_attention_data():
    """Get data from YOUR ADVANCED algorithm"""
    return jsonify({
        'success': True,
        'data': convert_numpy_types(current_data),
        'timestamp': time.time()
    })

@app.route('/api/ping', methods=['GET'])
def ping():
    """Ping endpoint"""
    return jsonify({
        'success': True,
        'message': 'pong',
        'camera_active': tracker is not None and tracker.cap is not None and tracker.cap.isOpened(),
        'timestamp': time.time()
    })

if __name__ == '__main__':
    print("=" * 70)
    print("🧠 STUDY SPARK AI ATTENTION TRACKING SERVER")
    print("=" * 70)
    print("Starting HTTP API server using YOUR ADVANCED MediaPipe-based Tracker")
    print("")
    print("🎯 YOUR ADVANCED Algorithm Features:")
    print("  ✅ MediaPipe Face Mesh (478 landmarks)")
    print("  ✅ MediaPipe Hands Detection")
    print("  ✅ MediaPipe Pose Detection")
    print("  ✅ Advanced Eye Aspect Ratio (EAR)")
    print("  ✅ Mouth Aspect Ratio (MAR) for Yawning")
    print("  ✅ Head Pose Estimation (Yaw/Pitch/Roll)")
    print("  ✅ Flexible Phone Detection")
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
    print("")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 70)

    app.run(host='localhost', port=8765, debug=False)
