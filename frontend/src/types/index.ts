// API Response Types

export interface APIStatus {
  status: 'ACTIVE' | 'DEPRECATED' | 'ORPHANED' | 'ZOMBIE';
  confidence: number;
  risk_score: number;
  reasoning: string[];
}

export interface API {
  id: number;
  name: string;
  endpoint: string;
  method: string;
  owner?: string;
  tech_stack?: string;
  status: string;
  risk_score: number;
  created_at: string;
  last_traffic?: string;
  is_documented?: boolean;
}

export interface ZombieDetectionResult {
  id: number;
  name: string;
  endpoint: string;
  status: string;
  confidence: number;
  risk_score: number;
  reasoning: string[];
  zombie_factors?: {
    traffic_activity: number;
    documentation_status: number;
    ownership: number;
    age_deprecation: number;
    maintenance_signals: number;
  };
}

export interface RemediationPlan {
  api_id: number;
  api_name: string;
  current_status: string;
  recommended_actions: RemediationAction[];
  urgency_level: 'low' | 'medium' | 'high' | 'critical';
  estimated_effort: string;
  cost_estimate: string;
}

export interface RemediationAction {
  action_type: 'DECOMMISSION' | 'ARCHIVE' | 'NOTIFY_OWNER' | 'MIGRATE_CONSUMERS' | 'REVIVE';
  description: string;
  priority: number;
  status: 'PENDING' | 'IN_PROGRESS' | 'COMPLETED' | 'FAILED' | 'CANCELLED';
}

export interface SystemHealth {
  timestamp: string;
  overall_status: 'healthy' | 'warning' | 'critical';
  health_score: number;
  total_apis: number;
  risk_distribution: {
    healthy: number;
    at_risk: number;
    critical: number;
  };
  active_alerts: number;
  unresolved_critical_alerts: number;
  recommendations: string[];
}

export interface Metric {
  metric_type: string;
  value: number;
  timestamp: string;
  api_id?: number;
  labels?: Record<string, string>;
}

export interface Alert {
  alert_id: string;
  severity: 'info' | 'warning' | 'critical';
  title: string;
  description: string;
  metric_type: string;
  triggered_value: number;
  threshold: number;
  timestamp: string;
  resolved: boolean;
}

export interface TrendAnalysis {
  period_days: number;
  analysis_timestamp: string;
  zombie_trend?: {
    current: number;
    average: number;
    min: number;
    max: number;
    direction: 'increasing' | 'decreasing';
  };
  health_trend?: {
    current: number;
    average: number;
    min: number;
    max: number;
    direction: 'improving' | 'declining';
  };
}

export interface AnalyticsReport {
  generated_at: string;
  summary: {
    overall_status: string;
    health_score: number;
    total_apis: number;
    risk_distribution: Record<string, number>;
    active_alerts: number;
  };
  metrics: {
    count: number;
    last_24h: Metric[];
  };
  alerts: {
    total: number;
    unresolved: number;
    by_severity: Record<string, number>;
    recent: Alert[];
  };
  trends: TrendAnalysis;
  recommendations: string[];
}

export interface ZombieStats {
  success: boolean;
  timestamp: string;
  total_apis: number;
  zombie_count: number;
  deprecated_count: number;
  orphaned_count: number;
  active_count: number;
  health_score: number;
}
