# Zombie API Discovery and Defence Platform

## Overview
A comprehensive platform for continuous discovery, classification, and remediation of undocumented, deprecated, or unused ("Zombie") APIs across distributed banking infrastructure. This system addresses critical security and governance gaps by providing visibility, automated assessment, and decommissioning workflows.

## Problem Statement
Modern distributed banking systems accumulate zombie APIs due to rapid development, poor lifecycle management, and lack of centralized visibility. These create security risks (expanded attack surface, missing controls, data exposure) and compliance violations (PII/PCI mishandling).

## Solution Objectives
- **Continuous Discovery**: Scan gateways, code repos, network traffic, deployment environments
- **Lifecycle Classification**: Categorize APIs (Active, Deprecated, Orphaned, Zombie)
- **Security Assessment**: Evaluate authentication, encryption, rate limiting, data exposure
- **Automated Remediation**: Provide actionable insights and decommissioning workflows
- **Prevention**: Monitor for new APIs and prevent future proliferation

## Team Roles & Responsibilities

| Role | Responsibilities |
|------|-----------------|
| **Backend / API Discovery Engineer** | Build discovery pipelines (code parsing, network scanning, traffic inspection); maintain centralized inventory; implement usage tracking; ensure scalability |
| **Security & Risk Analysis Engineer** | Define lifecycle classifications; implement security assessment checks; design risk scoring model; generate remediation insights |
| **Frontend & DevOps Engineer** | Build dashboard for visibility; implement alerting; create decommissioning workflows; containerize/deploy system; schedule monitoring jobs |

## Project Structure

```
AegisAPI/
├── backend/                    # API discovery & inventory service
│   ├── src/
│   ├── tests/
│   └── requirements.txt
├── security-engine/            # Risk analysis & classification service
│   ├── src/
│   ├── tests/
│   └── requirements.txt
├── frontend/                   # Dashboard UI (React/Vue)
│   ├── src/
│   ├── public/
│   └── package.json
├── devops/                     # Deployment, orchestration, monitoring
│   ├── docker/
│   ├── kubernetes/
│   ├── terraform/
│   ├── monitoring/
│   └── scripts/
├── docs/                       # Architecture, setup, API specs
│   ├── architecture.md
│   ├── api-spec.md
│   └── deployment.md
├── .github/                    # GitHub workflows (CI/CD)
│   └── workflows/
├── docker-compose.yml
├── README.md
├── CONTRIBUTING.md
└── .gitignore
```

## Tech Stack

### Backend
- **Language**: Python 3.9+
- **Framework**: FastAPI / Flask
- **Database**: PostgreSQL
- **Message Queue**: RabbitMQ / Kafka

### Security Engine
- **Language**: Python 3.9+
- **Libraries**: Security assessment libraries, risk calculation engines

### Frontend
- **Framework**: React 18+ / Vue 3
- **State Management**: Redux / Vuex
- **Charting**: Chart.js / D3.js
- **Styling**: Tailwind CSS / Material-UI

### DevOps & Infrastructure
- **Containerization**: Docker
- **Orchestration**: Kubernetes / Docker Compose
- **IaC**: Terraform
- **Monitoring**: Prometheus + Grafana
- **CI/CD**: GitHub Actions / GitLab CI

## Getting Started

### Prerequisites
- Git configured with your name and email
- Docker & Docker Compose (for containerized development)
- Python 3.9+ (for backend/security services)
- Node.js 16+ (for frontend development)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/ciphernet01/AegisAPI
   cd AegisAPI
   ```

2. **Configure Git user (if not already done)**
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your@email.com"
   ```

3. **Create your feature branch**
   ```bash
   git checkout -b feature/your-feature
   ```

4. **Set up local environment** (Backend example)
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

5. **Run Docker Compose for full stack** (optional, for integration)
   ```bash
   docker-compose up
   ```

## Development Workflow

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed:
- Branching strategy
- PR and code review process
- Commit message standards
- Team member responsibilities
- Communication guidelines

## Key Features

### API Discovery
- Multi-source scanning (code repos, gateways, runtime traffic)
- Automatic inventory sync
- Usage tracking and correlation

### Classification & Risk Scoring
- Lifecycle state determination (Active/Deprecated/Orphaned/Zombie)
- Security control assessment
- Risk scoring based on exposure, usage, and posture

### Dashboard & Visibility
- Real-time API inventory with filtering
- Risk heatmaps and drill-down analytics
- Historical trends and compliance reporting

### Alerting & Workflows
- New API discovery notifications
- High-risk API escalation
- Approval workflows for decommissioning
- Automated disable/quarantine actions

### Continuous Monitoring
- Scheduled discovery jobs
- Pipeline integration
- Health checks and observability

## Documentation

- **[Architecture](docs/architecture.md)** - System design and data flows
- **[API Specification](docs/api-spec.md)** - Backend API endpoints
- **[Deployment Guide](docs/deployment.md)** - Production setup
- **[Contributing](CONTRIBUTING.md)** - Workflow and guidelines

## Support & Communication

- **Issues**: Use GitHub Issues for bugs, features, and questions
- **Discussions**: GitHub Discussions for design topics
- **Team Chat**: Use Slack/Teams for real-time communication (link in wiki)

## License

[Add your license]

---

**Last Updated**: March 25, 2026  
**Maintained by**: Zombie API Platform Team
