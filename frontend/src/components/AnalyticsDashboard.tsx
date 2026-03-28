import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import { SystemHealth, Alert, TrendAnalysis } from '../types';

export function AnalyticsDashboard() {
  const [health, setHealth] = useState<SystemHealth | null>(null);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [trends, setTrends] = useState<TrendAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedSeverity, setSelectedSeverity] = useState<string | null>(null);

  useEffect(() => {
    loadAnalyticsData();
  }, []);

  const loadAnalyticsData = async () => {
    try {
      setLoading(true);
      const [healthData, alertsData, trendsData] = await Promise.all([
        apiService.getSystemHealth(),
        apiService.getAlerts(),
        apiService.getTrends()
      ]);
      
      setHealth(healthData.health);
      setAlerts(alertsData.alerts || []);
      setTrends(trendsData.trends);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load analytics data');
    } finally {
      setLoading(false);
    }
  };

  const resolveAlert = async (alertId: string) => {
    try {
      await apiService.resolveAlert(alertId);
      setAlerts(alerts.filter(a => a.alert_id !== alertId));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to resolve alert');
    }
  };

  if (loading) {
    return <div className="p-6 text-center text-gray-500">Loading analytics data...</div>;
  }

  const filteredAlerts = selectedSeverity
    ? alerts.filter(a => a.severity === selectedSeverity)
    : alerts;

  return (
    <div className="space-y-6">
      {/* Health Overview */}
      {health && (
        <HealthOverview health={health} />
      )}

      {/* Trends Section */}
      {trends && (
        <TrendSection trends={trends} />
      )}

      {/* Alerts Section */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-semibold text-gray-800">System Alerts</h2>
              <p className="text-sm text-gray-500 mt-1">
                {alerts.length} active alert(s)
              </p>
            </div>
            <div className="flex gap-2">
              {['critical', 'warning', 'info'].map((severity) => (
                <button
                  key={severity}
                  onClick={() => setSelectedSeverity(selectedSeverity === severity ? null : severity)}
                  className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                    selectedSeverity === severity
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {severity.charAt(0).toUpperCase() + severity.slice(1)}
                </button>
              ))}
            </div>
          </div>
        </div>

        {error && (
          <div className="p-4 bg-red-50 border-l-4 border-red-500 text-red-700">
            {error}
          </div>
        )}

        {filteredAlerts.length === 0 ? (
          <div className="p-8 text-center text-gray-500">
            {selectedSeverity ? 'No alerts with this severity' : 'No active alerts'}
          </div>
        ) : (
          <div className="divide-y divide-gray-200">
            {filteredAlerts.map((alert) => (
              <AlertCard
                key={alert.alert_id}
                alert={alert}
                onResolve={resolveAlert}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function HealthOverview({ health }: { health: SystemHealth }) {
  const statusColor = {
    healthy: 'text-green-600 bg-green-50',
    warning: 'text-yellow-600 bg-yellow-50',
    critical: 'text-red-600 bg-red-50'
  }[health.overall_status];

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-start justify-between mb-6">
        <div>
          <h2 className="text-xl font-semibold text-gray-800">System Health</h2>
          <p className="text-sm text-gray-500 mt-1">Last updated: {new Date(health.timestamp).toLocaleString()}</p>
        </div>
        <div className={`px-4 py-2 rounded-lg font-semibold ${statusColor}`}>
          {health.overall_status.toUpperCase()}
        </div>
      </div>

      {/* Health Score Bar */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-gray-700">Health Score</span>
          <span className="text-2xl font-bold text-gray-900">{health.health_score.toFixed(1)}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3">
          <div
            className={`h-3 rounded-full transition-all ${
              health.health_score >= 80 ? 'bg-green-500' :
              health.health_score >= 60 ? 'bg-yellow-500' :
              'bg-red-500'
            }`}
            style={{ width: `${health.health_score}%` }}
          />
        </div>
      </div>

      {/* Risk Distribution */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <RiskCard
          label="Healthy APIs"
          value={health.risk_distribution.healthy}
          color="green"
        />
        <RiskCard
          label="At Risk APIs"
          value={health.risk_distribution.at_risk}
          color="yellow"
        />
        <RiskCard
          label="Critical APIs"
          value={health.risk_distribution.critical}
          color="red"
        />
      </div>

      {/* Alerts Summary */}
      <div className="border-t pt-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-gray-600">Active Alerts</p>
            <p className="text-2xl font-bold text-gray-900">{health.active_alerts}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Critical Alerts</p>
            <p className="text-2xl font-bold text-red-600">{health.unresolved_critical_alerts}</p>
          </div>
        </div>
      </div>

      {/* Recommendations */}
      {health.recommendations.length > 0 && (
        <div className="border-t mt-4 pt-4">
          <h3 className="text-sm font-semibold text-gray-900 mb-2">Recommendations</h3>
          <ul className="space-y-2">
            {health.recommendations.map((rec, idx) => (
              <li key={idx} className="text-sm text-gray-700 flex items-start">
                <span className="text-blue-500 mr-2">→</span>
                {rec}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

function TrendSection({ trends }: { trends: TrendAnalysis }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {/* Zombie Trend */}
      {trends.zombie_trend && (
        <TrendCard
          title="Zombie APIs Trend"
          trend={trends.zombie_trend}
          metricLabel="Zombie Count"
          color="red"
        />
      )}

      {/* Health Trend */}
      {trends.health_trend && (
        <TrendCard
          title="Health Score Trend"
          trend={trends.health_trend}
          metricLabel="Health %"
          color="green"
        />
      )}
    </div>
  );
}

function TrendCard({
  title,
  trend,
  metricLabel,
  color
}: {
  title: string;
  trend: any;
  metricLabel: string;
  color: 'red' | 'green' | 'yellow';
}) {
  const directionIcon = trend.direction === 'increasing' || trend.direction === 'improving'
    ? '↑'
    : '↓';

  const directionColor = trend.direction === 'increasing' || trend.direction === 'improving'
    ? 'text-red-600'
    : 'text-green-600';

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>

      <div className="space-y-3">
        <div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-bold text-gray-900">{trend.current.toFixed(1)}</span>
            <span className={`text-lg font-semibold ${directionColor}`}>{directionIcon}</span>
          </div>
          <p className="text-sm text-gray-500">{metricLabel}</p>
        </div>

        <div className="grid grid-cols-2 gap-2 text-sm">
          <div>
            <p className="text-gray-600">Average (7d)</p>
            <p className="font-medium text-gray-900">{trend.average.toFixed(1)}</p>
          </div>
          <div>
            <p className="text-gray-600">Min/Max</p>
            <p className="font-medium text-gray-900">{trend.min.toFixed(1)} / {trend.max.toFixed(1)}</p>
          </div>
        </div>

        <div className="pt-3 border-t">
          <p className="text-xs font-medium text-gray-600">Trend Direction</p>
          <p className={`text-sm font-semibold capitalize ${directionColor}`}>
            {trend.direction}
          </p>
        </div>
      </div>
    </div>
  );
}

function RiskCard({
  label,
  value,
  color
}: {
  label: string;
  value: number;
  color: 'green' | 'yellow' | 'red';
}) {
  const bgColor = {
    green: 'bg-green-50',
    yellow: 'bg-yellow-50',
    red: 'bg-red-50'
  }[color];

  const textColor = {
    green: 'text-green-700',
    yellow: 'text-yellow-700',
    red: 'text-red-700'
  }[color];

  return (
    <div className={`${bgColor} rounded-lg p-4`}>
      <p className="text-sm text-gray-600">{label}</p>
      <p className={`text-2xl font-bold mt-2 ${textColor}`}>{value}</p>
    </div>
  );
}

function AlertCard({
  alert,
  onResolve
}: {
  alert: Alert;
  onResolve: (id: string) => Promise<void>;
}) {
  const [resolving, setResolving] = useState(false);

  const severityColor = {
    critical: 'bg-red-50 border-red-200 text-red-800',
    warning: 'bg-yellow-50 border-yellow-200 text-yellow-800',
    info: 'bg-blue-50 border-blue-200 text-blue-800'
  }[alert.severity] || 'bg-gray-50';

  const handleResolve = async () => {
    setResolving(true);
    try {
      await onResolve(alert.alert_id);
    } finally {
      setResolving(false);
    }
  };

  return (
    <div className={`p-4 border-l-4 ${severityColor}`}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <h4 className="font-semibold">{alert.title}</h4>
          <p className="text-sm mt-1">{alert.description}</p>
          <p className="text-xs mt-2 opacity-70">
            Triggered: {new Date(alert.timestamp).toLocaleString()}
          </p>
        </div>
        <button
          onClick={handleResolve}
          disabled={resolving || alert.resolved}
          className="ml-4 px-3 py-1 text-sm bg-white rounded hover:bg-gray-100 disabled:opacity-50 font-medium"
        >
          {resolving ? 'Resolving...' : 'Resolve'}
        </button>
      </div>
    </div>
  );
}
