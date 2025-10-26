#!/usr/bin/env python3
"""
Working WebSocket server for attention tracking integration
"""

import asyncio
import websockets
import json
import time
import threading
from typing import Dict, Any, Set

class WorkingAttentionServer:
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.tracking_active = False
        
        # Simulated attention data
        self.current_data = {
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
    
    async def handle_client(self, websocket, path):
        """Handle client connections and messages"""
        self.clients.add(websocket)
        print(f"Client connected from {websocket.remote_address}. Total clients: {len(self.clients)}")
        
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    command = data.get('command')
                    
                    if command == 'ping':
                        await websocket.send(json.dumps({
                            'type': 'pong',
                            'timestamp': time.time()
                        }))
                    
                    elif command == 'start_tracking':
                        self.tracking_active = True
                        await websocket.send(json.dumps({
                            'type': 'status',
                            'message': 'Tracking started',
                            'success': True
                        }))
                        
                        # Start broadcasting attention data
                        asyncio.create_task(self.broadcast_attention_data())
                    
                    elif command == 'stop_tracking':
                        self.tracking_active = False
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
                    
        except websockets.exceptions.ConnectionClosed:
            print(f"Client disconnected")
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            self.clients.discard(websocket)
            print(f"Client removed. Total clients: {len(self.clients)}")
    
    async def broadcast_attention_data(self):
        """Broadcast attention data to all clients"""
        counter = 0
        while self.tracking_active and self.clients:
            # Update simulated data
            self.current_data.update({
                'attention_score': 0.7 + (counter * 0.01) % 0.3,
                'eye_ar': 0.2 + (counter * 0.001) % 0.1,
                'mouth_ar': 0.1 + (counter * 0.002) % 0.05,
                'head_tilt': 5 + (counter * 0.1) % 10,
                'phone_detected': counter % 50 == 0,  # Occasionally detect phone
                'fps': 25 + (counter % 10),
                'timestamp': time.time(),
                'focus_status': 'focused' if counter % 20 < 15 else 'distracted',
                'session_active': self.tracking_active
            })
            
            # Broadcast to all clients
            if self.clients:
                message = json.dumps({
                    'type': 'attention_data',
                    'data': self.current_data
                })
                
                disconnected = set()
                for client in self.clients:
                    try:
                        await client.send(message)
                    except websockets.exceptions.ConnectionClosed:
                        disconnected.add(client)
                
                # Remove disconnected clients
                self.clients -= disconnected
            
            counter += 1
            await asyncio.sleep(0.1)  # 10 Hz update rate
    
    async def start_server(self):
        """Start the WebSocket server"""
        print(f"Starting WebSocket server on {self.host}:{self.port}")
        
        async with websockets.serve(self.handle_client, self.host, self.port):
            print(f"WebSocket server running on ws://{self.host}:{self.port}")
            await asyncio.Future()  # Run forever

def main():
    """Main function to run the server"""
    server = WorkingAttentionServer()
    
    try:
        asyncio.run(server.start_server())
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Server error: {e}")

if __name__ == "__main__":
    main()

