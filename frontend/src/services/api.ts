import axios from 'axios';

// Use VITE_API_URL when provided (docker/prod), otherwise rely on dev proxy
const API_BASE = (import.meta.env.VITE_API_URL || '').replace(/\/$/, '');
const API_BASE_URL = `${API_BASE}/api/v1`;

export const apiService = {
  // ===== GENERAL APIs =====
  async getDashboardSummary() {
    const response = await axios.get(`${API_BASE_URL}/apis/stats`);
    return response.data;
  },
  
  async listApis(params = {}) {
    const response = await axios.get(`${API_BASE_URL}/apis`, { params });
    return response.data;
  },
  
  async getApiDetails(id: number) {
    const response = await axios.get(`${API_BASE_URL}/apis/${id}`);
    return response.data;
  },
  
  async searchApis(query: string) {
    const response = await axios.get(`${API_BASE_URL}/apis/search`, { params: { q: query } });
    return response.data;
  },

  // ===== ZOMBIE DETECTION =====
  async listZombieApis() {
    const response = await axios.get(`${API_BASE_URL}/zombies`);
    return response.data;
  },

  async analyzeAllApis() {
    const response = await axios.post(`${API_BASE_URL}/analyze`);
    return response.data;
  },

  async analyzeApiById(id: number) {
    const response = await axios.get(`${API_BASE_URL}/apis/${id}/analysis`);
    return response.data;
  },

  async getZombieStats() {
    const response = await axios.get(`${API_BASE_URL}/stats`);
    return response.data;
  },

  // ===== REMEDIATION =====
  async getRemediationPlans(apiId?: number) {
    const url = apiId 
      ? `${API_BASE_URL}/remediation/plans/${apiId}`
      : `${API_BASE_URL}/remediation/plans`;
    const response = await axios.get(url);
    return response.data;
  },

  async decommissionApi(apiId: number) {
    const response = await axios.post(`${API_BASE_URL}/remediation/decommission/${apiId}`);
    return response.data;
  },

  async archiveApi(apiId: number) {
    const response = await axios.post(`${API_BASE_URL}/remediation/archive/${apiId}`);
    return response.data;
  },

  async notifyApiOwner(apiId: number) {
    const response = await axios.post(`${API_BASE_URL}/remediation/notify-owner/${apiId}`);
    return response.data;
  },

  async reviveApi(apiId: number) {
    const response = await axios.post(`${API_BASE_URL}/remediation/revive/${apiId}`);
    return response.data;
  },

  async bulkRemediation(apiIds: number[], action: string) {
    const response = await axios.post(`${API_BASE_URL}/remediation/bulk`, {
      api_ids: apiIds,
      action
    });
    return response.data;
  },

  async getRemediationStats() {
    const response = await axios.get(`${API_BASE_URL}/remediation/stats`);
    return response.data;
  },

  // ===== ANALYTICS & MONITORING =====
  async getMetrics(metricType?: string, hours: number = 24) {
    const params: any = { hours };
    if (metricType) params.metric_type = metricType;
    const response = await axios.get(`${API_BASE_URL}/analytics/metrics`, { params });
    return response.data;
  },

  async getAlerts(severity?: string, unresolvedOnly: boolean = true) {
    const params: any = { unresolved_only: unresolvedOnly };
    if (severity) params.severity = severity;
    const response = await axios.get(`${API_BASE_URL}/analytics/alerts`, { params });
    return response.data;
  },

  async resolveAlert(alertId: string) {
    const response = await axios.post(`${API_BASE_URL}/analytics/alerts/${alertId}/resolve`);
    return response.data;
  },

  async getSystemHealth() {
    const response = await axios.get(`${API_BASE_URL}/analytics/health`);
    return response.data;
  },

  async getTrends(days: number = 7) {
    const response = await axios.get(`${API_BASE_URL}/analytics/trends`, { params: { days } });
    return response.data;
  },

  async getAnalyticsReport() {
    const response = await axios.get(`${API_BASE_URL}/analytics/report`);
    return response.data;
  },

  async setAlertThreshold(metricType: string, threshold: number) {
    const response = await axios.post(`${API_BASE_URL}/analytics/thresholds/${metricType}`, null, {
      params: { threshold }
    });
    return response.data;
  }
};
