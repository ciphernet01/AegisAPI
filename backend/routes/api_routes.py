"""
API Discovery Routes - expose discovered APIs via REST endpoints.

Endpoints:
- GET /apis - List all discovered APIs
- GET /apis/{id} - Get single API details
- GET /apis/search?q=query - Search APIs
- GET /stats - API statistics
"""

from fastapi import APIRouter, Query, HTTPException
from typing import List, Dict, Any
from utils.logger import get_logger
from datetime import datetime

logger = get_logger(__name__)

# Create router
router = APIRouter(
    prefix="/apis",
    tags=["API Discovery"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    }
)

# Sample discovered APIs
SAMPLE_DISCOVERED_APIS = [
    {
        "id": 1,
        "name": "Legacy Auth Service",
        "endpoint": "/auth/legacy",
        "method": "POST",
        "status": "zombie",
        "owner": "John Smith",
        "tech_stack": ["Node.js", "Express"],
        "last_traffic": "2024-01-01",
        "is_documented": False,
        "discovered_at": "2023-01-01",
        "deprecation_date": "2023-12-01"
    },
    {
        "id": 2,
        "name": "Old Payment API",
        "endpoint": "/payments/v1",
        "method": "GET",
        "status": "deprecated",
        "owner": "Jane Doe",
        "tech_stack": ["Python", "Flask"],
        "last_traffic": "2024-02-01",
        "is_documented": True,
        "discovered_at": "2023-01-01",
        "deprecation_date": "2023-06-01"
    },
    {
        "id": 3,
        "name": "Image Processing service",
        "endpoint": "/images/process",
        "method": "POST",
        "status": "zombie",
        "owner": "Bob Johnson",
        "tech_stack": ["Java", "Spring"],
        "last_traffic": "2024-01-15",
        "is_documented": False,
        "discovered_at": "2023-02-01",
        "deprecation_date": "2023-11-01"
    },
    {
        "id": 4,
        "name": "Notification Service",
        "endpoint": "/notify/send",
        "method": "POST",
        "status": "zombie",
        "owner": "Alice Brown",
        "tech_stack": ["Go"],
        "last_traffic": "2024-01-08",
        "is_documented": False,
        "discovered_at": "2023-03-01",
        "deprecation_date": "2023-10-15"
    },
    {
        "id": 5,
        "name": "Reporting Dashboard API",
        "endpoint": "/reports/dashboard",
        "method": "GET",
        "status": "deprecated",
        "owner": "Charlie Davis",
        "tech_stack": ["C#", ".NET"],
        "last_traffic": "2024-02-15",
        "is_documented": True,
        "discovered_at": "2023-04-01",
        "deprecation_date": "2023-07-01"
    },
    {
        "id": 6,
        "name": "Legacy User Service",
        "endpoint": "/users/legacy",
        "method": "GET",
        "status": "zombie",
        "owner": "Eve Miller",
        "tech_stack": ["Ruby", "Rails"],
        "last_traffic": "2023-12-25",
        "is_documented": False,
        "discovered_at": "2023-05-01",
        "deprecation_date": "2023-09-01"
    },
    {
        "id": 7,
        "name": "User Management API",
        "endpoint": "/users/v2",
        "method": "GET",
        "status": "active",
        "owner": "Development Team",
        "tech_stack": ["Node.js", "Express", "PostgreSQL"],
        "last_traffic": "2024-03-15",
        "is_documented": True,
        "discovered_at": "2023-06-01",
        "deprecation_date": None
    },
    {
        "id": 8,
        "name": "Product Service",
        "endpoint": "/products/api",
        "method": "GET",
        "status": "active",
        "owner": "Product Team",
        "tech_stack": ["Python", "FastAPI", "MongoDB"],
        "last_traffic": "2024-03-16",
        "is_documented": True,
        "discovered_at": "2023-07-01",
        "deprecation_date": None
    },
]


@router.get("/stats")
async def get_statistics() -> Dict[str, Any]:
    """
    Get statistics about discovered APIs.
    
    Returns:
        dict with counts by:
        - Status (active, deprecated, orphaned, zombie)
        - Documented vs undocumented
    
    Example:
        GET /apis/stats
    
    Returns:
        {
            "total_apis": 8,
            "by_status": {
                "active": 2,
                "deprecated": 2,
                "orphaned": 0,
                "zombie": 3
            },
            "documented": 3,
            "undocumented": 5
        }
    """
    try:
        statuses = {}
        documented = 0
        
        for api in SAMPLE_DISCOVERED_APIS:
            status = api.get("status", "unknown")
            statuses[status] = statuses.get(status, 0) + 1
            if api.get("is_documented"):
                documented += 1
        
        # Ensure all status types are present
        for status in ["active", "deprecated", "orphaned", "zombie"]:
            if status not in statuses:
                statuses[status] = 0
        
        return {
            "success": True,
            "data": {
                "total_apis": len(SAMPLE_DISCOVERED_APIS),
                "by_status": statuses,
                "documented": documented,
                "undocumented": len(SAMPLE_DISCOVERED_APIS) - documented,
                "documentation_coverage": round((documented / len(SAMPLE_DISCOVERED_APIS) * 100), 1) if SAMPLE_DISCOVERED_APIS else 0
            },
            "message": "Scripted demo data active"
        }
    except Exception as e:
        logger.error(f"Get statistics failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get statistics")


@router.get("/search")
async def search_apis(
    q: str = Query(..., min_length=1, max_length=100, description="Search query"),
    limit: int = Query(50, ge=1, le=500)
) -> Dict[str, Any]:
    """
    Search APIs by name, endpoint, or owner.
    
    Example:
        GET /apis/search?q=user-service&limit=20
    
    Args:
        q: Search query (searches name, endpoint, owner)
        limit: Max results
    
    Returns:
        dict with matching APIs
    """
    try:
        q_lower = q.lower()
        results = [
            api for api in SAMPLE_DISCOVERED_APIS
            if q_lower in api["name"].lower() 
            or q_lower in api["endpoint"].lower()
            or q_lower in api["owner"].lower()
        ][:limit]
        
        return {
            "success": True,
            "query": q,
            "total": len(results),
            "data": results,
            "message": "Scripted demo data active"
        }
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Search failed")


@router.get("")
async def list_apis(
    limit: int = Query(50, ge=1, le=500, description="Max results to return"),
    offset: int = Query(0, ge=0, description="Pagination offset")
) -> Dict[str, Any]:
    """
    List all discovered APIs.
    
    Supports pagination:
    - limit: Maximum 500 APIs per request
    - offset: For pagination
    
    Example:
        GET /apis?limit=50&offset=0
    
    Returns:
        dict with apis list and metadata
    """
    try:
        # Apply pagination
        paginated_apis = SAMPLE_DISCOVERED_APIS[offset:offset + limit]
        
        return {
            "success": True,
            "total": len(SAMPLE_DISCOVERED_APIS),
            "limit": limit,
            "offset": offset,
            "count": len(paginated_apis),
            "data": paginated_apis,
            "message": "Scripted demo data active"
        }
    except Exception as e:
        logger.error(f"List APIs failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve APIs")


@router.get("/{api_id}")
async def get_api(api_id: int) -> Dict[str, Any]:
    """
    Get detailed information about a specific API.
    
    Args:
        api_id: API ID from database
    
    Returns:
        dict with API details
    """
    try:
        api = next((a for a in SAMPLE_DISCOVERED_APIS if a["id"] == api_id), None)
        
        if not api:
            raise HTTPException(status_code=404, detail=f"API {api_id} not found")
        
        return {
            "success": True,
            "data": api,
            "message": "Scripted demo data active"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get API {api_id} failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve API")
