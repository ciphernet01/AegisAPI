/**
 * API Types
 * Core type definitions for API inventory and assessment data
 */

export type ApiStatus = 'active' | 'deprecated' | 'orphaned' | 'zombie';
export type RiskLevel = 'critical' | 'high' | 'medium' | 'low';
export type AuthType = 'oauth2' | 'apikey' | 'mtls' | 'none';

export interface ApiEndpoint {
  id: string;
  url: string;
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH' | 'HEAD' | 'OPTIONS';
  name: string;
  description?: string;
  owner?: string;
  ownerEmail?: string;
  status: ApiStatus;
  lastSeen: Date;
  createdAt: Date;
  version?: string;
}

export interface SecurityAssessment {
  apiId: string;
  authentication: AuthType;
  hasRateLimit: boolean;
  hasEncryption: boolean;
  dataExposure: 'high' | 'medium' | 'low';
  complianceGaps: string[];
  vulnerabilities: SecurityVulnerability[];
  riskLevel: RiskLevel;
  riskScore: number; // 0-100
  lastAssessed: Date;
}

export interface SecurityVulnerability {
  cweId: string;
  title: string;
  severity: RiskLevel;
  description: string;
  remediation: string;
}

export interface ApiMetrics {
  apiId: string;
  requestsPerDay: number;
  errorRate: number;
  avgResponseTime: number;
  uniqueCallers: number;
  lastUsed: Date;
  usage7Days: number[];
  usage30Days: number[];
}

export interface RemediationRecommendation {
  id: string;
  apiId: string;
  type: 'authentication' | 'encryption' | 'rateLimit' | 'dataExposure' | 'deprecation' | 'decommission';
  title: string;
  description: string;
  priority: RiskLevel;
  estimatedEffort: 'low' | 'medium' | 'high';
  action: string;
  status: 'pending' | 'in-progress' | 'completed' | 'rejected';
  assignedTo?: string;
  dueDate?: Date;
}

export interface DecommissioningWorkflow {
  id: string;
  apiId: string;
  status: 'draft' | 'approved' | 'in-progress' | 'completed' | 'rejected';
  initiatedBy: string;
  initiatedAt: Date;
  approvedBy?: string;
  approvedAt?: Date;
  deprecationNoticeDate?: Date;
  sunsetDate?: Date;
  impactAnalysis?: string;
  affectedSystems: string[];
  automationScript?: string;
}

export interface ApiInventory {
  totalApis: number;
  activeApis: number;
  deprecatedApis: number;
  orphanedApis: number;
  zombieApis: number;
  criticalRiskApis: number;
  highRiskApis: number;
}

export interface DashboardMetrics {
  inventory: ApiInventory;
  discoveredThisMonth: number;
  remediatedThisMonth: number;
  averageRiskScore: number;
  complianceScore: number;
}
