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

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import Optional

from database.db import get_db
from services.monitoring import MonitoringEngine, MetricType, AlertSeverity
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])

# Global monitoring engine
monitoring_engine = MonitoringEngine()


@router.get("/metrics")
def get_metrics(
    metric_type: Optional[str] = Query(None, description="Filter by metric type"),
    hours: int = Query(24, description="Look back N hours"),
    db: Session = Depends(get_db)
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
        # If metric_type provided, validate it
        filter_type = None
        if metric_type:
            try:
                filter_type = MetricType(metric_type)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid metric type. Must be one of: {[m.value for m in MetricType]}"
                )
        
        metrics = monitoring_engine.get_metrics(metric_type=filter_type, hours=hours)
        
        return {
            "success": True,
            "count": len(metrics),
            "period_hours": hours,
            "filter": metric_type or "all",
            "metrics": metrics
        }
    
    except Exception as e:
        logger.error(f"Error getting metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts")
def get_alerts(
    severity: Optional[str] = Query(None, description="Filter by severity"),
    unresolved_only: bool = Query(True, description="Only unresolved alerts"),
    db: Session = Depends(get_db)
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
        # Validate severity if provided
        filter_severity = None
        if severity:
            try:
                filter_severity = AlertSeverity(severity)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid severity. Must be one of: {[s.value for s in AlertSeverity]}"
                )
        
        alerts = monitoring_engine.get_alerts(severity=filter_severity, unresolved_only=unresolved_only)
        
        return {
            "success": True,
            "count": len(alerts),
            "unresolved_filter": unresolved_only,
            "severity_filter": severity or "all",
            "alerts": alerts
        }
    
    except Exception as e:
        logger.error(f"Error getting alerts: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/alerts/{alert_id}/resolve")
def resolve_alert(
    alert_id: str,
    db: Session = Depends(get_db)
):
    """
    Mark an alert as resolved.
    
    Args:
        alert_id: ID of alert to resolve
        
    Returns:
        Success status
    """
    try:
        resolved = monitoring_engine.resolve_alert(alert_id)
        
        if not resolved:
            raise HTTPException(
                status_code=404,
                detail=f"Alert {alert_id} not found"
            )
        
        return {
            "success": True,
            "message": f"Alert {alert_id} resolved",
            "alert_id": alert_id
        }
    
    except Exception as e:
        logger.error(f"Error resolving alert: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
def get_system_health(db: Session = Depends(get_db)):
    """
    Get comprehensive system health assessment.
    
    Returns:
        System health metrics and recommendations
    """
    try:
        health = monitoring_engine.get_system_health(db)
        
        return {
            "success": True,
            "health": health
        }
    
    except Exception as e:
        logger.error(f"Error getting system health: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trends")
def get_trends(
    days: int = Query(7, description="Analyze last N days"),
    db: Session = Depends(get_db)
):
    """
    Get trend analysis over time period.
    
    Args:
        days: Analyze last N days (default 7)
        
    Returns:
        Trend analysis with direction indicators
    """
    try:
        if days < 1:
            raise HTTPException(
                status_code=400,
                detail="days parameter must be >= 1"
            )
        
        trends = monitoring_engine.get_trend_analysis(db, days=days)
        
        return {
            "success": True,
            "trends": trends
        }
    
    except Exception as e:
        logger.error(f"Error getting trends: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/report")
def get_comprehensive_report(db: Session = Depends(get_db)):
    """
    Get comprehensive analytics report.
    
    Returns:
        Complete system status, metrics, alerts, health, and recommendations
    """
    try:
        # Collect all components
        metrics = monitoring_engine.get_metrics(hours=24)
        alerts = monitoring_engine.get_alerts(unresolved_only=False)
        health = monitoring_engine.get_system_health(db)
        trends = monitoring_engine.get_trend_analysis(db, days=7)
        
        return {
            "success": True,
            "report": {
                "generated_at": health["timestamp"],
                "summary": {
                    "overall_status": health["overall_status"],
                    "health_score": health["health_score"],
                    "total_apis": health["total_apis"],
                    "risk_distribution": health["risk_distribution"],
                    "active_alerts": health["active_alerts"]
                },
                "metrics": {
                    "count": len(metrics),
                    "last_24h": metrics[:10]  # Last 10 metric points
                },
                "alerts": {
                    "total": len(alerts),
                    "unresolved": len([a for a in alerts if not a["resolved"]]),
                    "by_severity": {
                        "critical": len([a for a in alerts if a["severity"] == "critical"]),
                        "warning": len([a for a in alerts if a["severity"] == "warning"]),
                        "info": len([a for a in alerts if a["severity"] == "info"])
                    },
                    "recent": alerts[:5]  # Last 5 alerts
                },
                "trends": trends,
                "recommendations": health["recommendations"]
            }
        }
    
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/thresholds/{metric_type}")
def set_alert_threshold(
    metric_type: str,
    threshold: float = Query(..., description="Threshold value"),
    db: Session = Depends(get_db)
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
        # Validate metric type
        try:
            mtype = MetricType(metric_type)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid metric type. Must be one of: {[m.value for m in MetricType]}"
            )
        
        monitoring_engine.set_threshold(mtype, threshold)
        
        return {
            "success": True,
            "message": f"Threshold set for {metric_type}",
            "metric_type": metric_type,
            "threshold": threshold
        }
    
    except Exception as e:
        logger.error(f"Error setting threshold: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
