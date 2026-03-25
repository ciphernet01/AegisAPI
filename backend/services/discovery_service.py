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
import os
import yaml
import json
import re
from github import Github, GithubException

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
        - Swagger/OpenAPI files (swagger.yaml, openapi.json)
        - API route definitions (Python Flask/FastAPI, Node Express, Java Spring)
        - README documentation with API endpoints
        
        Args:
            org: GitHub organization to scan (from config if None)
        
        Returns:
            int: Number of new APIs discovered
        """
        logger.info(f"Starting GitHub API discovery...")
        
        try:
            # Get GitHub token from environment
            github_token = os.getenv("GITHUB_TOKEN")
            if not github_token:
                logger.warning("GITHUB_TOKEN not set - using public API (rate limited)")
                g = Github()
            else:
                g = Github(github_token)
            
            # Organization to scan (from config or parameter)
            org_name = org or os.getenv("GITHUB_ORG", "ciphernet01")
            
            try:
                organization = g.get_organization(org_name)
                logger.info(f"Scanning organization: {org_name}")
            except GithubException as e:
                logger.error(f"Failed to access organization {org_name}: {str(e)}")
                return 0
            
            new_apis_count = 0
            
            # Scan all repositories in organization
            for repo in organization.get_repos(type="all"):
                logger.info(f"Scanning repository: {repo.name}")
                
                try:
                    # Strategy 1: Look for OpenAPI/Swagger specs
                    spec_apis = self._scan_openapi_specs(repo)
                    new_apis_count += self._store_discovered_apis(spec_apis)
                    
                    # Strategy 2: Parse code for route definitions
                    code_apis = self._scan_code_routes(repo)
                    new_apis_count += self._store_discovered_apis(code_apis)
                    
                except Exception as e:
                    logger.warning(f"Error scanning {repo.name}: {str(e)}")
                    continue
            
            logger.info(f"GitHub discovery complete: {new_apis_count} new APIs found")
            return new_apis_count
            
        except Exception as e:
            logger.error(f"GitHub discovery failed: {str(e)}")
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
    
    def _scan_openapi_specs(self, repo) -> List[Dict[str, Any]]:
        """
        Search repository for OpenAPI/Swagger specification files.
        
        Looks for: swagger.yaml, swagger.json, openapi.yaml, openapi.json
        
        Args:
            repo: GitHub repository object
        
        Returns:
            List of discovered APIs from specs
        """
        apis = []
        spec_files = ["swagger.yaml", "swagger.json", "openapi.yaml", "openapi.json", "openapi.yml"]
        
        try:
            for filename in spec_files:
                try:
                    file = repo.get_contents(filename)
                    
                    # Parse YAML or JSON spec
                    if filename.endswith("json"):
                        spec = json.loads(file.decoded_content)
                    else:
                        spec = yaml.safe_load(file.decoded_content)
                    
                    # Extract APIs from spec
                    if "paths" in spec:
                        for path, methods in spec["paths"].items():
                            for method in methods:
                                if method.upper() in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
                                    api = {
                                        "name": spec.get("info", {}).get("title", repo.name),
                                        "endpoint": path,
                                        "method": method.upper(),
                                        "owner": repo.owner.login,
                                        "tech_stack": self._detect_tech_stack(repo),
                                        "status": "active",
                                        "is_documented": True,
                                        "risk_score": 0.0,
                                        "source_url": repo.html_url,
                                        "source_file": filename,
                                    }
                                    apis.append(api)
                    
                    logger.info(f"Found {len(apis)} APIs in {repo.name}/{filename}")
                    
                except Exception as e:
                    logger.debug(f"File not found or parse error: {filename} in {repo.name}")
        
        except Exception as e:
            logger.error(f"OpenAPI scan failed for {repo.name}: {str(e)}")
        
        return apis
    
    def _scan_code_routes(self, repo) -> List[Dict[str, Any]]:
        """
        Scan code files for API route definitions.
        
        Detects routes in:
        - Python: Flask (@app.route), FastAPI (@app.get), Django (urls.py)
        - JavaScript: Express (app.get), Fastify (fastify.get)
        - Java: Spring (@GetMapping, @PostMapping)
        
        Args:
            repo: GitHub repository object
        
        Returns:
            List of discovered APIs from code
        """
        apis = []
        
        try:
            # Search for route files in repo
            try:
                contents = repo.get_contents("")
                route_files = self._find_route_files(repo, contents)
                
                for file_path in route_files[:10]:  # Limit to first 10 files
                    try:
                        file = repo.get_contents(file_path)
                        content = file.decoded_content.decode("utf-8", errors="ignore")
                        
                        # Detect tech stack and extract routes
                        for route in self._extract_routes_from_content(content, file_path):
                            route["owner"] = repo.owner.login
                            route["tech_stack"] = self._detect_tech_stack(repo)
                            route["status"] = "active"
                            route["is_documented"] = False
                            route["risk_score"] = 45.0  # Higher risk for undocumented
                            route["source_url"] = repo.html_url
                            route["source_file"] = file_path
                            apis.append(route)
                    
                    except Exception as e:
                        logger.debug(f"Could not parse {file_path}")
            
            except Exception as e:
                logger.debug(f"Could not list contents for {repo.name}")
            
            logger.info(f"Found {len(apis)} APIs from code in {repo.name}")
            
        except Exception as e:
            logger.error(f"Code scan failed for {repo.name}: {str(e)}")
        
        return apis
    
    def _find_route_files(self, repo, contents, path="") -> List[str]:
        """
        Recursively find files likely to contain API route definitions.
        
        Returns:
            List of file paths
        """
        route_files = []
        route_indicators = ["route", "handler", "api", "controller", "endpoint", "server"]
        
        try:
            for item in contents:
                # Skip binary files and vendor directories
                if item.name in [".git", "node_modules", ".venv", "venv", "__pycache__"]:
                    continue
                
                # Check files
                if item.type == "file":
                    if any(indicator in item.name.lower() for indicator in route_indicators):
                        route_files.append(item.path)
                    elif item.name in ["main.py", "app.py", "server.py", "index.js", "app.js", "main.java"]:
                        route_files.append(item.path)
                
                # Recursively search directories (limit depth)
                elif item.type == "dir" and len(route_files) < 5:
                    if item.name not in [".git", "node_modules", ".venv", "venv", "__pycache__", "build", "dist"]:
                        try:
                            sub_contents = repo.get_contents(item.path)
                            route_files.extend(self._find_route_files(repo, sub_contents, item.path)[:3])
                        except:
                            pass
        
        except Exception as e:
            logger.debug(f"Directory scanning error: {str(e)}")
        
        return route_files
    
    def _extract_routes_from_content(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """
        Extract API routes from source code content.
        
        Args:
            content: File content as string
            file_path: Path to the file
        
        Returns:
            List of extracted route definitions
        """
        routes = []
        
        # Pattern for Python Flask/FastAPI
        if file_path.endswith(".py"):
            patterns = [
                (r"@(?:app|router|blueprint)\.(\w+)\s*\(\s*['\"]([^'\"]+)['\"]", "method"),
                (r"@(?:router|app)\.(\w+)\s*\(\s*['\"]([^'\"]+)['\"]", "method"),
            ]
            
            for pattern, _ in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    routes.append({
                        "name": f"{file_path.split('/')[-1]}-{match.group(2).replace('/', '-')}",
                        "endpoint": match.group(2),
                        "method": match.group(1).upper(),
                    })
        
        # Pattern for JavaScript Express
        elif file_path.endswith(".js"):
            patterns = [
                (r"(?:app|router)\.(\w+)\s*\(\s*['\"]([^'\"]+)['\"]", "method"),
                (r"fastify\.(\w+)\s*\(\s*['\"]([^'\"]+)['\"]", "method"),
            ]
            
            for pattern, _ in patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    routes.append({
                        "name": f"{file_path.split('/')[-1]}-{match.group(2).replace('/', '-')}",
                        "endpoint": match.group(2),
                        "method": match.group(1).upper(),
                    })
        
        # Pattern for Java Spring
        elif file_path.endswith(".java"):
            patterns = [
                (r"@(\w*Mapping)\s*\(\s*['\"]?([^'\"\\)]+)['\"]?", "annotation"),
            ]
            
            for pattern, _ in patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    mapping_type = match.group(1)
                    endpoint = match.group(2)
                    method = mapping_type.replace("Mapping", "").upper() or "GET"
                    
                    routes.append({
                        "name": f"{file_path.split('/')[-1]}-{endpoint.replace('/', '-')}",
                        "endpoint": endpoint,
                        "method": method,
                    })
        
        return routes
    
    def _detect_tech_stack(self, repo) -> str:
        """
        Detect technology stack from repository languages and files.
        
        Args:
            repo: GitHub repository object
        
        Returns:
            String describing the tech stack
        """
        tech_stack = []
        
        # Check primary language
        if repo.language:
            tech_stack.append(repo.language)
        
        # Check for common framework files
        try:
            # Python frameworks
            contents = repo.get_contents("requirements.txt")
            req_content = contents.decoded_content.decode("utf-8", errors="ignore").lower()
            if "fastapi" in req_content:
                tech_stack.append("FastAPI")
            elif "flask" in req_content:
                tech_stack.append("Flask")
            elif "django" in req_content:
                tech_stack.append("Django")
        except:
            pass
        
        try:
            # Node.js frameworks
            package_json_content = repo.get_contents("package.json")
            package_json = json.loads(package_json_content.decoded_content)
            deps = package_json.get("dependencies", {})
            if "express" in deps:
                tech_stack.append("Express")
            elif "fastify" in deps:
                tech_stack.append("Fastify")
        except:
            pass
        
        return "/".join(tech_stack) if tech_stack else "Unknown"
    
    def _store_discovered_apis(self, apis: List[Dict[str, Any]]) -> int:
        """
        Store discovered APIs in database, avoiding duplicates.
        
        Args:
            apis: List of API dictionaries to store
        
        Returns:
            int: Number of new APIs added
        """
        new_count = 0
        
        for api_data in apis:
            try:
                # Check if API already exists (by endpoint + method + owner)
                existing = self.db.query(API).filter(
                    API.endpoint == api_data.get("endpoint"),
                    API.method == api_data.get("method"),
                    API.owner == api_data.get("owner")
                ).first()
                
                if existing:
                    logger.debug(f"API already exists: {api_data['endpoint']}")
                    continue
                
                # Create new API record
                api = API(
                    name=api_data.get("name", "Unknown"),
                    endpoint=api_data.get("endpoint", ""),
                    method=api_data.get("method", "GET"),
                    owner=api_data.get("owner", "Unknown"),
                    tech_stack=api_data.get("tech_stack", "Unknown"),
                    status=api_data.get("status", "active"),
                    risk_score=api_data.get("risk_score", 50.0),
                    is_documented=api_data.get("is_documented", False),
                    created_at=datetime.utcnow(),
                )
                
                self.db.add(api)
                new_count += 1
            
            except Exception as e:
                logger.error(f"Failed to store API {api_data.get('name')}: {str(e)}")
        
        try:
            if new_count > 0:
                self.db.commit()
                logger.info(f"Stored {new_count} new APIs in database")
        except Exception as e:
            logger.error(f"Database commit failed: {str(e)}")
            self.db.rollback()
        
        return new_count
    
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
