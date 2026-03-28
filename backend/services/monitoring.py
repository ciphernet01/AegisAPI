"""
Monitoring and metrics collection for zombie API detection system.

Tracks:
- API classification changes
- Remediation actions performed
- System health metrics
- Historical trends
- Alert triggers
"""

from enum import Enum
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from database.models import API
from security.classification import classify_api, APIStatus
from utils.logger import get_logger

logger = get_logger(__name__)


class MetricType(str, Enum):
    """Types of metrics collected."""
    ZOMBIE_COUNT = "zombie_count"
    DEPRECATED_COUNT = "deprecated_count"
    ORPHANED_COUNT = "orphaned_count"
    ACTIVE_COUNT = "active_count"
    HEALTH_SCORE = "health_score"
    REMEDIATION_ACTION = "remediation_action"
    CLASSIFICATION_CHANGED = "classification_changed"


class AlertSeverity(str, Enum):
    """Severity levels for alerts."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class Metric:
    """Individual metric data point."""
    metric_type: MetricType
    value: float
    timestamp: datetime
    api_id: Optional[int] = None
    labels: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "metric_type": self.metric_type.value,
            "value": self.value,
            "timestamp": self.timestamp.isoformat(),
            "api_id": self.api_id,
            "labels": self.labels or {}
        }


@dataclass
class Alert:
    """Alert triggered by monitoring system."""
    alert_id: str
    severity: AlertSeverity
    title: str
    description: str
    metric_type: MetricType
    triggered_value: float
    threshold: float
    timestamp: datetime
    resolved: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "alert_id": self.alert_id,
            "severity": self.severity.value,
            "title": self.title,
            "description": self.description,
            "metric_type": self.metric_type.value,
            "triggered_value": self.triggered_value,
            "threshold": self.threshold,
            "timestamp": self.timestamp.isoformat(),
            "resolved": self.resolved
        }


class MonitoringEngine:
    """Engine for collecting and analyzing metrics."""

    def __init__(self):
        """Initialize monitoring engine."""
        self.metrics: List[Metric] = []
        self.alerts: List[Alert] = []
        self.thresholds = {
            MetricType.ZOMBIE_COUNT: 5,  # Alert if >= 5 zombies
            MetricType.HEALTH_SCORE: 70,  # Alert if <= 70%
            MetricType.ORPHANED_COUNT: 3  # Alert if >= 3 orphaned APIs
        }

    def collect_metrics(self, db: Session) -> Dict[str, Any]:
        """
        Collect current system metrics.
        
        Args:
            db: Database session
            
        Returns:
            Current metrics snapshot
        """
        all_apis = db.query(API).all()
        timestamp = datetime.utcnow()
        
        metrics_snapshot = {
            "timestamp": timestamp.isoformat(),
            "total_apis": len(all_apis),
            "classifications": {}
        }
        
        zombie_count = 0
        deprecated_count = 0
        orphaned_count = 0
        active_count = 0
        health_apis = 0
        
        # Classify all APIs
        for api in all_apis:
            status, analysis = classify_api(api)
            classification_risk_score = analysis.get("risk_score", 0.0)
            
            if status == APIStatus.ZOMBIE:
                zombie_count += 1
            elif status == APIStatus.DEPRECATED:
                deprecated_count += 1
            elif status == APIStatus.ORPHANED:
                orphaned_count += 1
            elif status == APIStatus.ACTIVE:
                active_count += 1
                if classification_risk_score < 50:
                    health_apis += 1
            
            # Record metric
            self.metrics.append(Metric(
                metric_type=MetricType.CLASSIFICATION_CHANGED,
                value=classification_risk_score,
                timestamp=timestamp,
                api_id=api.id,
                labels={"status": status.value}
            ))
        
        # Calculate aggregate metrics
        total = len(all_apis)
        health_score = (health_apis / total * 100) if total > 0 else 0
        
        metrics_snapshot["zombie_count"] = zombie_count
        metrics_snapshot["deprecated_count"] = deprecated_count
        metrics_snapshot["orphaned_count"] = orphaned_count
        metrics_snapshot["active_count"] = active_count
        metrics_snapshot["health_score"] = round(health_score, 2)
        metrics_snapshot["classifications"] = {
            "zombie": zombie_count,
            "deprecated": deprecated_count,
            "orphaned": orphaned_count,
            "active": active_count
        }
        
        # Store aggregate metrics
        self.metrics.extend([
            Metric(MetricType.ZOMBIE_COUNT, zombie_count, timestamp),
            Metric(MetricType.DEPRECATED_COUNT, deprecated_count, timestamp),
            Metric(MetricType.ORPHANED_COUNT, orphaned_count, timestamp),
            Metric(MetricType.ACTIVE_COUNT, active_count, timestamp),
            Metric(MetricType.HEALTH_SCORE, health_score, timestamp)
        ])
        
        # Check thresholds and generate alerts
        self._check_thresholds(zombie_count, deprecated_count, orphaned_count, health_score, timestamp)
        
        logger.info(f"Metrics collected: {metrics_snapshot}")
        return metrics_snapshot

    def _check_thresholds(
        self,
        zombie_count: int,
        deprecated_count: int,
        orphaned_count: int,
        health_score: float,
        timestamp: datetime
    ):
        """Check metrics against thresholds and generate alerts."""
        # Zombie count alert
        if zombie_count >= self.thresholds[MetricType.ZOMBIE_COUNT]:
            self._create_alert(
                severity=AlertSeverity.CRITICAL if zombie_count >= 10 else AlertSeverity.WARNING,
                title="High Zombie API Count",
                description=f"{zombie_count} zombie APIs detected. Threshold: {self.thresholds[MetricType.ZOMBIE_COUNT]}",
                metric_type=MetricType.ZOMBIE_COUNT,
                triggered_value=zombie_count,
                threshold=self.thresholds[MetricType.ZOMBIE_COUNT],
                timestamp=timestamp
            )
        
        # Health score alert
        if health_score <= self.thresholds[MetricType.HEALTH_SCORE]:
            self._create_alert(
                severity=AlertSeverity.WARNING,
                title="Low System Health Score",
                description=f"Health score is {health_score}%. Threshold: {self.thresholds[MetricType.HEALTH_SCORE]}%",
                metric_type=MetricType.HEALTH_SCORE,
                triggered_value=health_score,
                threshold=self.thresholds[MetricType.HEALTH_SCORE],
                timestamp=timestamp
            )
        
        # Orphaned count alert
        if orphaned_count >= self.thresholds[MetricType.ORPHANED_COUNT]:
            self._create_alert(
                severity=AlertSeverity.WARNING,
                title="Orphaned APIs Detected",
                description=f"{orphaned_count} orphaned APIs found. Threshold: {self.thresholds[MetricType.ORPHANED_COUNT]}",
                metric_type=MetricType.ORPHANED_COUNT,
                triggered_value=orphaned_count,
                threshold=self.thresholds[MetricType.ORPHANED_COUNT],
                timestamp=timestamp
            )

    def _create_alert(
        self,
        severity: AlertSeverity,
        title: str,
        description: str,
        metric_type: MetricType,
        triggered_value: float,
        threshold: float,
        timestamp: datetime
    ):
        """Create and store an alert."""
        import uuid
        alert = Alert(
            alert_id=str(uuid.uuid4()),
            severity=severity,
            title=title,
            description=description,
            metric_type=metric_type,
            triggered_value=triggered_value,
            threshold=threshold,
            timestamp=timestamp
        )
        self.alerts.append(alert)
        logger.warning(f"Alert triggered: {title} (severity: {severity.value})")

    def get_metrics(self, metric_type: Optional[MetricType] = None, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Get metrics from the last N hours.
        
        Args:
            metric_type: Filter by metric type (optional)
            hours: Look back N hours
            
        Returns:
            List of metrics
        """
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        filtered_metrics = [
            m for m in self.metrics
            if m.timestamp >= cutoff_time
        ]
        
        if metric_type:
            filtered_metrics = [m for m in filtered_metrics if m.metric_type == metric_type]
        
        return [m.to_dict() for m in filtered_metrics]

    def get_alerts(self, severity: Optional[AlertSeverity] = None, unresolved_only: bool = True) -> List[Dict[str, Any]]:
        """
        Get alerts.
        
        Args:
            severity: Filter by severity (optional)
            unresolved_only: Only show unresolved alerts
            
        Returns:
            List of alerts
        """
        filtered_alerts = self.alerts
        
        if unresolved_only:
            filtered_alerts = [a for a in filtered_alerts if not a.resolved]
        
        if severity:
            filtered_alerts = [a for a in filtered_alerts if a.severity == severity]
        
        return [a.to_dict() for a in filtered_alerts]

    def resolve_alert(self, alert_id: str) -> bool:
        """
        Mark an alert as resolved.
        
        Args:
            alert_id: ID of alert to resolve
            
        Returns:
            True if resolved, False if not found
        """
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.resolved = True
                logger.info(f"Alert {alert_id} resolved")
                return True
        return False

    def get_trend_analysis(self, db: Session, days: int = 7) -> Dict[str, Any]:
        """
        Analyze trends over time period.
        
        Args:
            db: Database session
            days: Analyze last N days
            
        Returns:
            Trend analysis
        """
        cutoff_time = datetime.utcnow() - timedelta(days=days)
        
        # Get metrics from period
        recent_metrics = [m for m in self.metrics if m.timestamp >= cutoff_time]
        
        if not recent_metrics:
            return {
                "period_days": days,
                "message": "No metrics available for period"
            }
        
        # Extract zombie count metrics
        zombie_metrics = [m for m in recent_metrics if m.metric_type == MetricType.ZOMBIE_COUNT]
        health_metrics = [m for m in recent_metrics if m.metric_type == MetricType.HEALTH_SCORE]
        
        analysis = {
            "period_days": days,
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "zombie_trend": None,
            "health_trend": None
        }
        
        if zombie_metrics:
            zombie_values = [m.value for m in zombie_metrics]
            analysis["zombie_trend"] = {
                "current": zombie_values[-1],
                "average": sum(zombie_values) / len(zombie_values),
                "min": min(zombie_values),
                "max": max(zombie_values),
                "direction": "increasing" if zombie_values[-1] > zombie_values[0] else "decreasing"
            }
        
        if health_metrics:
            health_values = [m.value for m in health_metrics]
            analysis["health_trend"] = {
                "current": health_values[-1],
                "average": sum(health_values) / len(health_values),
                "min": min(health_values),
                "max": max(health_values),
                "direction": "improving" if health_values[-1] > health_values[0] else "declining"
            }
        
        return analysis

    def set_threshold(self, metric_type: MetricType, threshold: float):
        """
        Set alert threshold for a metric.
        
        Args:
            metric_type: Type of metric
            threshold: Alert threshold value
        """
        self.thresholds[metric_type] = threshold
        logger.info(f"Threshold set for {metric_type.value}: {threshold}")

    def get_system_health(self, db: Session) -> Dict[str, Any]:
        """
        Get comprehensive system health assessment.
        
        Args:
            db: Database session
            
        Returns:
            Health assessment
        """
        # Collect latest metrics
        snapshot = self.collect_metrics(db)
        
        total_apis = snapshot["total_apis"]
        health_score = snapshot["health_score"]
        
        # Calculate risk distribution
        risk_distribution = {
            "healthy": snapshot["active_count"],
            "at_risk": snapshot["deprecated_count"],
            "critical": snapshot["zombie_count"] + snapshot["orphaned_count"]
        }
        
        # Overall status
        if health_score >= 80:
            overall_status = "healthy"
        elif health_score >= 60:
            overall_status = "warning"
        else:
            overall_status = "critical"
        
        return {
            "timestamp": snapshot["timestamp"],
            "overall_status": overall_status,
            "health_score": health_score,
            "total_apis": total_apis,
            "risk_distribution": risk_distribution,
            "active_alerts": len([a for a in self.alerts if not a.resolved]),
            "unresolved_critical_alerts": len([a for a in self.alerts if not a.resolved and a.severity == AlertSeverity.CRITICAL]),
            "recommendations": self._generate_recommendations(snapshot, self.alerts)
        }

    def _generate_recommendations(self, snapshot: Dict[str, Any], alerts: List[Alert]) -> List[str]:
        """Generate recommendations based on current state."""
        recommendations = []
        
        if snapshot["zombie_count"] > 5:
            recommendations.append("Execute bulk remediation for high-risk zombie APIs")
        
        if snapshot["orphaned_count"] > 2:
            recommendations.append("Assign owners to orphaned APIs or mark for archival")
        
        if snapshot["health_score"] < 70:
            recommendations.append("Review and remediate low-health APIs to improve system health")
        
        critical_alerts = [a for a in alerts if a.severity == AlertSeverity.CRITICAL and not a.resolved]
        if critical_alerts:
            recommendations.append(f"Address {len(critical_alerts)} critical alert(s)")
        
        return recommendations if recommendations else ["System health is good"]
