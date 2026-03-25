"""
Risk Scoring Model

This module provides a function to calculate a risk score for an API based on its security assessment and metadata.
"""
from typing import Dict, Any

def calculate_risk_score(api_metadata: Dict[str, Any]) -> int:
    """
    Calculate a risk score for an API. Higher score = higher risk.
    Args:
        api_metadata: Dict with assessment results and metadata.
    Returns:
        int: Risk score (0-100)
    """
    score = 0
    # No authentication: +30
    if not api_metadata.get("authentication", False):
        score += 30
    # No encryption: +25
    if not api_metadata.get("encryption", False):
        score += 25
    # No rate limiting: +15
    if not api_metadata.get("rate_limiting", False):
        score += 15
    # Sensitive data exposure: +20
    if api_metadata.get("sensitive_data_exposed", False):
        score += 20
    # Zombie or orphaned APIs: +10
    if api_metadata.get("status") in ("zombie", "orphaned"):
        score += 10
    return min(score, 100)
