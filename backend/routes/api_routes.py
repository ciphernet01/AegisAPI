"""
API Discovery Routes - expose discovered APIs via REST endpoints.

Endpoints:
- GET /apis - List all discovered APIs
- GET /apis/{id} - Get single API details
- GET /apis/search?q=query - Search APIs
- GET /stats - API statistics
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from database.db import get_db
from services.discovery_service import APIDiscoveryService
from utils.logger import get_logger

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


@router.get("", response_model=Dict[str, Any])
async def list_apis(
    limit: int = Query(50, ge=1, le=500, description="Max results to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    db: Session = Depends(get_db)
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
        service = APIDiscoveryService(db)
        apis = service.get_all_discovered_apis(limit=limit, offset=offset)
        
        return {
            "success": True,
            "total": len(apis),
            "limit": limit,
            "offset": offset,
            "data": apis,
        }
    except Exception as e:
        logger.error(f"List APIs failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve APIs")


@router.get("/{api_id}", response_model=Dict[str, Any])
async def get_api(
    api_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get detailed information about a specific API.
    
    Args:
        api_id: API ID from database
    
    Returns:
        dict with API details
    """
    try:
        service = APIDiscoveryService(db)
        api = service.get_api_by_id(api_id)
        
        if not api:
            raise HTTPException(status_code=404, detail=f"API {api_id} not found")
        
        return {
            "success": True,
            "data": api,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get API {api_id} failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve API")


@router.get("/search", response_model=Dict[str, Any])
async def search_apis(
    q: str = Query(..., min_length=1, max_length=100, description="Search query"),
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db)
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
        service = APIDiscoveryService(db)
        apis = service.search_apis(q, limit=limit)
        
        return {
            "success": True,
            "query": q,
            "total": len(apis),
            "data": apis,
        }
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Search failed")


@router.get("/stats", response_model=Dict[str, Any])
async def get_statistics(db: Session = Depends(get_db)) -> Dict[str, Any]:
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
            "total_apis": 150,
            "by_status": {
                "active": 120,
                "deprecated": 20,
                "orphaned": 8,
                "zombie": 2
            },
            "documented": 145,
            "undocumented": 5
        }
    """
    try:
        service = APIDiscoveryService(db)
        stats = service.get_statistics()
        
        return {
            "success": True,
            "data": stats,
        }
    except Exception as e:
        logger.error(f"Get statistics failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get statistics")
