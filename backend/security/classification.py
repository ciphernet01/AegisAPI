"""
Zombie API Classification Engine.

Classifies APIs as: ACTIVE, DEPRECATED, ORPHANED, or ZOMBIE
based on traffic patterns, documentation, ownership, and age.

Detection Algorithm:
1. **ZOMBIE**: No traffic > 90 days, undocumented, or orphaned
2. **DEPRECATED**: Marked deprecated in metadata
3. **ORPHANED**: No owner or missing critical metadata
4. **ACTIVE**: Recent traffic, documented, has owner
"""

from enum import Enum
from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from database.models import API
from utils.logger import get_logger

logger = get_logger(__name__)


class APIStatus(Enum):
    """API lifecycle status classification."""
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ORPHANED = "orphaned"
    ZOMBIE = "zombie"


class ZombieDetectionConfig:
    """
    Configuration for zombie API detection.
    
    Thresholds can be customized per environment.
    """
    # Traffic inactivity threshold (days)
    NO_TRAFFIC_THRESHOLD_DAYS = 90
    
    # Age threshold for young APIs (days)
    NEW_API_THRESHOLD_DAYS = 30
    
    # Documentation requirement
    REQUIRE_DOCUMENTATION = True
    
    # Ownership requirement
    REQUIRE_OWNER = True
    
    # Version requirement (undated versions indicate zombie)
    REQUIRE_VERSION_IN_NAME = False


class ZombieClassifier:
    """
    Zombie API Detection Engine.
    
    Analyzes APIs and classifies them as zombie, deprecated, orphaned, or active.
    Uses multi-factor scoring system with confidence levels.
    """
    
    def __init__(self, config: Optional[ZombieDetectionConfig] = None):
        """
        Initialize classifier with optional custom configuration.
        
        Args:
            config: Optional ZombieDetectionConfig instance
        """
        self.config = config or ZombieDetectionConfig()
        self.analysis_results = {}
    
    def classify(self, api: API) -> Tuple[APIStatus, Dict[str, Any]]:
        """
        Classify a single API.
        
        Args:
            api: API database model instance
        
        Returns:
            Tuple of (status, analysis_details)
        """
        logger.info(f"Classifying API: {api.name} (ID: {api.id})")
        
        # Run multi-factor analysis
        analysis = {
            "api_id": api.id,
            "api_name": api.name,
            "endpoint": api.endpoint,
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "factors": {},
            "confidence_score": 0.0,
            "reasoning": [],
        }
        
        try:
            # Factor 1: Traffic Activity
            traffic_factor = self._analyze_traffic(api)
            analysis["factors"]["traffic"] = traffic_factor
            
            # Factor 2: Documentation
            doc_factor = self._analyze_documentation(api)
            analysis["factors"]["documentation"] = doc_factor
            
            # Factor 3: Ownership
            owner_factor = self._analyze_ownership(api)
            analysis["factors"]["ownership"] = owner_factor
            
            # Factor 4: Age & Deprecation Status
            age_factor = self._analyze_age_and_deprecation(api)
            analysis["factors"]["age_deprecation"] = age_factor
            
            # Factor 5: Tech Stack & Maintenance Indicators
            maintenance_factor = self._analyze_maintenance(api)
            analysis["factors"]["maintenance"] = maintenance_factor
            
            # Make final classification
            status, confidence, reasoning = self._determine_status(analysis)
            
            analysis["confidence_score"] = confidence
            analysis["reasoning"] = reasoning
            analysis["classified_as"] = status.value
            
            logger.info(f"Classification result: {status.value} (confidence: {confidence:.2%})")
            logger.debug(f"Reasoning: {' | '.join(reasoning)}")
            
            self.analysis_results[api.id] = analysis
            return status, analysis
        
        except Exception as e:
            logger.error(f"Classification failed for API {api.id}: {str(e)}")
            raise
    
    def _analyze_traffic(self, api: API) -> Dict[str, Any]:
        """
        Analyze traffic patterns to detect zombie status.
        
        Returns:
            Dictionary with traffic analysis results
        """
        result = {
            "has_traffic": False,
            "is_active": False,
            "days_since_traffic": None,
            "threshold_exceeded": False,
            "risk_score_contribution": 0.0,
        }
        
        if api.last_traffic is None:
            # No traffic recorded
            result["days_since_traffic"] = (datetime.utcnow() - api.created_at).days
            result["threshold_exceeded"] = result["days_since_traffic"] > self.config.NO_TRAFFIC_THRESHOLD_DAYS
            result["risk_score_contribution"] = 50.0  # High risk: no traffic at all
            result["is_active"] = False
        else:
            # Has traffic history
            result["has_traffic"] = True
            days_elapsed = (datetime.utcnow() - api.last_traffic).days
            result["days_since_traffic"] = days_elapsed
            
            # Evaluate activity level
            if days_elapsed <= 7:
                result["is_active"] = True
                result["risk_score_contribution"] = 0.0  # Daily/weekly activity
            elif days_elapsed <= 30:
                result["is_active"] = True
                result["risk_score_contribution"] = 10.0  # Monthly activity
            elif days_elapsed <= self.config.NO_TRAFFIC_THRESHOLD_DAYS:
                result["is_active"] = False
                result["risk_score_contribution"] = 35.0  # Declining activity
                result["threshold_exceeded"] = False
            else:
                # Exceeded inactivity threshold - ZOMBIE indicator
                result["is_active"] = False
                result["threshold_exceeded"] = True
                result["risk_score_contribution"] = 60.0  # Critical: no traffic > 90 days
        
        return result
    
    def _analyze_documentation(self, api: API) -> Dict[str, Any]:
        """
        Analyze documentation status.
        
        Undocumented APIs are harder to maintain and more likely to become zombie.
        
        Returns:
            Dictionary with documentation analysis
        """
        result = {
            "is_documented": api.is_documented,
            "risk_score_contribution": 0.0,
        }
        
        if not api.is_documented:
            result["risk_score_contribution"] = 25.0  # Undocumented = harder to maintain
        else:
            result["risk_score_contribution"] = 0.0  # Documented = lower risk
        
        return result
    
    def _analyze_ownership(self, api: API) -> Dict[str, Any]:
        """
        Analyze ownership and accountability.
        
        Orphaned APIs (no owner) are classic zombies.
        
        Returns:
            Dictionary with ownership analysis
        """
        result = {
            "has_owner": api.owner is not None and api.owner != "",
            "owner": api.owner,
            "risk_score_contribution": 0.0,
        }
        
        if not result["has_owner"]:
            result["risk_score_contribution"] = 30.0  # Orphaned = zombie risk
        else:
            result["risk_score_contribution"] = 0.0  # Owned = responsibility assigned
        
        return result
    
    def _analyze_age_and_deprecation(self, api: API) -> Dict[str, Any]:
        """
        Analyze API age and deprecation status.
        
        Returns:
            Dictionary with age/deprecation analysis
        """
        age_days = (datetime.utcnow() - api.created_at).days
        is_new = age_days <= self.config.NEW_API_THRESHOLD_DAYS
        
        result = {
            "age_days": age_days,
            "is_new_api": is_new,
            "status_field": api.status,
            "is_explicitly_deprecated": api.status == "deprecated",
            "risk_score_contribution": 0.0,
        }
        
        if api.status == "deprecated":
            # Explicitly marked deprecated - expect decommissioning
            result["risk_score_contribution"] = 20.0  # Medium risk: planned for removal
        elif is_new:
            # New APIs should be maintained
            result["risk_score_contribution"] = 0.0
        elif age_days > 365:
            # Very old APIs need validation
            result["risk_score_contribution"] = 10.0
        
        return result
    
    def _analyze_maintenance(self, api: API) -> Dict[str, Any]:
        """
        Analyze maintenance indicators via tech stack analysis.
        
        Returns:
            Dictionary with maintenance analysis
        """
        result = {
            "tech_stack": api.tech_stack,
            "has_tech_info": api.tech_stack is not None and api.tech_stack != "" and api.tech_stack != "Unknown",
            "risk_score_contribution": 0.0,
        }
        
        if result["has_tech_info"]:
            # Known tech stack suggests maintained
            result["risk_score_contribution"] = 0.0
        else:
            # Unknown/missing tech info suggests neglect
            result["risk_score_contribution"] = 15.0
        
        return result
    
    def _determine_status(self, analysis: Dict[str, Any]) -> Tuple[APIStatus, float, list]:
        """
        Determine final API status based on multi-factor analysis.
        
        Returns:
            Tuple of (status, confidence_score, reasoning_list)
        """
        factors = analysis["factors"]
        reasoning = []
        
        # Calculate aggregate risk score
        total_risk = sum(
            factors.get(factor_name, {}).get("risk_score_contribution", 0.0)
            for factor_name in factors.keys()
        )
        
        # Normalize to 0-100 scale
        max_possible_risk = 210.0  # 50+25+30+20+15 worst case
        normalized_risk = min(100.0, (total_risk / max_possible_risk) * 100)
        
        # Rule 1: Explicitly Deprecated
        if factors["age_deprecation"]["is_explicitly_deprecated"]:
            reasoning.append("API is explicitly marked as DEPRECATED")
            return APIStatus.DEPRECATED, 0.95, reasoning
        
        # Rule 2: Orphaned (no owner + undocumented)
        if not factors["ownership"]["has_owner"] and not factors["documentation"]["is_documented"]:
            reasoning.append("API is orphaned (no owner + undocumented)")
            return APIStatus.ORPHANED, 0.90, reasoning
        
        # Rule 3: Zombie - No traffic > 90 days
        if factors["traffic"]["threshold_exceeded"]:
            reasoning.append(f"No traffic for {factors['traffic']['days_since_traffic']} days (threshold: {self.config.NO_TRAFFIC_THRESHOLD_DAYS})")
            
            # Additional zombie indicators
            if not factors["documentation"]["is_documented"]:
                reasoning.append("API is undocumented (harder to maintain)")
            if not factors["ownership"]["has_owner"]:
                reasoning.append("API has no owner (no accountability)")
            
            return APIStatus.ZOMBIE, 0.92, reasoning
        
        # Rule 4: Zombie - Cluster of risk factors
        if normalized_risk >= 70:
            reasoning.append(f"Multiple zombie indicators detected (risk score: {normalized_risk:.1f})")
            if factors["traffic"]["days_since_traffic"] and factors["traffic"]["days_since_traffic"] > 60:
                reasoning.append(f"High inactivity: {factors['traffic']['days_since_traffic']} days since last traffic")
            if not factors["documentation"]["is_documented"]:
                reasoning.append("API is undocumented")
            if not factors["ownership"]["has_owner"]:
                reasoning.append("API has no owner assigned")
            
            return APIStatus.ZOMBIE, 0.85, reasoning
        
        # Rule 5: Active - Recent traffic and documented
        if factors["traffic"]["is_active"]:
            reasoning.append("API has recent traffic activity")
            if factors["documentation"]["is_documented"]:
                reasoning.append("API is documented")
            if factors["ownership"]["has_owner"]:
                reasoning.append("API has assigned owner")
            
            return APIStatus.ACTIVE, 0.90, reasoning
        
        # Default: Active (conservative approach)
        reasoning.append("Not enough data to classify as zombie/orphaned/deprecated")
        return APIStatus.ACTIVE, 0.60, reasoning


def classify_api(api: API) -> Tuple[APIStatus, Dict[str, Any]]:
    """
    Convenience function to classify a single API.
    
    Args:
        api: API database model
    
    Returns:
        Tuple of (status, analysis_details)
    """
    classifier = ZombieClassifier()
    return classifier.classify(api)
