#!/usr/bin/env python3
"""
WebSocket server for real-time attention tracking data.
Integrates with Next.js frontend to provide live focus metrics.
"""

import asyncio
import websockets
import json
import time
import threading
import cv2
import numpy as np
from typing import Dict, Any, Set, Optional
from datetime import datetime
import base64

from precise_attention_tracker import PreciseAttentionTracker

class AttentionWebSocketServer:
    """
    WebSocket server that streams real-time attention data to connected clients.
    """
    
    def __init__(self, host: str = "localhost", port: int = 8765, 
                 camera_index: int = 0):
        """
        Initialize the attention tracking WebSocket server.
        
        Args:
            host: Server host address
            port: Server port
            camera_index: Camera device index
        """
        self.host = host
        self.port = port
        self.camera_index = camera_index
        
        # Connected clients
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        
        # Attention tracking
        self.tracker = None
        self.tracking_active = False
        self.tracking_thread = None
        
        # Data storage
        self.current_data = {
            'attention_score': 0,
            'eye_ar': 0,
            'mouth_ar': 0,
            'head_tilt': 0,
            'phone_detected': False,
            'fps': 0,
            'timestamp': 0,
            'focus_status': 'unknown',
            'session_active': False
        }
        
        # Performance tracking
        self.frame_count = 0
        self.start_time = time.time()
        
    async def register_client(self, websocket, path):
        """Register a new client connection."""
        self.clients.add(websocket)
        print(f"Client connected. Total clients: {len(self.clients)}")
        
        try:
            # Handle incoming messages
            async for message in websocket:
                await self.handle_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.remove(websocket)
            print(f"Client disconnected. Total clients: {len(self.clients)}")
    
    async def broadcast_data(self, data: Dict[str, Any]):
        """Broadcast data to all connected clients."""
        if self.clients:
            message = json.dumps(data)
            disconnected = set()
            
            for client in self.clients:
                try:
                    await client.send(message)
                except websockets.exceptions.ConnectionClosed:
                    disconnected.add(client)
            
            # Remove disconnected clients
            self.clients -= disconnected
    
    def start_tracking(self):
        """Start the attention tracking in a separate thread."""
        if self.tracking_active:
            return
        
        try:
            self.tracking_active = True
            self.tracker = PreciseAttentionTracker(camera_index=self.camera_index)
            self.tracking_thread = threading.Thread(target=self._tracking_loop)
            self.tracking_thread.daemon = True
            self.tracking_thread.start()
            print("Attention tracking started")
        except Exception as e:
            print(f"Failed to start tracking: {e}")
            self.tracking_active = False
            self.tracker = None
    
    def stop_tracking(self):
        """Stop the attention tracking."""
        self.tracking_active = False
        if self.tracker:
            self.tracker.release()
            self.tracker = None
        print("Attention tracking stopped")
    
    def _tracking_loop(self):
        """Main tracking loop running in separate thread."""
        while self.tracking_active and self.tracker:
            try:
                # Get frame and process
                ret, frame = self.tracker.cap.read()
                if not ret:
                    continue
                
                # Process frame for attention metrics
                results = self.tracker.process_frame(frame)
                
                # Update current data
                self.current_data.update({
                    'attention_score': results.get('attention_score', 0),
                    'eye_ar': results.get('eye_ar', 0),
                    'mouth_ar': results.get('mouth_ar', 0),
                    'head_tilt': results.get('head_tilt', 0),
                    'phone_detected': results.get('phone_detected', False),
                    'fps': results.get('fps', 0),
                    'timestamp': time.time(),
                    'focus_status': results.get('focus_status', 'unknown'),
                    'session_active': self.tracking_active
                })
                
                # Calculate FPS
                self.frame_count += 1
                elapsed = time.time() - self.start_time
                if elapsed > 0:
                    self.current_data['fps'] = self.frame_count / elapsed
                
                # Small delay to prevent overwhelming the system
                time.sleep(0.033)  # ~30 FPS
                
            except Exception as e:
                print(f"Error in tracking loop: {e}")
                time.sleep(0.1)
    
    async def handle_message(self, websocket, message):
        """Handle incoming messages from clients."""
        try:
            data = json.loads(message)
            command = data.get('command')
            
            if command == 'start_tracking':
                self.start_tracking()
                await websocket.send(json.dumps({
                    'type': 'status',
                    'message': 'Tracking started',
                    'success': True
                }))
            
            elif command == 'stop_tracking':
                self.stop_tracking()
                await websocket.send(json.dumps({
                    'type': 'status',
                    'message': 'Tracking stopped',
                    'success': True
                }))
            
            elif command == 'get_data':
                await websocket.send(json.dumps({
                    'type': 'data',
                    'data': self.current_data
                }))
            
            elif command == 'ping':
                await websocket.send(json.dumps({
                    'type': 'pong',
                    'timestamp': time.time()
                }))
                
        except json.JSONDecodeError:
            await websocket.send(json.dumps({
                'type': 'error',
                'message': 'Invalid JSON'
            }))
        except Exception as e:
            await websocket.send(json.dumps({
                'type': 'error',
                'message': str(e)
            }))
    
    async def periodic_broadcast(self):
        """Periodically broadcast current data to all clients."""
        while True:
            if self.clients and self.tracking_active:
                await self.broadcast_data({
                    'type': 'attention_data',
                    'data': self.current_data
                })
            
            await asyncio.sleep(0.1)  # 10 Hz update rate
    
    async def start_server(self):
        """Start the WebSocket server."""
        print(f"Starting WebSocket server on {self.host}:{self.port}")
        
        # Start periodic broadcast task
        broadcast_task = asyncio.create_task(self.periodic_broadcast())
        
        # Start WebSocket server
        async with websockets.serve(self.register_client, self.host, self.port):
            print(f"WebSocket server running on ws://{self.host}:{self.port}")
            await broadcast_task

def main():
    """Main function to run the server."""
    server = AttentionWebSocketServer()
    
    try:
        asyncio.run(server.start_server())
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.stop_tracking()
    except Exception as e:
        print(f"Server error: {e}")
        server.stop_tracking()

if __name__ == "__main__":
    main()
