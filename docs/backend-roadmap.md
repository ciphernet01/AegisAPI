# Zombie API Platform - BACKEND ROADMAP
**Simplified, Sprint-Based Development Plan**

---

## 🎯 PROJECT VISION
**Discover → Assess → Classify → Remediate → Monitor** all APIs across the bank

---

## 📊 SPRINT BREAKDOWN (2-Week Sprints)

### **SPRINT 1 & 2: Foundation** (Weeks 1-4)
**Goal**: Set up infrastructure and database

#### What to Build:
- Project structure (folders, configs, requirements)
- PostgreSQL database with core tables
- Authentication system (JWT + roles)
- Basic API server with health check

#### Deliverables:
- ✅ Running Flask/FastAPI server on `localhost:5000`
- ✅ PostgreSQL database connected
- ✅ `/health` endpoint working
- ✅ Initial CI/CD test passing

#### Key Files to Create:
```
backend/
├── app.py / main.py          # Main server
├── requirements.txt           # Dependencies
├── .env.example               # Config template
├── models.py / database.py    # Database schema
├── auth.py                    # Auth middleware
├── config.py                  # Settings
└── tests/
    └── test_health.py         # Basic test
```

---

### **SPRINT 3: API Discovery MVP** (Weeks 5-6)
**Goal**: Find APIs from code repos and containers

#### What to Build:
- GitHub repo scanner (find API code)
- Docker registry scanner (find API images)
- Basic OpenAPI parser
- Store discovered APIs in database

#### Deliverables:
- ✅ Discover 50+ APIs from test repos
- ✅ `GET /apis` endpoint returns list
- ✅ Remove duplicates
- ✅ API inventory dashboard ready for frontend

#### Quick Demo:
```bash
python scanner.py                    # Run discovery
# Result: 50 APIs found and stored in database

curl http://localhost:5000/apis      # Retrieve them
# Output: [{"name": "user-service", "url": "...", ...}]
```

---

### **SPRINT 4: Security Assessment MVP** (Weeks 7-8)
**Goal**: Test APIs for security issues

#### What to Build:
- Authentication checker (does it exist?)
- Encryption checker (HTTPS/TLS)
- Rate limiting detector
- Sensitive data scanner (detect exposed secrets)
- Security findings storage

#### Deliverables:
- ✅ Assess 50 APIs in database
- ✅ `POST /apis/{id}/assess` triggers assessment
- ✅ Store results: auth ✅/❌, encryption ✅/❌, etc.
- ✅ Risk score per API (0-100)

#### Quick Demo:
```bash
curl -X POST http://localhost:5000/apis/1/assess

# Result: 
{
  "api_id": 1,
  "auth_required": true,
  "uses_https": true,
  "has_rate_limiting": false,
  "risk_score": 35,
  "findings": ["No rate limiting detected"]
}
```

---

### **SPRINT 5: Classification & Risk** (Weeks 9-10)
**Goal**: Classify APIs as Active/Deprecated/Orphaned/Zombie

#### What to Build:
- API status classifier (based on traffic, maintenance)
- Risk scoring engine (combine all security findings)
- Dependency mapper (which APIs call which)
- Classification API endpoint

#### Deliverables:
- ✅ Every API has a status: Active/Deprecated/Orphaned/Zombie
- ✅ Every API has risk score: 0-100
- ✅ `GET /apis?status=zombie` filters by status
- ✅ Risk dashboard ready for frontend

#### Quick Demo:
```bash
# Check zombie APIs
curl http://localhost:5000/apis?status=zombie

# Get risk summary
curl http://localhost:5000/stats

# Output:
{
  "active": 40,
  "deprecated": 8,
  "orphaned": 2,
  "zombie": 5,
  "avg_risk_score": 45
}
```

---

### **SPRINT 6: Remediation Workflows** (Weeks 11-12)
**Goal**: Enable decommissioning of zombie APIs

#### What to Build:
- Workflow state machine (Proposed → Approved → Executing → Done)
- Approval request system (send notifications)
- Automated shutdown actions (disable endpoint, redirect)
- Rollback capability
- Audit log of all actions

#### Deliverables:
- ✅ Admin can propose removing a zombie API
- ✅ Team lead approves/rejects
- ✅ System disables API automatically
- ✅ `GET /remediation/workflows` shows progress

#### Quick Demo:
```bash
# Propose removal
curl -X POST http://localhost:5000/apis/5/remediation \
  -d '{"action": "decommission"}'

# Check who has to approve
curl http://localhost:5000/remediation/workflows

# Output:
[
  {
    "api_id": 5,
    "status": "pending_approval",
    "proposed_by": "alice@bank.com",
    "awaiting_approval_from": "bob@bank.com"
  }
]

# Approve it
curl -X POST http://localhost:5000/remediation/workflows/1/approve

# System disables API (updates DB)
# Sends notification to API owner
```

---

### **SPRINT 7: Monitoring & Continuous Discovery** (Weeks 13-14)
**Goal**: Keep the system running 24/7, detect new APIs

#### What to Build:
- Health checks for all APIs (ping every 5 min)
- New API detection (GitHub webhooks, scheduled scans)
- Anomaly alerts (unusual traffic patterns)
- Automated responses (disable high-risk APIs)

#### Deliverables:
- ✅ Background job discovers new APIs hourly
- ✅ Health status updated in real-time
- ✅ Alerts sent to Slack/email when:
  - New API discovered
  - API becomes zombie (no traffic for 30 days)
  - Critical security issue found
- ✅ High-risk APIs auto-disabled with approval chain

#### Quick Demo:
```bash
# Check real-time health
curl http://localhost:5000/apis/1/health

# Output:
{
  "status": "healthy",
  "last_check": "2026-03-25T14:30:00Z",
  "response_time_ms": 45,
  "uptime_percent": 99.8
}

# Monitoring endpoint
curl http://localhost:5000/monitoring/summary

# Output:
{
  "total_apis": 150,
  "healthy": 148,
  "unhealthy": 2,
  "new_apis_this_week": 3,
  "zombie_risk_apis": 5
}
```

---

### **SPRINT 8: Polish & Optimization** (Weeks 15-16)
**Goal**: Make it production-ready

#### What to Build:
- Performance optimization (caching, database indexes)
- Error handling improvements
- Comprehensive logging
- Complete API documentation
- Secrets management (API keys, credentials)

#### Deliverables:
- ✅ API response time < 500ms (p99)
- ✅ Handle 1000+ APIs smoothly
- ✅ Full OpenAPI/Swagger docs
- ✅ Dockerized and ready for deployment
- ✅ 80%+ test coverage

---

## 📈 PROGRESSION

```
Sprint 1-2          Sprint 3         Sprint 4          Sprint 5
Foundation       Discovery      Assessment      Classification
   ████              ▓▓▓             ▓▓▓               ▓▓▓
                    Find APIs       Test Security    Label + Risk
                                                    
Sprint 6           Sprint 7          Sprint 8
Remediation     Monitoring        Deploy
   ▓▓▓            ▓▓▓              ▓▓▓
  Remove        Watch 24/7        Go Live
  Safely        Auto-detect
```

---

## 🔑 KEY FEATURES BY SPRINT

| Sprint | Feature | Status | Users |
|--------|---------|--------|-------|
| 1-2 | Basic server + DB | Setup ⬜ | Engineers |
| 3 | Find APIs | Discovery ⬜ | Security team |
| 4 | Rate security | Assessment ⬜ | Security team |
| 5 | Label & Score | Classification ⬜ | Everyone |
| 6 | Remove safely | Remediation ⬜ | Admin + Leads |
| 7 | Watch always | Monitoring ⬜ | DevOps + Alert |
| 8 | Ship it | Prod Ready ⬜ | All teams |

---

## 💻 TECH STACK (CHOOSE ONE)

### **OPTION A: Python (Recommended)**
```
FastAPI           # Web framework (modern, fast)
PostgreSQL        # Database
Redis             # Caching
SQLAlchemy        # ORM
Celery            # Background jobs
pytest            # Testing
```

### **OPTION B: Node.js**
```
Express / Nest.js # Web framework
PostgreSQL        # Database
Redis             # Caching
Prisma / TypeORM  # ORM
Bull              # Job queue
Jest              # Testing
```

**→ Choose now & I'll set it up**

---

## 🚀 START NOW - SPRINT 1 CHECKLIST

### Week 1:
- [ ] Choose tech stack (Python or Node?)
- [ ] Create `backend/` folder structure
- [ ] Set up virtual environment or npm
- [ ] Create main server file (FastAPI/Express)
- [ ] Add PostgreSQL database connection
- [ ] Write first test (health check)
- [ ] Push to GitHub: `feature/backend/setup`

### Week 2:
- [ ] Design database schema (APIs, Findings, Status tables)
- [ ] Create database migration
- [ ] Add auth middleware (JWT)
- [ ] Create role-based access control (Admin, SecurityTeam, DevOps)
- [ ] Set up logging and error handling
- [ ] Deploy locally to `localhost:5000`
- [ ] Merge to `develop` branch

**End of Sprint 1-2**: Working server with empty API database ✅

---

## 📋 EACH SPRINT HAS:

```
📌 GOAL
   "What are we building?"

🛠️ WHAT TO BUILD
   "High-level components"

✅ DELIVERABLES
   "What we show at demo"

💾 KEY FILES
   "Important code files"

📊 DEMO
   "Test these URLs/commands to verify it works"
```

---

## ❓ QUESTIONS BEFORE WE START?

1. **Python or Node.js?**
   - Python: Simpler, great for data analysis, slower (fine for this project)
   - Node.js: Faster, JavaScript everywhere, more package choices

2. **Database**: PostgreSQL is recommended. OK?

3. **Want to start Sprint 1 TODAY?**
   - I can create the initial project structure
   - You code the basic server
   - We test it

---

## 🎯 HONEST TIMELINE

- **Sprint 1-2**: 2 weeks (boring but critical setup)
- **Sprint 3**: 1 week (exciting! APIs appear!)
- **Sprint 4**: 1 week (security scanning works!)
- **Sprint 5**: 1 week (risk scores calculated!)
- **Sprint 6**: 1 week (remediation flows!)
- **Sprint 7**: 1 week (monitoring live!)
- **Sprint 8**: 1 week (polish & testing!)

**Total**: ~8 weeks to MVP, ~10 weeks production-ready

---

**Ready? Let's build! 🚀**

Pick your answers:
1. Python or Node.js? ➜
2. Start Sprint 1 setup now? ➜
