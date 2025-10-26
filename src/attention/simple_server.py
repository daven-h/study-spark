#!/usr/bin/env python3
"""
Simple WebSocket server for testing attention tracking integration
"""

import asyncio
import websockets
import json
import time

async def handle_client(websocket, path):
    """Handle client connections and messages"""
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
                    
                    # Simulate attention data
                    for i in range(10):
                        await websocket.send(json.dumps({
                            'type': 'attention_data',
                            'data': {
                                'attention_score': 0.7 + (i * 0.02),
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
                        await asyncio.sleep(0.1)
                
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
    async with websockets.serve(handle_client, "localhost", 8765):
        print("WebSocket server running on ws://localhost:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())

