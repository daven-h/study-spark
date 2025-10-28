#!/usr/bin/env python3
"""
Production FastAPI server configuration for Study Spark AI Attention Tracking
"""

import uvicorn
from fastapi_server import app

if __name__ == "__main__":
    # Production configuration
    uvicorn.run(
        app,
        host="0.0.0.0",  # Listen on all interfaces for production
        port=8765,
        workers=1,  # Single worker for camera access
        log_level="info",
        access_log=True,
        reload=False,  # Disable reload in production
        loop="asyncio",
        http="httptools"  # Faster HTTP parsing
    )

