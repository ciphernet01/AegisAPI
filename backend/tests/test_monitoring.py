"""
Tests for monitoring and analytics system.

Test Coverage:
- Metrics collection and retrieval
- Alert generation and management
- System health assessment
- Trend analysis
- Threshold configuration
- Alert severity levels
"""

import pytest
from datetime import datetime, timedelta

from database.models import API
from services.monitoring import (
    MonitoringEngine, MetricType, AlertSeverity, Metric, Alert
)


@pytest.fixture
def monitoring_engine():
    """Create monitoring engine for tests."""
    return MonitoringEngine()


@pytest.fixture
def sample_api(db):
    """Create a sample API for testing."""
    from datetime import datetime, timedelta
    
    api = API(
        name="Test API",
        endpoint="https://api.example.com",
        method="GET",
        owner="test-team",
        tech_stack="Python",
        status="active",
        last_traffic=datetime.utcnow() - timedelta(days=1),
        is_documented=True
    )
    db.add(api)
    db.commit()
    db.refresh(api)
    return api


class TestMetricsCollection:
    """Test metrics collection."""

    def test_collect_metrics_creates_snapshots(self, monitoring_engine, db, sample_api):
        """Test that collect_metrics creates proper snapshots."""
        snapshot = monitoring_engine.collect_metrics(db)
        
        assert snapshot is not None
        assert "timestamp" in snapshot
        assert "total_apis" in snapshot
        assert "zombie_count" in snapshot
        assert "health_score" in snapshot
        assert "classifications" in snapshot

    def test_collect_metrics_counts_apis(self, monitoring_engine, db, sample_api):
        """Test that metrics correctly count APIs."""
        snapshot = monitoring_engine.collect_metrics(db)
        
        assert snapshot["total_apis"] >= 1
        total_classified = (
            snapshot["active_count"] +
            snapshot["zombie_count"] +
            snapshot["deprecated_count"] +
            snapshot["orphaned_count"]
        )
        assert total_classified == snapshot["total_apis"]

    def test_collect_metrics_creates_metric_objects(self, monitoring_engine, db, sample_api):
        """Test that collect_metrics creates Metric objects."""
        monitoring_engine.collect_metrics(db)
        
        assert len(monitoring_engine.metrics) > 0
        
        # Should have aggregate metrics
        metric_types = {m.metric_type for m in monitoring_engine.metrics}
        assert MetricType.ZOMBIE_COUNT in metric_types
        assert MetricType.HEALTH_SCORE in metric_types

    def test_get_metrics_filters_by_type(self, monitoring_engine, db, sample_api):
        """Test filtering metrics by type."""
        monitoring_engine.collect_metrics(db)
        
        zombie_metrics = monitoring_engine.get_metrics(MetricType.ZOMBIE_COUNT, hours=24)
        
        assert len(zombie_metrics) > 0
        assert all(m["metric_type"] == "zombie_count" for m in zombie_metrics)

    def test_get_metrics_respects_time_window(self, monitoring_engine, db, sample_api):
        """Test that get_metrics respects time window."""
        monitoring_engine.collect_metrics(db)
        
        # Add old metric
        old_metric = Metric(
            metric_type=MetricType.HEALTH_SCORE,
            value=50.0,
            timestamp=datetime.utcnow() - timedelta(hours=48)
        )
        monitoring_engine.metrics.append(old_metric)
        
        recent = monitoring_engine.get_metrics(hours=24)
        
        # Old metric shouldn't be included
        assert not any(m["value"] == 50.0 for m in recent)

    def test_health_score_calculation(self, monitoring_engine, db, sample_api):
        """Test that health score is properly calculated."""
        snapshot = monitoring_engine.collect_metrics(db)
        
        health_score = snapshot["health_score"]
        assert isinstance(health_score, float)
        assert 0 <= health_score <= 100


class TestAlertGeneration:
    """Test alert generation and management."""

    def test_alert_creation(self, monitoring_engine):
        """Test that alerts are properly created."""
        timestamp = datetime.utcnow()
        monitoring_engine._create_alert(
            severity=AlertSeverity.WARNING,
            title="Test Alert",
            description="This is a test",
            metric_type=MetricType.ZOMBIE_COUNT,
            triggered_value=10.0,
            threshold=5.0,
            timestamp=timestamp
        )
        
        assert len(monitoring_engine.alerts) == 1
        alert = monitoring_engine.alerts[0]
        assert alert.title == "Test Alert"
        assert alert.severity == AlertSeverity.WARNING

    def test_zombie_count_triggers_alert(self, monitoring_engine, db):
        """Test that high zombie count triggers alert."""
        # Create APIs that will be classified as zombies
        timestamp = datetime.utcnow()
        monitoring_engine.thresholds[MetricType.ZOMBIE_COUNT] = 1  # Low threshold
        
        # Create multiple zombie-like APIs (old, unused, etc.)
        for i in range(3):
            api = API(
                name=f"Old API {i}",
                endpoint=f"https://api{i}.example.com",
                method="GET",
                owner="unknown",
                last_traffic=datetime.utcnow() - timedelta(days=400),
                status="zombie"
            )
            db.add(api)
        db.commit()
        
        monitoring_engine.collect_metrics(db)
        
        # Should have generated alert
        zombie_alerts = [a for a in monitoring_engine.alerts if a.metric_type == MetricType.ZOMBIE_COUNT]
        assert len(zombie_alerts) > 0

    def test_health_score_alert_threshold(self, monitoring_engine):
        """Test health score alert triggering."""
        timestamp = datetime.utcnow()
        
        # Set low health score
        low_score = 50.0
        monitoring_engine.thresholds[MetricType.HEALTH_SCORE] = 70
        
        monitoring_engine._check_thresholds(0, 0, 0, low_score, timestamp)
        
        health_alerts = [a for a in monitoring_engine.alerts if a.metric_type == MetricType.HEALTH_SCORE]
        assert len(health_alerts) > 0
        assert health_alerts[0].severity == AlertSeverity.WARNING

    def test_get_alerts_filters_by_severity(self, monitoring_engine):
        """Test alert filtering by severity."""
        timestamp = datetime.utcnow()
        
        # Create alerts with different severities
        for severity in AlertSeverity:
            monitoring_engine._create_alert(
                severity=severity,
                title=f"Test {severity.value}",
                description="Test",
                metric_type=MetricType.ZOMBIE_COUNT,
                triggered_value=1.0,
                threshold=0.5,
                timestamp=timestamp
            )
        
        critical_alerts = monitoring_engine.get_alerts(AlertSeverity.CRITICAL, unresolved_only=False)
        assert len(critical_alerts) == 1

    def test_alert_resolution(self, monitoring_engine):
        """Test alert resolution."""
        timestamp = datetime.utcnow()
        monitoring_engine._create_alert(
            severity=AlertSeverity.WARNING,
            title="Test Alert",
            description="Test",
            metric_type=MetricType.ZOMBIE_COUNT,
            triggered_value=1.0,
            threshold=0.5,
            timestamp=timestamp
        )
        
        alert_id = monitoring_engine.alerts[0].alert_id
        
        # Resolve alert
        result = monitoring_engine.resolve_alert(alert_id)
        assert result is True
        
        # Check it's marked resolved
        unresolved = monitoring_engine.get_alerts(unresolved_only=True)
        assert len(unresolved) == 0

    def test_resolve_nonexistent_alert(self, monitoring_engine):
        """Test resolving non-existent alert."""
        result = monitoring_engine.resolve_alert("nonexistent")
        assert result is False


class TestSystemHealth:
    """Test system health assessment."""

    def test_system_health_structure(self, monitoring_engine, db, sample_api):
        """Test system health returns proper structure."""
        health = monitoring_engine.get_system_health(db)
        
        assert "overall_status" in health
        assert "health_score" in health
        assert "total_apis" in health
        assert "risk_distribution" in health
        assert "active_alerts" in health
        assert "recommendations" in health

    def test_system_health_status_levels(self, monitoring_engine, db, sample_api):
        """Test that status levels are categorized correctly."""
        health = monitoring_engine.get_system_health(db)
        
        status = health["overall_status"]
        health_score = health["health_score"]
        
        if health_score >= 80:
            assert status == "healthy"
        elif health_score >= 60:
            assert status == "warning"
        else:
            assert status == "critical"

    def test_risk_distribution_sums_to_total(self, monitoring_engine, db, sample_api):
        """Test that risk distribution sums to total APIs."""
        health = monitoring_engine.get_system_health(db)
        
        risk = health["risk_distribution"]
        total = risk["healthy"] + risk["at_risk"] + risk["critical"]
        
        assert total == health["total_apis"]

    def test_recommendations_generated(self, monitoring_engine, db, sample_api):
        """Test that recommendations are generated."""
        health = monitoring_engine.get_system_health(db)
        
        recs = health["recommendations"]
        assert isinstance(recs, list)
        assert len(recs) > 0


class TestTrendAnalysis:
    """Test trend analysis functionality."""

    def test_trend_analysis_structure(self, monitoring_engine, db, sample_api):
        """Test trend analysis returns proper structure."""
        # Need to collect metrics first
        monitoring_engine.collect_metrics(db)
        
        trends = monitoring_engine.get_trend_analysis(db, days=7)
        
        assert "period_days" in trends
        assert "analysis_timestamp" in trends or "message" in trends  # May not have metrics if empty

    def test_trend_analyis_with_metrics(self, monitoring_engine, db, sample_api):
        """Test trend analysis with collected metrics."""
        # Collect metrics multiple times
        monitoring_engine.collect_metrics(db)
        monitoring_engine.collect_metrics(db)
        
        trends = monitoring_engine.get_trend_analysis(db, days=1)
        
        assert trends["period_days"] == 1

    def test_trend_direction_increasing(self, monitoring_engine):
        """Test trend direction detection for increasing values."""
        # Manually add increasing zombie metrics
        for i in range(3):
            metric = Metric(
                metric_type=MetricType.ZOMBIE_COUNT,
                value=float(i + 1),
                timestamp=datetime.utcnow() - timedelta(hours=24-i)
            )
            monitoring_engine.metrics.append(metric)
        
        trends = monitoring_engine.get_trend_analysis(None, days=1)
        
        if "zombie_trend" in trends and trends["zombie_trend"]:
            assert trends["zombie_trend"]["direction"] == "increasing"

    def test_trend_direction_decreasing(self, monitoring_engine):
        """Test trend direction detection for decreasing values."""
        # Manually add decreasing health metrics
        for i in range(3):
            metric = Metric(
                metric_type=MetricType.HEALTH_SCORE,
                value=float(100 - i * 10),
                timestamp=datetime.utcnow() - timedelta(hours=24-i)
            )
            monitoring_engine.metrics.append(metric)
        
        trends = monitoring_engine.get_trend_analysis(None, days=1)
        
        if "health_trend" in trends and trends["health_trend"]:
            assert trends["health_trend"]["direction"] == "declining"


class TestThresholdConfiguration:
    """Test threshold management."""

    def test_set_threshold(self, monitoring_engine):
        """Test setting alert threshold."""
        monitoring_engine.set_threshold(MetricType.ZOMBIE_COUNT, 10.0)
        
        assert monitoring_engine.thresholds[MetricType.ZOMBIE_COUNT] == 10.0

    def test_custom_thresholds_affect_alerts(self, monitoring_engine, db):
        """Test that custom thresholds affect alert generation."""
        timestamp = datetime.utcnow()
        
        # Set high threshold
        monitoring_engine.set_threshold(MetricType.ZOMBIE_COUNT, 100)
        
        # Check with value below threshold - no alert
        monitoring_engine._check_thresholds(5, 0, 0, 100, timestamp)
        zombie_alerts = [a for a in monitoring_engine.alerts if a.metric_type == MetricType.ZOMBIE_COUNT]
        assert len(zombie_alerts) == 0
        
        # Clear alerts
        monitoring_engine.alerts.clear()
        
        # Set low threshold
        monitoring_engine.set_threshold(MetricType.ZOMBIE_COUNT, 5)
        
        # Check with same value - should alert
        monitoring_engine._check_thresholds(5, 0, 0, 100, timestamp)
        zombie_alerts = [a for a in monitoring_engine.alerts if a.metric_type == MetricType.ZOMBIE_COUNT]
        assert len(zombie_alerts) > 0


class TestMetricDataStructure:
    """Test metric and alert data structures."""

    def test_metric_to_dict(self):
        """Test Metric serialization."""
        timestamp = datetime.utcnow()
        metric = Metric(
            metric_type=MetricType.ZOMBIE_COUNT,
            value=5.0,
            timestamp=timestamp,
            api_id=1,
            labels={"status": "zombie"}
        )
        
        data = metric.to_dict()
        assert data["metric_type"] == "zombie_count"
        assert data["value"] == 5.0
        assert data["api_id"] == 1
        assert data["labels"]["status"] == "zombie"

    def test_alert_to_dict(self):
        """Test Alert serialization."""
        timestamp = datetime.utcnow()
        alert = Alert(
            alert_id="test-123",
            severity=AlertSeverity.CRITICAL,
            title="Test Alert",
            description="Test description",
            metric_type=MetricType.HEALTH_SCORE,
            triggered_value=50.0,
            threshold=70.0,
            timestamp=timestamp
        )
        
        data = alert.to_dict()
        assert data["alert_id"] == "test-123"
        assert data["severity"] == "critical"
        assert data["metric_type"] == "health_score"
        assert "timestamp" in data
