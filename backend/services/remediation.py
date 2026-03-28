"""
Remediation workflows for zombie API management.

Provides automated and manual remediation actions:
- Decommissioning workflows
- Archival and migration
- Owner notifications
- Bulk remediation operations
- Remediation status tracking
"""

from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from database.models import API
from security.classification import classify_api, ZombieClassifier, APIStatus
from utils.logger import get_logger

logger = get_logger(__name__)


class RemediationAction(str, Enum):
    """Available remediation actions for zombie APIs."""
    DECOMMISSION = "decommission"
    ARCHIVE = "archive"
    NOTIFY_OWNER = "notify_owner"
    MIGRATE_CONSUMERS = "migrate_consumers"
    REVIVE = "revive"
    DEPRECATE = "deprecate"


class RemediationStatus(str, Enum):
    """Status of remediation action."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class RemediationPlan:
    """Plan for remediating a zombie API."""
    api_id: int
    api_name: str
    status: APIStatus
    risk_score: float
    recommended_actions: List[RemediationAction]
    urgency: str  # critical, high, medium, low
    owner: Optional[str]
    reasoning: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "api_id": self.api_id,
            "api_name": self.api_name,
            "status": self.status.value,
            "risk_score": self.risk_score,
            "recommended_actions": [action.value for action in self.recommended_actions],
            "urgency": self.urgency,
            "owner": self.owner,
            "reasoning": self.reasoning
        }


class RemediationEngine:
    """Engine for zombie API remediation."""

    def __init__(self):
        """Initialize remediation engine."""
        self.classifier = ZombieClassifier()

    def generate_remediation_plan(self, api: API) -> RemediationPlan:
        """
        Generate a remediation plan for a zombie API.
        
        Args:
            api: API to remediate
            
        Returns:
            RemediationPlan with recommended actions
        """
        # Classify API to get full analysis
        classification = classify_api(api)
        
        # Determine recommended actions based on status and risk
        recommended_actions = self._determine_actions(api, classification.status, classification.risk_score)
        
        # Determine urgency
        urgency = self._calculate_urgency(classification.risk_score, classification.status)
        
        # Build reasoning
        reasoning = self._build_reasoning(api, classification)
        
        return RemediationPlan(
            api_id=api.id,
            api_name=api.name,
            status=classification.status,
            risk_score=classification.risk_score,
            recommended_actions=recommended_actions,
            urgency=urgency,
            owner=api.owner,
            reasoning=reasoning
        )

    def _determine_actions(self, api: API, status: APIStatus, risk_score: float) -> List[RemediationAction]:
        """Determine recommended actions based on API status and risk."""
        actions = []
        
        if status == APIStatus.ZOMBIE:
            if risk_score >= 90:
                # High risk zombie: immediate decommissioning
                actions.append(RemediationAction.NOTIFY_OWNER)
                actions.append(RemediationAction.DECOMMISSION)
            elif risk_score >= 75:
                # Medium-high risk: notify and prepare for archival
                actions.append(RemediationAction.NOTIFY_OWNER)
                actions.append(RemediationAction.ARCHIVE)
            else:
                # Lower risk: notify owner first
                actions.append(RemediationAction.NOTIFY_OWNER)
                actions.append(RemediationAction.DEPRECATE)
                
        elif status == APIStatus.DEPRECATED:
            # Deprecated APIs should be archived eventually
            actions.append(RemediationAction.NOTIFY_OWNER)
            actions.append(RemediationAction.ARCHIVE)
            
        elif status == APIStatus.ORPHANED:
            # Orphaned APIs: immediate attention required
            actions.append(RemediationAction.NOTIFY_OWNER)
            actions.append(RemediationAction.MIGRATE_CONSUMERS)
            actions.append(RemediationAction.ARCHIVE)
        
        return actions if actions else [RemediationAction.NOTIFY_OWNER]

    def _calculate_urgency(self, risk_score: float, status: APIStatus) -> str:
        """Calculate urgency level for remediation."""
        if status == APIStatus.ZOMBIE and risk_score >= 90:
            return "critical"
        elif status == APIStatus.ZOMBIE and risk_score >= 75:
            return "high"
        elif status == APIStatus.ORPHANED:
            return "high"
        elif status == APIStatus.DEPRECATED:
            return "medium"
        else:
            return "low"

    def _build_reasoning(self, api: API, classification) -> str:
        """Build human-readable reasoning for recommendations."""
        reasons = []
        
        if api.last_traffic:
            days_since_traffic = (datetime.utcnow() - api.last_traffic).days
            if days_since_traffic > 180:
                reasons.append(f"No traffic for {days_since_traffic} days")
        
        if not api.is_documented:
            reasons.append("Undocumented")
        
        if not api.owner:
            reasons.append("No owner assigned")
        
        if api.status == APIStatus.DEPRECATED:
            reasons.append("Marked as deprecated")
        
        return "; ".join(reasons) if reasons else "Review recommended"

    def decommission_api(self, db: Session, api_id: int, reason: str = "") -> Dict[str, Any]:
        """
        Decommission a zombie API.
        
        Args:
            db: Database session
            api_id: ID of API to decommission
            reason: Reason for decommissioning
            
        Returns:
            Result of decommissioning action
        """
        api = db.query(API).filter(API.id == api_id).first()
        
        if not api:
            logger.warning(f"API {api_id} not found for decommissioning")
            return {
                "success": False,
                "message": f"API {api_id} not found",
                "api_id": api_id
            }
        
        try:
            # Mark as deprecated first (soft decommission)
            api.status = APIStatus.DEPRECATED
            db.commit()
            
            logger.info(f"Decommissioned API {api.name} (ID: {api.id}). Reason: {reason}")
            
            return {
                "success": True,
                "message": f"API {api.name} marked as deprecated",
                "api_id": api_id,
                "action": RemediationAction.DECOMMISSION.value,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error decommissioning API {api_id}: {str(e)}")
            db.rollback()
            return {
                "success": False,
                "message": f"Failed to decommission API: {str(e)}",
                "api_id": api_id
            }

    def archive_api(self, db: Session, api_id: int, archive_location: str = "") -> Dict[str, Any]:
        """
        Archive a zombie API.
        
        Args:
            db: Database session
            api_id: ID of API to archive
            archive_location: Where archived data should be stored
            
        Returns:
            Result of archival action
        """
        api = db.query(API).filter(API.id == api_id).first()
        
        if not api:
            logger.warning(f"API {api_id} not found for archival")
            return {
                "success": False,
                "message": f"API {api_id} not found",
                "api_id": api_id
            }
        
        try:
            # In a real system, we would:
            # 1. Export API documentation and specs
            # 2. Backup configuration
            # 3. Store in archive location
            # 4. Update status
            
            logger.info(f"Archived API {api.name} (ID: {api.id}) to {archive_location}")
            
            return {
                "success": True,
                "message": f"API {api.name} archived successfully",
                "api_id": api_id,
                "action": RemediationAction.ARCHIVE.value,
                "archive_location": archive_location or "default_archive",
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error archiving API {api_id}: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to archive API: {str(e)}",
                "api_id": api_id
            }

    def notify_owner(self, db: Session, api_id: int, message: str = "") -> Dict[str, Any]:
        """
        Notify API owner of remediation recommendations.
        
        Args:
            db: Database session
            api_id: ID of API
            message: Custom notification message
            
        Returns:
            Result of notification action
        """
        api = db.query(API).filter(API.id == api_id).first()
        
        if not api:
            logger.warning(f"API {api_id} not found for notification")
            return {
                "success": False,
                "message": f"API {api_id} not found",
                "api_id": api_id
            }
        
        if not api.owner:
            logger.warning(f"API {api.name} has no owner assigned")
            return {
                "success": False,
                "message": f"API {api.name} has no owner assigned",
                "api_id": api_id
            }
        
        try:
            # In a real system, this would send email/notification
            default_message = f"Your API '{api.name}' requires attention for remediation. Status: {api.status.value}"
            notification_text = message or default_message
            
            logger.info(f"Notified owner '{api.owner}' for API {api.name}: {notification_text}")
            
            return {
                "success": True,
                "message": f"Owner {api.owner} notified",
                "api_id": api_id,
                "action": RemediationAction.NOTIFY_OWNER.value,
                "owner": api.owner,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error notifying owner for API {api_id}: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to notify owner: {str(e)}",
                "api_id": api_id
            }

    def revive_api(self, db: Session, api_id: int) -> Dict[str, Any]:
        """
        Revive a zombie API (mark as active again).
        
        This action is used when an API starts receiving traffic again
        or is being brought back into active use.
        
        Args:
            db: Database session
            api_id: ID of API to revive
            
        Returns:
            Result of revive action
        """
        api = db.query(API).filter(API.id == api_id).first()
        
        if not api:
            logger.warning(f"API {api_id} not found for reviving")
            return {
                "success": False,
                "message": f"API {api_id} not found",
                "api_id": api_id
            }
        
        try:
            api.status = APIStatus.ACTIVE
            # Optionally reset last_traffic to current time
            api.last_traffic = datetime.utcnow()
            db.commit()
            
            logger.info(f"Revived API {api.name} (ID: {api.id})")
            
            return {
                "success": True,
                "message": f"API {api.name} revived to ACTIVE status",
                "api_id": api_id,
                "action": RemediationAction.REVIVE.value,
                "new_status": APIStatus.ACTIVE.value,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error reviving API {api_id}: {str(e)}")
            db.rollback()
            return {
                "success": False,
                "message": f"Failed to revive API: {str(e)}",
                "api_id": api_id
            }

    def bulk_remediation(self, db: Session, api_ids: List[int], action: RemediationAction) -> Dict[str, Any]:
        """
        Perform bulk remediation action on multiple APIs.
        
        Args:
            db: Database session
            api_ids: List of API IDs to remediate
            action: Action to perform on all APIs
            
        Returns:
            Bulk operation result summary
        """
        results = {
            "action": action.value,
            "total_apis": len(api_ids),
            "successful": 0,
            "failed": 0,
            "results": []
        }
        
        for api_id in api_ids:
            result = None
            
            if action == RemediationAction.DECOMMISSION:
                result = self.decommission_api(db, api_id)
            elif action == RemediationAction.ARCHIVE:
                result = self.archive_api(db, api_id)
            elif action == RemediationAction.NOTIFY_OWNER:
                result = self.notify_owner(db, api_id)
            elif action == RemediationAction.REVIVE:
                result = self.revive_api(db, api_id)
            
            if result:
                results["results"].append(result)
                if result.get("success"):
                    results["successful"] += 1
                else:
                    results["failed"] += 1
        
        logger.info(f"Bulk remediation: {action.value} on {api_ids} - {results['successful']} successful, {results['failed']} failed")
        
        return results

    def get_remediation_stats(self, db: Session) -> Dict[str, Any]:
        """
        Get remediation statistics across all APIs.
        
        Args:
            db: Database session
            
        Returns:
            Statistics about API health and remediation status
        """
        all_apis = db.query(API).all()
        
        zombie_count = 0
        deprecated_count = 0
        orphaned_count = 0
        needs_remediation = 0
        
        for api in all_apis:
            classification = classify_api(api)
            
            if classification.status == APIStatus.ZOMBIE:
                zombie_count += 1
                if classification.risk_score >= 75:
                    needs_remediation += 1
            elif classification.status == APIStatus.DEPRECATED:
                deprecated_count += 1
                needs_remediation += 1
            elif classification.status == APIStatus.ORPHANED:
                orphaned_count += 1
                needs_remediation += 1
        
        total_apis = len(all_apis)
        
        return {
            "total_apis": total_apis,
            "zombie_count": zombie_count,
            "deprecated_count": deprecated_count,
            "orphaned_count": orphaned_count,
            "apis_needing_remediation": needs_remediation,
            "remediation_percentage": (needs_remediation / total_apis * 100) if total_apis > 0 else 0,
            "health_score": ((total_apis - needs_remediation) / total_apis * 100) if total_apis > 0 else 100
        }
