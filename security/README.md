# Security Module Structure

This document describes the structure and responsibilities of the security modules in the Zombie API Discovery and Defence Platform.

## Folders & Responsibilities

- **classification/**
  - Logic to classify APIs as active, deprecated, orphaned, or zombie.
  - Main file: `classification.py`
- **assessment/**
  - Functions to check authentication, encryption, rate limiting, and sensitive data exposure for APIs.
  - Main file: `assessment.py`
- **risk_scoring/**
  - Logic to calculate a risk score for each API based on assessment and metadata.
  - Main file: `risk_scoring.py`
- **remediation/**
  - (To be implemented) Logic to generate remediation recommendations and flag APIs for decommissioning.

## Integration Points
- These modules consume API metadata and assessment results from the backend discovery pipeline.
- Outputs are used by the dashboard and alerting systems for visibility and action.

## Next Steps
- Expand remediation logic.
- Integrate with backend and frontend modules.
- Add automated tests for each module.
