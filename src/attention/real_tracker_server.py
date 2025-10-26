#!/usr/bin/env python3
"""
HTTP-based attention tracking API with REAL PreciseAttentionTracker integration
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import threading
import json

# Import the real attention tracker
from precise_attention_tracker import PreciseAttentionTracker

app = Flask(__name__)
CORS(app)  # Enable CORS for Next.js frontend

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

def run_attention_tracking():
    """Background thread to run real attention tracking"""
    global current_data, tracking_active, tracker
    
    try:
        # Initialize the real attention tracker
        tracker = PreciseAttentionTracker(camera_index=0)
        print("✅ Real PreciseAttentionTracker initialized")
        
        while tracking_active:
            try:
                # Get real attention data from the tracker
                ret, frame = tracker.cap.read()
                if ret:
                    # Process frame for real attention metrics
                    results = tracker.process_frame(frame)
                    
                    # Update current data with real results
                    current_data.update({
                        'attention_score': results.get('attention_score', 0.85),
                        'eye_ar': results.get('eye_ar', 0.25),
                        'mouth_ar': results.get('mouth_ar', 0.12),
                        'head_tilt': results.get('head_tilt', 5.2),
                        'phone_detected': results.get('phone_detected', False),
                        'fps': results.get('fps', 30),
                        'timestamp': time.time(),
                        'focus_status': results.get('focus_status', 'focused'),
                        'session_active': tracking_active
                    })
                
                time.sleep(0.033)  # ~30 FPS
                
            except Exception as e:
                print(f"Error in attention tracking: {e}")
                time.sleep(0.1)
                
    except Exception as e:
        print(f"Failed to initialize PreciseAttentionTracker: {e}")
        print("Falling back to simulated data...")
        
        # Fallback to simulated data
        counter = 0
        while tracking_active:
            current_data.update({
                'attention_score': 0.7 + (counter * 0.01) % 0.3,
                'eye_ar': 0.2 + (counter * 0.001) % 0.1,
                'mouth_ar': 0.1 + (counter * 0.002) % 0.05,
                'head_tilt': 5 + (counter * 0.1) % 10,
                'phone_detected': counter % 50 == 0,
                'fps': 25 + (counter % 10),
                'timestamp': time.time(),
                'focus_status': 'focused' if counter % 20 < 15 else 'distracted',
                'session_active': tracking_active
            })
            counter += 1
            time.sleep(0.1)

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get server status"""
    return jsonify({
        'status': 'running',
        'tracking_active': tracking_active,
        'real_tracker': tracker is not None,
        'timestamp': time.time()
    })

@app.route('/api/start_tracking', methods=['POST'])
def start_tracking():
    """Start real attention tracking"""
    global tracking_active, tracker_thread
    
    if not tracking_active:
        tracking_active = True
        tracker_thread = threading.Thread(target=run_attention_tracking)
        tracker_thread.daemon = True
        tracker_thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Real attention tracking started',
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
    """Stop attention tracking"""
    global tracking_active, tracker
    
    tracking_active = False
    
    # Clean up tracker
    if tracker:
        try:
            tracker.release()
            tracker = None
            print("✅ PreciseAttentionTracker released")
        except Exception as e:
            print(f"Error releasing tracker: {e}")
    
    return jsonify({
        'success': True,
        'message': 'Attention tracking stopped',
        'timestamp': time.time()
    })

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
    """Ping endpoint"""
    return jsonify({
        'success': True,
        'message': 'pong',
        'real_tracker': tracker is not None,
        'timestamp': time.time()
    })

if __name__ == '__main__':
    print("Starting REAL Attention Tracking HTTP API server on localhost:8765")
    print("API endpoints:")
    print("  GET  /api/status - Server status")
    print("  POST /api/start_tracking - Start REAL tracking")
    print("  POST /api/stop_tracking - Stop tracking")
    print("  GET  /api/attention_data - Get attention data")
    print("  GET  /api/ping - Ping endpoint")
    print("\nPress Ctrl+C to stop")
    
    app.run(host='localhost', port=8765, debug=False)

