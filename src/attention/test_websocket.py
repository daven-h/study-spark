#!/usr/bin/env python3
"""
Simple test script to verify WebSocket server functionality
"""

import asyncio
import websockets
import json
import time

async def test_websocket():
    """Test WebSocket connection and basic functionality"""
    try:
        print("🔌 Connecting to WebSocket server...")
        async with websockets.connect("ws://localhost:8765") as websocket:
            print("✅ Connected successfully!")
            
            # Test ping
            print("📡 Sending ping...")
            await websocket.send(json.dumps({"command": "ping"}))
            response = await websocket.recv()
            print(f"📨 Received: {response}")
            
            # Test start tracking
            print("🎯 Starting attention tracking...")
            await websocket.send(json.dumps({"command": "start_tracking"}))
            response = await websocket.recv()
            print(f"📨 Received: {response}")
            
            # Listen for attention data
            print("👀 Listening for attention data (5 seconds)...")
            start_time = time.time()
            while time.time() - start_time < 5:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    data = json.loads(response)
                    if data.get('type') == 'attention_data':
                        attention_score = data['data'].get('attention_score', 0)
                        focus_status = data['data'].get('focus_status', 'unknown')
                        fps = data['data'].get('fps', 0)
                        print(f"📊 Attention: {attention_score:.2f}, Status: {focus_status}, FPS: {fps:.1f}")
                except asyncio.TimeoutError:
                    print("⏰ No data received in 1 second")
                    break
            
            # Test stop tracking
            print("🛑 Stopping attention tracking...")
            await websocket.send(json.dumps({"command": "stop_tracking"}))
            response = await websocket.recv()
            print(f"📨 Received: {response}")
            
            print("✅ Test completed successfully!")
            
    except ConnectionRefusedError:
        print("❌ Connection refused. Is the WebSocket server running?")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket())

