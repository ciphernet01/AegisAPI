# DevOps & Deployment Guide

## Overview

The Zombie API Discovery & Defence Platform can run in two modes:
- **Development**: SQLite database, hot-reload, quick setup
- **Production**: PostgreSQL + Redis, scalable, monitoring included

---

## Development Environment

### Quick Start

```bash
# Windows (PowerShell)
.\docker-run.ps1 -Environment dev

# Linux/Mac
bash docker-run.sh dev
```

This will start:
- ✅ Backend API (http://localhost:5000)
- ✅ Frontend Dashboard (http://localhost:3000)
- ✅ SQLite Database (auto-created)

### Manual Local Development (Without Docker)

```bash
# Terminal 1: Backend
cd backend
python -m uvicorn main:app --reload --port 5000

# Terminal 2: Frontend
cd frontend
npm run dev -- --port 3001
```

Access: http://localhost:3001

### Environment Setup (Local)

1. **Backend** (`.env.local`):
```env
DATABASE_URL=sqlite:///./database_files/app.db
USE_SQLITE=true
DEBUG=True
SECRET_KEY=development-secret-key
```

2. **Frontend** (`.env.local`):
```env
VITE_API_URL=http://localhost:5000
VITE_APP_ENV=development
```

---

## Production Deployment

### Prerequisites

- Docker & Docker Compose installed
- `.env` file with production values (copy from `.env.example`)

### Configuration

1. Copy environment template:
```bash
cp .env.example .env
```

2. Update `.env` with production values:
```env
DB_USER=secure_username
DB_PASSWORD=very_secure_password
DB_NAME=aegis_production
SECRET_KEY=generate_strong_secret_key_here
ALLOWED_ORIGINS=https://your-domain.com
```

### Deploy

```bash
# Windows (PowerShell)
.\docker-run.ps1 -Environment prod

# Linux/Mac
bash docker-run.sh prod
```

This will start:
- ✅ Backend API (port 8000)
- ✅ Frontend Dashboard (port 3000)
- ✅ PostgreSQL Database (port 5432)
- ✅ Redis Cache (port 6379)

### Verify Deployment

```bash
# Check services status
docker-compose -f devops/docker/docker-compose.prod.yml ps

# View logs
docker-compose -f devops/docker/docker-compose.prod.yml logs -f

# Test API
curl -X GET http://localhost:8000/health

# Test Frontend
curl -X GET http://localhost:3000
```

### Manage Services

```bash
# Stop services
.\docker-run.ps1 -Environment prod -Stop

# View logs
.\docker-run.ps1 -Environment prod -Logs

# Remove everything (including data!)
.\docker-run.ps1 -Environment prod -Down

# Restart after changes
docker-compose -f devops/docker/docker-compose.prod.yml restart backend
```

---

## Docker Files

### Structure

```
devops/
├── docker/
│   ├── Dockerfile.backend      # Backend service container
│   ├── Dockerfile.frontend     # Frontend service container
│   ├── docker-compose.yml      # Full stack (original)
│   ├── docker-compose.dev.yml  # Development (SQLite)
│   └── docker-compose.prod.yml # Production (PostgreSQL + Redis)
├── kubernetes/
│   ├── deployment.yaml
│   ├── policies.yaml
│   └── cronjobs.yaml
└── scripts/
    └── init-db.sql
```

### Dockerfile.backend

- Python 3.11-slim base image
- Multi-stage build for optimized size
- Non-root user for security
- Health check included
- Runs Uvicorn on port 8000

### Dockerfile.frontend

- Node 18-alpine base image
- Multi-stage build (build + serve)
- Optimized production build
- Non-root user for security
- Serve static files on port 3000

---

## Database Management

### Development (SQLite)

Database location: `backend/database_files/app.db`

Clear database:
```bash
rm backend/database_files/app.db
```

The database auto-recreates on next startup.

### Production (PostgreSQL)

Connect to database:
```bash
docker exec -it aegis-postgres psql -U aegisdb -d aegis_api
```

Common commands:
```sql
-- List tables
\dt

-- Check table structure
\d+ apis

-- Basic query
SELECT * FROM apis LIMIT 5;

-- Export data
\copy apis TO 'backup.csv' CSV HEADER;
```

Backup database:
```bash
docker exec aegis-postgres pg_dump -U aegisdb aegis_api > backup.sql
```

Restore database:
```bash
docker exec -i aegis-postgres psql -U aegisdb aegis_api < backup.sql
```

---

## Networking

### Development

```
localhost:3000 (Frontend)
      ↓
localhost:5000 (Backend)
      ↓
sqlite:///./database_files/app.db (SQLite)
```

### Production

All services connect via Docker network `aegis-network`:

```
Frontend
   ↓ (port 3000)
Backend
   ├→ PostgreSQL (port 5432)
   └→ Redis (port 6379)
```

### Port Mapping

| Service | Dev | Prod | Internal |
|--|--|--|--|
| Frontend | 3000 | 3000 | 3000 |
| Backend | 5000 | 8000 | 8000 |
| PostgreSQL | N/A | 5432 | 5432 |
| Redis | N/A | 6379 | 6379 |
| Prometheus | N/A | 9090 | 9090 |
| Grafana | N/A | 3001 | 3000 |

---

## Monitoring & Observability

### Development

- Console logs only
- Backend health check: `GET http://localhost:5000/health`
- Frontend served with hot-reload

### Production

Services included:
- **Prometheus**: Metrics collection (port 9090)
- **Grafana**: Visualization (port 3001)
- **Health checks**: All services monitored

Access Grafana:
```
http://localhost:3001
Username: admin
Password: admin (change in .env with GRAFANA_PASSWORD)
```

---

## Scaling Considerations

### For Production:

1. **Database**: Use managed PostgreSQL service (AWS RDS, Azure Database, etc.)
2. **Redis**: Use managed cache service or Redis Sentinel for HA
3. **Load Balancing**: Add Nginx/HAProxy in front
4. **Container Orchestration**: Use Kubernetes for auto-scaling
5. **CDN**: Put frontend behind CloudFront/Cloudflare

### Kubernetes Deployment

See `devops/kubernetes/`:
- `deployment.yaml`: Service deployments
- `policies.yaml`: Network policies
- `cronjobs.yaml`: Scheduled tasks

---

## Troubleshooting

### Services Won't Start

```bash
# Check Docker status
docker ps -a

# View error logs
docker-compose logs backend
docker-compose logs frontend

# Rebuild everything
docker-compose down -v
docker-compose build --no-cache
```

### Port Already in Use

```bash
# Find process using port
netstat -ano | findstr :5000

# Kill process
taskkill /PID <pid> /F
```

### Database Connection Issues

```bash
# Test PostgreSQL connection
docker exec -it aegis-postgres psql -U aegisdb -d aegis_api -c "SELECT 1"

# Reset database
docker-compose down -v
docker-compose up
```

### Frontend Can't Reach Backend

```bash
# Check VITE_API_URL in frontend
cat frontend/.env.local

# Verify backend is running
curl http://localhost:5000/health

# Check CORS settings in backend
# Allowed origins must include frontend URL
```

---

## Security Best Practices

✅ **Do:**
- Use environment variables for secrets (`.env`)
- Change default passwords in production
- Use strong SECRET_KEY (generate with `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
- Run services as non-root users
- Use health checks
- Enable HTTPS in production (add reverse proxy)
- Regularly update base images

❌ **Don't:**
- Commit `.env` files to git
- Use default credentials in production
- Expose sensitive ports publicly
- Run containers with `--privileged`
- Skip security updates

---

## Maintenance

### Regular Tasks

```bash
# Update Docker images
docker-compose pull

# Rebuild services
docker-compose build --no-cache

# Prune unused resources
docker system prune -a

# Backup database (daily)
docker exec aegis-postgres pg_dump -U aegisdb aegis_api > backup-$(date +%Y%m%d).sql
```

### Monitoring Checklist

- [ ] All services healthy: `docker-compose ps`
- [ ] No error logs: `docker-compose logs --tail 100 | grep -i error`
- [ ] Database size: `SELECT pg_size_pretty(pg_database_size('aegis_api'));`
- [ ] Disk usage: `docker system df`
- [ ] Performance metrics in Grafana

---

## Support & Documentation

For more details, see:
- Backend: `backend/README.md`
- Frontend: `frontend/README.md`
- API Docs: `http://localhost:5000/docs` (Swagger UI)
- Issues: GitHub Issues
