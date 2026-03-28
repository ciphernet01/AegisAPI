"""
REST API endpoints for remediation workflows.

Provides endpoints for:
- Getting remediation plans for zombie APIs
- Executing remediation actions
- Tracking remediation status
- Bulk remediation operations
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from database.db import get_db
from database.models import API
from services.remediation import RemediationEngine, RemediationAction, RemediationStatus
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/v1/remediation", tags=["remediation"])

# Initialize remediation engine
remediation_engine = RemediationEngine()


@router.get("/plans")
def get_remediation_plans(db: Session = Depends(get_db)):
    """
    Get remediation plans for all zombie/high-risk APIs.
    
    Returns list of RemediationPlan with recommended actions for each API.
    """
    try:
        # Find all APIs that need remediation
        all_apis = db.query(API).all()
        plans = []
        
        for api in all_apis:
            plan = remediation_engine.generate_remediation_plan(api)
            # Only include plans with recommended actions (zombie/deprecated/orphaned)
            if plan.recommended_actions:
                plans.append(plan.to_dict())
        
        return {
            "total_plans": len(plans),
            "plans": plans
        }
    except Exception as e:
        logger.error(f"Error getting remediation plans: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting remediation plans: {str(e)}")


@router.get("/plans/{api_id}")
def get_api_remediation_plan(api_id: int, db: Session = Depends(get_db)):
    """
    Get remediation plan for specific API.
    
    Args:
        api_id: ID of API to get plan for
        
    Returns:
        RemediationPlan with recommended actions
    """
    try:
        api = db.query(API).filter(API.id == api_id).first()
        
        if not api:
            raise HTTPException(status_code=404, detail=f"API {api_id} not found")
        
        plan = remediation_engine.generate_remediation_plan(api)
        return plan.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting remediation plan for API {api_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting remediation plan: {str(e)}")


@router.post("/decommission/{api_id}")
def decommission_api(api_id: int, reason: str = "", db: Session = Depends(get_db)):
    """
    Decommission a zombie API (mark as deprecated).
    
    Args:
        api_id: ID of API to decommission
        reason: Reason for decommissioning
        
    Returns:
        Result of decommissioning action
    """
    try:
        result = remediation_engine.decommission_api(db, api_id, reason)
        
        if not result.get("success"):
            raise HTTPException(status_code=404, detail=result.get("message"))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error decommissioning API {api_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error decommissioning API: {str(e)}")


@router.post("/archive/{api_id}")
def archive_api(api_id: int, archive_location: str = "", db: Session = Depends(get_db)):
    """
    Archive a zombie API.
    
    Args:
        api_id: ID of API to archive
        archive_location: Where to store archived data
        
    Returns:
        Result of archival action
    """
    try:
        result = remediation_engine.archive_api(db, api_id, archive_location)
        
        if not result.get("success"):
            raise HTTPException(status_code=404, detail=result.get("message"))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error archiving API {api_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error archiving API: {str(e)}")


@router.post("/notify-owner/{api_id}")
def notify_api_owner(api_id: int, message: str = "", db: Session = Depends(get_db)):
    """
    Send notification to API owner about remediation.
    
    Args:
        api_id: ID of API
        message: Custom notification message
        
    Returns:
        Result of notification action
    """
    try:
        result = remediation_engine.notify_owner(db, api_id, message)
        
        if not result.get("success"):
            raise HTTPException(status_code=404, detail=result.get("message"))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error notifying owner for API {api_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error notifying owner: {str(e)}")


@router.post("/revive/{api_id}")
def revive_api(api_id: int, db: Session = Depends(get_db)):
    """
    Revive a zombie API (mark as active again).
    
    Use when an API starts receiving traffic again or is brought back into use.
    
    Args:
        api_id: ID of API to revive
        
    Returns:
        Result of revive action
    """
    try:
        result = remediation_engine.revive_api(db, api_id)
        
        if not result.get("success"):
            raise HTTPException(status_code=404, detail=result.get("message"))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reviving API {api_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error reviving API: {str(e)}")


@router.post("/bulk")
def bulk_remediation(
    api_ids: List[int],
    action: str,
    db: Session = Depends(get_db)
):
    """
    Perform bulk remediation action on multiple APIs.
    
    Args:
        api_ids: List of API IDs to remediate
        action: Action to perform (decommission, archive, notify_owner, revive)
        
    Returns:
        Summary of bulk operation results
    """
    try:
        # Validate action
        try:
            remediation_action = RemediationAction(action)
        except ValueError:
            valid_actions = [a.value for a in RemediationAction]
            raise HTTPException(
                status_code=400,
                detail=f"Invalid action '{action}'. Valid actions: {valid_actions}"
            )
        
        # Validate API IDs
        if not api_ids or len(api_ids) == 0:
            raise HTTPException(status_code=400, detail="No API IDs provided")
        
        if len(api_ids) > 100:
            raise HTTPException(status_code=400, detail="Maximum 100 APIs per bulk operation")
        
        # Perform bulk operation
        result = remediation_engine.bulk_remediation(db, api_ids, remediation_action)
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error performing bulk remediation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error performing bulk remediation: {str(e)}")


@router.get("/stats")
def get_remediation_stats(db: Session = Depends(get_db)):
    """
    Get remediation statistics and health metrics.
    
    Returns statistics about zombie APIs and remediation status.
    """
    try:
        stats = remediation_engine.get_remediation_stats(db)
        return stats
    except Exception as e:
        logger.error(f"Error getting remediation stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting remediation stats: {str(e)}")
