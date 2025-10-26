#!/usr/bin/env python3
"""
WebSocket server for real-time focus data streaming.
Allows Next.js frontend to receive live attention tracking data.
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

from tracker import FocusTracker
from focus_logic import FocusEvaluator
from visualizer import FocusVisualizer

class FocusDataServer:
    """
    WebSocket server that streams real-time focus data to connected clients.
    """
    
    def __init__(self, host: str = "localhost", port: int = 8765, 
                 camera_index: int = 0):
        """
        Initialize the focus data server.
        
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
        
        # Focus tracking components
        self.tracker = FocusTracker()
        self.evaluator = FocusEvaluator()
        self.visualizer = FocusVisualizer()
        
        # Video capture
        self.cap = None
        self.frame_width = 640
        self.frame_height = 480
        
        # Data streaming
        self.latest_focus_data = {}
        self.streaming = False
        self.stream_thread = None
        
        # FPS tracking
        self.fps_counter = FPSCounter()
    
    async def register_client(self, websocket: websockets.WebSocketServerProtocol, path: str):
        """
        Register a new client connection.
        
        Args:
            websocket: WebSocket connection
            path: Connection path
        """
        self.clients.add(websocket)
        print(f"Client connected: {websocket.remote_address}")
        
        # Send initial data
        if self.latest_focus_data:
            await websocket.send(json.dumps(self.latest_focus_data))
        
        try:
            # Keep connection alive and handle client messages
            async for message in websocket:
                await self.handle_client_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.remove(websocket)
            print(f"Client disconnected: {websocket.remote_address}")
    
    async def handle_client_message(self, websocket: websockets.WebSocketServerProtocol, message: str):
        """
        Handle incoming client messages.
        
        Args:
            websocket: WebSocket connection
            message: Client message
        """
        try:
            data = json.loads(message)
            message_type = data.get("type", "unknown")
            
            if message_type == "ping":
                # Respond to ping with pong
                await websocket.send(json.dumps({"type": "pong", "timestamp": time.time()}))
            
            elif message_type == "get_status":
                # Send current status
                status = {
                    "type": "status",
                    "streaming": self.streaming,
                    "clients_connected": len(self.clients),
                    "camera_active": self.cap is not None and self.cap.isOpened(),
                    "timestamp": time.time()
                }
                await websocket.send(json.dumps(status))
            
            elif message_type == "start_stream":
                # Start focus tracking stream
                if not self.streaming:
                    await self.start_streaming()
                    await websocket.send(json.dumps({"type": "stream_started"}))
            
            elif message_type == "stop_stream":
                # Stop focus tracking stream
                if self.streaming:
                    await self.stop_streaming()
                    await websocket.send(json.dumps({"type": "stream_stopped"}))
            
            elif message_type == "get_latest":
                # Send latest focus data
                if self.latest_focus_data:
                    await websocket.send(json.dumps(self.latest_focus_data))
        
        except json.JSONDecodeError:
            await websocket.send(json.dumps({"type": "error", "message": "Invalid JSON"}))
        except Exception as e:
            await websocket.send(json.dumps({"type": "error", "message": str(e)}))
    
    async def start_streaming(self):
        """Start the focus tracking stream."""
        if self.streaming:
            return
        
        # Initialize camera
        if not await self.initialize_camera():
            raise Exception("Failed to initialize camera")
        
        self.streaming = True
        self.stream_thread = threading.Thread(target=self._stream_loop, daemon=True)
        self.stream_thread.start()
        
        print("Focus tracking stream started")
    
    async def stop_streaming(self):
        """Stop the focus tracking stream."""
        self.streaming = False
        
        if self.cap:
            self.cap.release()
            self.cap = None
        
        print("Focus tracking stream stopped")
    
    async def initialize_camera(self) -> bool:
        """
        Initialize camera capture.
        
        Returns:
            True if camera initialized successfully
        """
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            if not self.cap.isOpened():
                print(f"Error: Could not open camera {self.camera_index}")
                return False
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            # Get actual frame dimensions
            self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            print(f"Camera initialized: {self.frame_width}x{self.frame_height}")
            return True
            
        except Exception as e:
            print(f"Error initializing camera: {e}")
            return False
    
    def _stream_loop(self):
        """Main streaming loop (runs in separate thread)."""
        while self.streaming and self.cap and self.cap.isOpened():
            try:
                # Capture frame
                ret, frame = self.cap.read()
                if not ret:
                    print("Error: Could not read frame from camera")
                    break
                
                # Process frame
                results = self.tracker.process_frame(frame)
                focus_metrics = self.evaluator.evaluate_focus(
                    results["face"], results["hands"], results["pose"],
                    self.frame_width, self.frame_height
                )
                
                # Add FPS and timestamp
                fps = self.fps_counter.get_fps()
                focus_metrics["fps"] = fps
                focus_metrics["timestamp"] = datetime.utcnow().isoformat() + "Z"
                
                # Store latest data
                self.latest_focus_data = focus_metrics
                
                # Broadcast to all connected clients
                if self.clients:
                    asyncio.run_coroutine_threadsafe(
                        self._broadcast_to_clients(focus_metrics), 
                        asyncio.get_event_loop()
                    )
                
                # Control frame rate
                time.sleep(1.0 / 30.0)  # Target 30 FPS
            
            except Exception as e:
                print(f"Error in stream loop: {e}")
                break
        
        self.streaming = False
    
    async def _broadcast_to_clients(self, data: Dict[str, Any]):
        """Broadcast data to all connected clients."""
        if not self.clients:
            return
        
        message = json.dumps(data)
        disconnected_clients = set()
        
        for client in self.clients:
            try:
                await client.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected_clients.add(client)
            except Exception as e:
                print(f"Error sending to client {client.remote_address}: {e}")
                disconnected_clients.add(client)
        
        # Remove disconnected clients
        self.clients -= disconnected_clients
    
    async def start_server(self):
        """Start the WebSocket server."""
        print(f"Starting WebSocket server on {self.host}:{self.port}")
        
        async with websockets.serve(
            self.register_client, 
            self.host, 
            self.port,
            ping_interval=20,
            ping_timeout=10
        ):
            print(f"WebSocket server running on ws://{self.host}:{self.port}")
            print("Clients can connect to receive real-time focus data")
            print("Press Ctrl+C to stop the server")
            
            try:
                await asyncio.Future()  # Run forever
            except KeyboardInterrupt:
                print("\nShutting down server...")
                await self.stop_streaming()
    
    def cleanup(self):
        """Clean up resources."""
        self.streaming = False
        
        if self.cap:
            self.cap.release()
        
        if self.tracker:
            self.tracker.release()

class FPSCounter:
    """Simple FPS counter for performance monitoring."""
    
    def __init__(self, window_size: int = 30):
        self.window_size = window_size
        self.frame_times = []
        self.last_time = time.time()
    
    def get_fps(self) -> float:
        """Get current FPS."""
        current_time = time.time()
        frame_time = current_time - self.last_time
        self.last_time = current_time
        
        self.frame_times.append(frame_time)
        if len(self.frame_times) > self.window_size:
            self.frame_times.pop(0)
        
        if self.frame_times:
            avg_frame_time = sum(self.frame_times) / len(self.frame_times)
            return 1.0 / avg_frame_time if avg_frame_time > 0 else 0.0
        
        return 0.0

def main():
    """Main entry point for the WebSocket server."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Focus Data WebSocket Server")
    parser.add_argument("--host", default="localhost", help="Server host (default: localhost)")
    parser.add_argument("--port", type=int, default=8765, help="Server port (default: 8765)")
    parser.add_argument("--camera", type=int, default=0, help="Camera index (default: 0)")
    
    args = parser.parse_args()
    
    # Create and start server
    server = FocusDataServer(args.host, args.port, args.camera)
    
    try:
        asyncio.run(server.start_server())
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    finally:
        server.cleanup()

if __name__ == "__main__":
    main()
