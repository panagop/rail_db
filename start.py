#!/usr/bin/env python3
"""
Railway startup script for FastAPI
"""
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Starting Rail DB FastAPI on Railway - Port {port}")
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )