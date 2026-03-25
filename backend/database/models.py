"""
SQLAlchemy ORM models representing database tables.

Tables:
- API: Discovered APIs
- SecurityFinding: Security assessment results
- APIStatus: Classification status
- RemediationWorkflow: Decommissioning workflows
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db import Base


class API(Base):
    """
    Represents a discovered API.
    
    Attributes:
        id: Unique identifier
        name: API name
        endpoint: API URL/endpoint
        method: HTTP method (GET, POST, etc)
        owner: Team/person who owns this API
        tech_stack: Technology (Node.js, Java, Python, etc)
        status: Active, Deprecated, Orphaned, Zombie
        risk_score: 0-100 risk assessment
        created_at: When discovered
        last_traffic: Last request timestamp
    """
    __tablename__ = "apis"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    endpoint = Column(String(512), unique=True, index=True)
    method = Column(String(10))  # GET, POST, PUT, DELETE
    owner = Column(String(255), nullable=True)
    tech_stack = Column(String(255), nullable=True)
    status = Column(String(50), default="active")  # active, deprecated, orphaned, zombie
    risk_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_traffic = Column(DateTime, nullable=True)
    is_documented = Column(Boolean, default=False)
    
    # Relationships
    findings = relationship("SecurityFinding", back_populates="api")
    workflows = relationship("RemediationWorkflow", back_populates="api")


class SecurityFinding(Base):
    """
    Security assessment finding for an API.
    
    Attributes:
        api_id: Foreign key to API
        finding_type: auth, encryption, rate_limiting, data_exposure, etc
        severity: critical, high, medium, low
        description: Finding details
        remediation: Recommended fix
    """
    __tablename__ = "security_findings"
    
    id = Column(Integer, primary_key=True, index=True)
    api_id = Column(Integer, ForeignKey("apis.id"), index=True)
    finding_type = Column(String(100))  # auth, encryption, rate_limiting, etc
    severity = Column(String(20))  # critical, high, medium, low
    description = Column(Text)
    remediation = Column(Text, nullable=True)
    status = Column(String(50), default="open")  # open, in_progress, resolved
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    api = relationship("API", back_populates="findings")


class RemediationWorkflow(Base):
    """
    Tracks decommissioning/remediation workflows for APIs.
    
    Attributes:
        api_id: Which API to remediate
        workflow_status: proposed, approved, executing, completed, rolled_back
        action: decommission, deprecate, redirect, etc
        proposed_by: User who proposed
        approved_by: User who approved
    """
    __tablename__ = "remediation_workflows"
    
    id = Column(Integer, primary_key=True, index=True)
    api_id = Column(Integer, ForeignKey("apis.id"), index=True)
    workflow_status = Column(String(50))  # proposed, approved, executing, completed, rolled_back
    action = Column(String(100))  # decommission, deprecate, redirect
    proposed_by = Column(String(255))
    approved_by = Column(String(255), nullable=True)
    scheduled_date = Column(DateTime, nullable=True)
    completed_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    api = relationship("API", back_populates="workflows")


class AuditLog(Base):
    """
    Audit trail for compliance and debugging.
    
    Logs all actions: API discovered, assessment run, approval, decommissioning, etc.
    """
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(255))  # api_discovered, assessment_run, api_approved, etc
    entity_type = Column(String(50))  # api, finding, workflow
    entity_id = Column(Integer)
    user = Column(String(255))
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
