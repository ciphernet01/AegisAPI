# Backend - Zombie API Discovery Platform

Python FastAPI backend for discovering, assessing, and managing zombie APIs.

---

## 🚀 Quick Start

### **Prerequisites**
- Python 3.10 or higher
- PostgreSQL database
- Redis (for caching)

### **Installation**

1. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Create .env file**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. **Run server**
```bash
python app.py
```

Server starts at: `http://localhost:5000`

---

## 📖 Project Structure

```
backend/
├── app.py                    # Entry point
├── main.py                   # FastAPI app factory
├── config.py                 # Settings management
├── requirements.txt          # Dependencies
│
├── routes/                   # API endpoints
│   ├── api_routes.py        # /apis endpoints
│   ├── health_routes.py     # /health endpoint
│   └── remediation_routes.py # /remediation endpoints
│
├── services/                 # Business logic
│   ├── discovery_service.py  # Find APIs
│   ├── assessment_service.py # Test APIs
│   └── classification_service.py  # Label APIs
│
├── database/                 # Database layer
│   ├── db.py                # Connection setup
│   └── models.py            # ORM models
│
├── utils/                    # Helpers
│   ├── logger.py            # Logging setup
│   └── validators.py        # Data validation
│
└── tests/                    # Test suite
    ├── conftest.py          # Test configuration
    ├── test_health.py       # Health endpoint tests
    └── test_api.py          # API endpoint tests
```

---

## 💾 Database Setup

### **Create PostgreSQL database**
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE zombie_api_db;
```

### **Run migrations**
```bash
# Using Alembic (when migrations exist)
alembic upgrade head
```

---

## 🧪 Testing

### **Run all tests**
```bash
pytest
```

### **Run with coverage**
```bash
pytest --cov=. --cov-report=html
```

### **Run specific test**
```bash
pytest tests/test_health.py -v
```

---

## 📝 API Endpoints

### **Health Check**
```bash
curl http://localhost:5000/health
```

Response:
```json
{
  "status": "healthy",
  "service": "zombie-api-backend",
  "version": "0.1.0"
}
```

### **Auto-generated Docs**
- Swagger UI: `http://localhost:5000/docs`
- ReDoc: `http://localhost:5000/redoc`

---

## 🔧 Development

### **Code formatting**
```bash
black .
```

### **Linting**
```bash
flake8 .
```

### **Type checking**
```bash
mypy .
```

---

## 📚 Implementation Progress

**SPRINT 1-2**: Foundation ✅
- [x] Project structure
- [x] FastAPI setup
- [x] Database connection
- [x] Health endpoint
- [ ] Database migrations
- [ ] Authentication

**SPRINT 3**: API Discovery
- [ ] GitHub scanner
- [ ] Docker registry scanner
- [ ] OpenAPI parser
- [ ] API inventory endpoint

**SPRINT 4**: Security Assessment
- [ ] Auth tester
- [ ] Encryption checker
- [ ] Rate limiter detector
- [ ] Data exposure scanner

---

## 🤔 Troubleshooting

### **"Connection refused" error**
```
psycopg2.OperationalError: could not connect to server
```
Solution: Check PostgreSQL is running and `.env` has correct DATABASE_URL

### **"ModuleNotFoundError: No module named 'fastapi'"**
Solution: Install dependencies: `pip install -r requirements.txt`

### **Port 5000 already in use**
Solution: Change port in `.env` or kill process: `lsof -ti:5000 | xargs kill`

---

## 🚢 Deployment

See [devops/README.md](../devops/README.md) for Docker and Kubernetes setup.

---

## 📞 Support

For questions, create an issue or contact the backend team.
