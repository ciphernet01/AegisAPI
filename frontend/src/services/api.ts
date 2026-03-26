import axios from 'axios';

// Use VITE_API_URL when provided (docker/prod), otherwise rely on dev proxy
const API_BASE = (import.meta.env.VITE_API_URL || '').replace(/\/$/, '');
const API_BASE_URL = `${API_BASE}/api/v1`;

export const apiService = {
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
  }
};
