"""
FastAPI application startup script
"""
import uvicorn

if __name__ == "__main__":
    print("🚀 Starting Rail DB FastAPI Server...")
    print("📊 Student Grades API")
    print("🌐 Available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("📖 ReDoc Documentation: http://localhost:8000/redoc")
    print("\n" + "=" * 50)
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )