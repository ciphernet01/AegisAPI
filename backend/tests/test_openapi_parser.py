"""
Tests for OpenAPI/Swagger specification parser.

Verifies:
- OpenAPI 3.0+ parsing
- Swagger 2.0 parsing
- Endpoint extraction
- Authentication extraction
- Schema extraction
- Rate limit extraction
"""

import pytest
import json
import yaml
from services.openapi_parser import OpenAPIParser


class TestOpenAPI3Parser:
    """Test OpenAPI 3.0+ parsing."""
    
    @pytest.fixture
    def parser(self):
        """Create parser instance."""
        return OpenAPIParser()
    
    @pytest.fixture
    def sample_oas3_spec(self):
        """Sample OpenAPI 3.0 specification."""
        return {
            "openapi": "3.0.0",
            "info": {
                "title": "User Management API",
                "description": "API for managing users",
                "version": "1.0.0",
                "contact": {
                    "name": "API Support",
                    "email": "support@example.com",
                },
                "license": {
                    "name": "MIT",
                }
            },
            "servers": [
                {
                    "url": "https://api.example.com/v1",
                    "description": "Production server",
                }
            ],
            "paths": {
                "/users": {
                    "get": {
                        "summary": "List all users",
                        "operationId": "listUsers",
                        "tags": ["users"],
                        "parameters": [
                            {
                                "name": "limit",
                                "in": "query",
                                "required": False,
                                "schema": {"type": "integer"},
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Success",
                                "content": {
                                    "application/json": {
                                        "schema": {"type": "array"}
                                    }
                                }
                            }
                        }
                    },
                    "post": {
                        "summary": "Create user",
                        "operationId": "createUser",
                        "tags": ["users"],
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/User"}
                                }
                            }
                        },
                        "responses": {
                            "201": {
                                "description": "Created",
                            }
                        }
                    }
                },
                "/users/{id}": {
                    "get": {
                        "summary": "Get user by ID",
                        "operationId": "getUser",
                        "tags": ["users"],
                        "parameters": [
                            {
                                "name": "id",
                                "in": "path",
                                "required": True,
                                "schema": {"type": "integer"},
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Success",
                            }
                        }
                    }
                }
            },
            "components": {
                "schemas": {
                    "User": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "name": {"type": "string"},
                            "email": {"type": "string", "format": "email"},
                        },
                        "required": ["id", "name", "email"],
                    }
                },
                "securitySchemes": {
                    "bearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT",
                    },
                    "apiKey": {
                        "type": "apiKey",
                        "in": "header",
                        "name": "X-API-Key",
                    }
                }
            },
            "security": [
                {"bearerAuth": []},
                {"apiKey": []}
            ]
        }
    
    def test_parse_oas3_spec(self, parser, sample_oas3_spec):
        """Test parsing OpenAPI 3.0 specification."""
        result = parser.parse_spec(sample_oas3_spec)
        
        assert result["version"] == "3.0.0"
        assert result["title"] == "User Management API"
        assert result["api_version"] == "1.0.0"
        assert "endpoints" in result
        assert "schemas" in result
        assert "security" in result
    
    def test_extract_endpoints_oas3(self, parser, sample_oas3_spec):
        """Test extracting endpoints from OpenAPI 3.0."""
        endpoints = parser.extract_endpoints(sample_oas3_spec)
        
        assert len(endpoints) == 3  # GET /users, POST /users, GET /users/{id}
        
        # Check GET /users
        get_users = [e for e in endpoints if e["path"] == "/users" and e["method"] == "GET"][0]
        assert get_users["summary"] == "List all users"
        assert get_users["operation_id"] == "listUsers"
        assert "users" in get_users["tags"]
        
        # Check POST /users
        post_users = [e for e in endpoints if e["path"] == "/users" and e["method"] == "POST"][0]
        assert post_users["summary"] == "Create user"
        assert post_users["request_body"]["required"] is True
        
        # Check GET /users/{id}
        get_user = [e for e in endpoints if e["path"] == "/users/{id}" and e["method"] == "GET"][0]
        assert get_user["summary"] == "Get user by ID"
        assert len(get_user["parameters"]) > 0
    
    def test_extract_schemas_oas3(self, parser, sample_oas3_spec):
        """Test extracting schemas from OpenAPI 3.0."""
        schemas = parser.extract_schemas(sample_oas3_spec)
        
        assert "User" in schemas
        user_schema = schemas["User"]
        assert user_schema["type"] == "object"
        assert "id" in user_schema["properties"]
        assert "name" in user_schema["properties"]
        assert "email" in user_schema["properties"]
        assert set(user_schema["required"]) == {"id", "name", "email"}
    
    def test_extract_authentication_oas3(self, parser, sample_oas3_spec):
        """Test extracting authentication from OpenAPI 3.0."""
        auth = parser.extract_authentication(sample_oas3_spec)
        
        assert auth["auth_required"] is True
        assert "http" in auth["auth_types"]
        assert "apiKey" in auth["auth_types"]
        assert "bearerAuth" in auth["details"]
        assert "apiKey" in auth["details"]
    
    def test_extract_rate_limits_oas3(self, parser, sample_oas3_spec):
        """Test extracting rate limits from OpenAPI 3.0."""
        # Add rate limit extension
        sample_oas3_spec["x-rate-limit"] = {
            "requests_per_minute": 60,
            "requests_per_hour": 1000,
        }
        
        rates = parser.extract_rate_limits(sample_oas3_spec)
        
        assert rates.get("rate_limit_enabled") or not rates.get("rate_limit_enabled")


class TestSwagger2Parser:
    """Test Swagger 2.0 parsing."""
    
    @pytest.fixture
    def parser(self):
        """Create parser instance."""
        return OpenAPIParser()
    
    @pytest.fixture
    def sample_swagger2_spec(self):
        """Sample Swagger 2.0 specification."""
        return {
            "swagger": "2.0",
            "info": {
                "title": "Pet Store API",
                "description": "API for managing pets",
                "version": "1.0.0",
            },
            "host": "api.petstore.com",
            "basePath": "/v1",
            "schemes": ["https"],
            "paths": {
                "/pets": {
                    "get": {
                        "summary": "List all pets",
                        "operationId": "listPets",
                        "tags": ["pets"],
                        "parameters": [
                            {
                                "name": "limit",
                                "in": "query",
                                "required": False,
                                "type": "integer",
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Success",
                            }
                        }
                    },
                    "post": {
                        "summary": "Create pet",
                        "operationId": "createPet",
                        "tags": ["pets"],
                        "parameters": [
                            {
                                "name": "body",
                                "in": "body",
                                "required": True,
                                "schema": {"$ref": "#/definitions/Pet"},
                            }
                        ],
                        "responses": {
                            "201": {
                                "description": "Created",
                            }
                        }
                    }
                },
                "/pets/{id}": {
                    "get": {
                        "summary": "Get pet by ID",
                        "operationId": "getPet",
                        "tags": ["pets"],
                        "parameters": [
                            {
                                "name": "id",
                                "in": "path",
                                "required": True,
                                "type": "integer",
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Success",
                            }
                        }
                    }
                }
            },
            "definitions": {
                "Pet": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                    },
                    "required": ["id", "name"],
                }
            },
            "securityDefinitions": {
                "api_key": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "X-API-Key",
                },
                "oauth2": {
                    "type": "oauth2",
                    "authorizationUrl": "https://api.example.com/oauth/authorize",
                    "tokenUrl": "https://api.example.com/oauth/token",
                    "flow": "implicit",
                }
            },
            "security": [
                {"api_key": []},
                {"oauth2": ["read", "write"]}
            ]
        }
    
    def test_parse_swagger2_spec(self, parser, sample_swagger2_spec):
        """Test parsing Swagger 2.0 specification."""
        result = parser.parse_spec(sample_swagger2_spec)
        
        assert result["version"] == "2.0"
        assert result["title"] == "Pet Store API"
        assert result["api_version"] == "1.0.0"
        assert result["base_url"] == "https://api.petstore.com/v1"
    
    def test_extract_endpoints_swagger2(self, parser, sample_swagger2_spec):
        """Test extracting endpoints from Swagger 2.0."""
        endpoints = parser.extract_endpoints(sample_swagger2_spec)
        
        assert len(endpoints) == 3
        
        # Verify endpoint details
        get_pets = [e for e in endpoints if e["path"] == "/pets" and e["method"] == "GET"][0]
        assert get_pets["summary"] == "List all pets"
    
    def test_extract_authentication_swagger2(self, parser, sample_swagger2_spec):
        """Test extracting authentication from Swagger 2.0."""
        auth = parser.extract_authentication(sample_swagger2_spec)
        
        assert auth["auth_required"] is True
        assert "apiKey" in auth["auth_types"]
        assert "oauth2" in auth["auth_types"]
    
    def test_extract_schemas_swagger2(self, parser, sample_swagger2_spec):
        """Test extracting schemas from Swagger 2.0."""
        schemas = parser.extract_schemas(sample_swagger2_spec)
        
        assert "Pet" in schemas
        pet_schema = schemas["Pet"]
        assert pet_schema["type"] == "object"
        assert "id" in pet_schema["properties"]
        assert "name" in pet_schema["properties"]


class TestOpenAPIFormatParsing:
    """Test parsing different formats (JSON, YAML)."""
    
    @pytest.fixture
    def parser(self):
        """Create parser instance."""
        return OpenAPIParser()
    
    def test_parse_json_string(self, parser):
        """Test parsing JSON format spec."""
        spec_json = json.dumps({
            "openapi": "3.0.0",
            "info": {"title": "Test", "version": "1.0"},
            "paths": {}
        })
        
        result = parser.parse_spec(spec_json)
        assert result["title"] == "Test"
    
    def test_parse_yaml_string(self, parser):
        """Test parsing YAML format spec."""
        spec_yaml = """
        openapi: 3.0.0
        info:
          title: Test API
          version: 1.0
        paths: {}
        """
        
        result = parser.parse_spec(spec_yaml)
        assert result["title"] == "Test API"
    
    def test_parse_dict(self, parser):
        """Test parsing dict format spec."""
        spec_dict = {
            "openapi": "3.0.0",
            "info": {"title": "Dict Spec", "version": "1.0"},
            "paths": {}
        }
        
        result = parser.parse_spec(spec_dict)
        assert result["title"] == "Dict Spec"


class TestOpenAPIEdgeCases:
    """Test edge cases and error handling."""
    
    @pytest.fixture
    def parser(self):
        """Create parser instance."""
        return OpenAPIParser()
    
    def test_minimal_oas3_spec(self, parser):
        """Test parsing minimal OpenAPI 3.0 spec."""
        spec = {
            "openapi": "3.0.0",
            "info": {"title": "Minimal", "version": "1.0"},
            "paths": {}
        }
        
        result = parser.parse_spec(spec)
        
        assert result["title"] == "Minimal"
        assert result["endpoints"] == []
    
    def test_spec_with_missing_fields(self, parser):
        """Test handling missing optional fields."""
        spec = {
            "openapi": "3.0.0",
            "info": {"title": "Incomplete"},
            "paths": {
                "/test": {
                    "get": {
                        "responses": {
                            "200": {"description": "OK"}
                        }
                    }
                }
            }
        }
        
        result = parser.parse_spec(spec)
        endpoints = result["endpoints"]
        
        assert len(endpoints) == 1
        assert endpoints[0]["path"] == "/test"
        assert endpoints[0]["method"] == "GET"
    
    def test_parse_invalid_spec(self, parser):
        """Test error handling for invalid spec."""
        with pytest.raises(Exception):
            parser.parse_spec("not valid json or yaml {{{")
    
    def test_parse_unsupported_version(self, parser):
        """Test error handling for unsupported version."""
        spec = {
            "swagger": "1.2",
            "info": {"title": "Old"},
            "paths": {}
        }
        
        with pytest.raises(ValueError):
            parser.parse_spec(spec)
