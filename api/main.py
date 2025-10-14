"""
Main FastAPI application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routers.students import router as students_router
from .routers.analytics import router as analytics_router
from database import DatabaseManager

# Create FastAPI app
app = FastAPI(
    title="Rail DB Student Grades API",
    description="API for managing student grades data with PostgreSQL backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(students_router)
app.include_router(analytics_router)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Rail DB Student Grades API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "students": "/students",
            "analytics": "/analytics"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        with DatabaseManager() as db:
            # Simple database connectivity test
            result = db.execute_query("SELECT 1 as status;")
            if result:
                return {
                    "status": "healthy",
                    "database": "connected",
                    "timestamp": "2024-01-01T00:00:00Z"
                }
            else:
                raise HTTPException(status_code=503, detail="Database connection failed")
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")


@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    print("🚀 Rail DB API starting up...")
    
    # Test database connection
    try:
        with DatabaseManager() as db:
            result = db.execute_query("SELECT COUNT(*) as count FROM student_grades;")
            if result:
                count = result[0]["count"]
                print(f"✅ Database connected successfully! Found {count:,} student grade records.")
            else:
                print("⚠️ Database connected but no student_grades table found.")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("⚠️ API will start but database endpoints may not work.")
    
    print("🎉 Rail DB API is ready!")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    print("👋 Rail DB API shutting down...")


if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Starting FastAPI server on port {port}...")
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # Disable reload in production
        log_level="info"
    )