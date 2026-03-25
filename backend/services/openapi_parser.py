"""
OpenAPI/Swagger Specification Parser.

Parses and standardizes OpenAPI 2.0 (Swagger) and OpenAPI 3.0+ specifications.

Extracts:
- API metadata (title, version, description)
- Endpoints (paths, methods, parameters)
- Request/response schemas
- Authentication requirements
- Rate limiting policies
- API versioning information
"""

from typing import List, Dict, Any, Optional, Union
import json
import yaml
from utils.logger import get_logger

logger = get_logger(__name__)


class OpenAPIParser:
    """
    Parse and analyze OpenAPI/Swagger specifications.
    
    Supports:
    - OpenAPI 3.0.0+
    - Swagger 2.0
    - YAML and JSON formats
    """
    
    def __init__(self):
        """Initialize the OpenAPI parser."""
        self.spec = None
        self.spec_version = None
        self.api_info = {}
    
    def parse_spec(self, spec_data: Union[str, Dict]) -> Dict[str, Any]:
        """
        Parse OpenAPI/Swagger specification.
        
        Args:
            spec_data: Raw spec as string (YAML/JSON) or parsed dict
        
        Returns:
            Standardized API specification dict
        """
        try:
            # Parse input format
            if isinstance(spec_data, str):
                spec = self._parse_string(spec_data)
            elif isinstance(spec_data, dict):
                spec = spec_data
            else:
                raise ValueError("Spec must be string or dict")
            
            self.spec = spec
            
            # Detect OpenAPI version
            self.spec_version = self._detect_version(spec)
            logger.info(f"Detected OpenAPI version: {self.spec_version}")
            
            # Parse based on version
            if self.spec_version.startswith("3"):
                return self._parse_openapi3(spec)
            elif self.spec_version.startswith("2"):
                return self._parse_swagger2(spec)
            else:
                raise ValueError(f"Unsupported OpenAPI version: {self.spec_version}")
        
        except Exception as e:
            logger.error(f"Failed to parse spec: {str(e)}")
            raise
    
    def extract_endpoints(self, spec_data: Union[str, Dict]) -> List[Dict[str, Any]]:
        """
        Extract all endpoints from OpenAPI spec.
        
        Returns standardized endpoint format:
        {
            "path": "/api/users/{id}",
            "method": "GET",
            "summary": "Get user by ID",
            "description": "Retrieve a user by their unique identifier",
            "parameters": [...],
            "request_body": {...},
            "responses": {...},
            "auth_required": bool,
            "auth_types": ["bearer", "api_key"],
            "deprecated": bool,
        }
        
        Args:
            spec_data: OpenAPI specification
        
        Returns:
            List of endpoint definitions
        """
        try:
            parsed = self.parse_spec(spec_data)
            return parsed.get("endpoints", [])
        
        except Exception as e:
            logger.error(f"Failed to extract endpoints: {str(e)}")
            return []
    
    def extract_authentication(self, spec_data: Union[str, Dict]) -> Dict[str, Any]:
        """
        Extract authentication requirements from spec.
        
        Returns:
        {
            "auth_required": bool,
            "auth_types": ["bearer", "api_key", "oauth2", "basic"],
            "details": {
                "bearer": {"scheme": "JWT", "format": "bearer <token>"},
                "api_key": {"in": "header", "name": "X-API-Key"},
                ...
            }
        }
        
        Args:
            spec_data: OpenAPI specification
        
        Returns:
            Authentication configuration
        """
        try:
            parsed = self.parse_spec(spec_data)
            return parsed.get("security", {})
        
        except Exception as e:
            logger.error(f"Failed to extract authentication: {str(e)}")
            return {"auth_required": False, "auth_types": []}
    
    def extract_schemas(self, spec_data: Union[str, Dict]) -> Dict[str, Dict[str, Any]]:
        """
        Extract data schemas/models from spec.
        
        Returns:
        {
            "User": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "email": {"type": "string", "format": "email"},
                },
                "required": ["id", "name", "email"],
            },
            ...
        }
        
        Args:
            spec_data: OpenAPI specification
        
        Returns:
            Dictionary of data schemas
        """
        try:
            parsed = self.parse_spec(spec_data)
            return parsed.get("schemas", {})
        
        except Exception as e:
            logger.error(f"Failed to extract schemas: {str(e)}")
            return {}
    
    def extract_rate_limits(self, spec_data: Union[str, Dict]) -> Dict[str, Any]:
        """
        Extract rate limiting information from spec.
        
        Returns:
        {
            "rate_limit_enabled": bool,
            "requests_per_second": int,
            "requests_per_minute": int,
            "requests_per_hour": int,
            "burst_size": int,
            "reset_period": str,
        }
        
        Args:
            spec_data: OpenAPI specification
        
        Returns:
            Rate limiting configuration
        """
        try:
            parsed = self.parse_spec(spec_data)
            return parsed.get("rate_limits", {})
        
        except Exception as e:
            logger.error(f"Failed to extract rate limits: {str(e)}")
            return {"rate_limit_enabled": False}
    
    def _parse_string(self, spec_str: str) -> Dict:
        """
        Parse spec from string (YAML or JSON).
        
        Args:
            spec_str: Spec as string
        
        Returns:
            Parsed spec dict
        """
        # Try JSON first
        try:
            return json.loads(spec_str)
        except json.JSONDecodeError:
            pass
        
        # Try YAML
        try:
            return yaml.safe_load(spec_str)
        except yaml.YAMLError:
            pass
        
        raise ValueError("Could not parse spec as JSON or YAML")
    
    def _detect_version(self, spec: Dict) -> str:
        """
        Detect OpenAPI/Swagger version.
        
        Args:
            spec: Parsed spec dict
        
        Returns:
            Version string (e.g., "3.0.0", "2.0")
        """
        if "openapi" in spec:
            return spec["openapi"]
        elif "swagger" in spec:
            return spec["swagger"]
        else:
            raise ValueError("Could not detect API specification version")
    
    def _parse_openapi3(self, spec: Dict) -> Dict[str, Any]:
        """
        Parse OpenAPI 3.0+ specification.
        
        Args:
            spec: OpenAPI 3.0+ spec
        
        Returns:
            Standardized spec dict
        """
        logger.info("Parsing OpenAPI 3.0+ specification...")
        
        result = {
            "version": spec.get("openapi", "3.0.0"),
            "title": spec.get("info", {}).get("title", "Unknown API"),
            "description": spec.get("info", {}).get("description", ""),
            "api_version": spec.get("info", {}).get("version", "1.0.0"),
            "base_url": self._extract_base_url_oas3(spec),
            "endpoints": [],
            "schemas": {},
            "security": self._extract_security_oas3(spec),
            "rate_limits": self._extract_rate_limits_oas3(spec),
            "contact": spec.get("info", {}).get("contact", {}),
            "license": spec.get("info", {}).get("license", {}),
        }
        
        # Extract schemas
        if "components" in spec and "schemas" in spec["components"]:
            result["schemas"] = spec["components"]["schemas"]
        
        # Extract endpoints
        if "paths" in spec:
            result["endpoints"] = self._extract_endpoints_oas3(spec["paths"], spec)
        
        return result
    
    def _parse_swagger2(self, spec: Dict) -> Dict[str, Any]:
        """
        Parse Swagger 2.0 specification.
        
        Args:
            spec: Swagger 2.0 spec
        
        Returns:
            Standardized spec dict
        """
        logger.info("Parsing Swagger 2.0 specification...")
        
        result = {
            "version": "2.0",
            "title": spec.get("info", {}).get("title", "Unknown API"),
            "description": spec.get("info", {}).get("description", ""),
            "api_version": spec.get("info", {}).get("version", "1.0.0"),
            "base_url": self._extract_base_url_swagger2(spec),
            "endpoints": [],
            "schemas": {},
            "security": self._extract_security_swagger2(spec),
            "rate_limits": self._extract_rate_limits_swagger2(spec),
            "contact": spec.get("info", {}).get("contact", {}),
            "license": spec.get("info", {}).get("license", {}),
        }
        
        # Extract schemas (definitions in Swagger 2.0)
        if "definitions" in spec:
            result["schemas"] = spec["definitions"]
        
        # Extract endpoints
        if "paths" in spec:
            result["endpoints"] = self._extract_endpoints_swagger2(spec["paths"], spec)
        
        return result
    
    def _extract_base_url_oas3(self, spec: Dict) -> str:
        """Extract base URL from OpenAPI 3.0+ spec."""
        try:
            if "servers" in spec and len(spec["servers"]) > 0:
                server = spec["servers"][0]
                url = server.get("url", "")
                
                # Handle variables
                if "variables" in server:
                    for var_name, var_obj in server["variables"].items():
                        default = var_obj.get("default", "")
                        url = url.replace(f"{{{var_name}}}", default)
                
                return url
        except Exception as e:
            logger.debug(f"Error extracting base URL: {str(e)}")
        
        return "/"
    
    def _extract_base_url_swagger2(self, spec: Dict) -> str:
        """Extract base URL from Swagger 2.0 spec."""
        try:
            scheme = spec.get("schemes", ["https"])[0]
            host = spec.get("host", "localhost")
            base_path = spec.get("basePath", "/")
            
            return f"{scheme}://{host}{base_path}"
        except Exception as e:
            logger.debug(f"Error extracting base URL: {str(e)}")
        
        return "/"
    
    def _extract_endpoints_oas3(self, paths: Dict, spec: Dict) -> List[Dict[str, Any]]:
        """Extract endpoints from OpenAPI 3.0+ paths."""
        endpoints = []
        
        for path, path_item in paths.items():
            for method, operation in path_item.items():
                if method.startswith("x-"):  # Skip extensions
                    continue
                
                if not isinstance(operation, dict):
                    continue
                
                endpoint = {
                    "path": path,
                    "method": method.upper(),
                    "summary": operation.get("summary", ""),
                    "description": operation.get("description", ""),
                    "operation_id": operation.get("operationId", ""),
                    "tags": operation.get("tags", []),
                    "parameters": self._extract_parameters_oas3(operation),
                    "request_body": self._extract_request_body_oas3(operation),
                    "responses": self._extract_responses_oas3(operation),
                    "auth_required": self._check_auth_required_oas3(operation, spec),
                    "deprecated": operation.get("deprecated", False),
                }
                
                endpoints.append(endpoint)
        
        return endpoints
    
    def _extract_endpoints_swagger2(self, paths: Dict, spec: Dict) -> List[Dict[str, Any]]:
        """Extract endpoints from Swagger 2.0 paths."""
        endpoints = []
        
        for path, path_item in paths.items():
            for method, operation in path_item.items():
                if method == "parameters":  # Shared parameters
                    continue
                
                if method.startswith("x-"):  # Skip extensions
                    continue
                
                if not isinstance(operation, dict):
                    continue
                
                endpoint = {
                    "path": path,
                    "method": method.upper(),
                    "summary": operation.get("summary", ""),
                    "description": operation.get("description", ""),
                    "operation_id": operation.get("operationId", ""),
                    "tags": operation.get("tags", []),
                    "parameters": self._extract_parameters_swagger2(operation),
                    "request_body": self._extract_request_body_swagger2(operation),
                    "responses": self._extract_responses_swagger2(operation),
                    "auth_required": self._check_auth_required_swagger2(operation, spec),
                    "deprecated": operation.get("deprecated", False),
                }
                
                endpoints.append(endpoint)
        
        return endpoints
    
    def _extract_parameters_oas3(self, operation: Dict) -> List[Dict[str, Any]]:
        """Extract parameters from OpenAPI 3.0+ operation."""
        parameters = []
        
        for param in operation.get("parameters", []):
            parameters.append({
                "name": param.get("name", ""),
                "in": param.get("in", ""),  # query, path, header
                "required": param.get("required", False),
                "schema": param.get("schema", {}),
                "description": param.get("description", ""),
            })
        
        return parameters
    
    def _extract_parameters_swagger2(self, operation: Dict) -> List[Dict[str, Any]]:
        """Extract parameters from Swagger 2.0 operation."""
        parameters = []
        
        for param in operation.get("parameters", []):
            parameters.append({
                "name": param.get("name", ""),
                "in": param.get("in", ""),  # query, path, header, formData, body
                "required": param.get("required", False),
                "type": param.get("type", ""),
                "description": param.get("description", ""),
            })
        
        return parameters
    
    def _extract_request_body_oas3(self, operation: Dict) -> Dict[str, Any]:
        """Extract request body from OpenAPI 3.0+ operation."""
        if "requestBody" not in operation:
            return {}
        
        req_body = operation["requestBody"]
        content = req_body.get("content", {})
        
        return {
            "required": req_body.get("required", False),
            "content_types": list(content.keys()),
            "description": req_body.get("description", ""),
        }
    
    def _extract_request_body_swagger2(self, operation: Dict) -> Dict[str, Any]:
        """Extract request body from Swagger 2.0 operation (via parameters)."""
        for param in operation.get("parameters", []):
            if param.get("in") == "body":
                return {
                    "required": param.get("required", False),
                    "schema": param.get("schema", {}),
                    "description": param.get("description", ""),
                }
        
        return {}
    
    def _extract_responses_oas3(self, operation: Dict) -> Dict[str, Any]:
        """Extract responses from OpenAPI 3.0+ operation."""
        responses = {}
        
        for status_code, response in operation.get("responses", {}).items():
            responses[status_code] = {
                "description": response.get("description", ""),
                "content": list(response.get("content", {}).keys()),
            }
        
        return responses
    
    def _extract_responses_swagger2(self, operation: Dict) -> Dict[str, Any]:
        """Extract responses from Swagger 2.0 operation."""
        responses = {}
        
        for status_code, response in operation.get("responses", {}).items():
            responses[status_code] = {
                "description": response.get("description", ""),
            }
        
        return responses
    
    def _extract_security_oas3(self, spec: Dict) -> Dict[str, Any]:
        """Extract security requirements from OpenAPI 3.0+."""
        security_schemes = {}
        auth_types = []
        
        if "components" in spec and "securitySchemes" in spec["components"]:
            schemes = spec["components"]["securitySchemes"]
            
            for scheme_name, scheme_obj in schemes.items():
                scheme_type = scheme_obj.get("type", "")
                auth_types.append(scheme_type)
                
                security_schemes[scheme_name] = {
                    "type": scheme_type,
                    "description": scheme_obj.get("description", ""),
                    "scheme": scheme_obj.get("scheme"),
                    "bearer_format": scheme_obj.get("bearerFormat"),
                    "flows": scheme_obj.get("flows", {}),
                }
        
        return {
            "auth_required": len(auth_types) > 0,
            "auth_types": list(set(auth_types)),
            "details": security_schemes,
        }
    
    def _extract_security_swagger2(self, spec: Dict) -> Dict[str, Any]:
        """Extract security requirements from Swagger 2.0."""
        security_schemes = {}
        auth_types = []
        
        if "securityDefinitions" in spec:
            schemes = spec["securityDefinitions"]
            
            for scheme_name, scheme_obj in schemes.items():
                scheme_type = scheme_obj.get("type", "")
                auth_types.append(scheme_type)
                
                security_schemes[scheme_name] = {
                    "type": scheme_type,
                    "description": scheme_obj.get("description", ""),
                    "in": scheme_obj.get("in"),  # header, query
                    "name": scheme_obj.get("name"),
                }
        
        return {
            "auth_required": len(auth_types) > 0,
            "auth_types": list(set(auth_types)),
            "details": security_schemes,
        }
    
    def _extract_rate_limits_oas3(self, spec: Dict) -> Dict[str, Any]:
        """Extract rate limit info from OpenAPI 3.0+ extensions."""
        # Check for x-rate-limit or similar extensions
        info = spec.get("info", {})
        
        for key, value in info.items():
            if "rate" in key.lower():
                return {
                    "rate_limit_enabled": True,
                    "limits": value,
                }
        
        # Check global extensions
        for key, value in spec.items():
            if key.startswith("x-rate") or key.startswith("x-ratelimit"):
                return {
                    "rate_limit_enabled": True,
                    "limits": value,
                }
        
        return {"rate_limit_enabled": False}
    
    def _extract_rate_limits_swagger2(self, spec: Dict) -> Dict[str, Any]:
        """Extract rate limit info from Swagger 2.0 extensions."""
        info = spec.get("info", {})
        
        for key, value in info.items():
            if "rate" in key.lower():
                return {
                    "rate_limit_enabled": True,
                    "limits": value,
                }
        
        for key, value in spec.items():
            if key.startswith("x-rate") or key.startswith("x-ratelimit"):
                return {
                    "rate_limit_enabled": True,
                    "limits": value,
                }
        
        return {"rate_limit_enabled": False}
    
    def _check_auth_required_oas3(self, operation: Dict, spec: Dict) -> bool:
        """Check if auth is required for OAS3 operation."""
        if "security" in operation:
            return len(operation["security"]) > 0
        
        if "security" in spec:
            return len(spec["security"]) > 0
        
        return False
    
    def _check_auth_required_swagger2(self, operation: Dict, spec: Dict) -> bool:
        """Check if auth is required for Swagger 2.0 operation."""
        if "security" in operation:
            return len(operation["security"]) > 0
        
        if "security" in spec:
            return len(spec["security"]) > 0
        
        return False
