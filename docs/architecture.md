# Architecture Overview

## System Design

### Core Components

1. **Frontend Dashboard** (React + TypeScript)
   - API inventory with advanced filtering
   - Risk heatmap visualization
   - Remediation tracking interface
   - Decommissioning workflows
   - Real-time alerts

2. **API Discovery Service** (Python + FastAPI)
   - Code repository scanning (Git, GitHub, GitLab)
   - API gateway inspection (Kong, AWS API Gateway, Azure APIM)
   - Network traffic analysis (service mesh telemetry)
   - Runtime API detection
   - Centralized inventory management

3. **Security & Risk Assessment Engine** (Python)
   - Authentication evaluation (OAuth2, API keys, mTLS, none)
   - Encryption validation (TLS version, data at rest)
   - Rate limiting checks
   - PII/sensitive data detection
   - Risk scoring algorithm
   - Compliance gap identification

4. **Data Layer** (PostgreSQL + Redis)
   - API inventory with metadata
   - Security assessment results
   - Remediation tracking
   - Audit logs
   - Session caching

### Data Flow

```
API Sources
├── Git Repositories
├── API Gateways
├── Service Mesh
└── Runtime Traffic
    ↓
API Discovery Service
    ├── Parse & Extract metadata
    ├── Deduplicate across sources
    ├── Detect new/orphaned APIs
    └── Store in Inventory DB
        ↓
    Security Assessment Engine
        ├── Evaluate auth methods
        ├── Check encryption
        ├── Assess data exposure
        └── Calculate risk score
            ↓
        Frontend Dashboard
            ├── Display inventory
            ├── Visualize risk
            ├── Track remediations
            └── Execute decommissioning
```

## API Classification Logic

```
API State Classification

Active
  ├─ Regular traffic (> 100 requests/day)
  ├─ Known owner
  └─ Current version

Deprecated
  ├─ Marked for sunset
  ├─ Replacement announced
  └─ Timeline defined

Orphaned
  ├─ No clear owner
  ├─ Minimal traffic
  └─ Legacy codebase

Zombie
  ├─ No traffic (X days)
  ├─ Missing owner
  ├─ Outdated security
  └─ HIGH PRIORITY FOR REMOVAL
```

## Risk Scoring Model

**Risk Score = (Usage Factor × 0.3) + (Security Factor × 0.5) + (Compliance Factor × 0.2)**

### Usage Factor
- 0-30: High usage, many callers → Lower score
- 30-70: Moderate usage → Medium score
- 70-100: Zero/minimal usage → Higher score

### Security Factor
- 0-30: Modern auth, strong encryption → Lower score
- 30-70: Missing controls, weak standards → Medium score
- 70-100: No authentication, exposed data → Higher score

### Compliance Factor
- PII exposure: +20 points
- Financial data handling: +15 points
- Regulatory scope (PCI, HIPAA): +10 points
- Untracked audit access: +10 points

## Security Assessment Checks

| Check | Type | Severity |
|-------|------|----------|
| No Authentication | Critical | High |
| TLS < 1.2 | Critical | High |
| Exposed API Key in Code | Critical | High |
| No Rate Limiting | Major | Medium |
| Data without Encryption | Major | Medium |
| Missing Audit Logging | Major | Medium |
| Hardcoded Credentials | Critical | High |
| No Input Validation | Major | Medium |
| CORS too Permissive | Minor | Low |
| Old Framework Version | Minor | Low |

## Decommissioning Workflow States

```
Discovery
    ↓
Risk Assessment
    ↓
Owner Notification (Email/Slack)
    ↓
Impact Analysis (Dependent services?)
    ↓
Approval Gate (Manager review)
    ↓
Deprecation Notice (30-day warning)
    ↓
Traffic Blocking (Start returning HTTP410)
    ↓
Dependency Migration (Client updates)
    ↓
Resource Cleanup (Remove from gateway/cluster)
    ↓
Archive & Audit Log
```

## Technology Stack

### Frontend
- **Framework**: React 18 + TypeScript
- **Styling**: Tailwind CSS
- **State**: Zustand
- **Charting**: Recharts
- **HTTP**: Axios
- **Build**: Vite

### Backend
- **Runtime**: Python 3.11
- **Framework**: FastAPI
- **Database**: PostgreSQL 16
- **Cache**: Redis 7
- **ORM**: SQLAlchemy
- **Async**: Uvicorn + asyncio

### DevOps
- **Containerization**: Docker
- **Orchestration**: Kubernetes (EKS/AKS/GKE)
- **Infrastructure**: Terraform
- **Monitoring**: Prometheus + Grafana
- **Logging**: CloudWatch / ELK
- **CI/CD**: GitHub Actions
- **Registry**: ECR / Docker Hub

## High Availability Design

### Load Balancing
- Frontend: Nginx ingress with load balancing
- Backend: Kubernetes service with round-robin
- Database: Read replicas for scaling queries

### Fault Tolerance
- **Pod Replicas**: Min 2 per service
- **Pod Disruption Budgets**: Minimum 1 available
- **Health Checks**: Liveness + Readiness probes
- **Auto-healing**: Automatic pod restart on failure

### Data Durability
- **Database**: Multi-AZ RDS with automated backups
- **Redis**: Sentinel for automatic failover
- **State**: Persistent volumes with snapshots

## Security Architecture

### Network Security
- VPC isolation with public/private subnets
- Security groups restricting traffic
- Network policies for pod-to-pod communication
- TLS encryption for all API calls

### Identity & Access
- Kubernetes RBAC for cluster access
- IAM roles for AWS service access
- Secrets Manager for credential rotation
- Audit logging for all privileged actions

### Data Protection
- Encrypted volumes (EBS, RDS, ElastiCache)
- TLS 1.3 for data in transit
- Database encryption at rest (KMS)
- Secrets encrypted in Kubernetes

### Compliance Controls
- Audit logs retained for compliance
- Regular security scanning (Trivy, CodeQL)
- Vulnerability management with CVE tracking
- SOC2 / ISO 27001 alignment
