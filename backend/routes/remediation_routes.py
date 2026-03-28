"""
REST API endpoints for remediation workflows.

Provides endpoints for:
- Getting remediation plans for zombie APIs
- Executing remediation actions
- Tracking remediation status
- Bulk remediation operations
"""

from fastapi import APIRouter, HTTPException
from typing import List
from utils.logger import get_logger
from datetime import datetime, timedelta

logger = get_logger(__name__)

router = APIRouter(prefix="/api/v1/remediation", tags=["remediation"])

# Sample remediation plans
SAMPLE_PLANS = {
    1: {
        "api_id": 1,
        "api_name": "Legacy Auth Service",
        "status": "zombie",
        "priority": "high",
        "recommended_actions": [
            {
                "action": "notify_owner",
                "description": "Send decommissioning notification to API owner",
                "timeline": "Immediate"
            },
            {
                "action": "migrate_clients",
                "description": "Migrate all clients to new authentication service",
                "timeline": "30 days"
            },
            {
                "action": "decommission",
                "description": "Fully decommission and remove service",
                "timeline": "45 days"
            }
        ],
        "estimated_effort": "Medium - 3 teams involved",
        "risk_level": "High - breaking change"
    },
    2: {
        "api_id": 2,
        "api_name": "Old Payment API",
        "status": "deprecated",
        "priority": "medium",
        "recommended_actions": [
            {
                "action": "notify_owner",
                "description": "Send deprecation warning",
                "timeline": "Immediate"
            },
            {
                "action": "request_stakeholder_confirmation",
                "description": "Confirm no active usage",
                "timeline": "7 days"
            },
            {
                "action": "archive",
                "description": "Archive API for historical reference",
                "timeline": "30 days"
            }
        ],
        "estimated_effort": "Low - follows standard deprecation process",
        "risk_level": "Low"
    },
    3: {
        "api_id": 3,
        "api_name": "Image Processing service",
        "status": "zombie",
        "priority": "high",
        "recommended_actions": [
            {
                "action": "analyze_dependencies",
                "description": "Identify all dependent services",
                "timeline": "Immediate"
            },
            {
                "action": "redirect_to_replacement",
                "description": "Point clients to modern image service",
                "timeline": "14 days"
            },
            {
                "action": "decommission",
                "description": "Remove legacy service",
                "timeline": "30 days"
            }
        ],
        "estimated_effort": "High - complex dependencies",
        "risk_level": "High"
    },
}

SAMPLE_ACTIONS_LOG = [
    {
        "id": 1,
        "api_id": 1,
        "action": "notify_owner",
        "status": "completed",
        "timestamp": (datetime.now() - timedelta(days=5)).isoformat(),
        "result": "Notification sent to john.smith@company.com",
        "notes": "Owner confirmed receipt"
    },
    {
        "id": 2,
        "api_id": 2,
        "action": "request_stakeholder_confirmation",
        "status": "in_progress",
        "timestamp": (datetime.now() - timedelta(days=2)).isoformat(),
        "result": "Awaiting response from billing team",
        "notes": "Sent to jane.doe@company.com"
    }
]


@router.get("/plans")
def get_remediation_plans():
    """
    Get remediation plans for all zombie/high-risk APIs.
    
    Returns list of RemediationPlan with recommended actions for each API.
    """
    try:
        plans = list(SAMPLE_PLANS.values())
        
        return {
            "success": True,
            "total_plans": len(plans),
            "plans": plans,
            "message": "Scripted demo data active"
        }
    except Exception as e:
        logger.error(f"Error getting remediation plans: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get remediation plans")


@router.get("/plans/{api_id}")
def get_api_remediation_plan(api_id: int):
    """
    Get remediation plan for specific API.
    
    Args:
        api_id: ID of API to get plan for
        
    Returns:
        RemediationPlan with recommended actions
    """
    try:
        plan = SAMPLE_PLANS.get(api_id)
        
        if not plan:
            raise HTTPException(status_code=404, detail=f"API {api_id} not found or no remediation plan")
        
        return {
            "success": True,
            "plan": plan,
            "message": "Scripted demo data active"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting remediation plan for API {api_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get remediation plan")


@router.post("/decommission/{api_id}")
def decommission_api(api_id: int, reason: str = ""):
    """
    Decommission a zombie API (mark as deprecated).
    
    Args:
        api_id: ID of API to decommission
        reason: Reason for decommissioning
        
    Returns:
        Result of decommissioning action
    """
    try:
        plan = SAMPLE_PLANS.get(api_id)
        
        if not plan:
            raise HTTPException(status_code=404, detail=f"API {api_id} not found")
        
        return {
            "success": True,
            "api_id": api_id,
            "action": "decommission",
            "status": "scheduled",
            "scheduled_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "reason": reason or "Scheduled for removal - no recent usage",
            "message": "Decommissioning scheduled (demo - not persistent)"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error decommissioning API {api_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to decommission API")


@router.post("/archive/{api_id}")
def archive_api(api_id: int, archive_location: str = ""):
    """
    Archive a zombie API.
    
    Args:
        api_id: ID of API to archive
        archive_location: Where to store archived data
        
    Returns:
        Result of archival action
    """
    try:
        plan = SAMPLE_PLANS.get(api_id)
        
        if not plan:
            raise HTTPException(status_code=404, detail=f"API {api_id} not found")
        
        return {
            "success": True,
            "api_id": api_id,
            "action": "archive",
            "status": "completed",
            "archive_location": archive_location or "s3://api-archive/legacy-apis/",
            "archived_items": ["source_code", "documentation", "deployment_configs", "access_logs"],
            "message": "API archived successfully (demo - not persistent)"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error archiving API {api_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to archive API")


@router.post("/notify-owner/{api_id}")
def notify_api_owner(api_id: int, message: str = ""):
    """
    Send notification to API owner about remediation.
    
    Args:
        api_id: ID of API
        message: Custom notification message
        
    Returns:
        Result of notification action
    """
    try:
        plan = SAMPLE_PLANS.get(api_id)
        
        if not plan:
            raise HTTPException(status_code=404, detail=f"API {api_id} not found")
        
        owner_email = {
            1: "john.smith@company.com",
            2: "jane.doe@company.com",
            3: "bob.johnson@company.com"
        }.get(api_id, "unknown@company.com")
        
        return {
            "success": True,
            "api_id": api_id,
            "action": "notify_owner",
            "status": "sent",
            "recipient": owner_email,
            "timestamp": datetime.now().isoformat(),
            "message_preview": message or f"API {plan['api_name']} has been marked for remediation. Please review the remediation plan.",
            "note": "Notification sent (demo - not persistent)"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error notifying owner for API {api_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to notify owner")


@router.post("/revive/{api_id}")
def revive_api(api_id: int):
    """
    Revive a zombie API (mark as active again).
    
    Use when an API starts receiving traffic again or is brought back into use.
    
    Args:
        api_id: ID of API to revive
        
    Returns:
        Result of revive action
    """
    try:
        plan = SAMPLE_PLANS.get(api_id)
        
        if not plan:
            raise HTTPException(status_code=404, detail=f"API {api_id} not found")
        
        return {
            "success": True,
            "api_id": api_id,
            "action": "revive",
            "status": "completed",
            "new_status": "active",
            "revival_reason": "Resumed activity detected",
            "timestamp": datetime.now().isoformat(),
            "message": "API marked as active (demo - not persistent)"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reviving API {api_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to revive API")


@router.post("/bulk")
def bulk_remediation(api_ids: List[int], action: str):
    """
    Perform bulk remediation action on multiple APIs.
    
    Args:
        api_ids: List of API IDs to remediate
        action: Action to perform (decommission, archive, notify_owner, revive)
        
    Returns:
        Summary of bulk operation results
    """
    try:
        valid_actions = ["decommission", "archive", "notify_owner", "revive"]
        
        if action not in valid_actions:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid action '{action}'. Valid actions: {valid_actions}"
            )
        
        if not api_ids or len(api_ids) == 0:
            raise HTTPException(status_code=400, detail="No API IDs provided")
        
        if len(api_ids) > 100:
            raise HTTPException(status_code=400, detail="Maximum 100 APIs per bulk operation")
        
        # Validate all API IDs exist
        results = []
        for api_id in api_ids:
            if api_id in SAMPLE_PLANS:
                results.append({
                    "api_id": api_id,
                    "status": "success",
                    "result": f"{action.replace('_', ' ').title()} scheduled for API {api_id}"
                })
            else:
                results.append({
                    "api_id": api_id,
                    "status": "not_found",
                    "result": f"API {api_id} not found"
                })
        
        successful = len([r for r in results if r["status"] == "success"])
        
        return {
            "success": True,
            "action": action,
            "total_apis": len(api_ids),
            "successful": successful,
            "failed": len(api_ids) - successful,
            "results": results,
            "message": "Bulk operation scheduled (demo - not persistent)"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error performing bulk remediation: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to perform bulk remediation")


@router.get("/stats")
def get_remediation_stats():
    """
    Get remediation statistics and health metrics.
    
    Returns statistics about zombie APIs and remediation status.
    """
    try:
        completed_actions = len([a for a in SAMPLE_ACTIONS_LOG if a["status"] == "completed"])
        in_progress_actions = len([a for a in SAMPLE_ACTIONS_LOG if a["status"] == "in_progress"])
        
        stats = {
            "total_zombie_apis": len(SAMPLE_PLANS),
            "remediation_plans": len(SAMPLE_PLANS),
            "actions_completed": completed_actions,
            "actions_in_progress": in_progress_actions,
            "actions_pending": len(SAMPLE_PLANS) - completed_actions - in_progress_actions,
            "by_priority": {
                "high": len([p for p in SAMPLE_PLANS.values() if p["priority"] == "high"]),
                "medium": len([p for p in SAMPLE_PLANS.values() if p["priority"] == "medium"]),
                "low": len([p for p in SAMPLE_PLANS.values() if p["priority"] == "low"])
            },
            "estimated_total_effort": "High - Multiple teams and timeline",
            "last_action": SAMPLE_ACTIONS_LOG[-1]["timestamp"] if SAMPLE_ACTIONS_LOG else None
        }
        
        return {
            "success": True,
            "stats": stats,
            "message": "Scripted demo data active"
        }
    except Exception as e:
        logger.error(f"Error getting remediation stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get remediation stats")
