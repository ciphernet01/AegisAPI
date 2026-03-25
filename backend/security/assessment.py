"""
Security Assessment Checks

This module provides functions to assess API security posture:
- Authentication enforcement
- Encryption (TLS/HTTPS)
- Rate limiting
- Sensitive data exposure
"""
from typing import Dict, Any

def check_authentication(api_metadata: Dict[str, Any]) -> bool:
    """Returns True if authentication is enforced."""
    return api_metadata.get("authentication", False)

def check_encryption(api_metadata: Dict[str, Any]) -> bool:
    """Returns True if API uses HTTPS/TLS encryption."""
    return api_metadata.get("encryption", False)

def check_rate_limiting(api_metadata: Dict[str, Any]) -> bool:
    """Returns True if rate limiting is enabled."""
    return api_metadata.get("rate_limiting", False)

def check_sensitive_data_exposure(api_metadata: Dict[str, Any]) -> bool:
    """Returns True if sensitive data is exposed (should be False for secure APIs)."""
    return api_metadata.get("sensitive_data_exposed", False)
