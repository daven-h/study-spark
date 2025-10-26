#!/usr/bin/env python3
"""
Minimal working WebSocket server for attention tracking
"""

import asyncio
import websockets
import json
import time

async def echo_handler(websocket, path):
    """Simple echo handler that responds to messages"""
    print(f"Client connected from {websocket.remote_address}")
    
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
                    await websocket.send(json.dumps({
                        'type': 'status',
                        'message': 'Tracking started',
                        'success': True
                    }))
                    
                    # Send some simulated attention data
                    for i in range(5):
                        await websocket.send(json.dumps({
                            'type': 'attention_data',
                            'data': {
                                'attention_score': 0.7 + (i * 0.05),
                                'eye_ar': 0.25,
                                'mouth_ar': 0.12,
                                'head_tilt': 5.2,
                                'phone_detected': False,
                                'fps': 30,
                                'timestamp': time.time(),
                                'focus_status': 'focused',
                                'session_active': True
                            }
                        }))
                        await asyncio.sleep(0.2)
                
                elif command == 'stop_tracking':
                    await websocket.send(json.dumps({
                        'type': 'status',
                        'message': 'Tracking stopped',
                        'success': True
                    }))
                
                elif command == 'get_data':
                    await websocket.send(json.dumps({
                        'type': 'data',
                        'data': {
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
                    }))
                
                else:
                    await websocket.send(json.dumps({
                        'type': 'error',
                        'message': f'Unknown command: {command}'
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

async def main():
    """Start the WebSocket server"""
    print("Starting WebSocket server on localhost:8765")
    
    # Use the correct handler signature
    async with websockets.serve(echo_handler, "localhost", 8765):
        print("WebSocket server running on ws://localhost:8765")
        print("Press Ctrl+C to stop")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Server error: {e}")

