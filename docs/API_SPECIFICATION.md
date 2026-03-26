# 🔌 API Specification

## Base URL

- **Development**: `http://localhost:5000`
- **Production**: `https://api.aegisapi.com` (example)

## Authentication

All authenticated endpoints require the `Authorization` header:

```
Authorization: Bearer <jwt_token>
```

JWT tokens are obtained from the `/auth/login` endpoint and expire after a set time (default: 24 hours). Use `/auth/refresh` to refresh expired tokens.

---

## Authentication Endpoints

### 1. Register New User

**POST** `/auth/register`

Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "full_name": "John Doe"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "uuid-here",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "analyst"
  }
}
```

**Error Responses:**
- `400 Bad Request`: Email already exists, password too weak
- `422 Validation Error`: Invalid email format

---

### 2. User Login

**POST** `/auth/login`

Authenticate user and get JWT token.

**Request Body (Form Data):**
```
username: user@example.com
password: SecurePassword123!
```

**OR JSON:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "uuid-here",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "analyst"
  }
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid credentials
- `404 Not Found`: User not found

---

### 3. Refresh Token

**POST** `/auth/refresh`

Get a new access token using the current token.

**Headers:**
```
Authorization: Bearer <current_token>
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**
- `401 Unauthorized`: Token expired or invalid

---

### 4. Get Current User

**GET** `/auth/me`

Get authenticated user's profile.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**
```json
{
  "id": "uuid-here",
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "analyst",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or expired token

---

## API Discovery Endpoints

### 1. List All APIs

**GET** `/apis`

Retrieve paginated list of discovered APIs.

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Number of records to return (default: 20, max: 100)
- `status`: Filter by status (`active`, `deprecated`, `zombie`)
- `risk_level`: Filter by risk level (`critical`, `high`, `medium`, `low`)
- `search`: Search in API name and description

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**
```json
{
  "total": 145,
  "items": [
    {
      "id": "api-001",
      "name": "User Management API",
      "description": "Handles user CRUD operations",
      "endpoint": "https://api.example.com/v1/users",
      "status": "active",
      "risk_score": 65,
      "owner": "platform-team",
      "created_at": "2024-01-15T10:30:00Z",
      "last_scanned": "2024-01-20T15:45:00Z"
    }
  ],
  "has_more": true
}
```

**Error Responses:**
- `401 Unauthorized`: Missing or invalid token
- `400 Bad Request`: Invalid query parameters

---

### 2. Get API Details

**GET** `/apis/{api_id}`

Get detailed information about a specific API.

**Path Parameters:**
- `api_id`: Unique API identifier

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**
```json
{
  "id": "api-001",
  "name": "User Management API",
  "description": "Handles user CRUD operations",
  "endpoint": "https://api.example.com/v1/users",
  "status": "active",
  "risk_score": 65,
  "owner": "platform-team",
  "documentation_url": "https://docs.example.com/users",
  "authentication": "OAuth2",
  "created_at": "2024-01-15T10:30:00Z",
  "last_scanned": "2024-01-20T15:45:00Z",
  "findings": [
    {
      "id": "finding-001",
      "type": "missing_authentication",
      "severity": "critical",
      "description": "API endpoint lacks proper authentication",
      "remediation": "Implement OAuth2 authentication"
    }
  ],
  "usage_metrics": {
    "monthly_calls": 1500000,
    "average_response_time_ms": 145,
    "error_rate": 0.05
  }
}
```

**Error Responses:**
- `401 Unauthorized`: Missing or invalid token
- `404 Not Found`: API not found

---

### 3. Search APIs

**GET** `/apis/search`

Search and filter APIs with advanced criteria.

**Query Parameters:**
- `q`: Search query (name, description, endpoint)
- `status`: Filter by status
- `risk_level`: Filter by risk level
- `owner`: Filter by owner
- `authentication`: Filter by auth type
- `no_docs`: Boolean - APIs without documentation
- `no_owner`: Boolean - APIs without owner

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**
```json
{
  "total": 23,
  "results": [
    {
      "id": "api-002",
      "name": "Payment Processing API",
      "risk_score": 85,
      "status": "active"
    }
  ]
}
```

---

### 4. Get API Statistics

**GET** `/apis/stats`

Get aggregated statistics about discovered APIs.

**Query Parameters:**
- `period`: Time period for stats (`week`, `month`, `quarter`, `year`)

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**
```json
{
  "total_apis": 245,
  "by_status": {
    "active": 180,
    "deprecated": 50,
    "zombie": 15
  },
  "by_risk_level": {
    "critical": 5,
    "high": 25,
    "medium": 85,
    "low": 130
  },
  "average_risk_score": 54,
  "unowned_apis": 23,
  "undocumented_apis": 18,
  "new_apis_discovered": 12,
  "recently_deprecated": 3
}
```

---

### 5. Create New API Entry

**POST** `/apis`

Manually register a new API in the system.

**Request Body:**
```json
{
  "name": "Custom Service API",
  "description": "Internal service endpoint",
  "endpoint": "https://internal.company.com/api/v2",
  "owner": "dev-team",
  "documentation_url": "https://docs.internal.com/api",
  "authentication": "JWT",
  "status": "active"
}
```

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (201 Created):**
```json
{
  "id": "api-new-001",
  "name": "Custom Service API",
  "endpoint": "https://internal.company.com/api/v2",
  "created_at": "2024-01-21T08:15:00Z"
}
```

---

### 6. Update API Entry

**PUT** `/apis/{api_id}`

Update an existing API entry.

**Path Parameters:**
- `api_id`: Unique API identifier

**Request Body:**
```json
{
  "status": "deprecated",
  "owner": "deprecated-services",
  "decommission_date": "2024-06-01"
}
```

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**
```json
{
  "id": "api-001",
  "status": "deprecated",
  "updated_at": "2024-01-21T10:00:00Z"
}
```

---

## Security Assessment Endpoints

### 1. Get Security Findings for API

**GET** `/apis/{api_id}/findings`

Get all security findings for a specific API.

**Path Parameters:**
- `api_id`: Unique API identifier

**Query Parameters:**
- `severity`: Filter by severity (`critical`, `high`, `medium`, `low`)

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**
```json
{
  "api_id": "api-001",
  "findings": [
    {
      "id": "finding-001",
      "type": "missing_authentication",
      "severity": "critical",
      "description": "API endpoint lacks proper authentication",
      "remediation": "Implement OAuth2 authentication",
      "status": "open",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

---

### 2. Get Risk Score

**GET** `/apis/{api_id}/risk-score`

Calculate and get risk score for an API.

**Path Parameters:**
- `api_id`: Unique API identifier

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**
```json
{
  "api_id": "api-001",
  "risk_score": 72,
  "risk_level": "high",
  "factors": [
    {
      "factor": "missing_authentication",
      "weight": 30,
      "value": 10
    },
    {
      "factor": "api_age",
      "weight": 10,
      "value": 8
    }
  ]
}
```

---

## Remediation Endpoints

### 1. List Remediation Workflows

**GET** `/remediations`

Get all remediation workflows.

**Query Parameters:**
- `status`: Filter by status (`pending`, `in_progress`, `completed`, `failed`)
- `api_id`: Filter by API

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**
```json
{
  "total": 15,
  "workflows": [
    {
      "id": "workflow-001",
      "api_id": "api-001",
      "api_name": "User Management API",
      "action": "add_authentication",
      "status": "in_progress",
      "created_at": "2024-01-19T14:30:00Z",
      "started_at": "2024-01-19T15:00:00Z"
    }
  ]
}
```

---

### 2. Create Remediation Workflow

**POST** `/remediations`

Create a new remediation workflow for an API.

**Request Body:**
```json
{
  "api_id": "api-001",
  "action": "add_authentication",
  "priority": "high",
  "description": "Add OAuth2 authentication to API",
  "target_completion": "2024-02-01"
}
```

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (201 Created):**
```json
{
  "id": "workflow-new-001",
  "api_id": "api-001",
  "status": "pending",
  "created_at": "2024-01-21T09:00:00Z"
}
```

---

### 3. Update Workflow Status

**PATCH** `/remediations/{workflow_id}`

Update remediation workflow status.

**Path Parameters:**
- `workflow_id`: Workflow identifier

**Request Body:**
```json
{
  "status": "completed",
  "completion_notes": "Successfully implemented OAuth2"
}
```

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**
```json
{
  "id": "workflow-001",
  "status": "completed",
  "completed_at": "2024-01-21T16:30:00Z"
}
```

---

## Health & Status Endpoints

### 1. Health Check

**GET** `/health`

Check if API is running.

**Response (200 OK):**
```json
{
  "status": "ok",
  "timestamp": "2024-01-21T10:00:00Z"
}
```

---

### 2. API Documentation

**GET** `/docs`

Interactive Swagger UI documentation (development only).

**GET** `/redoc`

ReDoc API documentation (development only).

---

## Error Handling

All errors follow this format:

```json
{
  "detail": "Error message here",
  "error_code": "INVALID_REQUEST",
  "timestamp": "2024-01-21T10:00:00Z"
}
```

### Common Error Codes

| Code | Status | Description |
|--|--|--|
| `UNAUTHORIZED` | 401 | Missing or invalid authentication |
| `FORBIDDEN` | 403 | User lacks permission |
| `NOT_FOUND` | 404 | Resource not found |
| `VALIDATION_ERROR` | 422 | Invalid request data |
| `CONFLICT` | 409 | Resource already exists |
| `INTERNAL_ERROR` | 500 | Server error |

---

## Rate Limiting

- **Limit**: 1000 requests per hour per user
- **Header**: `X-RateLimit-Remaining`

---

## Pagination

Endpoints that return lists support pagination:

```json
{
  "total": 245,
  "skip": 0,
  "limit": 20,
  "items": [...],
  "has_more": true
}
```

---

## Filters

### Status Filter
Values: `active`, `deprecated`, `zombie`

### Risk Level Filter
Values: `critical`, `high`, `medium`, `low`

### Authentication Types
Values: `JWT`, `OAuth2`, `API_Key`, `BasicAuth`, `mTLS`, `None`

---

## SDK/Client Examples

### JavaScript/TypeScript

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000'
});

// Login
const { data } = await api.post('/auth/login', {
  email: 'user@example.com',
  password: 'password'
});

// Set token
api.defaults.headers.common['Authorization'] = `Bearer ${data.access_token}`;

// Get APIs
const apis = await api.get('/apis?limit=10');
```

### Python

```python
import requests

base_url = 'http://localhost:5000'

# Login
response = requests.post(f'{base_url}/auth/login', json={
    'email': 'user@example.com',
    'password': 'password'
})
token = response.json()['access_token']

# Get APIs
headers = {'Authorization': f'Bearer {token}'}
apis = requests.get(f'{base_url}/apis', headers=headers).json()
```

---

## WebSocket Events

(Coming soon)

---

## Changelog

### v1.0.0 (January 2024)
- Initial API release
- Authentication endpoints
- API discovery endpoints
- Security assessment endpoints
- Remediation endpoints

---

**Last Updated**: January 21, 2024
**API Version**: 1.0.0
