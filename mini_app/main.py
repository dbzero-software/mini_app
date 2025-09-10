"""
Main FastAPI application for Mini App
Includes DBZero initialization, FastAPI setup, and example endpoints
"""

import os
from contextlib import asynccontextmanager
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from dbzero_ce import Connection

from mini_app.config import get_settings, get_dbzero_config
from mini_app.settings import InstanceType


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager
    Handles DBZero initialization and cleanup
    """
    # Startup
    print("🚀 Starting Mini App...")
    
    settings = get_settings()
    config = get_dbzero_config()
    
    try:
        # Initialize DBZero connection
        Connection.setup(
            read_write=(settings.instance_type == InstanceType.RW), 
            **config
        )
        Connection.assure_initialized()
        print("✅ DBZero connection initialized successfully!")
        print(f"📊 Instance type: {settings.instance_type.value}")
        print(f"💾 Database directory: {settings.db_dir}")
        
    except Exception as e:
        print(f"❌ Failed to initialize DBZero: {e}")
        raise
    
    yield
    
    # Shutdown
    print("🛑 Shutting down Mini App...")
    try:
        Connection.close()
        print("✅ DBZero connection closed successfully!")
    except Exception as e:
        print(f"⚠️  Error during shutdown: {e}")
    print("👋 Shutdown complete!")


# Create FastAPI application
def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    
    settings = get_settings()
    
    # Get root path from environment (useful for reverse proxy setups)
    root_path = os.getenv("ROOT_PATH", "")
    if root_path:
        print(f"🔗 Root path: {root_path}")
    
    app = FastAPI(
        title=settings.app_name,
        description="A template FastAPI application with DBZero integration",
        version=settings.app_version,
        root_path=root_path,
        openapi_prefix=root_path,
        lifespan=lifespan
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app


# Create the app instance
app = create_app()


@app.get("/healthcheck", tags=["Health"])
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint
    Verifies that the application and DBZero connection are working
    """
    try:
        # Ensure DBZero connection is active
        Connection.assure_initialized()
        
        settings = get_settings()
        
        return {
            "status": "healthy",
            "app_name": settings.app_name,
            "version": settings.app_version,
            "dbzero_status": "connected",
            "instance_type": settings.instance_type.value
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Health check failed: {str(e)}"
        )


@app.get("/", tags=["Root"])
async def root() -> Dict[str, str]:
    """
    Root endpoint with basic information
    """
    settings = get_settings()
    return {
        "message": f"Welcome to {settings.app_name}!",
        "version": settings.app_version,
        "docs": "/docs",
        "healthcheck": "/healthcheck"
    }


if __name__ == "__main__":
    import uvicorn
        
    settings = get_settings()
    
    print(f"🏃 Running {settings.app_name} v{settings.app_version}")
    print(f"🌐 Server: http://{settings.host}:{settings.port}")
    print(f"📚 API Docs: http://{settings.host}:{settings.port}/docs")
    
    uvicorn.run(
        "mini_app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
