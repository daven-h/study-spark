#!/usr/bin/env python3
"""
Simple test using basic socket connection
"""

import socket
import time

def test_connection():
    """Test basic socket connection to WebSocket server"""
    try:
        # Create socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 8765))
        print("✅ Socket connection successful!")
        
        # Send WebSocket handshake
        handshake = (
            "GET / HTTP/1.1\r\n"
            "Host: localhost:8765\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            "Sec-WebSocket-Key: x3JJHMbDL1EzLkh9GBhXDw==\r\n"
            "Sec-WebSocket-Version: 13\r\n"
            "\r\n"
        )
        
        sock.send(handshake.encode())
        response = sock.recv(1024).decode()
        print(f"📨 Handshake response: {response[:100]}...")
        
        if "101 Switching Protocols" in response:
            print("✅ WebSocket handshake successful!")
        else:
            print("❌ WebSocket handshake failed")
        
        sock.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()

