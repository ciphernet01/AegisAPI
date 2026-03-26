# 👨‍💻 Developer Guide

Welcome to the **Aegis API** development team! This guide will help you get up to speed quickly and start contributing productively.

---

## Table of Contents

1. [Environment Setup](#-environment-setup)
2. [Project Structure](#-project-structure)
3. [Development Workflow](#-development-workflow)
4. [Code Standards](#-code-standards)
5. [Common Tasks](#-common-tasks)
6. [Debugging](#-debugging)
7. [Testing](#-testing)
8. [Git Workflow](#-git-workflow)
9. [Performance Tips](#-performance-tips)
10. [Troubleshooting](#-troubleshooting)

---

## 🛠️ Environment Setup

### Total Setup Time: 30 minutes

### Step 1: Prerequisites Check

```bash
# Verify Node.js (should be 18+)
node --version

# Verify Python (should be 3.11+)
python --version

# Verify Git
git --version
```

### Step 2: Clone Repository

```bash
git clone https://github.com/ciphernet01/AegisAPI.git
cd AegisAPI
```

### Step 3: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py
```

### Step 4: Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Create environment file
copy .env.example .env.local  # Windows
cp .env.example .env.local    # Mac/Linux

# Verify environment
cat .env.local  # Check VITE_API_URL=http://localhost:5000
```

### Step 5: IDE Setup (VS Code Recommended)

**Extensions to install:**
- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- ESLint (dbaeumer.vscode-eslint)
- Prettier (esbenp.prettier-vscode)
- Thunder Client or Postman (for API testing)

**VS Code Settings** (`.vscode/settings.json`):
```json
{
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "[python]": {
    "editor.defaultFormatter": "ms-python.python",
    "editor.formatOnSave": true
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  },
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  }
}
```

---

## 📁 Project Structure

### Backend Structure

```
backend/
├── main.py                      # FastAPI app entry point
├── config.py                    # Configuration management
├── init_db.py                   # Database initialization script
├── requirements.txt             # Python dependencies
├── database/
│   ├── db.py                   # Database setup & engine
│   ├── models.py               # SQLAlchemy ORM models
│   └── __init__.py
├── routes/
│   ├── auth_routes.py          # /auth/* endpoints
│   ├── api_routes.py           # /apis/* endpoints
│   └── __init__.py
├── services/
│   ├── auth_service.py         # JWT & password logic
│   ├── discovery_service.py    # API discovery scanners
│   ├── assessment_service.py   # Security assessment
│   └── __init__.py
├── schemas/
│   ├── auth_schemas.py         # Pydantic models for auth
│   ├── api_schemas.py          # Pydantic models for APIs
│   └── __init__.py
└── database_files/
    └── app.db                  # SQLite database (dev only)
```

**Key Files to Know:**

- **main.py**: Entry point, startup/shutdown events, middleware setup
- **config.py**: Environment variables, settings management
- **database/models.py**: Data structures (User, API, Finding, etc.)
- **services/**: Business logic (discovery, scoring, remediation)
- **routes/**: HTTP endpoints and request handlers

### Frontend Structure

```
frontend/
├── src/
│   ├── main.tsx               # Entry point
│   ├── App.tsx                # Root component
│   ├── pages/
│   │   ├── Dashboard.tsx      # Main dashboard
│   │   ├── ApiInventory.tsx   # API list & search
│   │   ├── RiskAssessment.tsx # Risk analysis
│   │   ├── Remediations.tsx   # Workflow management
│   │   ├── Settings.tsx       # User settings
│   │   └── Profile.tsx        # User profile
│   ├── components/
│   │   ├── Navbar.tsx         # Top navigation
│   │   ├── Sidebar.tsx        # Side navigation
│   │   ├── ApiCard.tsx        # API display card
│   │   ├── RiskBadge.tsx      # Risk indicator
│   │   └── ...
│   ├── context/
│   │   ├── AuthContext.tsx    # AUTH state & JWT
│   │   └── ThemeContext.tsx   # Dark/light mode
│   ├── services/
│   │   └── ApiService.ts      # API client & interceptors
│   └── styles/
│       └── globals.css        # Global styles
├── public/                    # Static assets
├── vite.config.ts            # Vite configuration
├── package.json              # Dependencies
└── .env.local                # Development env vars
```

**Key Files to Know:**

- **src/main.tsx**: React app initialization
- **src/context/AuthContext.tsx**: User auth state, JWT tokens
- **src/services/ApiService.ts**: Axios setup with interceptors
- **src/pages/***: Main feature pages
- **vite.config.ts**: Build config, API proxy setup

---

## 🚀 Development Workflow

### Starting Your Day

```bash
# Terminal 1: Start backend
cd backend
python -m uvicorn main:app --reload --port 5000

# Terminal 2: Start frontend
cd frontend
npm run dev -- --port 3001
```

Both services start with hot-reload enabled - changes appear immediately.

### During Development

**Making Backend Changes:**
1. Edit files in `backend/services/`, `backend/routes/`, etc.
2. Backend automatically reloads (watch for "Uvicorn reloaded")
3. Test via http://localhost:5000/docs (Swagger UI)

**Making Frontend Changes:**
1. Edit files in `frontend/src/`
2. Browser auto-refreshes (watch for HMR notification)
3. Test in browser at http://localhost:3001

**Making Database Schema Changes:**
1. Edit models in `backend/database/models.py`
2. Restart backend (Ctrl+C, then re-run uvicorn)
3. Or run `python backend/init_db.py` to recreate database

### Testing API Endpoints

```bash
# Use Swagger UI (interactive)
http://localhost:5000/docs

# Or with curl
curl -X GET http://localhost:5000/apis \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Or with Thunder Client / Postman
POST http://localhost:5000/auth/login
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "password123"
}
```

---

## 📝 Code Standards

### Python (Backend)

**Style Guide**: PEP 8 + Black formatter

```bash
# Format code
black backend/

# Check style
flake8 backend/

# Type checking
mypy backend/
```

**File Template:**

```python
"""Module description."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Type hints required
def discover_apis(
    source: str,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> List[APIDiscovery]:
    """
    Discover APIs from specified source.
    
    Args:
        source: API source ('github', 'docker', etc.)
        limit: Maximum APIs to return
        db: Database session
        
    Returns:
        List of discovered APIs
        
    Raises:
        ValueError: If source is invalid
    """
    if source not in ['github', 'docker']:
        raise ValueError(f"Invalid source: {source}")
    # Implementation
```

**Key Rules:**
- ✅ Type hints on all functions
- ✅ Docstrings on all public functions
- ✅ Constants in UPPER_CASE
- ✅ Private functions prefixed with `_`
- ✅ Exception handling with meaningful messages
- ❌ No `print()` statements (use logging)
- ❌ No hardcoded secrets

### TypeScript/React (Frontend)

**Style Guide**: ESLint + Prettier

```bash
# Format code
npm run prettier -- --write src/

# Check style
npm run lint

# Fix auto-fixable issues
npm run lint -- --fix
```

**Component Template:**

```typescript
import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { apiService } from '../services/ApiService';

interface Props {
  apiId: string;
  onSuccess?: () => void;
}

/**
 * Component for displaying API details.
 * 
 * @param props Component props
 * @returns React component
 */
export const ApiDetails: React.FC<Props> = ({ apiId, onSuccess }) => {
  const { user } = useAuth();
  const [api, setApi] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch data on mount
  useEffect(() => {
    const fetchApi = async () => {
      try {
        const data = await apiService.getApi(apiId);
        setApi(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    };

    fetchApi();
  }, [apiId]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div className="text-red-600">{error}</div>;
  if (!api) return <div>Not found</div>;

  return (
    <div className="p-4">
      <h1>{api.name}</h1>
      {/* Content */}
    </div>
  );
};

export default ApiDetails;
```

**Key Rules:**
- ✅ Functional components with hooks
- ✅ Props with TypeScript interfaces
- ✅ Component-level state management
- ✅ Error boundaries for crash protection
- ✅ Loading states always shown
- ❌ Class components (use hooks)
- ❌ Direct DOM manipulation (use React)
- ❌ Type `any` (use proper types)

### Git Commits

```bash
# Good commits follow format: type(scope): message

git commit -m "feat(discovery): add GitHub API scanner"
git commit -m "fix(auth): handle token refresh correctly"
git commit -m "docs(readme): update installation steps"
git commit -m "test(api): add risk scoring tests"
git commit -m "refactor(models): simplify APIDiscovery model"
git commit -m "perf(discovery): optimize deduplication algorithm"
```

**Types**: feat, fix, docs, test, refactor, perf, style, chore
**Scopes**: discovery, assessment, remediation, auth, database, ui, etc.

---

## 🔧 Common Tasks

### Add New API Endpoint

**Backend:**

1. Create schema in `backend/schemas/api_schemas.py`:
```python
from pydantic import BaseModel

class NewAPIRequest(BaseModel):
    name: str
    endpoint: str
    description: Optional[str] = None
```

2. Create route in `backend/routes/api_routes.py`:
```python
from fastapi import APIRouter
from backend.schemas import NewAPIRequest

router = APIRouter()

@router.post("/apis/new")
async def create_new_api(
    request: NewAPIRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new API entry."""
    api = API(**request.dict())
    db.add(api)
    db.commit()
    return api
```

3. Register route in `main.py`:
```python
from backend.routes import api_routes
app.include_router(api_routes.router)
```

**Frontend:**

1. Add method to `src/services/ApiService.ts`:
```typescript
async createNewApi(request: NewAPIRequest): Promise<API> {
  return this.api.post('/apis/new', request);
}
```

2. Use in component:
```typescript
const handleCreate = async () => {
  try {
    const result = await apiService.createNewApi({
      name: 'My API',
      endpoint: 'https://...',
      description: '...'
    });
    onSuccess?.();
  } catch (err) {
    setError(err.message);
  }
};
```

### Add Database Migration

```bash
# 1. Edit models in backend/database/models.py
# 2. Backup database (if production): cp database_files/app.db database_files/app.db.bak
# 3. Recreate database:
python backend/init_db.py
# 4. Test thoroughly
```

### Add New Page

**Frontend:**

1. Create page in `src/pages/NewPage.tsx`
2. Add route in `src/App.tsx`:
```typescript
<Routes>
  <Route path="/new-page" element={<NewPage />} />
</Routes>
```
3. Add navigation link in `src/components/Sidebar.tsx`

---

## 🐛 Debugging

### Backend Debugging

**Option 1: Print Debugging**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Variable value: {my_var}")
logger.info("Operation started")
logger.error(f"Error occurred: {error}")
```

**Option 2: Python Debugger**
```python
import pdb; pdb.set_trace()  # Pause here in debugger
```

**Option 3: VS Code Debugger**

Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["main:app", "--reload"],
      "jinja": true,
      "cwd": "${workspaceFolder}/backend"
    }
  ]
}
```

Then press F5 to start debugging.

### Frontend Debugging

**Option 1: Browser DevTools**
- F12 or Ctrl+Shift+I
- Console tab for logs: `console.log()`
- Network tab for API calls
- Sources tab for breakpoints

**Option 2: VS Code Debugger**

Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "chrome",
      "request": "launch",
      "name": "Launch Chrome",
      "url": "http://localhost:3001",
      "webRoot": "${workspaceFolder}/frontend/src"
    }
  ]
}
```

**Option 3: React DevTools**
- Install React DevTools browser extension
- Inspect components, props, state, hooks

### Common Debug Scenarios

**Backend Error on Startup:**
```bash
# Check logs in terminal - look for:
# - Import errors
# - Database connection issues
# - Missing dependencies

# Test connection:
python -c "from backend.database.db import engine; print('OK')"
```

**Frontend Blank Page:**
```
Check browser console (F12):
- CORS errors? → Update vite.config.ts proxy
- 404 on API calls? → Verify backend is running
- Blank page? → Check main.tsx for rendering errors
```

**API Returns 401 Unauthorized:**
```bash
# Token expired? Use /auth/refresh to get new token
# Token missing? Check Authorization header in request
# Wrong scope? Check user role has permission
```

---

## ✅ Testing

### Backend Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run all tests
pytest backend/

# Run specific test file
pytest backend/tests/test_discovery.py

# Run with coverage
pytest --cov=backend backend/

# Watch mode (re-run on changes)
pytest-watch backend/
```

### Frontend Tests

```bash
# Install test dependencies
npm install --save-dev vitest @testing-library/react @testing-library/jest-dom

# Run tests
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage
```

### Writing Tests

**Backend Example:**
```python
# tests/test_discovery.py
import pytest
from backend.services.discovery_service import GitHubScanner

@pytest.fixture
def scanner():
    return GitHubScanner(token="test_token")

def test_scan_organization_finds_apis(scanner):
    """Test that GitHub scanner finds APIs."""
    apis = scanner.scan_organization("test-org")
    assert len(apis) > 0
    assert all(hasattr(api, 'name') for api in apis)

@pytest.mark.asyncio
async def test_async_api_call():
    """Test async API call."""
    result = await discover_apis_async("github")
    assert result is not None
```

**Frontend Example:**
```typescript
// src/components/__tests__/ApiCard.test.tsx
import { render, screen } from '@testing-library/react';
import ApiCard from '../ApiCard';

describe('ApiCard', () => {
  it('renders API name', () => {
    const api = { id: '1', name: 'Test API', risk_score: 50 };
    render(<ApiCard api={api} />);
    
    expect(screen.getByText('Test API')).toBeInTheDocument();
  });

  it('displays risk badge', () => {
    const api = { id: '1', name: 'Test API', risk_score: 85 };
    render(<ApiCard api={api} />);
    
    expect(screen.getByText(/High Risk/)).toBeInTheDocument();
  });
});
```

---

## 🌳 Git Workflow

### Feature Development

```bash
# 1. Get latest code
git fetch origin
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/my-feature

# 3. Make changes and commit
git add .
git commit -m "feat(scope): description"

# 4. Keep updated with main
git fetch origin
git rebase origin/main

# 5. Push and create PR
git push origin feature/my-feature
# Then create PR on GitHub
```

### Opening a Pull Request

**PR Title Format**: `[Scope] Description (e.g., [Discovery] Add GitHub scanner)`

**PR Description Template:**
```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update

## Changes Made
- Change 1
- Change 2

## Testing
How to test:
1. Step 1
2. Step 2

## Screenshots (if UI changes)
[Add screenshots]

## Checklist
- [ ] Code follows style guidelines
- [ ] I have commented my code
- [ ] I have tested this change
- [ ] Tests pass locally
```

### Code Review

- Be respectful and constructive
- Request changes if needed
- Approve when satisfied
- Merge only after approval + tests pass

---

## ⚡ Performance Tips

### Backend

```python
# ✅ Use database indexes
@event.listens_for(API, "before_create")
def receive_before_create(mapper, connection, target):
    # Queries on these fields should be fast
    pass

# ✅ Cache expensive operations
from functools import lru_cache

@lru_cache(maxsize=128)
def get_risk_factors(api_type: str) -> dict:
    # Cached result reused
    return expensive_calculation(api_type)

# ❌ Don't load entire table
# Bad:
all_apis = db.query(API).all()

# Good:
apis = db.query(API).limit(100).offset(skip).all()
```

### Frontend

```typescript
// ✅ Memoize expensive components
import React, { memo } from 'react';

const ApiCard = memo(({ api }: { api: API }) => {
  return <div>{api.name}</div>;
});

// ✅ Use useCallback for event handlers
const handleClick = useCallback(() => {
  // Only recreated when dependencies change
}, [dependency]);

// ❌ Don't create new objects in render
// Bad:
render() {
  const style = { color: 'red' };  // New object every render
  return <div style={style}>{text}</div>;
}

// Good:
const style = { color: 'red' };  // Created once
render() {
  return <div style={style}>{text}</div>;
}
```

---

## 🚨 Troubleshooting

### Backend Issues

**"ModuleNotFoundError: No module named X"**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check venv is activated
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
```

**"Address already in use :5000"**
```bash
# Find what's using port 5000
netstat -ano | findstr :5000

# Use different port
python -m uvicorn main:app --port 5001

# Or kill the process
taskkill /PID <PID> /F
```

**Database locked error**
```bash
# SQLite doesn't support concurrent writes
# Restart backend to reset connection pool
# Or use PostgreSQL for production
```

### Frontend Issues

**"Cannot find module src/..."**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**"API returns 404"**
```bash
# Check backend is running
netstat -ano | findstr :5000

# Check API endpoint is registered
# Visit http://localhost:5000/docs to see endpoints
```

**"CORS error"**
```bash
# Check vite.config.ts proxy is configured correctly:
```

### Connection Issues

**"Can't connect to http://localhost:5000"**
```bash
# Check backend is running
curl http://localhost:5000/health

# Check firewall allows port 5000
# Check .env.local has correct VITE_API_URL
```

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Vite Documentation](https://vitejs.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)

---

## 🎓 Learning Path

**Week 1:**
- [ ] Set up development environment
- [ ] Read GETTING_STARTED.md
- [ ] Understand project structure
- [ ] Make a small bug fix

**Week 2:**
- [ ] Study backend architecture (main.py, routes, services)
- [ ] Study frontend architecture (pages, components, context)
- [ ] Implement a small feature
- [ ] Write tests

**Week 3+:**
- [ ] Own features from specification → PR → deployment
- [ ] Mentoring new developers
- [ ] Architecture improvements

---

## ❓ FAQ

**Q: How do I reset my local database?**
```bash
rm backend/database_files/app.db
python backend/init_db.py
```

**Q: How do I switch between PostgreSQL and SQLite?**
Edit `backend/config.py`:
```python
use_sqlite: bool = True  # Change to False for PostgreSQL
```

**Q: How do I add a new dependency?**
```bash
# Backend
pip install package-name
pip freeze > requirements.txt

# Frontend
npm install package-name
```

**Q: How do I deploy locally with Docker?**
```bash
.\docker-run.ps1 -Environment dev  # Windows
bash docker-run.sh dev              # Mac/Linux
```

---

## 🤝 Need Help?

- Check [Troubleshooting](#-troubleshooting) section
- Look at GitHub Issues
- Ask in GitHub Discussions
- Contact project maintainers

---

**Happy coding! 🚀**

---

*Last updated: January 21, 2024*
*Version: 1.0*
