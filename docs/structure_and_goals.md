# Project Structure and Goals

## File/Folder Structure

- backend/
  - discovery/           # API discovery modules (code parsing, network, traffic)
  - inventory/           # Centralized API inventory database logic
  - usage_tracking/      # Usage tracking and log/gateway integration
  - __init__.py
- security/
  - classification/      # API lifecycle classification logic
  - assessment/          # Security posture checks (auth, encryption, etc.)
  - risk_scoring/        # Risk scoring model
  - remediation/         # Remediation and decommissioning logic
  - __init__.py
- frontend/
  - dashboard/           # UI for API visibility and risk monitoring
  - alerting/            # Alerting and notification mechanisms
  - workflows/           # Decommissioning workflows
  - __init__.py
- devops/
  - container/           # Dockerfiles, containerization scripts
  - ci_cd/               # CI/CD pipeline configs
- tests/                 # Automated tests for all modules
- docs/
  - architecture.md      # System architecture and data flow
  - api.md               # API documentation
  - team_roles.md        # Team responsibilities and contacts
- .gitignore
- CONTRIBUTING.md
- README.md

## Project Goals

1. **Automated API Discovery**
   - Scan code, network, and traffic to find all APIs (including undocumented/zombie APIs).
2. **Centralized API Inventory**
   - Store metadata: endpoint, method, owner, last usage, source, etc.
3. **API Classification & Security Assessment**
   - Classify APIs (active, deprecated, orphaned, zombie).
   - Assess security posture: authentication, encryption, rate limiting, data exposure.
4. **Risk Scoring & Remediation**
   - Score APIs based on risk factors.
   - Provide actionable remediation and decommissioning workflows.
5. **Visibility & Monitoring**
   - Dashboard for API status, filtering, and risk monitoring.
   - Alerting for new/high-risk APIs.
6. **Continuous Integration & Deployment**
   - Containerized deployment and automated monitoring.

---

This structure and goals document keeps the team aligned as we build the Zombie API Discovery and Defence Platform.
