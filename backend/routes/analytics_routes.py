"""
Analytics and monitoring API routes.

Endpoints:
- GET /api/v1/analytics/metrics - Get current metrics
- GET /api/v1/analytics/alerts - Get alerts
- POST /api/v1/analytics/alerts/{id}/resolve - Resolve an alert
- GET /api/v1/analytics/trends - Get trend analysis
- GET /api/v1/analytics/health - Get system health
- GET /api/v1/analytics/report - Get comprehensive report
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime, timedelta
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])

# Sample data for analytics
SAMPLE_METRICS = [
    {
        "timestamp": (datetime.now() - timedelta(hours=i)).isoformat(),
        "metric_type": "zombie_count",
        "value": 6 + (i % 3),
        "unit": "count"
    }
    for i in range(24)
] + [
    {
        "timestamp": (datetime.now() - timedelta(hours=i)).isoformat(),
        "metric_type": "health_score",
        "value": 65 - (i % 10),
        "unit": "percentage"
    }
    for i in range(24)
]

SAMPLE_ALERTS = [
    {
        "id": "alert_1",
        "title": "High zombie API count detected",
        "description": "6 APIs classified as zombie - immediate action recommended",
        "severity": "critical",
        "type": "zombie_detection",
        "created_at": (datetime.now() - timedelta(hours=2)).isoformat(),
        "resolved": False,
        "api_ids": [1, 3, 4]
    },
    {
        "id": "alert_2",
        "title": "Deprecated API nearing end of support",
        "description": "Old Payment API will be decommissioned in 30 days",
        "severity": "warning",
        "type": "deprecation_warning",
        "created_at": (datetime.now() - timedelta(hours=5)).isoformat(),
        "resolved": False,
        "api_ids": [2]
    },
    {
        "id": "alert_3",
        "title": "Documentation update required",
        "description": "3 APIs have outdated or missing documentation",
        "severity": "warning",
        "type": "documentation",
        "created_at": (datetime.now() - timedelta(hours=12)).isoformat(),
        "resolved": False,
        "api_ids": [1, 3, 4]
    },
    {
        "id": "alert_4",
        "title": "System health improving",
        "description": "No new zombie APIs detected in last 7 days",
        "severity": "info",
        "type": "system_health",
        "created_at": (datetime.now() - timedelta(days=1)).isoformat(),
        "resolved": True,
        "api_ids": []
    }
]


@router.get("/metrics")
def get_metrics(
    metric_type: Optional[str] = Query(None, description="Filter by metric type"),
    hours: int = Query(24, description="Look back N hours")
):
    """
    Get system metrics from the last N hours.
    
    Args:
        metric_type: Filter by metric type (zombie_count, health_score, etc)
        hours: Look back N hours (default 24)
        
    Returns:
        List of metrics with timestamps
    """
    try:
        # Filter metrics based on parameters
        metrics = SAMPLE_METRICS
        
        if metric_type:
            metrics = [m for m in metrics if m["metric_type"] == metric_type]
        
        # Take only the last N hours worth
        metrics = metrics[:hours]
        
        return {
            "success": True,
            "count": len(metrics),
            "period_hours": hours,
            "filter": metric_type or "all",
            "metrics": metrics,
            "message": "Scripted demo data active"
        }
    
    except Exception as e:
        logger.error(f"Error getting metrics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve metrics")


@router.get("/alerts")
def get_alerts(
    severity: Optional[str] = Query(None, description="Filter by severity"),
    unresolved_only: bool = Query(True, description="Only unresolved alerts")
):
    """
    Get alerts from monitoring system.
    
    Args:
        severity: Filter by severity (info, warning, critical)
        unresolved_only: Only show unresolved alerts
        
    Returns:
        List of alerts
    """
    try:
        # Filter alerts based on parameters
        alerts = SAMPLE_ALERTS
        
        if severity:
            alerts = [a for a in alerts if a["severity"] == severity]
        
        if unresolved_only:
            alerts = [a for a in alerts if not a["resolved"]]
        
        return {
            "success": True,
            "count": len(alerts),
            "unresolved_filter": unresolved_only,
            "severity_filter": severity or "all",
            "alerts": alerts,
            "message": "Scripted demo data active"
        }
    
    except Exception as e:
        logger.error(f"Error getting alerts: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve alerts")


@router.post("/alerts/{alert_id}/resolve")
def resolve_alert(alert_id: str):
    """
    Mark an alert as resolved.
    
    Args:
        alert_id: ID of alert to resolve
        
    Returns:
        Success status
    """
    try:
        # Find and update the alert
        for alert in SAMPLE_ALERTS:
            if alert["id"] == alert_id:
                alert["resolved"] = True
                return {
                    "success": True,
                    "message": f"Alert {alert_id} resolved",
                    "alert_id": alert_id
                }
        
        raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")
    
    except Exception as e:
        logger.error(f"Error resolving alert: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to resolve alert")


@router.get("/health")
def get_system_health():
    """
    Get comprehensive system health assessment.
    
    Returns:
        System health metrics and recommendations
    """
    try:
        health = {
            "status": "warning",
            "health_score": 68,
            "timestamp": datetime.now().isoformat(),
            "total_apis": 6,
            "api_breakdown": {
                "active": 0,
                "zombie": 3,
                "deprecated": 2,
                "orphaned": 1
            },
            "risk_distribution": {
                "critical": 3,
                "high": 2,
                "medium": 1,
                "low": 0
            },
            "active_alerts": 3,
            "last_scan": (datetime.now() - timedelta(hours=1)).isoformat(),
            "recommendations": [
                "Review and remediate 3 zombie APIs immediately",
                "Schedule deprecation timeline for 2 deprecated APIs",
                "Update documentation for 3 APIs",
                "Establish ownership for orphaned API",
                "Implement automated monitoring for new API deployments"
            ]
        }
        
        return {
            "success": True,
            "health": health,
            "message": "Scripted demo data active"
        }
    
    except Exception as e:
        logger.error(f"Error getting system health: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get system health")


@router.get("/trends")
def get_trends(days: int = Query(7, description="Analyze last N days")):
    """
    Get trend analysis over time period.
    
    Args:
        days: Analyze last N days (default 7)
        
    Returns:
        Trend analysis with direction indicators
    """
    try:
        if days < 1:
            raise HTTPException(status_code=400, detail="days parameter must be >= 1")
        
        trends = {
            "period_days": days,
            "zombie_apis": {
                "current": 3,
                "previous_period": 3,
                "change": 0,
                "trend": "stable",
                "details": "Zombie API count has remained stable over the past week"
            },
            "health_score": {
                "current": 68,
                "previous_period": 70,
                "change": -2,
                "trend": "declining",
                "details": "Health score showing slight decline due to increased zombie API detection"
            },
            "api_coverage": {
                "documented": 3,
                "undocumented": 3,
                "percentage": 50,
                "trend": "stable",
                "details": "Documentation coverage needs improvement"
            },
            "deprecation_status": {
                "on_schedule": 2,
                "overdue": 0,
                "trend": "good",
                "details": "All deprecation timelines are being met"
            }
        }
        
        return {
            "success": True,
            "trends": trends,
            "message": "Scripted demo data active"
        }
    
    except Exception as e:
        logger.error(f"Error getting trends: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to analyze trends")


@router.get("/report")
def get_comprehensive_report():
    """
    Get comprehensive analytics report.
    
    Returns:
        Complete system status, metrics, alerts, health, and recommendations
    """
    try:
        report = {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "overall_status": "warning",
                "health_score": 68,
                "total_apis": 6,
                "zombie_apis": 3,
                "deprecated_apis": 2,
                "orphaned_apis": 1,
                "active_alerts": 3
            },
            "metrics": {
                "count": 48,
                "period_hours": 24,
                "latest_values": {
                    "zombie_count": 3,
                    "health_score": 68
                }
            },
            "alerts": {
                "total": 4,
                "unresolved": 3,
                "by_severity": {
                    "critical": 1,
                    "warning": 2,
                    "info": 1
                },
                "recent": [
                    {
                        "id": "alert_1",
                        "title": "High zombie API count detected",
                        "severity": "critical",
                        "created_at": (datetime.now() - timedelta(hours=2)).isoformat()
                    }
                ]
            },
            "trends": {
                "zombie_trend": "stable",
                "health_trend": "declining",
                "recommendations_count": 5
            },
            "recommendations": [
                "Review and remediate 3 zombie APIs immediately",
                "Schedule deprecation timeline for 2 deprecated APIs",
                "Update documentation for 3 APIs",
                "Establish ownership for orphaned API",
                "Implement automated monitoring for new API deployments"
            ],
            "next_scan": (datetime.now() + timedelta(hours=1)).isoformat()
        }
        
        return {
            "success": True,
            "report": report,
            "message": "Scripted demo data active"
        }
    
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate report")


@router.post("/thresholds/{metric_type}")
def set_alert_threshold(
    metric_type: str,
    threshold: float = Query(..., description="Threshold value")
):
    """
    Set alert threshold for a metric type.
    
    Args:
        metric_type: Type of metric
        threshold: Threshold value
        
    Returns:
        Success status
    """
    try:
        valid_types = ["zombie_count", "health_score", "api_age", "documentation_coverage"]
        
        if metric_type not in valid_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid metric type. Must be one of: {valid_types}"
            )
        
        return {
            "success": True,
            "message": f"Threshold set for {metric_type}",
            "metric_type": metric_type,
            "threshold": threshold,
            "note": "Configuration stored (demo mode - not persistent)"
        }
    
    except Exception as e:
        logger.error(f"Error setting threshold: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to set threshold")
