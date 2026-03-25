# API Specification

## Base URL

**Development:** `http://localhost:8000`
**Staging:** `https://api-staging.aegis.example.com`
**Production:** `https://api.aegis.example.com`

## Authentication

### OAuth 2.0 (Recommended)

```
POST /api/auth/token
Content-Type: application/json

{
  "client_id": "your-client-id",
  "client_secret": "your-client-secret",
  "grant_type": "client_credentials"
}

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

## API Endpoints

### API Inventory

#### List APIs
```
GET /api/v1/apis?skip=0&limit=100&status=active&risk_level=high

Response:
{
  "total": 250,
  "items": [
    {
      "id": "api-001",
      "url": "/api/v1/users",
      "method": "GET",
      "name": "List Users",
      "status": "active",
      "risk_level": "high",
      "owner": "backend-team",
      "last_seen": "2024-01-15T10:30:00Z",
      "vulnerable_count": 2
    }
  ]
}
```

#### Get API Details
```
GET /api/v1/apis/{api_id}

Response:
{
  "id": "api-001",
  "url": "/api/v1/users",
  "method": "GET",
  "name": "List Users",
  "description": "Retrieves paginated list of users",
  "owner": "backend-team",
  "owner_email": "backend@example.com",
  "status": "active",
  "version": "1.0",
  "created_at": "2023-06-01T00:00:00Z",
  "last_seen": "2024-01-15T10:30:00Z",
  "source": "gateway_scan",
  "security_assessment": {
    "authentication": "oauth2",
    "has_rate_limit": true,
    "has_encryption": true,
    "data_exposure": "low",
    "risk_level": "high",
    "risk_score": 42
  }
}
```

### Security Assessment

#### Get Risk Assessment
```
GET /api/v1/apis/{api_id}/assessment

Response:
{
  "api_id": "api-001",
  "authentication": "oauth2",
  "has_rate_limit": true,
  "has_encryption": true,
  "data_exposure": "medium",
  "compliance_gaps": [
    "Missing CORS policy",
    "No API versioning"
  ],
  "vulnerabilities": [
    {
      "cwe_id": "CWE-79",
      "title": "Cross-site Scripting (XSS)",
      "severity": "high",
      "remediation": "Implement input validation and output encoding"
    }
  ],
  "risk_level": "high",
  "risk_score": 72,
  "last_assessed": "2024-01-15T09:00:00Z"
}
```

#### Run Security Assessment
```
POST /api/v1/apis/{api_id}/assess

Response:
{
  "job_id": "assess-job-12345",
  "status": "in_progress",
  "created_at": "2024-01-15T10:35:00Z"
}
```

### Remediation

#### List Recommendations
```
GET /api/v1/apis/{api_id}/recommendations

Response:
{
  "total": 3,
  "items": [
    {
      "id": "rec-001",
      "type": "authentication",
      "title": "Implement OAuth2 Authentication",
      "description": "API currently lacks authentication",
      "priority": "critical",
      "estimated_effort": "high",
      "action": "Implement OAuth2 token validation",
      "status": "pending",
      "assigned_to": "john@example.com"
    }
  ]
}
```

#### Update Recommendation Status
```
PATCH /api/v1/recommendations/{rec_id}

{
  "status": "in_progress",
  "assigned_to": "john@example.com"
}
```

### Decommissioning

#### Create Decommissioning Workflow
```
POST /api/v1/decommissioning

{
  "api_id": "api-001",
  "reason": "Replaced by new API v2",
  "deprecation_notice_date": "2024-02-01",
  "sunset_date": "2024-03-01",
  "affected_systems": ["mobile-app", "web-ui"],
  "impact_analysis": "Affects 3 internal clients..."
}

Response:
{
  "id": "decomm-001",
  "api_id": "api-001",
  "status": "draft",
  "created_at": "2024-01-15T10:40:00Z"
}
```

#### Approve Decommissioning
```
POST /api/v1/decommissioning/{decomm_id}/approve

{
  "approved_by": "manager@example.com",
  "comments": "Approved. Ensure client notification within 7 days."
}
```

#### Block API Traffic
```
POST /api/v1/decommissioning/{decomm_id}/block

{
  "response_code": 410,
  "response_body": "This API is deprecated as of 2024-03-01. Please migrate to /api/v2/users"
}
```

### Analytics & Metrics

#### Get API Metrics
```
GET /api/v1/apis/{api_id}/metrics?period=30d

Response:
{
  "api_id": "api-001",
  "requests_per_day": 1250,
  "error_rate": 0.02,
  "avg_response_time_ms": 145,
  "unique_callers": 12,
  "last_used": "2024-01-15T10:30:00Z",
  "usage_7_days": [1200, 1180, 1220, 1250, 1240, 1100, 800],
  "usage_30_days": [...]
}
```

#### Get Dashboard Summary
```
GET /api/v1/dashboard/summary

Response:
{
  "total_apis": 450,
  "active_apis": 380,
  "deprecated_apis": 35,
  "orphaned_apis": 20,
  "zombie_apis": 15,
  "critical_risk_apis": 8,
  "high_risk_apis": 25,
  "discovered_this_month": 12,
  "remediated_this_month": 5,
  "average_risk_score": 42.5,
  "compliance_score": 78
}
```

## Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input parameters",
    "details": [
      {
        "field": "risk_level",
        "message": "Must be one of: critical, high, medium, low"
      }
    ]
  }
}
```

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid credentials |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Resource already exists |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Server Error - Internal server error |

## Rate Limiting

```
Rate-Limit-Limit: 1000
Rate-Limit-Remaining: 995
Rate-Limit-Reset: 1705328400
```

**Limits:**
- General API: 1000 requests/hour
- Assessment jobs: 100/day
- Decommissioning actions: 50/day

## Pagination

```
GET /api/v1/apis?skip=0&limit=50

Parameters:
- skip: Number of items to skip (default: 0)
- limit: Number of items to return (default: 50, max: 500)

Response includes:
- total: Total number of items
- items: Array of items
- skip: Current skip value
- limit: Current limit value
```

## Filtering & Sorting

### Filters
```
GET /api/v1/apis?status=active&risk_level=high&owner=backend-team

Supported filters:
- status: active, deprecated, orphaned, zombie
- risk_level: critical, high, medium, low
- owner: username or team name
- has_security_issues: true, false
- last_seen_days: 1-365
```

### Sorting
```
GET /api/v1/apis?sort_by=risk_score&sort_order=desc

- sort_by: risk_score, created_at, last_seen, requests_per_day
- sort_order: asc, desc
```

## Webhooks (Coming Soon)

Subscribe to events like:
- API discovered
- High-risk API detected
- Critical security issue found
- Decommissioning started/completed

```
POST /api/v1/webhooks

{
  "url": "https://your-domain.com/webhook",
  "events": ["api.discovered", "api.high_risk", "decomm.completed"]
}
```

## SDK Examples

### Python
```python
from aegis_api import Client

client = Client(
    api_url="https://api.aegis.example.com",
    client_id="xxx",
    client_secret="xxx"
)

# List APIs
apis = client.apis.list(status="zombie", limit=100)

# Get security assessment
assessment = client.assessments.get(api_id="api-001")

# Create decommissioning workflow
decomm = client.decommissioning.create(
    api_id="api-001",
    reason="Replaced by v2",
    sunset_date="2024-03-01"
)
```

### JavaScript/TypeScript
```typescript
import { AegisClient } from '@aegis/js-sdk';

const client = new AegisClient({
  apiUrl: 'https://api.aegis.example.com',
  clientId: 'xxx',
  clientSecret: 'xxx'
});

// List APIs
const apis = await client.apis.list({ status: 'zombie' });

// Get metrics
const metrics = await client.apis.getMetrics('api-001');

// Start decommissioning
const workflow = await client.decommissioning.create({
  apiId: 'api-001',
  reason: 'Replaced by v2',
  sunsetDate: '2024-03-01'
});
```

## Versioning

API follows semantic versioning:
- **v1** - Current stable release
- **v1.beta** - Beta features (unstable)

Deprecation policy: Minor version bump for deprecations, resolved in next major version.

## Support

- **Documentation**: https://docs.aegis.example.com
- **Issues**: https://github.com/your-org/aegis/issues
- **Email**: api-support@example.com
