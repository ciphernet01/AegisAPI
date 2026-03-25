# Getting Started - Team Setup Guide

Welcome to the **Zombie API Discovery and Defence Platform**! This guide helps you set up your development environment for local work and understand the repository structure.

## Prerequisites

### For Backend Developers
- Python 3.11+
- pip or poetry
- PostgreSQL client (psql)
- Redis client (optional)

### For Frontend Developers
- Node.js 18+
- npm or yarn
- Git

### For DevOps Engineers
- Docker & Docker Compose
- kubectl
- Helm 3.0+
- Terraform 1.0+ (for AWS infrastructure)

## Quick Start (Choose Your Role)

### Frontend Developer Setup (60 seconds)

```bash
# 1. Clone and navigate
git clone https://github.com/your-org/AegisAPI.git
cd AegisAPI

# 2. Configure Git
git config --global user.name "Your Full Name"
git config --global user.email "your.email@company.com"

# 3. Create a feature branch
git checkout -b feature/your-feature-name

# 4. Install dependencies
cd frontend
npm install

# 5. Start development server
npm run dev
```

**Access:** http://localhost:3000

**Available commands:**
```bash
npm run dev         # Start dev server
npm run build       # Build for production
npm run lint        # Run ESLint
npm run format      # Format code with Prettier
npm run test        # Run tests
```

### Backend Developer Setup (2 minutes)

```bash
# 1. Start backend services
cd devops/scripts
chmod +x deploy-local.sh
./deploy-local.sh

# 2. Wait for services to initialize (~30 seconds)

# 3. Test backend API
curl http://localhost:8000/health

# 4. View logs
docker-compose logs -f backend
```

**Access:**
- Backend API: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### DevOps Engineer Setup (5 minutes)

```bash
# 1. Verify Docker
docker --version
docker-compose --version

# 2. Start local environment
cd devops/scripts
chmod +x deploy-local.sh
./deploy-local.sh

# 3. Verify all services
kubectl get pods  # if using Kubernetes
docker-compose ps # if using Docker Compose

# 4. Check monitoring
# Grafana: http://localhost:3001
# Prometheus: http://localhost:9090
```

## Repository Structure

```
AegisAPI/
├── frontend/              # React dashboard
│   ├── src/              # Source code
│   ├── tests/            # Unit tests
│   ├── package.json
│   └── README.md
├── backend/              # API discovery service
│   ├── src/
│   ├── tests/
│   └── requirements.txt
├── security-engine/      # Risk assessment
│   ├── src/
│   ├── tests/
│   └── requirements.txt
├── devops/               # Infrastructure & deployment
│   ├── docker/          # Docker images & compose
│   ├── kubernetes/      # K8s manifests
│   ├── terraform/       # AWS infrastructure
│   ├── monitoring/      # Prometheus & Grafana
│   ├── scripts/         # Deployment scripts
│   └── README.md
├── docs/                 # Documentation
│   ├── architecture.md
│   ├── deployment.md
│   └── api-spec.md
├── .github/workflows/    # CI/CD pipelines
├── CONTRIBUTING.md       # Contributing guidelines
├── README.md
└── .gitignore
```

## Development Workflow

### 1. Create Feature Branch
```bash
git checkout main
git pull origin main
git checkout -b feature/dashboard-risk-heatmap
```

### 2. Make Changes
```bash
# Frontend example
cd frontend
npm run lint
npm run format
npm run test

# Commit often
git add .
git commit -m "[Frontend] Add: Risk heatmap visualization component"
git push origin feature/dashboard-risk-heatmap
```

### 3. Open Pull Request
- Wait for CI/CD checks to pass
- Add description of changes
- Request reviews from teammates
- Address feedback

### 4. Merge & Deploy
- Squash and merge to main
- Delete feature branch
- Deployment triggered automatically

## Common Tasks

### Running Tests

**Frontend:**
```bash
cd frontend
npm run test              # Run tests
npm run test:coverage    # With coverage report
npm run test:ui          # With UI
```

**Backend:**
```bash
cd backend
python -m pytest tests/
python -m pytest --cov  # With coverage
```

### Linting & Formatting

**Frontend:**
```bash
cd frontend
npm run lint            # Check code quality
npm run format          # Auto-format code
npm run type-check      # TypeScript checks
```

**Backend:**
```bash
cd backend
black .                 # Format Python code
flake8 .               # Lint Python code
mypy .                 # Type checking
```

### Building Docker Images

```bash
cd devops/scripts
chmod +x build-push-images.sh
./build-push-images.sh v1.0.0
```

### Deploying to Kubernetes

```bash
cd devops/scripts
chmod +x deploy-k8s.sh
./deploy-k8s.sh staging   # Deploy to staging
./deploy-k8s.sh prod      # Deploy to production
```

## Troubleshooting

### Port Already in Use

```bash
# Kill process using port
lsof -i :3000  # Find process
kill -9 <PID>  # Kill it

# Or use different port
export PORT=3001
npm run dev
```

### Docker Daemon Not Running

```bash
# macOS
open /Applications/Docker.app

# Linux
sudo systemctl start docker

# Windows
Open Docker Desktop
```

### Database Connection Failed

```bash
# Check if postgres is running
docker-compose ps

# Restart postgres
docker-compose restart postgres

# Check logs
docker-compose logs postgres
```

### Node Modules Issues

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Environment Variables

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
VITE_APP_ENV=development
VITE_ANALYTICS_ID=
```

### Backend (.env)
```env
DATABASE_URL=postgresql://aegisdb:changeme@localhost:5432/aegis_api
REDIS_URL=redis://localhost:6379
API_ENV=development
```

## Useful Commands

```bash
# View running services
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs frontend

# Execute command in container
docker-compose exec backend python script.py
docker-compose exec -T postgres psql -U aegisdb

# Restart services
docker-compose restart
docker-compose restart backend

# Stop all services
docker-compose down

# Remove everything (careful!)
docker-compose down -v

# Kubernetes status
kubectl get pods -n aegis
kubectl logs deployment/frontend -n aegis
kubectl describe pod <pod-name> -n aegis
```

## Getting Help

1. **Code Questions** → Open GitHub Issue
2. **Design Questions** → Team Slack channel
3. **Environment Issues** → DevOps engineer
4. **API Questions** → Check [api-spec.md](docs/api-spec.md)
5. **General Help** → See [CONTRIBUTING.md](CONTRIBUTING.md)

## Next Steps

1. Review the [project architecture](docs/architecture.md)
2. Read the [API specification](docs/api-spec.md)
3. Check out existing [GitHub Issues](https://github.com/your-org/AegisAPI/issues)
4. Pick a task and create a feature branch
5. Follow the [contribution guidelines](CONTRIBUTING.md)

## Resources

- **Architecture**: [docs/architecture.md](docs/architecture.md)
- **Deployment**: [devops/README.md](devops/README.md)
- **Frontend**: [frontend/README.md](frontend/README.md)
- **API Spec**: [docs/api-spec.md](docs/api-spec.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Questions?** Ping the team on Slack or open a GitHub issue!

Happy coding! 🚀
