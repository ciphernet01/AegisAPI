"""
Entry point for running the Zombie API backend server.

Run with:
    python app.py          # Development with auto-reload
    
Or use Uvicorn directly:
    uvicorn main:app --reload --port 5000
"""

import uvicorn
from config import get_settings


def run():
    """Run the FastAPI server with Uvicorn."""
    settings = get_settings()
    
    uvicorn.run(
        "main:app",  # module_name:app_instance
        host="0.0.0.0",  # Listen on all network interfaces
        port=settings.port,  # From config (default: 5000)
        reload=settings.debug,  # Auto-reload on code changes (dev only)
        log_level=settings.log_level.lower(),  # From config (default: INFO)
        access_log=True,  # Show HTTP request logs
    )


if __name__ == "__main__":
    print("Starting Zombie API Backend Server...")
    print("Available at: http://localhost:5000")
    print("Health check: http://localhost:5000/health")
    print("Docs: http://localhost:5000/docs")
    print()
    run()
