export interface AuthUser {
  id: string;
  name: string;
  email: string;
  role: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface AuthResponse {
  token: string;
  user: AuthUser;
}

export interface DatabaseHistoryEntry {
  id: string;
  action: string;
  table: string;
  status: 'success' | 'failed';
  rowsAffected: number;
  requestedBy: string;
  timestamp: string;
  sourceIp: string;
}
