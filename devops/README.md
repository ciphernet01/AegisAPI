# DevOps & Infrastructure

Complete Infrastructure-as-Code and deployment automation for the Zombie API Discovery and Defence Platform.

## Quick Start

### Local Development (Docker Compose)

```bash
cd devops/scripts
chmod +x deploy-local.sh
./deploy-local.sh
```

**Access Points:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Grafana: http://localhost:3001 (admin/admin)

### Kubernetes Deployment

```bash
# Deploy to staging
devops/scripts/deploy-k8s.sh staging

# Or to production
devops/scripts/deploy-k8s.sh production
```

### AWS Infrastructure (Terraform)

```bash
cd devops/terraform
terraform init
terraform plan -var-file=production.tfvars
terraform apply -var-file=production.tfvars
```

## Directory Structure

```
devops/
├── docker/                 # Containerization
│   ├── Dockerfile.frontend # React build
│   ├── Dockerfile.backend  # Python services
│   ├── docker-compose.yml  # Development stack
│   └── .dockerignore
├── kubernetes/             # K8s manifests
│   ├── deployment.yaml     # Services, deployments, ingress
│   ├── cronjobs.yaml       # Scheduled discovery & assessment
│   └── policies.yaml       # HPA, PDB, network policies
├── terraform/              # Infrastructure as Code
│   ├── main.tf            # EKS, RDS, ALB, ECR
│   ├── variables.tf       # Input variables
│   ├── outputs.tf         # Output values
│   └── modules/vpc/       # VPC module
├── monitoring/             # Observability
│   ├── prometheus.yml     # Metrics scraping
│   ├── alerts.yml         # Alert rules
│   └── grafana/           # Grafana configuration
└── scripts/                # Automation
    ├── deploy-local.sh
    ├── deploy-k8s.sh
    └── build-push-images.sh
```

## Deployment Models

### Model 1: Local Development with Docker Compose

**When to use:** Development, testing, proof-of-concept

**Setup Time:** 5-10 minutes

**Requirements:**
- Docker & Docker Compose
- 8GB RAM, 20GB disk

**Services included:**
- PostgreSQL, Redis, Backend, Security Engine, Frontend
- Prometheus, Grafana for monitoring

### Model 2: Kubernetes (AWS EKS)

**When to use:** Staging, production environments

**Setup Time:** 30-45 minutes

**Requirements:**
- Kubernetes cluster
- kubectl configured
- Helm 3.0+
- Container registry access

**Features:**
- Auto-scaling (HPA)
- High availability (2+ replicas)
- Auto-healing (health checks)
- Network policies
- Scheduled jobs
- Ingress with TLS

### Model 3: Infrastructure with Terraform

**When to use:** Complete AWS setup from scratch

**Setup Time:** 45-60 minutes

**Creates:**
- EKS cluster
- RDS PostgreSQL
- ElastiCache Redis
- ECR repositories
- VPC with public/private subnets
- Security groups & IAM roles
- CloudWatch monitoring
- Prometheus & Grafana stack

## Configuration Files

### Environment Variables

**Docker Compose (.env):**
```env
DB_USER=aegisdb
DB_PASSWORD=secure_password_123
DB_NAME=aegis_api
API_ENV=development
GRAFANA_PASSWORD=admin_password
```

**Kubernetes (secrets.yaml):**
```bash
kubectl create secret generic aegis-secrets \
  --from-literal=DB_USER=aegisdb \
  --from-literal=DB_PASSWORD=xxx \
  -n aegis
```

**Terraform (production.tfvars):**
```hcl
aws_region = "us-east-1"
environment = "production"
node_group_desired_size = 3
db_instance_class = "db.m5.large"
```

## Monitoring & Alerting

### Prometheus Metrics

**Key metrics monitored:**
- `container_cpu_usage_seconds_total` - CPU utilization
- `container_memory_usage_bytes` - Memory usage
- `http_requests_total` - API request rate
- `pg_connections_active` - Database connections
- `redis_connected_clients` - Redis clients

### Grafana Dashboards

**Pre-built dashboards:**
1. **System Health** - CPU, memory, disk, network
2. **API Discovery** - Discovery rate, API trends
3. **Security Assessment** - Risk distribution, remediation status
4. **Database** - Connections, query performance, replication
5. **Application** - Request rate, error rate, latency

### Alerting Rules

| Alert | Condition | Action |
|-------|-----------|--------|
| HighCPUUsage | CPU > 80% for 5m | Page on-call |
| HighMemoryUsage | Memory > 85% for 5m | Page on-call |
| DatabaseDown | pg_up == 0 for 2m | Critical |
| HighErrorRate | 5xx errors > 5% for 5m | Warning |
| DiskFull | Available disk < 10% | Critical |

## CI/CD Pipelines

### GitHub Actions Workflows

**frontend.yml** - Build, test, lint, container build
```bash
npm install → lint → test → build → push to ECR
```

**deploy.yml** - Deploy to Kubernetes
```bash
Build images → Update kubeconfig → Apply manifests → Verify health
```

**security.yml** - Vulnerability scanning
```bash
Trivy, npm audit, CodeQL, dependency-check
```

### Manual Deployment

```bash
# Build and push images
devops/scripts/build-push-images.sh v1.0.0

# Deploy to Kubernetes
devops/scripts/deploy-k8s.sh staging

# Verify deployment
kubectl get deployments -n aegis
kubectl logs -f deployment/frontend -n aegis
```

## Scaling

### Horizontal Pod Autoscaler (HPA)

**Backend:**
- Min: 2 replicas
- Max: 5 replicas
- Target CPU: 70%
- Target Memory: 80%

**Frontend:**
- Min: 2 replicas
- Max: 4 replicas
- Target CPU: 80%

### Database Scaling

**PostgreSQL:**
- Read replicas for scaling reads
- Write remains on primary
- Multi-AZ for failover

**Redis:**
- Cluster mode for sharding
- Sentinel mode for failover

## Backup & Recovery

### Backup Strategy

```
PostgreSQL
├─ Continuous WAL archiving
├─ Daily snapshots (7-day retention)
├─ Monthly archives to S3
└─ Test restore monthly

Redis
├─ RDB snapshots every 5 minutes
├─ AOF for durability
└─ Replicated across nodes
```

### Disaster Recovery

**Database Failure:**
```bash
# Restore from snapshot
aws rds restore-db-instance-from-db-snapshot \
  --db-snapshot-identifier aegis-backup-2024-01-15 \
  --db-instance-identifier aegis-restored
```

**Cluster Failure:**
```bash
# Redeploy infrastructure
terraform plan -destroy
terraform apply -destroy
terraform apply -var-file=production.tfvars
```

## Security

### Network Security

**VPC Design:**
```
Public Subnets     Private Subnets    Database Subnets
   ↓                    ↓                   ↓
NAT Gateway         EKS Nodes         PostgreSQL/Redis
ALB                 Services          Security Groups
                    Pods
```

**Security Groups:**
- Ingress: Only necessary ports (80, 443, 5432)
- Egress: Default allow all (restrict if needed)

### Secrets Management

**Kubernetes:**
```bash
kubectl create secret generic aegis-secrets
kubectl get secret aegis-secrets -o yaml
```

**AWS Secrets Manager:**
- Automatic rotation of DB credentials
- Encryption with KMS
- Audit trail for all access

## Troubleshooting

### Services Won't Start

```bash
# Check logs
docker-compose logs backend
kubectl logs deployment/backend -n aegis

# Check resource constraints
kubectl describe pod <pod-name> -n aegis

# Check networking
kubectl exec -it <pod-name> -n aegis -- curl http://postgres:5432
```

### High Resource Usage

```bash
# Check current metrics
kubectl top nodes
kubectl top pods -n aegis

# Scale horizontally
kubectl scale deployment backend --replicas=5 -n aegis
```

### Database Connection Issues

```bash
# Test connection
kubectl run -it --rm debug --image=postgres:16 -- psql \
  -h postgres \
  -U aegisdb \
  -d aegis_api

# Check connection pool
kubectl exec -it postgres-0 -n aegis -- psql -c "SELECT datname, count(*) FROM pg_stat_activity GROUP BY datname;"
```

## Cost Optimization

### Compute
- Use spot instances for non-critical workloads
- Right-size node instance types
- Schedule scale-down during off-hours

### Storage
- Use gp3 volumes instead of gp2
- Enable EBS auto-scaling
- Archive old logs to S3

### Network
- Use VPC endpoints to avoid NAT charges
- Consolidate replication traffic
- Enable S3 transfer acceleration for backups

## Documentation

- [Deployment Guide](deployment.md)
- [Architecture](../docs/architecture.md)
- [Contributing Guidelines](../CONTRIBUTING.md)

## Support

For issues or questions:
1. Check logs: `kubectl logs -f <pod-name> -n aegis`
2. Review metrics in Grafana
3. Check alerts in Prometheus
4. Open GitHub issue with logs and configuration
