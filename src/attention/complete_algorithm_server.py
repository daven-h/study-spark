#!/usr/bin/env python3
"""
HTTP server using YOUR COMPLETE PreciseAttentionTracker algorithm
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import cv2
import time
import threading
import json
import numpy as np

# Import YOUR Precise Attention Tracker class
from precise_attention_tracker import PreciseAttentionTracker

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

def run_your_complete_algorithm():
    """Background thread using YOUR COMPLETE PreciseAttentionTracker algorithm"""
    global current_data, tracking_active, tracker
    
    while tracking_active and tracker:
        try:
            # Use YOUR COMPLETE algorithm - capture frame
            ret, frame = tracker.cap.read()
            if not ret:
                print("❌ Failed to read frame from camera")
                continue
            
            # Flip frame horizontally for mirror effect (YOUR EXACT CODE)
            frame = cv2.flip(frame, 1)
            
            # Use YOUR COMPLETE process_frame algorithm
            metrics = tracker.process_frame(frame)
            
            # Convert YOUR algorithm results to API format (ensure JSON serializable)
            current_data.update({
                'attention_score': float(metrics.get('focus_score', 0.0)),
                'eye_ar': float(metrics.get('ear', 0.0)),
                'mouth_ar': float(metrics.get('mar', 0.0)),
                'head_tilt': float(metrics.get('head_tilt', 0.0)),
                'phone_detected': bool(metrics.get('phone_near_face', False)),
                'fps': float(metrics.get('fps', 30)),
                'timestamp': time.time(),
                'focus_status': 'focused' if bool(metrics.get('focused', False)) else 'distracted',
                'session_active': bool(tracking_active),
                'camera_active': True,
                'frame_width': int(tracker.frame_width),
                'frame_height': int(tracker.frame_height),
                # YOUR COMPLETE algorithm data
                'face_visible': bool(metrics.get('face_visible', False)),
                'orientation_good': bool(metrics.get('orientation_good', False)),
                'yaw': float(metrics.get('yaw', 0.0)),
                'pitch': float(metrics.get('pitch', 0.0)),
                'roll': float(metrics.get('roll', 0.0)),
                'eye_closed': bool(metrics.get('eye_closed', False)),
                'yawning': bool(metrics.get('yawning', False)),
                'hand_near_face': bool(metrics.get('hand_near_face', False)),
                'phone_confidence': float(metrics.get('phone_confidence', 0.0)),
                'posture_stable': bool(metrics.get('posture_stable', False)),
                'status_messages': metrics.get('status_messages', {})
            })
            
            # Small delay to prevent overwhelming
            time.sleep(0.033)  # ~30 FPS
            
        except Exception as e:
            print(f"Error in YOUR complete algorithm: {e}")
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
    """Start tracking using YOUR COMPLETE PreciseAttentionTracker algorithm"""
    global tracking_active, tracker_thread, tracker
    
    if not tracking_active:
        try:
            # Use YOUR Precise Attention Tracker class
            tracker = PreciseAttentionTracker(camera_index=0, frame_width=640, frame_height=480)
            print("✅ YOUR Precise Attention Tracker initialized")
            
            tracking_active = True
            tracker_thread = threading.Thread(target=run_your_complete_algorithm)
            tracker_thread.daemon = True
            tracker_thread.start()
            
            return jsonify({
                'success': True,
                'message': 'YOUR ADVANCED Attention Tracker algorithm started',
                'algorithm_features': [
                    'dlib 68-point Facial Landmarks',
                    'Advanced Gaze Analysis', 
                    'Eye/Mouth Detection',
                    'Phone Detection',
                    'Head Pose Estimation',
                    'Hand Detection',
                    'Posture Analysis',
                    'Enhanced Focus Logic'
                ],
                'camera_params': {
                    'width': tracker.frame_width,
                    'height': tracker.frame_height,
                    'fps': 30
                },
                'timestamp': time.time()
            })
            
        except Exception as e:
            print(f"❌ Failed to initialize YOUR algorithm: {e}")
            return jsonify({
                'success': False,
                'message': f'Failed to initialize algorithm: {str(e)}',
                'timestamp': time.time()
            })
    else:
        return jsonify({
            'success': False,
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
            tracker.release()  # YOUR cleanup method
            tracker = None
            print("✅ YOUR PreciseAttentionTracker algorithm stopped")
        except Exception as e:
            print(f"Error stopping YOUR algorithm: {e}")
    
    return jsonify({
        'success': True,
        'message': 'YOUR PreciseAttentionTracker algorithm stopped',
        'timestamp': time.time()
    })

@app.route('/api/attention_data', methods=['GET'])
def get_attention_data():
    """Get data from YOUR COMPLETE algorithm"""
    return jsonify({
        'success': True,
        'data': current_data,
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
    print("Starting HTTP API server using YOUR COMPLETE PreciseAttentionTracker algorithm")
    print("Using YOUR MediaPipe + EAR/MAR + Phone Detection + Head Pose + Everything!")
    print("\nYOUR Algorithm Features:")
    print("  ✅ MediaPipe Face Mesh Processing")
    print("  ✅ Precise Eye Aspect Ratio (EAR) Calculations")
    print("  ✅ Precise Mouth Aspect Ratio (MAR) Calculations") 
    print("  ✅ Phone Detection with YOLO")
    print("  ✅ Head Pose Estimation")
    print("  ✅ Hand Detection")
    print("  ✅ Posture Analysis")
    print("  ✅ Focus Score Calculation")
    print("\nAPI endpoints:")
    print("  GET  /api/status - Server status")
    print("  POST /api/start_tracking - Start YOUR complete algorithm")
    print("  POST /api/stop_tracking - Stop YOUR algorithm")
    print("  GET  /api/attention_data - Get algorithm data")
    print("  GET  /api/ping - Ping endpoint")
    print("\nPress Ctrl+C to stop")
    
    app.run(host='localhost', port=8765, debug=False)
