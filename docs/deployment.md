# Architecture & Deployment Guide

## System Architecture

The Zombie API Discovery and Defence Platform consists of three main services:

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   Frontend  │────▶│   Backend    │────▶│   PostgreSQL    │
│  (React)    │     │   (FastAPI)  │     │   (Inventory)   │
└─────────────┘     └──────────────┘     └─────────────────┘
                            ▲
                            │
                    ┌──────────────┐
                    │    Redis     │
                    │   (Cache)    │
                    └──────────────┘

┌─────────────────────┐
│  Security Engine    │
│  (Risk Assessment)  │────▶ PostgreSQL
└─────────────────────┘
```

## Deployment Options

### 1. Local Development (Docker Compose)

**Quick Start:**
```bash
cd devops/docker
docker-compose up -d
```

**Services:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Security Engine: http://localhost:8001
- PostgreSQL: localhost:5432
- Redis: localhost:6379
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001 (admin/admin)

### 2. Kubernetes (Production)

**Prerequisites:**
- kubectl configured
- Kubernetes cluster (EKS, AKS, GKE)
- ECR/Docker registry access

**Deploy:**
```bash
cd devops/scripts
chmod +x deploy-k8s.sh
./deploy-k8s.sh staging
```

**Features:**
- Auto-scaling with HPA
- Pod Disruption Budgets for high availability
- Network policies for security
- Scheduled API discovery and security assessment jobs

### 3. Terraform (Infrastructure)

**Prerequisites:**
- Terraform >= 1.0
- AWS credentials configured
- Helm >= 3.0

**Deploy:**
```bash
cd devops/terraform
terraform init
terraform plan -var-file=staging.tfvars
terraform apply -var-file=staging.tfvars
```

**Creates:**
- EKS cluster with auto-scaling node group
- RDS PostgreSQL database
- ElastiCache Redis cluster
- ECR repositories
- Networking, security groups, and IAM roles
- CloudWatch monitoring and Prometheus/Grafana stack

## Configuration

### Environment Variables

**Frontend (.env):**
```
VITE_API_URL=http://localhost:8000
VITE_APP_ENV=development
```

**Backend (.env):**
```
DATABASE_URL=postgresql://user:pass@postgres:5432/aegis_api
REDIS_URL=redis://redis:6379
API_ENV=development
```

**DevOps (devops/docker/.env):**
```
DB_USER=aegisdb
DB_PASSWORD=<secure-password>
DB_NAME=aegis_api
GRAFANA_PASSWORD=<secure-password>
```

### Secrets Management

**Kubernetes:**
```bash
kubectl create secret generic aegis-secrets \
  --from-literal=DB_USER=aegisdb \
  --from-literal=DB_PASSWORD=<password> \
  -n aegis
```

**AWS Secrets Manager:**
All database credentials are stored and rotated automatically.

## Continuous Monitoring

### API Discovery

Runs every 6 hours via Kubernetes CronJob:
- Scans API gateways
- Parses code repositories
- Inspects network traffic
- Updates inventory database

### Security Assessment

Runs daily via Kubernetes CronJob:
- Evaluates authentication controls
- Checks encryption standards
- Assesses rate limiting
- Detects data exposure risks
- Updates risk scores

### Observability

**Prometheus Metrics:**
- Container CPU/memory usage
- HTTP request rate and latency
- Database connection pool
- Custom application metrics

**Grafana Dashboards:**
- System health and resource utilization
- API discovery trends
- Risk assessment distribution
- Alert status

**Alerts:**
- High CPU/memory usage
- Database connection failures
- Redis unavailability
- High error rates
- Low disk space

## Scaling and Performance

### Horizontal Scaling

**Frontend:**
- Min replicas: 2
- Max replicas: 4
- Target CPU: 80%

**Backend:**
- Min replicas: 2
- Max replicas: 5
- Target CPU: 70%, Memory: 80%

### Database

**PostgreSQL:**
- Instance class: db.t3.medium (adjustable)
- Storage: 50GB with auto-scaling
- Multi-AZ for production

**Redis:**
- Multi-node for redundancy (production)
- Automatic failover enabled

## Security Best Practices

1. **Network Policies** - Restrict pod-to-pod communication
2. **Pod Security** - Non-root users, read-only filesystems
3. **Secrets** - Encrypted storage, rotation policies
4. **RBAC** - Service accounts with minimal permissions
5. **Image Scanning** - Trivy scans for vulnerabilities
6. **Audit Logging** - All API calls and decommissioning actions

## Disaster Recovery

### Backup Strategy

- **Database**: Automated daily snapshots retained 7 days
- **Configuration**: Version controlled in Git
- **State**: Terraform state stored in S3 with encryption

### Recovery Procedures

1. **Database Failure**: Restore from latest snapshot
2. **Cluster Failure**: Redeploy using Terraform
3. **Service Failure**: Automatic restart via health checks

## Troubleshooting

### Services Won't Start

```bash
# Check logs
docker-compose logs -f backend

# Verify database connectivity
docker-compose exec backend curl http://postgres:5432
```

### High Memory Usage

```bash
# Scale down and up
kubectl scale deployment/backend --replicas=1 -n aegis
kubectl scale deployment/backend --replicas=3 -n aegis
```

### API Discovery Not Running

```bash
# Check CronJob status
kubectl describe cronjob api-discovery-job -n aegis

# View logs
kubectl logs -f -l job-name=api-discovery-job-* -n aegis
```

## Documentation Links

- [Frontend README](../frontend/README.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [API Specification](api-spec.md)
- [Security Guidelines](../docs/SECURITY.md)
