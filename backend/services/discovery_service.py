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

# Import security modules
try:
    from security import classify_api, calculate_risk_score, APIStatus
except ImportError:
    # Fallback if imported from a different context
    from ..security import classify_api, calculate_risk_score, APIStatus
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
        Scan Docker registry and local Docker daemon for API services.
        
        Looks for services that appear to be APIs based on:
        - Image names matching patterns (api-, service-, backend-, -api, -server)
        - Port exposure patterns (common API ports: 3000, 5000, 8000, 8080, 9000)
        - Labels in image metadata (com.example.api=true, service.type=api)
        - Environment variables and configurations
        
        Args:
            registry: Docker registry URL (Docker Hub if None)
        
        Returns:
            int: Number of new APIs discovered
        """
        logger.info(f"Starting Docker API discovery...")
        
        try:
            new_apis_count = 0
            
            # Strategy 1: Scan local Docker daemon for running containers
            local_apis = self._scan_local_docker()
            new_apis_count += self._store_discovered_apis(local_apis)
            
            # Strategy 2: Scan Docker registry (requires registry token if private)
            registry_url = registry or os.getenv("DOCKER_REGISTRY", "https://registry-1.docker.io")
            registry_apis = self._scan_docker_registry(registry_url)
            new_apis_count += self._store_discovered_apis(registry_apis)
            
            logger.info(f"Docker discovery complete: {new_apis_count} new APIs found")
            return new_apis_count
            
        except Exception as e:
            logger.error(f"Docker discovery failed: {str(e)}")
            return 0
    
    def _scan_local_docker(self) -> List[Dict[str, Any]]:
        """
        Scan local Docker daemon for running API services.
        
        Examines:
        - Running containers
        - Exposed ports
        - Environment variables
        - Container labels
        - Image metadata
        
        Returns:
            List of discovered APIs from local Docker
        """
        apis = []
        
        try:
            import docker
            from docker.errors import DockerException
            
            # Connect to local Docker daemon
            try:
                client = docker.from_env()
                client.ping()
            except DockerException as e:
                logger.warning(f"Cannot connect to Docker daemon: {str(e)}")
                return apis
            
            logger.info("Scanning local Docker daemon...")
            
            # Get list of running containers
            try:
                containers = client.containers.list()
                
                for container in containers:
                    try:
                        # Extract API information from container
                        api_info = self._extract_api_from_container(container)
                        
                        if api_info:
                            apis.append(api_info)
                            logger.debug(f"Found API service: {api_info['name']}")
                    
                    except Exception as e:
                        logger.debug(f"Could not extract API from container {container.name}: {str(e)}")
            
            except Exception as e:
                logger.error(f"Failed to list containers: {str(e)}")
            
            logger.info(f"Found {len(apis)} APIs in local Docker")
            
        except ImportError:
            logger.warning("docker package not installed - skipping local Docker scan")
        
        except Exception as e:
            logger.error(f"Local Docker scan failed: {str(e)}")
        
        return apis
    
    def _scan_docker_registry(self, registry_url: str) -> List[Dict[str, Any]]:
        """
        Scan Docker registry (Docker Hub or private) for API service images.
        
        Searches for repositories that match API patterns:
        - Name contains 'api', 'service', 'backend', 'gateway', 'server'
        - Description mentions APIs
        - Recent activity (likely in use)
        
        Args:
            registry_url: Docker registry URL
        
        Returns:
            List of discovered APIs from registry
        """
        apis = []
        
        try:
            import requests
            
            logger.info(f"Scanning Docker registry: {registry_url}")
            
            # Popular API service image patterns to check
            search_terms = ["api", "service", "gateway", "backend", "server"]
            
            for term in search_terms:
                try:
                    # Query Docker Hub API for repositories
                    search_url = f"https://hub.docker.com/v2/repositories/search?query={term}&page_size=20"
                    response = requests.get(search_url, timeout=10)
                    
                    if response.status_code == 200:
                        results = response.json()
                        
                        for repo in results.get("results", []):
                            try:
                                api_info = {
                                    "name": repo.get("repo_name", "unknown"),
                                    "endpoint": f"docker://{repo.get('repo_name')}",
                                    "method": "DOCKER",
                                    "owner": repo.get("repo_user", "docker-hub"),
                                    "tech_stack": "Docker/Container",
                                    "status": "active" if repo.get("is_private") == False else "private",
                                    "is_documented": True if repo.get("description") else False,
                                    "is_documented": True if repo.get("description") else False,
                                    "risk_score": 0.0, # Will be calculated below
                                    "source_url": f"https://hub.docker.com/r/{repo.get('repo_name')}",
                                    "source_url": f"https://hub.docker.com/r/{repo.get('repo_name')}",
                                    "source_file": "Dockerfile",
                                }
                                
                                api_info["name"] = f"{repo.get('repo_name').split('/')[-1]}-image"
                                apis.append(api_info)
                            
                            except Exception as e:
                                logger.debug(f"Could not parse registry image: {str(e)}")
                
                except Exception as e:
                    logger.debug(f"Registry search failed for term '{term}': {str(e)}")
            
            logger.info(f"Found {len(apis)} APIs in registry")
            
        except ImportError:
            logger.warning("requests package not installed - skipping registry scan")
        
        except Exception as e:
            logger.error(f"Registry scan failed: {str(e)}")
        
        return apis
    
    def _extract_api_from_container(self, container) -> Optional[Dict[str, Any]]:
        """
        Extract API information from a Docker container.
        
        Analyzes:
        - Container name and image
        - Exposed ports
        - Environment variables
        - Labels and metadata
        
        Args:
            container: Docker container object
        
        Returns:
            API information dict or None if not an API service
        """
        try:
            # API service indicators
            api_indicators = ["api", "service", "backend", "gateway", "server", "rest", "http"]
            
            container_name = container.name.lower()
            image_name = container.image.tags[0].lower() if container.image.tags else ""
            
            # Check if this looks like an API service
            is_api_service = any(
                indicator in container_name or indicator in image_name 
                for indicator in api_indicators
            )
            
            if not is_api_service:
                # Check labels
                labels = container.labels or {}
                if not any(
                    "api" in str(k).lower() or "api" in str(v).lower()
                    for k, v in labels.items()
                ):
                    return None
            
            # Extract port information
            ports = container.ports or {}
            exposed_endpoints = []
            
            api_port_patterns = [3000, 5000, 8000, 8080, 9000, 9090, 3001, 5001, 8001, 8081]
            
            for port_spec, mappings in ports.items():
                if mappings:
                    port_num = int(port_spec.split('/')[0])
                    if port_num in api_port_patterns:
                        exposed_endpoints.append(f":{port_num}")
            
            # If no common API ports, try to infer from any exposed port
            if not exposed_endpoints and ports:
                exposed_endpoints = [f":{int(port_spec.split('/')[0])}" for port_spec in ports.keys()][:3]
            
            if not exposed_endpoints:
                return None  # No ports exposed, likely not an API
            
            # Get environment variables for tech stack hints
            env_vars = container.attrs.get("Config", {}).get("Env", []) or []
            tech_stack = self._detect_tech_from_env(env_vars, image_name)
            
            return {
                "name": container.name,
                "endpoint": f"docker://{image_name}",
                "method": "DOCKER",
                "owner": container.attrs.get("Config", {}).get("User", "root"),
                "tech_stack": tech_stack,
                "status": "active",
                "is_documented": False,
                "is_documented": False,
                "risk_score": 0.0, # Will be calculated below
                "source_url": f"container://{container.id[:12]}",
                "source_url": f"container://{container.id[:12]}",
                "source_file": "docker-compose or container config",
            }
        
        except Exception as e:
            logger.debug(f"Could not extract API from container: {str(e)}")
            return None
    
    def _detect_tech_from_env(self, env_vars: List[str], image_name: str) -> str:
        """
        Detect technology stack from environment variables and image name.
        
        Args:
            env_vars: List of environment variables
            image_name: Docker image name
        
        Returns:
            Technology stack string
        """
        tech_stack = []
        
        # Check image name for common frameworks
        image_lower = image_name.lower()
        
        if "node" in image_lower or "npm" in image_lower:
            tech_stack.append("Node.js")
            if "express" in image_lower:
                tech_stack.append("Express")
            elif "fastify" in image_lower:
                tech_stack.append("Fastify")
        
        elif "python" in image_lower or "flask" in image_lower or "django" in image_lower:
            tech_stack.append("Python")
            if "fastapi" in image_lower:
                tech_stack.append("FastAPI")
            elif "flask" in image_lower:
                tech_stack.append("Flask")
            elif "django" in image_lower:
                tech_stack.append("Django")
        
        elif "java" in image_lower or "spring" in image_lower:
            tech_stack.append("Java")
            if "spring" in image_lower:
                tech_stack.append("Spring Boot")
        
        elif "rust" in image_lower:
            tech_stack.append("Rust")
        
        elif "golang" in image_lower or "go:" in image_lower:
            tech_stack.append("Go")
        
        # Check environment variables for additional clues
        env_str = " ".join(env_vars).lower()
        
        if "fastapi" in env_str:
            if "FastAPI" not in tech_stack:
                tech_stack.append("FastAPI")
        if "flask" in env_str:
            if "Flask" not in tech_stack:
                tech_stack.append("Flask")
        if "express" in env_str:
            if "Express" not in tech_stack:
                tech_stack.append("Express")
        
        return "/".join(tech_stack) if tech_stack else "Container"
    
    def _parse_dockerfile(self, dockerfile_content: str) -> Dict[str, Any]:
        """
        Parse Dockerfile to understand service capabilities.
        
        Extracts:
        - Base image (tech stack)
        - Exposed ports
        - Environment variables
        - Health checks
        
        Args:
            dockerfile_content: Raw Dockerfile content
        
        Returns:
            Dictionary with parsed information
        """
        info = {
            "base_image": None,
            "exposed_ports": [],
            "environment": {},
            "health_check": False,
        }
        
        try:
            for line in dockerfile_content.split('\n'):
                line = line.strip()
                
                if line.startswith("FROM"):
                    info["base_image"] = line.replace("FROM", "").strip()
                
                elif line.startswith("EXPOSE"):
                    ports_str = line.replace("EXPOSE", "").strip()
                    ports = [int(p.split('/')[0]) for p in ports_str.split() if p.isdigit()]
                    info["exposed_ports"].extend(ports)
                
                elif line.startswith("ENV"):
                    env_str = line.replace("ENV", "").strip()
                    if "=" in env_str:
                        key, val = env_str.split("=", 1)
                        info["environment"][key.strip()] = val.strip()
                
                elif line.startswith("HEALTHCHECK"):
                    info["health_check"] = True
        
        except Exception as e:
            logger.debug(f"Error parsing Dockerfile: {str(e)}")
        
        return info
    
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
                            route["is_documented"] = False
                            route["risk_score"] = 0.0 # Will be calculated below
                            route["source_url"] = repo.html_url
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
                
                # Perform security assessment and classification
                status_obj = classify_api(api_data)
                risk_score = calculate_risk_score(api_data)
                
                # Create new API record
                api = API(
                    name=api_data.get("name", "Unknown"),
                    endpoint=api_data.get("endpoint", ""),
                    method=api_data.get("method", "GET"),
                    owner=api_data.get("owner", "Unknown"),
                    tech_stack=api_data.get("tech_stack", "Unknown"),
                    status=status_obj.value if hasattr(status_obj, 'value') else status_obj,
                    risk_score=float(risk_score),
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
