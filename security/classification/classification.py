"""
API Classification Logic

This module provides functions to classify APIs as active, deprecated, orphaned, or zombie based on usage and metadata.
"""

from enum import Enum
from typing import Dict, Any

class APIStatus(Enum):
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ORPHANED = "orphaned"
    ZOMBIE = "zombie"

def classify_api(api_metadata: Dict[str, Any]) -> APIStatus:
    """
    Classify an API based on its metadata and usage.
    Args:
        api_metadata: Dict with keys like 'last_used', 'deprecated', 'owner', 'documented', etc.
    Returns:
        APIStatus: Classification of the API.
    """
    if api_metadata.get("deprecated", False):
        return APIStatus.DEPRECATED
    if not api_metadata.get("owner") or not api_metadata.get("documented", True):
        return APIStatus.ORPHANED
    if api_metadata.get("last_used") is None or api_metadata.get("last_used", 0) < api_metadata.get("zombie_threshold", 180):
        return APIStatus.ZOMBIE
    return APIStatus.ACTIVE
