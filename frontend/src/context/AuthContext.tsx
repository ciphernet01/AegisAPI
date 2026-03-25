import React, { createContext, useContext, useEffect, useMemo, useState } from 'react';
import type { AuthUser, LoginPayload } from '@/types/auth';
import { apiService, setAuthToken } from '@services/api';

interface AuthContextValue {
  user: AuthUser | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (payload: LoginPayload) => Promise<void>;
  logout: () => void;
}

const AUTH_STORAGE_KEY = 'aegis_auth';

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

function loadStoredAuth(): { token: string; user: AuthUser } | null {
  const raw = localStorage.getItem(AUTH_STORAGE_KEY);
  if (!raw) return null;

  try {
    return JSON.parse(raw) as { token: string; user: AuthUser };
  } catch {
    localStorage.removeItem(AUTH_STORAGE_KEY);
    return null;
  }
}

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const stored = loadStoredAuth();
  const [user, setUser] = useState<AuthUser | null>(stored?.user ?? null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (stored?.token) {
      setAuthToken(stored.token);
    }
  }, [stored?.token]);

  const login = async (payload: LoginPayload) => {
    setIsLoading(true);
    try {
      const auth = await apiService.login(payload);
      setAuthToken(auth.token);
      localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(auth));
      setUser(auth.user);
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem(AUTH_STORAGE_KEY);
    setAuthToken(null);
    setUser(null);
  };

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      isAuthenticated: !!user,
      isLoading,
      login,
      logout
    }),
    [user, isLoading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return ctx;
}
