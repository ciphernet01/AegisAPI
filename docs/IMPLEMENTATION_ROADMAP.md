# 📋 Implementation Roadmap

## Project Vision

**Zombie API Discovery & Defence Platform** - Enterprise solution for automatically discovering, analyzing, and remediating undocumented, deprecated, and zombie APIs across infrastructure.

**Target Users**: Enterprise DevOps teams, API governance teams, security teams

**Core Value Proposition**: Reduce API sprawl, eliminate shadow APIs, automate remediation workflows

---

## Current Status: MVP Foundation (25% Complete)

### ✅ Completed Infrastructure
- JWT authentication system (registration, login, token refresh)
- Database schema with SQLAlchemy ORM
- Frontend UI (6 main pages)
- Backend API route structure
- Development environment (SQLite + hot-reload)
- Production infrastructure (Docker Compose, PostgreSQL, Redis)
- Environment configuration system
- DevOps documentation and deployment scripts

### 🟡 Partially Implemented
- API discovery framework (40%): Routes exist, services stubbed
- Security assessment (5%): Models exist, logic not implemented
- Classification system (30%): Status enums defined, detection logic missing
- User management (60%): Auth works, role-based access control incomplete

### 🔴 Not Started
- GitHub API scanner
- Docker registry scanner
- Kubernetes API scanner
- AWS API scanner
- Multi-source consolidation
- Background job scheduling
- Continuous monitoring
- Risk scoring algorithm
- Zombie detection logic
- Remediation automation
- Advanced analytics & reporting

### 📊 Metrics
- **Codebase Size**: ~2500 lines (backend + frontend)
- **Frontend Build**: 1426 modules, 269.6 kB
- **API Endpoints Defined**: 15+
- **Database Tables**: 5 (users, apis, security_findings, remediation_workflows, audit_logs)
- **Time to MVP Completion**: 4-6 weeks estimated

---

## Phase 1: API Discovery Engine (Week 1-2)

### Objective
Enable automatic discovery of APIs from multiple sources, populate database with real data.

### 1.1 GitHub Repository Scanner
**Estimated Time**: 2-3 days
**Complexity**: Medium

Create scanner to detect APIs in GitHub repositories:

**Features to implement:**
1. Scan GitHub organizations/repositories
2. Detect API definitions:
   - OpenAPI/Swagger (YAML/JSON files)
   - GraphQL schemas
   - REST endpoints in code (regex patterns)
   - Docker Compose files (service endpoints)
   - Kubernetes manifests (service endpoints)
3. Extract metadata:
   - Base URL/endpoint
   - Authentication method
   - API documentation URL
   - Owner/maintainer from repo metadata

**File**: `backend/services/discovery_service.py`

```python
class GitHubScanner:
    def __init__(self, token: str):
        self.session = requests.Session()
        self.session.headers['Authorization'] = f'token {token}'
    
    def scan_organization(self, org: str) -> List[APIDiscovery]:
        """Scan all repos in organization for APIs"""
        repos = self.session.get(f'https://api.github.com/orgs/{org}/repos').json()
        
        apis = []
        for repo in repos:
            apis.extend(self._scan_repo(repo))
        return apis
    
    def _scan_repo(self, repo: dict) -> List[APIDiscovery]:
        """Find APIs in single repository"""
        # Check for OpenAPI/Swagger files
        # Check for GraphQL schema
        # Scan for REST endpoints in code
        # Parse Docker Compose
        # Parse Kubernetes manifests
```

**API Endpoint**: `POST /discovery/scan-github`

**Input**:
```json
{
  "organization": "myorg",
  "github_token": "ghp_xxxx",
  "scan_recursive": true
}
```

### 1.2 OpenAPI/Swagger Parser
**Estimated Time**: 1-2 days
**Complexity**: Low

Parse OpenAPI 3.0+ and Swagger 2.0 specs:

```python
class OpenAPIParser:
    def parse(self, spec: dict) -> APIDiscovery:
        """Parse OpenAPI/Swagger specification"""
        return APIDiscovery(
            name=spec['info']['title'],
            description=spec['info']['description'],
            endpoint=spec['servers'][0]['url'],
            authentication=self._get_auth(spec),
            endpoints=self._get_endpoints(spec)
        )
```

### 1.3 Docker Registry Scanner
**Estimated Time**: 2-3 days
**Complexity**: Medium

Scan Docker registries for containerized APIs:

**Features:**
1. Connect to Docker Hub, ECR, ACR, GCR
2. List repositories and images
3. Parse image metadata (labels, environment variables)
4. Detect APIs from exposed ports and environment configs

### 1.4 Consolidation & Deduplication
**Estimated Time**: 1 day
**Complexity**: Low

Create logic to:
1. Detect duplicate APIs across scanners
2. Merge data from multiple sources
3. Resolve conflicts (different versions of same API)

```python
def consolidate_discovered_apis(apis: List[APIDiscovery]) -> List[APIDiscovery]:
    """Merge duplicate APIs, keep highest quality data"""
    deduplicated = {}
    for api in apis:
        key = api.endpoint  # Use endpoint as unique key
        if key in deduplicated:
            # Keep most complete record
            deduplicated[key] = merge_api_records(deduplicated[key], api)
        else:
            deduplicated[key] = api
    return list(deduplicated.values())
```

### Deliverables
✅ APIs table populated with 50+ real API entries
✅ Discovery service with multiple scanner implementations
✅ Dashboard showing discovered API count
✅ Inventory page displaying real APIs with filters

### Success Criteria
- [ ] GitHub scanner successfully discovers 20+ APIs from test org
- [ ] Dashboard shows total API count (>50)
- [ ] API list page displays real data with proper pagination
- [ ] No 404s on discovered API endpoints

---

## Phase 2: Security Assessment (Week 2-3)

### Objective
Analyze APIs for security issues and calculate risk scores.

### 2.1 Authentication Detection
**Estimated Time**: 1-2 days

Detect authentication mechanisms:

```python
class SecurityAssessment:
    def detect_authentication(self, api: APIDiscovery) -> str:
        """Identify authentication method"""
        # Check OpenAPI spec for securitySchemes
        # Test endpoint for 401/403 responses
        # Analyze headers for auth tokens
        # Return: OAuth2, JWT, API_Key, BasicAuth, mTLS, None
```

### 2.2 Risk Scoring Algorithm
**Estimated Time**: 2-3 days

Calculate 0-100 risk score based on:

```python
def calculate_risk_score(api: APIDiscovery) -> int:
    """
    Risk scoring model:
    - Missing authentication: +30 points
    - No documentation: +15 points
    - No owner: +10 points
    - Deprecated status: +20 points
    - Old API (>2 years): +10 points
    - Exposed to public internet: +15 points
    - No HTTPS: +10 points
    - High error rate: +5 points
    """
    score = 0
    
    if not api.authentication or api.authentication == 'None':
        score += 30
    if not api.documentation_url:
        score += 15
    if not api.owner:
        score += 10
    if api.status == 'deprecated':
        score += 20
    if (datetime.now() - api.created_at).days > 730:
        score += 10
    if api.is_public:
        score += 15
    if not api.uses_https:
        score += 10
    if api.error_rate > 0.05:
        score += 5
    
    return min(score, 100)
```

### 2.3 Security Finding Generation
**Estimated Time**: 1-2 days

Create findings for detected issues:

```python
class FindingsGenerator:
    def generate_findings(self, api: APIDiscovery) -> List[SecurityFinding]:
        """Generate findings for security issues"""
        findings = []
        
        if not api.authentication:
            findings.append(SecurityFinding(
                type='missing_authentication',
                severity='critical',
                description='API exposed without authentication',
                remediation='Implement OAuth2 or JWT authentication'
            ))
        
        if not api.documentation_url:
            findings.append(SecurityFinding(
                type='undocumented',
                severity='medium',
                description='No API documentation available',
                remediation='Create OpenAPI specification'
            ))
        
        return findings
```

### 2.4 Risk Assessment Dashboard
**Estimated Time**: 1 day

Update frontend Risk Assessment page to display:
- Risk distribution (pie chart)
- APIs by severity
- Top 10 risky APIs
- Trends over time

### Deliverables
✅ Risk scores calculated for all discovered APIs
✅ Security findings generated for each API
✅ Risk Assessment page shows real data
✅ Risk filtering working on API inventory page

### Success Criteria
- [ ] All APIs have risk scores (0-100)
- [ ] Critical findings properly identified for high-risk APIs
- [ ] Risk Assessment page shows distribution
- [ ] Filter by risk level working correctly

---

## Phase 3: Zombie APIs Detection (Week 3-4)

### Objective
Identify and classify zombie APIs (undocumented, deprecated, unused).

### 3.1 Traffic Analysis & Usage Metrics
**Estimated Time**: 2 days

Track API usage patterns:

```python
class UsageAnalyzer:
    def analyze_traffic(self, api: APIDiscovery) -> UsageMetrics:
        """Analyze API traffic patterns"""
        # Connect to monitoring systems (ELK, CloudWatch, Prometheus)
        # Get request counts for last 30/60/90 days
        # Calculate trend: increasing, stable, declining
        # Calculate error rate and latency
        
        return UsageMetrics(
            monthly_calls=1500000,
            trend='declining',
            error_rate=0.02,
            avg_latency_ms=145,
            last_call=datetime.now() - timedelta(days=5)
        )
```

### 3.2 Zombie Detection Logic
**Estimated Time**: 1-2 days

Classify APIs by lifecycle stage:

```python
class ZombieDetector:
    ZOMBIE_THRESHOLD_DAYS = 90  # No traffic in 90+ days
    
    def classify_api(self, api: APIDiscovery) -> APIStatus:
        """Classify API as active, deprecated, or zombie"""
        
        metrics = self.analyze_traffic(api)
        
        if api.status == 'deprecated':
            return APIStatus.DEPRECATED
        
        # Check traffic
        days_since_last_call = (datetime.now() - metrics.last_call).days
        if days_since_last_call > self.ZOMBIE_THRESHOLD_DAYS:
            return APIStatus.ZOMBIE
        
        # Check trends
        if metrics.trend == 'declining' and metrics.monthly_calls < 1000:
            return APIStatus.ZOMBIE
        
        return APIStatus.ACTIVE
```

### 3.3 Orphan API Detection
**Estimated Time**: 1 day

Find APIs without ownership/maintenance:

```python
def find_orphan_apis(apis: List[APIDiscovery]) -> List[APIDiscovery]:
    """Find APIs with no clear owner"""
    return [
        api for api in apis 
        if not api.owner or 
           not api.maintained_by or
           api.last_maintenance_date < (datetime.now() - timedelta(days=180))
    ]
```

### 3.4 Update Classification System
**Estimated Time**: 1 day

Update database schema and frontend to reflect classifications:

```sql
ALTER TABLE apis ADD COLUMN status ENUM('active', 'deprecated', 'zombie') DEFAULT 'active';
ALTER TABLE apis ADD COLUMN classification_reason TEXT;
ALTER TABLE apis ADD COLUMN usage_metrics JSON;
```

### Deliverables
✅ APIs classified by status (active/deprecated/zombie)
✅ Dashboard shows zombie count and trend
✅ Zombie APIs highlighted in inventory
✅ Remediation workflows auto-created for zombies

### Success Criteria
- [ ] At least 5% of APIs marked as zombie
- [ ] Zombie detection algorithm tested with known data
- [ ] Dashboard shows zombie API metrics
- [ ] Filters working for status-based searches

---

## Phase 4: Monitoring & Automation (Week 4-5)

### Objective
Implement continuous monitoring and automated remediation workflows.

### 4.1 Background Job Scheduling
**Estimated Time**: 1-2 days

Add APScheduler for periodic tasks:

```python
# backend/main.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup_event():
    scheduler.add_job(discover_new_apis, 'interval', hours=6)
    scheduler.add_job(assess_security, 'interval', hours=12)
    scheduler.add_job(detect_zombies, 'interval', days=1)
    scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()
```

### 4.2 Continuous API Discovery
**Estimated Time**: 1 day

Schedule periodic API discovery:

```python
async def discover_new_apis():
    """Run every 6 hours"""
    github_scanner = GitHubScanner(GITHUB_TOKEN)
    docker_scanner = DockerScanner(DOCKER_CREDENTIALS)
    
    github_apis = github_scanner.scan_organization('myorg')
    docker_apis = docker_scanner.scan_registries()
    
    all_apis = consolidate_discovered_apis(github_apis + docker_apis)
    
    for api in all_apis:
        existing = db.query(APIs).filter_by(endpoint=api.endpoint).first()
        if not existing:
            db.add(API(**api.dict()))
    
    db.commit()
```

### 4.3 Automated Risk Assessment
**Estimated Time**: 1 day

Schedule periodic security assessment:

```python
async def assess_security():
    """Run every 12 hours"""
    apis = db.query(APIs).all()
    
    for api in apis:
        risk_score = calculate_risk_score(api)
        findings = generate_findings(api)
        
        # Update database
        api.risk_score = risk_score
        api.last_assessed = datetime.now()
        
        db.add_all(findings)
    
    db.commit()
    
    # Alert on score changes
    send_alerts_for_high_risk_apis()
```

### 4.4 Zombie Detection Scheduler
**Estimated Time**: 1 day

Daily zombie detection and workflow creation:

```python
async def detect_zombies():
    """Run daily"""
    apis = db.query(APIs).all()
    
    for api in apis:
        status = zombie_detector.classify_api(api)
        
        if status == APIStatus.ZOMBIE:
            api.status = APIStatus.ZOMBIE
            
            # Auto-create remediation workflow
            workflow = RemediationWorkflow(
                api_id=api.id,
                action='review_and_decommission',
                priority='high'
            )
            db.add(workflow)
    
    db.commit()
```

### 4.5 Workflow Automation
**Estimated Time**: 2-3 days

Implement remediation workflow execution:

```python
class RemediationWorkflowExecutor:
    async def execute(self, workflow: RemediationWorkflow):
        """Execute remediation actions"""
        
        if workflow.action == 'add_authentication':
            await self._add_authentication(workflow.api)
        elif workflow.action == 'decommission':
            await self._decommission_api(workflow.api)
        elif workflow.action == 'create_documentation':
            await self._create_documentation(workflow.api)
        
        workflow.status = 'completed'
        workflow.completed_at = datetime.now()
```

### 4.6 Alerting & Notifications
**Estimated Time**: 1-2 days

Add notification system:

```python
class AlertService:
    async def alert_high_risk_api(self, api: APIDiscovery):
        """Alert when API risk score > threshold"""
        message = f"High-risk API detected: {api.name} (score: {api.risk_score})"
        
        # Send to Slack/Teams/Email
        await self.slack_client.send_message(message)
        await self.email_service.send(
            to=api.owner_email,
            subject=f"API Risk Alert: {api.name}",
            body=f"Your API has a high risk score: {api.risk_score}"
        )
```

### Deliverables
✅ Discovery runs automatically every 6 hours
✅ Risk assessments run every 12 hours
✅ Zombie detection runs daily
✅ Alerts sent for high-risk APIs
✅ Basic remediation workflows auto-execute

### Success Criteria
- [ ] Discovery job runs successfully and finds new APIs
- [ ] Risk scores update automatically
- [ ] Zombie detection identifies APIs with no traffic
- [ ] Slack/email alerts sent for critical findings
- [ ] Workflow execution logs show completed actions

---

## Phase 5: Advanced Features & Optimization (Week 5-6)

### 5.1 Advanced Analytics & Reporting
**Estimated Time**: 2 days

Add comprehensive reporting:

```python
class ReportingService:
    def generate_monthly_report(self) -> dict:
        return {
            "total_apis": self.count_apis(),
            "new_apis": self.count_new_apis(days=30),
            "deprecated_apis": self.count_deprecated(days=30),
            "zombies_detected": self.count_zombies(),
            "risk_distribution": self.get_risk_distribution(),
            "top_risky_apis": self.get_top_risky_apis(limit=10),
            "remediation_status": self.get_remediation_stats(),
            "recommendations": self.generate_recommendations()
        }
```

### 5.2 Advanced Filtering & Search
**Estimated Time**: 1 day

Add full-text search and advanced filters:

```python
# API endpoint
GET /apis/search?q=payment%20service&status=active&risk_level=high&owner=platform-team
```

### 5.3 Export & Integration
**Estimated Time**: 1-2 days

Add export capabilities:
- CSV export
- JSON export
- Webhook notifications
- Jira/ServiceNow integration

### 5.4 Performance Optimization
**Estimated Time**: 1 day

Optimize for scale:
- Add database indexes
- Implement caching (Redis)
- Optimize API query times
- Add query result pagination

### 5.5 UI/UX Polish
**Estimated Time**: 1-2 days

Enhance user experience:
- Add data visualization improvements
- Improve dashboard layout
- Add keyboard shortcuts
- Improve mobile responsiveness

### Deliverables
✅ Monthly/weekly report generation working
✅ Advanced search and filtering
✅ Export to CSV/JSON
✅ Third-party integrations (Slack, Jira)
✅ Performance optimized for 1000+ APIs

---

## Phase 6: Production Hardening & Testing (Week 6)

### 6.1 Security Hardening
**Estimated Time**: 1-2 days

- [ ] Rate limiting on all endpoints
- [ ] CORS configuration review
- [ ] SQL injection prevention audit
- [ ] XSS protection validation
- [ ] Authentication/authorization testing
- [ ] Dependency vulnerability scan

### 6.2 Load Testing
**Estimated Time**: 1 day

Test performance with realistic load:

```bash
# Load testing with 100 concurrent users
ab -n 10000 -c 100 http://localhost:5000/apis
```

### 6.3 Integration Testing
**Estimated Time**: 1-2 days

Create comprehensive test suite:

```python
# tests/test_api_discovery.py
def test_github_scanner_finds_apis():
    scanner = GitHubScanner(TEST_TOKEN)
    apis = scanner.scan_organization('test-org')
    assert len(apis) > 0

def test_risk_score_calculation():
    api = create_test_api()
    score = calculate_risk_score(api)
    assert 0 <= score <= 100

def test_zombie_detection():
    api = create_test_api_no_traffic()
    status = classify_api(api)
    assert status == APIStatus.ZOMBIE
```

### 6.4 Documentation Finalization
**Estimated Time**: 1 day

- [ ] API documentation complete
- [ ] Administrator guide
- [ ] User guide
- [ ] Architecture documentation
- [ ] Deployment guide
- [ ] Troubleshooting guide

### 6.5 User Acceptance Testing
**Estimated Time**: 1-2 days

- [ ] Test with representative users
- [ ] Collect feedback
- [ ] Make final adjustments
- [ ] Create training materials

### Deliverables
✅ Security audit complete, no critical issues
✅ Load testing passed (1000+ requests/sec)
✅ 80%+ code coverage with tests
✅ All documentation complete
✅ UAT sign-off received

---

## MVP Success Criteria

### Must Have (Critical Path)
- [x] User authentication system (JWT)
- [x] Database persistent storage
- [ ] API discovery from GitHub
- [ ] Security risk scoring
- [ ] Zombie API detection
- [ ] Dashboard showing metrics
- [ ] Inventory page with real data
- [ ] Risk Assessment page working
- [ ] Remediation workflow creation

### Should Have (High Priority)
- [ ] Background job scheduling
- [ ] Multi-source scanning (Docker, K8s)
- [ ] Automated alerts
- [ ] Export to CSV
- [ ] Monthly reports
- [ ] Role-based access control

### Nice to Have (Future)
- [ ] Machine learning risk scoring
- [ ] Advanced analytics
- [ ] Mobile app
- [ ] GraphQL API
- [ ] AI-powered remediation suggestions

---

## Deployment Strategy

### Development
```bash
npm run dev          # Frontend on 3001
python -m uvicorn main:app --reload --port 5000  # Backend
```

### Staging (Docker)
```bash
.\docker-run.ps1 -Environment dev
# LocalStack for AWS services simulation
```

### Production
```bash
.\docker-run.ps1 -Environment prod -Detach
# PostgreSQL + Redis + monitoring
```

---

## Key Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|--|--|--|--|
| GitHub API rate limits | High | Medium | Implement caching, use GitHub App tokens |
| Database scalability issues | Medium | High | Use connection pooling, add indexes, shard if needed |
| Scanner misses APIs | Medium | Medium | Multiple scanner types, community feedback |
| Risk scoring inaccuracy | Medium | Medium | Validate model with known data, iterate |
| Performance degradation | Low | High | Early load testing, CDN for static files |

---

## Resource Requirements

### Development Team
- 1 Backend Engineer (Python/FastAPI)
- 1 Frontend Engineer (React/TypeScript)
- 1 DevOps Engineer (Kubernetes/Docker)
- 0.5 QA Engineer (Testing)

### Infrastructure
- Development: Local machines + Docker
- Staging: Single EC2 instance or equivalent
- Production: Kubernetes cluster (3+ nodes) or managed container service

### External Services
- GitHub API (free tier supported)
- Docker Registry credentials
- Monitoring (ELK, DataDog, or similar)
- Alerting (Slack, PagerDuty, or similar)

---

## Timeline Summary

| Phase | Weeks | Status |
|--|--|--|
| Foundation (Auth, DB, UI) | 0 (Complete) | ✅ |
| Phase 1: Discovery | 2 | To Start |
| Phase 2: Assessment | 2 | To Start |
| Phase 3: Zombie Detection | 2 | To Start |
| Phase 4: Automation | 2 | To Start |
| Phase 5: Advanced Features | 2 | To Start |
| Phase 6: Hardening & Testing | 1 | To Start |
| **Total to MVP** | **6 weeks** | 25% Complete |

**Estimated Completion**: 8-10 weeks from now (by late February 2024)

---

## Post-MVP Roadmap (3-6 months)

### Q1 2024
- Multi-cloud support (AWS, GCP, Azure)
- Kubernetes API discovery
- Jira/Azure DevOps integration
- Advanced analytics dashboard

### Q2 2024
- Machine learning for risk scoring
- GraphQL API
- Mobile companion app
- Advanced RBAC & audit logging

### Q3 2024
- Third-party marketplace
- Custom scanner plugins
- On-premise deployment ready
- SLA tracking & reporting

---

**Last Updated**: January 21, 2024
**Next Review**: After Phase 1 completion
