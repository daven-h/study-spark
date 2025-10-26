#!/usr/bin/env python3
"""
HTTP-based attention tracking API as alternative to WebSocket
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import threading
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for Next.js frontend

# Global state
tracking_active = False
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

def update_attention_data():
    """Background thread to update attention data"""
    global current_data, tracking_active
    counter = 0
    
    while True:
        if tracking_active:
            # Simulate changing attention data
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
        
        time.sleep(0.1)  # 10 Hz update rate

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get server status"""
    return jsonify({
        'status': 'running',
        'tracking_active': tracking_active,
        'timestamp': time.time()
    })

@app.route('/api/start_tracking', methods=['POST'])
def start_tracking():
    """Start attention tracking"""
    global tracking_active
    tracking_active = True
    return jsonify({
        'success': True,
        'message': 'Tracking started',
        'timestamp': time.time()
    })

@app.route('/api/stop_tracking', methods=['POST'])
def stop_tracking():
    """Stop attention tracking"""
    global tracking_active
    tracking_active = False
    return jsonify({
        'success': True,
        'message': 'Tracking stopped',
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
        'timestamp': time.time()
    })

if __name__ == '__main__':
    # Start background thread for data updates
    data_thread = threading.Thread(target=update_attention_data)
    data_thread.daemon = True
    data_thread.start()
    
    print("Starting HTTP API server on localhost:8765")
    print("API endpoints:")
    print("  GET  /api/status - Server status")
    print("  POST /api/start_tracking - Start tracking")
    print("  POST /api/stop_tracking - Stop tracking")
    print("  GET  /api/attention_data - Get attention data")
    print("  GET  /api/ping - Ping endpoint")
    print("\nPress Ctrl+C to stop")
    
    app.run(host='localhost', port=8765, debug=False)

