"""
API Discovery Service - finds all APIs across the infrastructure.

Orchestrates scanning from multiple sources:
- GitHub repositories
- Docker registries
- Kubernetes clusters
- AWS API Gateways
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from database.models import API
from sqlalchemy.orm import Session
from utils.logger import get_logger

logger = get_logger(__name__)


class APIDiscoveryService:
    """
    Main discovery orchestrator.
    
    Coordinates scanning from multiple sources and stores results in database.
    """
    
    def __init__(self, db: Session):
        """
        Initialize discovery service with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
    
    def discover_all_apis(self) -> Dict[str, Any]:
        """
        Run comprehensive API discovery from all sources.
        
        Must meet user requirements for finding:
        - Documented APIs (Swagger/OpenAPI)
        - Code-based APIs (Express, Flask, Spring Boot)
        - Undocumented APIs (Shadow APIs)
        - Containerized APIs (Docker)
        
        Returns:
            dict: Discovery results with counts and details
        """
        logger.info("Starting comprehensive API discovery...")
        
        results = {
            "timestamp": datetime.utcnow().isoformat(),
            "sources": {
                "github": 0,
                "docker": 0,
                "kubernetes": 0,
                "aws_api_gateway": 0,
            },
            "total_discovered": 0,
            "new_apis": 0,
            "duplicates_removed": 0,
        }
        
        try:
            # TODO: Implement GitHub scanning
            # results["sources"]["github"] = self.discover_from_github()
            
            # TODO: Implement Docker scanning
            # results["sources"]["docker"] = self.discover_from_docker()
            
            # TODO: Implement Kubernetes scanning
            # results["sources"]["kubernetes"] = self.discover_from_kubernetes()
            
            # TODO: Implement AWS API Gateway scanning
            # results["sources"]["aws"] = self.discover_from_aws()
            
            logger.info(f"Discovery complete: {results}")
            return results
        
        except Exception as e:
            logger.error(f"Discovery failed: {str(e)}")
            raise
    
    def discover_from_github(self, org: str = None) -> int:
        """
        Scan GitHub repositories for APIs.
        
        Looks for:
        - Swagger/OpenAPI files
        - API route definitions
        - README documentation
        
        Args:
            org: GitHub organization to scan (from config if None)
        
        Returns:
            int: Number of new APIs discovered
        """
        logger.info(f"Scanning GitHub organization: {org}")
        # TODO: Implement GitHub API scanning
        return 0
    
    def discover_from_docker(self, registry: str = None) -> int:
        """
        Scan Docker registry for API service images.
        
        Looks for services that appear to be APIs based on:
        - Image names (api-, service-, backend-)
        - Labels in image metadata
        - Port exposure patterns
        
        Args:
            registry: Docker registry URL
        
        Returns:
            int: Number of new APIs discovered
        """
        logger.info(f"Scanning Docker registry: {registry}")
        # TODO: Implement Docker registry scanning
        return 0
    
    def get_all_discovered_apis(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Retrieve all discovered APIs from database.
        
        Args:
            limit: Maximum number to return
            offset: Pagination offset
        
        Returns:
            List of API dictionaries
        """
        try:
            apis = self.db.query(API).limit(limit).offset(offset).all()
            return [self._api_to_dict(api) for api in apis]
        except Exception as e:
            logger.error(f"Failed to retrieve APIs: {str(e)}")
            return []
    
    def get_api_by_id(self, api_id: int) -> Optional[Dict[str, Any]]:
        """
        Get single API by ID.
        
        Args:
            api_id: API primary key
        
        Returns:
            API dictionary or None if not found
        """
        try:
            api = self.db.query(API).filter(API.id == api_id).first()
            return self._api_to_dict(api) if api else None
        except Exception as e:
            logger.error(f"Failed to retrieve API {api_id}: {str(e)}")
            return None
    
    def search_apis(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Full-text search across API names, endpoints, owners.
        
        Args:
            query: Search query string
            limit: Max results
        
        Returns:
            List of matching APIs
        """
        try:
            # Simple text search (upgrade to PostgreSQL FTS later)
            apis = self.db.query(API).filter(
                (API.name.ilike(f"%{query}%")) |
                (API.endpoint.ilike(f"%{query}%")) |
                (API.owner.ilike(f"%{query}%"))
            ).limit(limit).all()
            
            return [self._api_to_dict(api) for api in apis]
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get discovery and API statistics.
        
        Returns:
            dict with counts by status, tech stack, etc.
        """
        try:
            total = self.db.query(API).count()
            active = self.db.query(API).filter(API.status == "active").count()
            deprecated = self.db.query(API).filter(API.status == "deprecated").count()
            orphaned = self.db.query(API).filter(API.status == "orphaned").count()
            zombie = self.db.query(API).filter(API.status == "zombie").count()
            
            documented = self.db.query(API).filter(API.is_documented == True).count()
            
            return {
                "total_apis": total,
                "by_status": {
                    "active": active,
                    "deprecated": deprecated,
                    "orphaned": orphaned,
                    "zombie": zombie,
                },
                "documented": documented,
                "undocumented": total - documented,
            }
        except Exception as e:
            logger.error(f"Statistics failed: {str(e)}")
            return {}
    
    @staticmethod
    def _api_to_dict(api: API) -> Dict[str, Any]:
        """
        Convert API ORM model to dictionary.
        
        Args:
            api: API model instance
        
        Returns:
            Dictionary representation
        """
        if not api:
            return None
        
        return {
            "id": api.id,
            "name": api.name,
            "endpoint": api.endpoint,
            "method": api.method,
            "owner": api.owner,
            "tech_stack": api.tech_stack,
            "status": api.status,
            "risk_score": api.risk_score,
            "is_documented": api.is_documented,
            "created_at": api.created_at.isoformat() if api.created_at else None,
            "last_traffic": api.last_traffic.isoformat() if api.last_traffic else None,
        }
