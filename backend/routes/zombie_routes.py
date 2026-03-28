"""
Zombie API Detection Routes.

Endpoints for finding and analyzing zombie, orphaned, and deprecated APIs.
"""

from fastapi import APIRouter, HTTPException
from typing import List
from utils.logger import get_logger
from datetime import datetime, timedelta

logger = get_logger(__name__)
router = APIRouter(prefix="/api/v1", tags=["zombie-detection"])

# Sample data for MVP testing
SAMPLE_ZOMBIES = [
    {
        "id": 1,
        "name": "Legacy Auth Service",
        "endpoint": "/auth/legacy",
        "status": "zombie",
        "riskScore": 92,
        "confidence": 0.95,
        "lastUsed": "2024-01-01",
        "deprecationDate": "2023-12-01",
        "owner": "John Smith",
        "techStack": ["Node.js", "Express"],
        "method": "POST",
        "isDocumented": False,
    },
    {
        "id": 2,
        "name": "Old Payment API",
        "endpoint": "/payments/v1",
        "status": "deprecated",
        "riskScore": 75,
        "confidence": 0.82,
        "lastUsed": "2024-02-01",
        "deprecationDate": "2023-06-01",
        "owner": "Jane Doe",
        "techStack": ["Python", "Flask"],
        "method": "GET",
        "isDocumented": True,
    },
    {
        "id": 3,
        "name": "Image Processing service",
        "endpoint": "/images/process",
        "status": "zombie",
        "riskScore": 88,
        "confidence": 0.91,
        "lastUsed": "2024-01-15",
        "deprecationDate": "2023-11-01",
        "owner": "Bob Johnson",
        "techStack": ["Java", "Spring"],
        "method": "POST",
        "isDocumented": False,
    },
    {
        "id": 4,
        "name": "Notification Service",
        "endpoint": "/notify/send",
        "status": "zombie",
        "riskScore": 85,
        "confidence": 0.88,
        "lastUsed": "2024-01-08",
        "deprecationDate": "2023-10-15",
        "owner": "Alice Brown",
        "techStack": ["Go"],
        "method": "POST",
        "isDocumented": False,
    },
    {
        "id": 5,
        "name": "Reporting Dashboard API",
        "endpoint": "/reports/dashboard",
        "status": "deprecated",
        "riskScore": 72,
        "confidence": 0.79,
        "lastUsed": "2024-02-15",
        "deprecationDate": "2023-07-01",
        "owner": "Charlie Davis",
        "techStack": ["C#", ".NET"],
        "method": "GET",
        "isDocumented": True,
    },
    {
        "id": 6,
        "name": "Legacy User Service",
        "endpoint": "/users/legacy",
        "status": "zombie",
        "riskScore": 90,
        "confidence": 0.93,
        "lastUsed": "2023-12-25",
        "deprecationDate": "2023-09-01",
        "owner": "Eve Miller",
        "techStack": ["Ruby", "Rails"],
        "method": "GET",
        "isDocumented": False,
    },
]


@router.get("/zombies")
def list_zombie_apis():
    """
    Get list of all detected zombie APIs.
    
    Returns:
        List of zombie APIs with classification details
    """
    try:
        logger.info("Fetching zombie APIs - using sample data")
        
        # Filter to only zombie and deprecated APIs for this endpoint
        filtered_apis = [api for api in SAMPLE_ZOMBIES if api["status"] in ["zombie", "deprecated"]]
        
        return {
            "success": True,
            "count": len(filtered_apis),
            "apis": filtered_apis
        }
    
    except Exception as e:
        logger.error(f"Error listing zombie APIs: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch zombie APIs")


@router.post("/analyze")
def analyze_all_apis():
    """
    Run classification analysis on all APIs.
    
    Returns:
        Comprehensive analysis of all APIs with classification details
    """
    try:
        logger.info("Running full API analysis - using sample data")
        
        # Prepare sample analysis results
        results = []
        status_counts = {"active": 0, "zombie": 0, "orphaned": 0, "deprecated": 0}
        
        for api in SAMPLE_ZOMBIES:
            result = {
                "id": api["id"],
                "name": api["name"],
                "endpoint": api["endpoint"],
                "method": api["method"],
                "owner": api["owner"],
                "tech_stack": api["techStack"],
                "status": api["status"],
                "confidence": api["confidence"],
                "risk_score": api["riskScore"],
                "reasoning": [
                    f"API has not received traffic since {api['lastUsed']}",
                    f"Service marked for deprecation since {api['deprecationDate']}",
                    "No recent maintenance commits detected",
                    "Documentation is outdated or missing" if not api["isDocumented"] else "Documentation is available"
                ],
                "last_traffic": api["lastUsed"],
                "created_at": "2023-01-01",
                "is_documented": api["isDocumented"],
            }
            
            results.append(result)
            status_counts[api["status"]] += 1
        
        logger.info(f"Analysis complete: {len(SAMPLE_ZOMBIES)} APIs analyzed")
        
        return {
            "success": True,
            "total_apis": len(SAMPLE_ZOMBIES),
            "analysis_results": results,
            "summary": status_counts,
            "message": "Scripted demo data active"
        }
    
    except Exception as e:
        logger.error(f"Error analyzing APIs: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to analyze APIs")


@router.get("/apis/{api_id}/analysis")
def analyze_single_api(api_id: int):
    """
    Get detailed analysis for a single API.
    
    Args:
        api_id: ID of the API to analyze
    
    Returns:
        Detailed classification analysis
    """
    try:
        logger.info(f"Analyzing API ID: {api_id}")
        
        # Find the API in sample data
        api = next((a for a in SAMPLE_ZOMBIES if a["id"] == api_id), None)
        
        if not api:
            logger.warning(f"API not found: {api_id}")
            raise HTTPException(status_code=404, detail=f"API with ID {api_id} not found")
        
        # Build detailed response
        response = {
            "success": True,
            "id": api["id"],
            "name": api["name"],
            "endpoint": api["endpoint"],
            "method": api["method"],
            "owner": api["owner"],
            "tech_stack": api["techStack"],
            "status": api["status"],
            "confidence": api["confidence"],
            "risk_score": api["riskScore"],
            "reasoning": [
                f"Last traffic recorded: {api['lastUsed']}",
                f"Deprecation date: {api['deprecationDate']}",
                f"Documentation status: {'Available' if api['isDocumented'] else 'Missing or Outdated'}",
                "No active maintenance detected",
                "High dependency risk due to age and disuse"
            ],
            "is_documented": api["isDocumented"],
            "last_traffic": api["lastUsed"],
            "created_at": "2023-01-01",
            "classification_details": {
                "traffic_analysis": {
                    "last_request": api["lastUsed"],
                    "inactive_days": 45,
                    "traffic_trend": "declining"
                },
                "documentation_analysis": {
                    "documented": api["isDocumented"],
                    "last_updated": "2023-06-01" if api["isDocumented"] else "Never"
                },
                "ownership_analysis": {
                    "owner": api["owner"],
                    "team": "Legacy Systems",
                    "contact_available": True
                },
                "age_deprecation_analysis": {
                    "created_date": "2023-01-01",
                    "deprecation_date": api["deprecationDate"],
                    "days_deprecated": 90
                },
                "maintenance_analysis": {
                    "last_commit": api["lastUsed"],
                    "commit_frequency": "none",
                    "active_development": False
                }
            },
            "message": "Scripted demo data active"
        }
        
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing API {api_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to analyze API")


@router.get("/stats")
def get_zombie_stats():
    """
    Get quick zombie statistics.
    
    Returns:
        Summary statistics about API health
    """
    try:
        logger.info("Generating zombie statistics - using sample data")
        
        status_counts = {"active": 0, "zombie": 0, "orphaned": 0, "deprecated": 0}
        
        for api in SAMPLE_ZOMBIES:
            status_counts[api["status"]] += 1
        
        total = len(SAMPLE_ZOMBIES)
        zombie_percentage = (status_counts["zombie"] / total * 100) if total > 0 else 0
        
        return {
            "success": True,
            "total_apis": total,
            "active": status_counts.get("active", 0),
            "zombie": status_counts.get("zombie", 0),
            "zombie_percentage": round(zombie_percentage, 1),
            "orphaned": status_counts.get("orphaned", 0),
            "deprecated": status_counts.get("deprecated", 0),
            "message": "Scripted demo data active"
        }
    
    except Exception as e:
        logger.error(f"Error generating statistics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate statistics")
