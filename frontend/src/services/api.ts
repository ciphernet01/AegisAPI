import axios from 'axios';

const API_BASE_URL = '/api/v1';

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
