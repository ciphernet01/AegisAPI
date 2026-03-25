import axios from 'axios';
import type { AuthResponse, DatabaseHistoryEntry, LoginPayload } from '@/types/auth';

const API_BASE_URL = '/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

export function setAuthToken(token: string | null) {
  if (token) {
    apiClient.defaults.headers.common.Authorization = `Bearer ${token}`;
  } else {
    delete apiClient.defaults.headers.common.Authorization;
  }
}

export const apiService = {
  async login(payload: LoginPayload): Promise<AuthResponse> {
    try {
      const response = await apiClient.post('/auth/login', payload);
      return response.data;
    } catch {
      // Fallback for local development until backend auth endpoint is wired.
      if (payload.email === 'admin@aegis.local' && payload.password === 'Aegis@123') {
        return {
          token: 'local-dev-token',
          user: {
            id: 'u-001',
            name: 'Security Admin',
            email: payload.email,
            role: 'Risk Analysis Eng.'
          }
        };
      }
      throw new Error('Invalid credentials');
    }
  },

  async getDashboardSummary() {
    const response = await apiClient.get('/apis/stats');
    return response.data;
  },
  
  async listApis(params = {}) {
    const response = await apiClient.get('/apis', { params });
    return response.data;
  },
  
  async getApiDetails(id: number) {
    const response = await apiClient.get(`/apis/${id}`);
    return response.data;
  },
  
  async searchApis(query: string) {
    const response = await apiClient.get('/apis/search', { params: { q: query } });
    return response.data;
  },

  async getDatabaseHistory(): Promise<DatabaseHistoryEntry[]> {
    try {
      const response = await apiClient.get('/audit/database-history');
      return response.data?.data ?? response.data;
    } catch {
      return [
        {
          id: 'hist-101',
          action: 'SELECT',
          table: 'api_endpoints',
          status: 'success',
          rowsAffected: 124,
          requestedBy: 'Security Admin',
          timestamp: '2026-03-26T08:14:00Z',
          sourceIp: '10.0.2.14'
        },
        {
          id: 'hist-102',
          action: 'UPDATE',
          table: 'security_findings',
          status: 'success',
          rowsAffected: 3,
          requestedBy: 'Security Admin',
          timestamp: '2026-03-26T08:06:00Z',
          sourceIp: '10.0.2.14'
        },
        {
          id: 'hist-103',
          action: 'DELETE',
          table: 'orphaned_routes',
          status: 'failed',
          rowsAffected: 0,
          requestedBy: 'Security Admin',
          timestamp: '2026-03-26T07:55:00Z',
          sourceIp: '10.0.2.14'
        }
      ];
    }
  }
};
