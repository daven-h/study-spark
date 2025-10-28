#!/usr/bin/env python3
"""
Startup script for Study Spark AI Attention Tracking FastAPI Server
"""

import subprocess
import sys
import os

def main():
    """Start the FastAPI server"""
    print("🚀 Starting Study Spark AI Attention Tracking Server...")
    
    # Change to the attention directory
    attention_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(attention_dir)
    
    # Check if requirements are installed
    try:
        import fastapi
        import uvicorn
        print("✅ FastAPI dependencies found")
    except ImportError:
        print("❌ FastAPI dependencies not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Start the server
    try:
        print("🎯 Starting FastAPI server on http://localhost:8765")
        print("📚 API Documentation available at http://localhost:8765/docs")
        print("🛑 Press Ctrl+C to stop")
        print("-" * 50)
        
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "fastapi_server:app", 
            "--host", "localhost", 
            "--port", "8765", 
            "--reload"
        ])
        
    except KeyboardInterrupt:
        print("\n✅ Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main()

