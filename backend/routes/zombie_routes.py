"""
Zombie API Detection Routes.

Endpoints for finding and analyzing zombie, orphaned, and deprecated APIs.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.db import get_db
from database.models import API
from security.classification import ZombieClassifier, APIStatus, classify_api
from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/v1", tags=["zombie-detection"])

# Initialize classifier
classifier = ZombieClassifier()


class APIAnalysis:
    """Response model for API analysis."""
    
    def __init__(self, api_id: int, name: str, endpoint: str, status: str, confidence: float, risk_score: float, reasoning: list):
        self.id = api_id
        self.name = name
        self.endpoint = endpoint
        self.status = status
        self.confidence = confidence
        self.risk_score = risk_score
        self.reasoning = reasoning


@router.get("/zombies")
def list_zombie_apis(db: Session = Depends(get_db)):
    """
    Get list of all detected zombie APIs.
    
    Returns:
        List of zombie APIs with classification details
    """
    try:
        logger.info("Fetching zombie APIs")
        
        # Get all APIs
        apis = db.query(API).all()
        
        if not apis:
            logger.warning("No APIs found in database")
            return {
                "total_apis": 0,
                "zombie_count": 0,
                "orphaned_count": 0,
                "deprecated_count": 0,
                "active_count": 0,
                "zombies": []
            }
        
        # Classify each API
        zombies = []
        orphaned = []
        deprecated = []
        active = []
        
        for api in apis:
            status, analysis = classify_api(api)
            
            api_result = {
                "id": api.id,
                "name": api.name,
                "endpoint": api.endpoint,
                "status": status.value,
                "confidence": analysis["confidence_score"],
                "risk_score": analysis.get("risk_score", 0),
                "reasoning": analysis["reasoning"],
            }
            
            if status == APIStatus.ZOMBIE:
                zombies.append(api_result)
            elif status == APIStatus.ORPHANED:
                orphaned.append(api_result)
            elif status == APIStatus.DEPRECATED:
                deprecated.append(api_result)
            else:
                active.append(api_result)
        
        logger.info(f"Classified {len(apis)} APIs: {len(zombies)} zombies, {len(orphaned)} orphaned, {len(deprecated)} deprecated")
        
        return {
            "total_apis": len(apis),
            "zombie_count": len(zombies),
            "orphaned_count": len(orphaned),
            "deprecated_count": len(deprecated),
            "active_count": len(active),
            "zombies": zombies,
            "orphaned": orphaned,
            "deprecated": deprecated,
        }
    
    except Exception as e:
        logger.error(f"Error listing zombie APIs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze")
def analyze_all_apis(db: Session = Depends(get_db)):
    """
    Run classification analysis on all APIs.
    
    Returns:
        Comprehensive analysis of all APIs with classification details
    """
    try:
        logger.info("Running full API analysis")
        
        # Get all APIs
        apis = db.query(API).all()
        
        if not apis:
            logger.warning("No APIs found for analysis")
            return {
                "total_apis": 0,
                "analysis_results": [],
                "summary": {
                    "active": 0,
                    "zombie": 0,
                    "orphaned": 0,
                    "deprecated": 0,
                }
            }
        
        # Analyze each API
        results = []
        status_counts = {"active": 0, "zombie": 0, "orphaned": 0, "deprecated": 0}
        
        for api in apis:
            status, analysis = classify_api(api)
            
            result = {
                "id": api.id,
                "name": api.name,
                "endpoint": api.endpoint,
                "method": api.method,
                "owner": api.owner,
                "tech_stack": api.tech_stack,
                "status": status.value,
                "confidence": analysis["confidence_score"],
                "risk_score": analysis.get("risk_score", 0),
                "reasoning": analysis["reasoning"],
                "last_traffic": api.last_traffic.isoformat() if api.last_traffic else None,
                "created_at": api.created_at.isoformat(),
                "is_documented": api.is_documented,
            }
            
            results.append(result)
            status_counts[status.value] += 1
        
        logger.info(f"Analysis complete: {len(apis)} APIs analyzed")
        logger.info(f"Summary: {status_counts}")
        
        return {
            "total_apis": len(apis),
            "analysis_results": results,
            "summary": status_counts,
        }
    
    except Exception as e:
        logger.error(f"Error analyzing APIs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/apis/{api_id}/analysis")
def analyze_single_api(api_id: int, db: Session = Depends(get_db)):
    """
    Get detailed analysis for a single API.
    
    Args:
        api_id: ID of the API to analyze
    
    Returns:
        Detailed classification analysis
    """
    try:
        logger.info(f"Analyzing API ID: {api_id}")
        
        # Get the API
        api = db.query(API).filter(API.id == api_id).first()
        
        if not api:
            logger.warning(f"API not found: {api_id}")
            raise HTTPException(status_code=404, detail=f"API with ID {api_id} not found")
        
        # Classify the API
        status, analysis = classify_api(api)
        
        # Build detailed response
        response = {
            "id": api.id,
            "name": api.name,
            "endpoint": api.endpoint,
            "method": api.method,
            "owner": api.owner,
            "tech_stack": api.tech_stack,
            "status": status.value,
            "confidence": analysis["confidence_score"],
            "risk_score": analysis.get("risk_score", 0),
            "reasoning": analysis["reasoning"],
            "is_documented": api.is_documented,
            "last_traffic": api.last_traffic.isoformat() if api.last_traffic else None,
            "created_at": api.created_at.isoformat(),
            "classification_details": {
                "traffic_analysis": analysis.get("factors", {}).get("traffic", {}),
                "documentation_analysis": analysis.get("factors", {}).get("documentation", {}),
                "ownership_analysis": analysis.get("factors", {}).get("ownership", {}),
                "age_deprecation_analysis": analysis.get("factors", {}).get("age_deprecation", {}),
                "maintenance_analysis": analysis.get("factors", {}).get("maintenance", {}),
            }
        }
        
        logger.info(f"API {api_id} classified as {status.value} (confidence: {analysis['confidence_score']})")
        
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing API {api_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
def get_zombie_stats(db: Session = Depends(get_db)):
    """
    Get quick zombie statistics.
    
    Returns:
        Summary statistics about API health
    """
    try:
        logger.info("Generating zombie statistics")
        
        apis = db.query(API).all()
        
        status_counts = {"active": 0, "zombie": 0, "orphaned": 0, "deprecated": 0}
        
        for api in apis:
            status, _ = classify_api(api)
            status_counts[status.value] += 1
        
        total = len(apis)
        zombie_percentage = (status_counts["zombie"] / total * 100) if total > 0 else 0
        
        return {
            "total_apis": total,
            "active": status_counts["active"],
            "zombie": status_counts["zombie"],
            "zombie_percentage": round(zombie_percentage, 1),
            "orphaned": status_counts["orphaned"],
            "deprecated": status_counts["deprecated"],
        }
    
    except Exception as e:
        logger.error(f"Error generating statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
