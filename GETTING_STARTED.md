# 🚀 Getting Started Guide

## Project Overview

**Zombie API Discovery & Defence Platform** - An automated solution for discovering, classifying, and remediating undocumented and deprecated APIs in enterprise infrastructure.

---

## 📋 Prerequisites

### Local Development

- **Node.js**: 18+ (for frontend development)
- **Python**: 3.11+ (for backend development)
- **npm/yarn**: Latest version
- **pip**: Python package manager
- **Git**: For version control

### Docker Deployment

- **Docker**: 20.10+
- **Docker Compose**: 1.29+

**Verification:**
```bash
node --version      # Should be 18+
python --version    # Should be 3.11+
docker --version    # Should be 20.10+
```

---

## ⚡ Quick Start (Development)

### 1. Clone the Repository
```bash
git clone https://github.com/ciphernet01/AegisAPI.git
cd AegisAPI
```

### 2. Setup Backend
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database initialization
python init_db.py
```

### 3. Setup Frontend
```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Update API URL in .env.local if needed
# VITE_API_URL=http://localhost:5000
```

### 4. Run Services

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn main:app --reload --port 5000
```

Backend runs at: **http://localhost:5000**
- API Docs: http://localhost:5000/docs
- Health Check: http://localhost:5000/health

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev -- --port 3001
```

Frontend runs at: **http://localhost:3001**

### 5. Access the Application

Open browser to: **http://localhost:3001**

Default login credentials (if demo data exists):
- Email: `test@example.com`
- Password: (check test data in code)

---

## 🐳 Docker Deployment

### Development (Local)

```bash
# Windows (PowerShell)
.\docker-run.ps1 -Environment dev

# Linux/Mac
bash docker-run.sh dev
```

**What starts:**
- Backend: http://localhost:5000
- Frontend: http://localhost:3000
- SQLite Database: Auto-created

**Stop services:**
```bash
# Windows
.\docker-run.ps1 -Environment dev -Stop

# Linux/Mac
bash docker-run.sh dev  # Then press Ctrl+C
```

### Production (Full Stack)

1. **Prepare configuration:**
```bash
cp .env.example .env
# Edit .env with production values
```

2. **Start services:**
```bash
# Windows (PowerShell)
.\docker-run.ps1 -Environment prod -Detach

# Linux/Mac
bash docker-run.sh prod
```

3. **Verify services:**
```bash
docker-compose -f devops/docker/docker-compose.prod.yml ps
```

4. **View logs:**
```bash
# Windows
.\docker-run.ps1 -Environment prod -Logs

# Linux/Mac
docker-compose -f devops/docker/docker-compose.prod.yml logs -f
```

---

## 📁 Project Structure

```
AegisAPI/
├── backend/
│   ├── main.py                 # FastAPI entry point
│   ├── config.py               # Configuration
│   ├── requirements.txt         # Python dependencies
│   ├── database/
│   │   ├── db.py              # Database setup
│   │   └── models.py          # ORM models
│   ├── routes/
│   │   ├── auth_routes.py      # Authentication endpoints
│   │   └── api_routes.py       # API discovery endpoints
│   ├── services/
│   │   ├── discovery_service.py # API discovery logic
│   │   └── auth_service.py      # JWT authentication
│   └── database_files/
│       └── app.db             # SQLite database (dev)
│
├── frontend/
│   ├── src/
│   │   ├── main.tsx           # React entry point
│   │   ├── App.tsx            # Main app component
│   │   ├── pages/             # Page components
│   │   ├── components/        # Reusable components
│   │   ├── context/           # React context (auth, theme)
│   │   └── services/          # API services
│   ├── package.json           # NPM dependencies
│   └── vite.config.ts         # Vite configuration
│
├── devops/
│   ├── docker/
│   │   ├── Dockerfile.backend
│   │   ├── Dockerfile.frontend
│   │   ├── docker-compose.yml    # Full stack
│   │   ├── docker-compose.dev.yml # Development
│   │   └── docker-compose.prod.yml# Production
│   ├── kubernetes/            # K8s manifests
│   └── terraform/             # IaC scripts
│
├── docs/                       # Documentation
├── .env.example               # Environment template
├── DEVOPS.md                  # DevOps guide
└── README.md                  # Project readme
```

---

## 🔐 Authentication

The platform uses **JWT (JSON Web Tokens)** for authentication.

### Login Flow

1. User enters credentials on login page
2. Backend validates and returns JWT token
3. Frontend stores token in `localStorage`
4. All API requests include token in header: `Authorization: Bearer <token>`
5. Token auto-refreshes on expiry

### User Roles

- **Admin**: Full access, can manage all APIs and settings
- **Analyst**: Can view APIs, create assessments
- **Read-Only**: View-only access

---

## 🧪 Development Workflow

### Make Changes to Backend

```bash
cd backend

# Backend has auto-reload enabled, just edit files
# Changes reflect immediately

# Run tests (if available)
pytest

# Check code quality
flake8 .
```

### Make Changes to Frontend

```bash
cd frontend

# Frontend has hot-reload enabled
# Edit files and see changes in browser immediately

# Build for production
npm run build

# Preview production build
npm run preview
```

### Database Changes

1. Update model in `backend/database/models.py`
2. Restart backend (it auto-migrates on restart)
3. Or manually run:
```bash
cd backend
python init_db.py
```

---

## 🚨 Troubleshooting

### "Connection refused" on port 5000

```bash
# Check if backend is running
netstat -ano | findstr :5000

# If not, start backend:
cd backend
python -m uvicorn main:app --reload --port 5000
```

### "Cannot find module" errors in frontend

```bash
cd frontend

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
rm -rf .vite

# Restart dev server
npm run dev
```

### Database errors

```bash
# Clear SQLite database
rm backend/database_files/app.db

# Reinitialize
cd backend
python init_db.py
```

### Port already in use

Change port in command:
```bash
# Frontend on different port
npm run dev -- --port 3002

# Backend on different port
python -m uvicorn main:app --port 5001

# Update .env.local to point to new backend port
```

---

## 📚 Key Technologies

| Layer | Technology | Version |
|--|--|--|
| **Backend** | FastAPI | 0.104.1 |
| **Database** | SQLite (dev) / PostgreSQL (prod) | 3.x / 16 |
| **Cache** | Redis | 7.x |
| **Frontend** | React + TypeScript | 18.x |
| **Build Tool** | Vite | 5.4.21 |
| **Styling** | Tailwind CSS | 3.x |
| **Authentication** | JWT | HS256 |
| **Containerization** | Docker | 20.10+ |

---

## 🔗 Useful Links

- **API Documentation**: http://localhost:5000/docs (Swagger UI)
- **Frontend Dashboard**: http://localhost:3001 or http://localhost:3000
- **Backend Health**: http://localhost:5000/health
- **DevOps Guide**: [DEVOPS.md](./DEVOPS.md)
- **API Specification**: [docs/api-spec.md](./docs/api-spec.md)

---

## 📝 Next Steps

1. ✅ Complete setup using this guide
2. Explore the dashboard at http://localhost:3001
3. Review [DEVOPS.md](./DEVOPS.md) for production deployment
4. Check [docs/api-spec.md](./docs/api-spec.md) for API details
5. Start implementing API discovery features

---

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and test locally
3. Commit with clear messages: `git commit -m "feat: description"`
4. Push to branch: `git push origin feature/your-feature`
5. Open Pull Request

---

## 📞 Support

- **Issues**: GitHub Issues
- **Docs**: See DEVOPS.md and backend/README.md
- **Architecture Decisions**: Check docs/ folder

---

## ✨ Quick Commands Reference

```bash
# Backend
cd backend && python -m uvicorn main:app --reload --port 5000

# Frontend
cd frontend && npm run dev -- --port 3001

# Docker Dev
.\docker-run.ps1 -Environment dev  # Windows

# Docker Prod
.\docker-run.ps1 -Environment prod -Detach  # Windows

# View Logs
docker-compose logs -f

# Stop Services
docker-compose down

# Database
python backend/init_db.py

# Build Frontend
npm run build

# Run Tests
pytest
```

---

**Happy coding! 🚀**
