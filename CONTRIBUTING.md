# Contributing to Zombie API Discovery and Defence Platform

## Table of Contents
1. [Initial Setup](#initial-setup)
2. [Branching Strategy](#branching-strategy)
3. [Development Workflow](#development-workflow)
4. [Pull Request Process](#pull-request-process)
5. [Code Style & Standards](#code-style--standards)
6. [Communication](#communication)

---

## Initial Setup

### For Team Members (First Time)

1. **Fork or Clone the Repository**
   ```bash
   git clone https://github.com/ciphernet01/AegisAPI
   cd AegisAPI
   ```

2. **Configure Git User Information**
   ```bash
   git config --global user.name "Your Full Name"
   git config --global user.email "your.email@company.com"
   ```

3. **Add Upstream Remote** (for long-term collaboration)
   ```bash
   git remote add upstream https://github.com/ciphernet01/AegisAPI
   git fetch upstream
   ```

4. **Install Pre-commit Hooks** (optional but recommended)
   ```bash
   pip install pre-commit
   pre-commit install
   ```

5. **Set Up Your Local Environment**
   - Backend Developer:
     ```bash
     cd backend
     python -m venv venv
     source venv/bin/activate  # venv\Scripts\activate on Windows
     pip install -r requirements.txt
     ```
   - Frontend Developer:
     ```bash
     cd frontend
     npm install
     ```
   - DevOps/Infrastructure:
     ```bash
     # Verify Docker, Terraform, kubectl are installed
     docker --version
     terraform --version
     kubectl version
     ```

---

## Branching Strategy

### Main Branches
- **`main`** - Production-ready code, stable, deployable
- **`develop`** - Integration branch for features (optional, per team preference)

### Feature/Work Branches
Create a branch for each task using clear naming conventions:

```
feature/dashboard-risk-heatmap
feature/api-discovery-gateway-scanner
feature/auth0-integration
bugfix/missing-validation-on-decommission
hotfix/critical-security-scan
docs/deployment-guide
```

### Branch Naming Conventions
- **`feature/`** - New features or enhancements
- **`bugfix/`** - Bug fixes (non-critical)
- **`hotfix/`** - Critical fixes for production issues
- **`docs/`** - Documentation updates
- **`chore/`** - Maintenance, dependency updates, configs

### Creating a Branch

```bash
# Update from main first
git checkout main
git pull origin main

# Create your feature branch
git checkout -b feature/your-feature-name

# Work on your changes
git add .
git commit -m "Descriptive commit message"
git push origin feature/your-feature-name
```

---

## Development Workflow

### 1. Keep Your Branch Updated
Before starting work and periodically during development:
```bash
git checkout main
git pull origin main
git checkout feature/your-branch
git merge main
```

### 2. Make Commits Early & Often
```bash
git add <specific-files>        # Don't use 'git add .' blindly
git commit -m "Clear, concise message"
git push origin feature/your-branch
```

### 3. Commit Message Standard
**Format**: `[Component] Action: Description`

**Examples**:
```
[Frontend] Add: Risk heatmap visualization component
[Backend] Fix: Duplicate API detection in inventory service
[DevOps] Chore: Update Dockerfile base image to Python 3.11
[Security] Feat: Implement CWE-352 CSRF validation check
```

**Guidelines**:
- Capitalize first letter
- Use imperative mood ("Add" not "Added")
- Keep subject line under 50 characters
- Add detailed description in body (separated by blank line) for complex changes
- Reference GitHub issues if applicable: "Closes #123"

---

## Pull Request Process

### 1. Push Your Changes
```bash
git push origin feature/your-feature-name
```

### 2. Open a Pull Request on GitHub
- **Title**: Clear, follows commit message format
- **Description**: Include:
  - What you changed and why
  - Related issue(s): "Closes #123"
  - Testing performed
  - Deployment considerations (if applicable)

### 3. PR Template Example
```markdown
## Description
Brief description of changes.

## Closes
- Closes #123

## Type of Change
- [ ] Feature (non-breaking change)
- [ ] Bug fix (non-breaking change)
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe how you tested:
- [ ] Unit tests added/updated
- [ ] Manual testing performed
- [ ] Integration tested

## Deployment Notes
Any environment variables, database migrations, or config changes?

## Screenshots (if UI changes)
[Add screenshots for dashboard, alerts, etc.]
```

### 4. Code Review Process
- **Assign reviewers** based on component:
  - Backend features → Backend engineer + Security engineer
  - Frontend/Dashboard → Frontend engineer + Backend engineer (for API)
  - DevOps/Deployment → DevOps engineer + Backend engineer
  - Security checks → Security engineer + 1 other
  
- **Review expectations**:
  - Approval from 2+ engineers for critical paths
  - Approval from 1+ engineer for documentation
  - All tests must pass (CI/CD checks)
  - No merge conflicts

### 5. Address Feedback
```bash
# Make requested changes
git add <changed-files>
git commit -m "[PR Review] Address feedback on X"
git push origin feature/your-branch
# Conversation will update automatically
```

### 6. Merge to Main
After approval:
- Use "Squash and merge" for feature branches (cleaner history)
- Use "Create a merge commit" for release branches
- Delete feature branch after merge

---

## Code Style & Standards

### Python (Backend / Security Engine)
- **Style Guide**: PEP 8
- **Formatter**: `black` (`pip install black`)
- **Linter**: `flake8` (`pip install flake8`)
- **Type Hints**: Use type hints for function signatures
- **Docstrings**: Google style format

```python
def assess_api_security(api_id: str, checks: List[str]) -> Dict[str, Any]:
    """
    Assess security posture of an API against defined checks.
    
    Args:
        api_id: Unique API identifier
        checks: List of security checks to perform
        
    Returns:
        Dictionary containing assessment results and risk score
    """
    pass
```

**Check before committing**:
```bash
black backend/
flake8 backend/ --max-line-length=100
```

### JavaScript/React (Frontend)
- **Style Guide**: Airbnb JavaScript Standard
- **Formatter**: `prettier` (`npm install prettier`)
- **Linter**: `eslint` (`npm install eslint`)
- **Type Hints**: TypeScript recommended

```bash
npm run format
npm run lint
```

### Docker & Terraform (DevOps)
- **Format**: Follow best practices from official docs
- **Comments**: Document all custom configurations
- **Security**: No hardcoded secrets, use environment variables

---

## Component-Specific Contribution Guidelines

### Backend / API Discovery Engineer
- Add unit tests for discovery pipelines
- Document new inventory schema changes
- Ensure backward compatibility for API contracts
- Update API specification document

### Security & Risk Analysis Engineer
- Include test cases for security checks
- Document risk scoring algorithm changes
- Validate against OWASP/banking compliance standards
- Include evidence/rationale in risk decisions

### Frontend & DevOps Engineer
- Add tests for UI components (React Testing Library)
- Screenshot new dashboard features in PR
- Document deployment prerequisites
- Ensure changes work in containerized environment
- Add Kubernetes manifests if applicable

---

## Issues & Project Tracking

### Creating an Issue
Use GitHub Issues for bugs, features, and questions:
```
Title: [Type] Clear description
Assignee: Primary owner
Labels: bug, enhancement, documentation, critical, etc.
Milestone: Planned release (if applicable)
```

### Linking Issues to PRs
In PR description or commits:
```
Closes #123
Relates to #456
```

### Issue Labels
- `bug` - Something isn't working
- `enhancement` - New feature request
- `documentation` - Docs need update
- `critical` - High priority/security
- `help-wanted` - Community input needed
- `team-discussion` - Needs team decision

---

## Keeping Your Fork Updated

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

Or using rebase (if you prefer linear history):
```bash
git fetch upstream
git rebase upstream/main
git push origin main --force  # Use with caution!
```

---

## Communication Guidelines

### Preferred Channels
- **GitHub Issues**: Questions about specific code/features
- **GitHub Discussions**: Design decisions, team discussions
- **Pull Requests**: Technical feedback and code review
- **Slack/Teams**: Real-time blockers or urgent questions
- **Weekly Sync**: Team coordination on blocked items

### Writing Clear Comments
- **Be specific**: Reference lines, files, or decisions
- **Ask questions**: Propose alternatives rather than demands
- **Acknowledge effort**: Thank reviewers for time
- **Escalate respectfully**: Tag maintainers if decision needed

### Review Etiquette
**As a Reviewer:**
- Complete reviews within 24 hours if possible
- Be constructive and educational
- Ask clarifying questions if unclear
- Approve when satisfied (use GitHub "Approve" feature)

**As a PR Author:**
- Respond to all feedback
- Don't take criticism personally
- Ask for clarification if confused
- Thank reviewers

---

## Before You Merge

**Checklist**:
- [ ] Branch is up to date with main: `git pull origin main`
- [ ] All tests pass locally
- [ ] Code follows style guidelines (black, eslint, etc.)
- [ ] Commit messages are clear
- [ ] PR has required approvals
- [ ] No merge conflicts
- [ ] Documentation updated (README, API spec, deployment guide if needed)
- [ ] Screenshots added for UI changes
- [ ] Related issues mentioned

---

## Questions or Blocked?

1. **Check existing issues/PRs** for similar solutions
2. **Ask in GitHub Issues** with context and what you've tried
3. **Slack the team** for urgent blockers
4. **Escalate to team lead** if stuck >2 hours

---

## Recognition

Thank you for contributing to the Zombie API Defence Platform! Your work helps secure banking infrastructure against evolving threats.

**Last Updated**: March 25, 2026
