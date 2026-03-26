# 🛡️ Aegis API - Zombie API Discovery & Defence Platform

<div align="center">

**Enterprise solution for discovering, analyzing, and remediating undocumented, deprecated, and zombie APIs across infrastructure**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-brightgreen.svg)](docs/VERSION.md)
[![Status](https://img.shields.io/badge/status-MVP%20Development-yellow.svg)](#-current-status)

[Quick Start](#-quick-start) • [Features](#-features) • [Documentation](#-documentation) • [Architecture](#-architecture) • [Contributing](#-contributing)

</div>

---

## 🎯 The Problem

Enterprises suffer from **API sprawl** - undocumented, deprecated, and unused APIs proliferate across infrastructure:

- ❌ **Shadow APIs**: Undocumented endpoints created by teams
- ❌ **Zombie APIs**: Unused APIs consuming resources and creating security risks
- ❌ **Deprecated APIs**: Old APIs still running but no longer maintained
- ❌ **Security Gaps**: APIs without proper authentication, documentation, or monitoring
- ❌ **Manual Processes**: No automated way to discover, assess, or remediate issues

**Impact**: Security vulnerabilities, compliance violations, wasted infrastructure costs, operational chaos.

---

## ✨ The Solution

**Aegis API** is a comprehensive platform that:

1. 🔍 **Discovers** APIs automatically from multiple sources (GitHub, Docker, Kubernetes, AWS)
2. 📊 **Analyzes** security posture, risk levels, and lifecycle status
3. 🧟 **Identifies** zombie APIs (unused, undocumented, deprecated)
4. 🤖 **Automates** remediation workflows and compliance actions
5. 📈 **Monitors** API landscape continuously with real-time alerts
6. 📋 **Reports** on API governance and trends

---

## 🚀 Features

### Core Capabilities

#### 🔐 Authentication & Authorization
- JWT-based authentication with refresh tokens
- Role-based access control (Admin, Analyst, Read-Only)
- Audit logging of all actions
- Secure token storage and rotation

#### 🔍 API Discovery
- **GitHub Scanner**: Find APIs in repositories (OpenAPI specs, REST endpoints, Docker Compose)
- **Docker Registry Scanner**: Discover containerized APIs
- **Kubernetes Scanner**: Identify Kubernetes services
- **AWS Scanner**: Detect API Gateway, Lambda, and managed services (coming soon)
- **Deduplication**: Automatically merge duplicate API records
- **Scheduled Discovery**: Continuous scanning every 6 hours

#### 📊 Security Assessment
- **Risk Scoring**: 0-100 risk scores based on multiple factors
- **Security Findings**: Automated detection of:
  - Missing authentication
  - Undocumented endpoints
  - Orphaned APIs (no owner)
  - Exposed to internet
  - No HTTPS
  - High error rates
- **Risk Classification**: Critical, High, Medium, Low
- **Continuous Monitoring**: Periodic reassessment of all APIs

#### 🧟 Zombie Detection
- **Traffic Analysis**: Detect APIs with no activity in 90+ days
- **Usage Metrics**: Track calls, error rates, latency trends
- **Orphan Detection**: APIs without clear ownership
- **Automatic Classification**: Active → Deprecated → Zombie
- **Workflow Triggers**: Auto-create remediation tasks

#### 🤖 Remediation Automation
- **Workflow Creation**: Tasks for authentication, documentation, decommissioning
- **Status Tracking**: Track remediation progress
- **Automated Actions**: Execute approved remediation steps
- **Notifications**: Alerts to owners and security teams
- **Compliance Reporting**: Document remediation efforts

#### 📈 Monitoring & Analytics
- **Real-Time Dashboard**: API metrics, risk distribution, zombie count
- **Historical Trends**: Track changes over time
- **Monthly Reports**: Governance and compliance reporting
- **Alerting**: Slack, email notifications for critical issues
- **Export**: CSV, JSON, API access to all data

---

## 📋 Current Status

### ✅ Completed (MVP Foundation - 25%)
- JWT authentication system (register, login, token refresh)
- Database schema (SQLAlchemy ORM with 5 tables)
- Frontend UI (6 main pages: Dashboard, Inventory, Risk Assessment, Remediations, Settings, Profile)
- Backend API route structure
- Development environment (SQLite + hot-reload)
- Production infrastructure (Docker Compose, PostgreSQL, Redis)
- DevOps documentation and deployment scripts

### 🟡 In Progress (4-6 weeks to MVP)
- API discovery framework (GitHub, Docker, OpenAPI parsers)
- Security assessment engine (risk scoring, findings generation)
- Zombie detection logic (usage analysis, classification)
- Background job scheduling (discovery, assessment, detection)
- Remediation workflow automation

### 🔴 Planned (Post-MVP)
- Advanced analytics and reporting
- Multi-cloud support (AWS, GCP, Azure)
- Machine learning risk scoring
- GraphQL API
- Third-party integrations (Jira, ServiceNow, Azure DevOps)
- On-premise deployment support

---

## 🏗️ Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React + Vite)                 │
│  Dashboard │ Inventory │ Risk │ Remediations │ Settings     │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTP/HTTPS
                             │
┌────────────────────────────────────────────────────────────┐
│                 Backend (FastAPI + SQLAlchemy)              │
│  ┌────────────┬──────────────┬─────────────┬────────────┐  │
│  │   Auth     │  Discovery   │ Assessment  │Remediation │  │
│  │  Routes    │   Services   │  Services   │  Services  │  │
│  └────────────┴──────────────┴─────────────┴────────────┘  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │     Background Jobs (APScheduler)                   │   │
│  │  • Discover APIs (every 6h)                        │   │
│  │  • Assess Security (every 12h)                     │   │
│  │  • Detect Zombies (every 24h)                      │   │
│  └─────────────────────────────────────────────────────┘   │
└────────┬───────────────────────────────────────┬────────────┘
         │                                       │
    ┌────▼─────────┐                  ┌─────────▼────┐
    │  SQLite/     │                  │   External   │
    │  PostgreSQL  │                  │   Scanners   │
    │  Database    │                  │  • GitHub    │
    │              │                  │  • Docker    │
    └──────────────┘                  │  • K8s       │
                                      │  • AWS       │
                                      └──────────────┘
```

### Technology Stack

| Layer | Technology | Version |
|--|--|--|
| **Frontend** | React + TypeScript | 18.x |
| **Build** | Vite | 5.4.21 |
| **Styling** | Tailwind CSS | 3.x |
| **State** | Zustand | 4.x |
| **API Client** | Axios | 1.x |
| **Backend** | FastAPI | 0.104+ |
| **Async** | AsyncIO + APScheduler | 3.10+ |
| **Database** | SQLAlchemy | 2.0+ |
| **Auth** | JWT + Bcrypt | - |
| **Dev DB** | SQLite | 3.x |
| **Prod DB** | PostgreSQL | 16+ |
| **Cache** | Redis | 7.x |
| **Container** | Docker | 20.10+ |

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- Git
- (Optional) Docker 20.10+

### Local Development (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/ciphernet01/AegisAPI.git
cd AegisAPI

# 2. Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python init_db.py

# 3. Frontend setup
cd ../frontend
npm install

# 4. Start backend (Terminal 1)
cd backend
python -m uvicorn main:app --reload --port 5000

# 5. Start frontend (Terminal 2)
cd frontend
npm run dev -- --port 3001
```

Open http://localhost:3001 in browser.

### Docker (1 command)

```bash
# Development
.\docker-run.ps1 -Environment dev  # Windows
bash docker-run.sh dev              # Linux/Mac

# Production (requires .env configuration)
.\docker-run.ps1 -Environment prod -Detach  # Windows
```

**Full guide**: See [GETTING_STARTED.md](./GETTING_STARTED.md)

---

## 📚 Documentation

| Document | Purpose |
|--|--|
| [GETTING_STARTED.md](./GETTING_STARTED.md) | Quick start guides, troubleshooting |
| [API_SPECIFICATION.md](./docs/API_SPECIFICATION.md) | Complete API endpoint documentation |
| [IMPLEMENTATION_ROADMAP.md](./docs/IMPLEMENTATION_ROADMAP.md) | 6-week MVP development plan with detailed phases |
| [DEVOPS.md](./DEVOPS.md) | Deployment guides, Docker setup, monitoring |
| [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) | System design and component interactions |

---

## 🔗 Key Endpoints

### Authentication
- `POST /auth/register` - Create new user
- `POST /auth/login` - Login and get JWT
- `POST /auth/refresh` - Refresh access token
- `GET /auth/me` - Get current user profile

### APIs (Discovery & Management)
- `GET /apis` - List all discovered APIs
- `GET /apis/{id}` - Get API details
- `GET /apis/search` - Search with filters
- `GET /apis/stats` - Get statistics
- `POST /apis` - Manually add API

### Security
- `GET /apis/{id}/findings` - Get security findings
- `GET /apis/{id}/risk-score` - Calculate risk score

### Remediation
- `GET /remediations` - List workflows
- `POST /remediations` - Create workflow
- `PATCH /remediations/{id}` - Update workflow

**Complete API docs**: [API_SPECIFICATION.md](./docs/API_SPECIFICATION.md)
Interactive API docs: `http://localhost:5000/docs` (Swagger UI)

---

## 🛠️ Development

### Project Structure

```
AegisAPI/
├── backend/                 # FastAPI backend
│   ├── main.py             # Entry point
│   ├── config.py           # Configuration
│   ├── database/           # ORM models & setup
│   ├── routes/             # API endpoints
│   └── services/           # Business logic
├── frontend/               # React frontend
│   ├── src/
│   │   ├── pages/         # Page components
│   │   ├── components/    # Reusable components
│   │   └── services/      # API integration
│   └── vite.config.ts     # Vite configuration
├── devops/                # Docker & deployment
│   ├── docker/           # Docker Compose configs
│   └── kubernetes/       # K8s manifests (coming)
├── docs/                 # Documentation
└── GETTING_STARTED.md   # Quick start guide
```

### Making Changes

**Backend:**
```bash
cd backend
python -m uvicorn main:app --reload  # Auto-reloads on save
```

**Frontend:**
```bash
cd frontend
npm run dev  # Auto-refreshes on save
```

### Running Tests

```bash
# Backend tests (when test suite is created)
cd backend && pytest

# Frontend tests
cd frontend && npm run test
```

---

## 🚢 Deployment

### Development (Local)
```bash
.\docker-run.ps1 -Environment dev
```
Frontend: http://localhost:3000
Backend: http://localhost:5000

### Production
```bash
cp .env.example .env
# Edit .env with prod values
.\docker-run.ps1 -Environment prod -Detach
```

**Detailed guide**: See [DEVOPS.md](./DEVOPS.md)

---

## 📊 MVP Roadmap

**Phase 1: API Discovery** (Week 1-2)
- GitHub repository scanner
- OpenAPI/Swagger parser
- Docker registry scanner
- Multi-source consolidation

**Phase 2: Security Assessment** (Week 2-3)
- Authentication detection
- Risk scoring algorithm
- Security finding generation
- Risk Assessment page

**Phase 3: Zombie Detection** (Week 3-4)
- Traffic analysis
- Usage metrics collection
- Zombie classification
- Auto-workflow creation

**Phase 4: Monitoring & Automation** (Week 4-5)
- Background job scheduling
- Continuous discovery
- Workflow execution
- Alerting system

**Phase 5: Advanced Features** (Week 5-6)
- Analytics & reporting
- Search & filtering
- Export to CSV/JSON
- Third-party integrations

**Phase 6: Hardening & Testing** (Week 6)
- Security audit
- Load testing
- Integration tests
- UAT sign-off

**Target Completion**: 6 weeks (Late February 2024)

---

## 🤝 Contributing

### Workflow

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes with clear commits: `git commit -m "feat: description"`
3. Push to branch: `git push origin feature/your-feature`
4. Open Pull Request with description

### Code Standards

- **Backend**: PEP 8, type hints, >80% test coverage
- **Frontend**: ESLint/Prettier, TypeScript, component-based
- **Git**: Meaningful commit messages, atomic commits
- **Docs**: Update README and docs/ for changes

### Local Development Tips

```bash
# Format code
black backend/      # Python
prettier frontend/  # JavaScript

# Check types
mypy backend/
tsc frontend/

# Lint
flake8 backend/
npm run lint frontend/
```

---

## 🐛 Troubleshooting

### Backend won't connect to database
```bash
# SQLite (development)
rm backend/database_files/app.db
python backend/init_db.py
```

### Port already in use
```bash
# Find what's using port 5000
netstat -ano | findstr :5000

# Use different port
python -m uvicorn main:app --port 5001
```

### Frontend can't reach backend
- Check backend is running: `netstat -ano | findstr :5000`
- Update `.env.local`: `VITE_API_URL=http://localhost:5000`
- Restart frontend: `npm run dev`

**More help**: See [GETTING_STARTED.md](./GETTING_STARTED.md#-troubleshooting)

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/ciphernet01/AegisAPI/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ciphernet01/AegisAPI/discussions)
- **Documentation**: [docs/](./docs/)

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

- FastAPI framework and documentation
- React and TypeScript communities
- Open source contributors

---

## 📈 Statistics

- **Codebase Size**: ~2,500 lines (backend + frontend)
- **Frontend Build**: 1426 modules, 269.6 kB
- **API Endpoints**: 15+ fully documented
- **Database Tables**: 5 (users, apis, security_findings, remediation_workflows, audit_logs)
- **Development Time**: 2 weeks (foundation)
- **MVP Completion**: 6 weeks (estimated)

---

## 🗺️ Project Roadmap (High Level)

```
Current (MVP)
    ↓
API Discovery Engine (Week 1-2)
    ↓
Security Assessment (Week 2-3)
    ↓
Zombie Detection (Week 3-4)
    ↓
Monitoring & Automation (Week 4-5)
    ↓
Advanced Features (Week 5-6)
    ↓
Production MVP Release (Week 6)
    ↓
Version 1.0 (March 2024)
    ↓
Enterprise Features (Q2 2024)
    ↓
Multi-Cloud Support (Q3 2024)
```

---

## 💡 Future Vision

By Q3 2024, **Aegis API** will be the industry standard for:
- ✅ API discovery and governance
- ✅ Automated API security assessment
- ✅ Zombie API elimination
- ✅ Compliance and audit reporting
- ✅ Multi-cloud and on-premise support

Helping enterprises:
- 🎯 Reduce API sprawl by 80%
- 🎯 Cut security vulnerability remediation time by 60%
- 🎯 Achieve API governance compliance
- 🎯 Reduce infrastructure waste

---

<div align="center">

**Built with ❤️ for enterprise API governance**

[Back to top](#-aegis-api---zombie-api-discovery--defence-platform)

</div>
