"""
Main FastAPI application factory and configuration.
Sets up the FastAPI app with middleware, routes, and settings.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config import get_settings

# Import routes (we'll create these later)
# from routes.health_routes import router as health_router
# from routes.api_routes import router as api_router


# ========== LIFESPAN EVENTS ==========
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    App startup and shutdown events.
    
    STARTUP:
    - Connect to database
    - Initialize Redis cache
    - Start background jobs
    
    SHUTDOWN:
    - Close database connections
    - Clean up resources
    """
    # Startup
    print("🚀 Application starting...")
    # TODO: Connect to database
    # TODO: Initialize Redis
    yield
    
    # Shutdown
    print("🛑 Application shutting down...")
    # TODO: Close database connections


def create_app() -> FastAPI:
    """
    Factory function to create and configure FastAPI application.
    
    Features:
    - CORS middleware (allow frontend to call API)
    - Request/response logging
    - Error handling
    - Database connectivity
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    
    settings = get_settings()
    
    # Create FastAPI app instance
    app = FastAPI(
        title="Zombie API Discovery & Defence Platform",
        description="Automated API discovery, security assessment, and remediation",
        version="0.1.0",
        lifespan=lifespan,
        debug=settings.debug
    )
    
    # ========== MIDDLEWARE SETUP ==========
    
    # 1. CORS Middleware - Allow frontend to call our API
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 2. TODO: Add request logging middleware
    # 3. TODO: Add error handling middleware
    # 4. TODO: Add authentication middleware
    
    # ========== INCLUDE ROUTES ==========
    
    # Health check endpoint (simple, no dependencies)
    @app.get("/health", tags=["Health"])
    async def health_check():
        """
        Health check endpoint - verify API is running.
        
        Called by:
        - Kubernetes/Docker health probes
        - Load balancers
        - Monitoring systems
        
        Returns:
            dict: Status and timestamp
        """
        return {
            "status": "healthy",
            "service": "zombie-api-backend",
            "version": "0.1.0"
        }
    
    # Include route modules
    from routes.api_routes import router as api_router
    app.include_router(api_router, prefix="/api/v1")
    
    return app


# Create the app instance
app = create_app()
