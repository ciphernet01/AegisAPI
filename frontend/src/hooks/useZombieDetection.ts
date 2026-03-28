import { useState, useCallback, useEffect } from 'react';
import { apiService } from '../services/api';
import {
  ZombieDetectionResult,
  RemediationPlan,
  SystemHealth,
  Alert
} from '../types';

export interface ZombieDetectionState {
  zombies: ZombieDetectionResult[];
  plans: RemediationPlan[];
  health: SystemHealth | null;
  alerts: Alert[];
  loading: boolean;
  error: string | null;
  lastUpdated: Date | null;
}

export interface ZombieDetectionActions {
  loadZombies: () => Promise<void>;
  loadRemediationPlans: () => Promise<void>;
  loadHealth: () => Promise<void>;
  loadAlerts: () => Promise<void>;
  loadAll: () => Promise<void>;
  executeRemediationAction: (apiId: number, action: string) => Promise<void>;
  resolveAlert: (alertId: string) => Promise<void>;
  clearError: () => void;
  refreshAll: () => Promise<void>;
}

const initialState: ZombieDetectionState = {
  zombies: [],
  plans: [],
  health: null,
  alerts: [],
  loading: false,
  error: null,
  lastUpdated: null
};

export function useZombieDetection(): ZombieDetectionState & ZombieDetectionActions {
  const [state, setState] = useState<ZombieDetectionState>(initialState);

  const setError = useCallback((error: string | null) => {
    setState(prev => ({ ...prev, error }));
  }, []);

  const setLoading = useCallback((loading: boolean) => {
    setState(prev => ({ ...prev, loading }));
  }, []);

  const loadZombies = useCallback(async () => {
    try {
      setLoading(true);
      const response = await apiService.listZombieApis();
      setState(prev => ({
        ...prev,
        zombies: response.apis || [],
        lastUpdated: new Date()
      }));
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load zombies');
    } finally {
      setLoading(false);
    }
  }, [setError, setLoading]);

  const loadRemediationPlans = useCallback(async () => {
    try {
      setLoading(true);
      const response = await apiService.getRemediationPlans();
      setState(prev => ({
        ...prev,
        plans: response.plans || [],
        lastUpdated: new Date()
      }));
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load remediation plans');
    } finally {
      setLoading(false);
    }
  }, [setError, setLoading]);

  const loadHealth = useCallback(async () => {
    try {
      setLoading(true);
      const response = await apiService.getSystemHealth();
      setState(prev => ({
        ...prev,
        health: response.health,
        lastUpdated: new Date()
      }));
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load health data');
    } finally {
      setLoading(false);
    }
  }, [setError, setLoading]);

  const loadAlerts = useCallback(async () => {
    try {
      setLoading(true);
      const response = await apiService.getAlerts();
      setState(prev => ({
        ...prev,
        alerts: response.alerts || [],
        lastUpdated: new Date()
      }));
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load alerts');
    } finally {
      setLoading(false);
    }
  }, [setError, setLoading]);

  const loadAll = useCallback(async () => {
    try {
      setLoading(true);
      const [zombiesRes, plansRes, healthRes, alertsRes] = await Promise.all([
        apiService.listZombieApis(),
        apiService.getRemediationPlans(),
        apiService.getSystemHealth(),
        apiService.getAlerts()
      ]);

      setState({
        zombies: zombiesRes.apis || [],
        plans: plansRes.plans || [],
        health: healthRes.health,
        alerts: alertsRes.alerts || [],
        loading: false,
        error: null,
        lastUpdated: new Date()
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load data');
    } finally {
      setLoading(false);
    }
  }, [setError, setLoading]);

  const executeRemediationAction = useCallback(
    async (apiId: number, action: string) => {
      try {
        setLoading(true);
        switch (action.toLowerCase()) {
          case 'decommission':
            await apiService.decommissionApi(apiId);
            break;
          case 'archive':
            await apiService.archiveApi(apiId);
            break;
          case 'notify':
            await apiService.notifyApiOwner(apiId);
            break;
          case 'revive':
            await apiService.reviveApi(apiId);
            break;
          default:
            throw new Error(`Unknown action: ${action}`);
        }

        // Reload plans after action
        await loadRemediationPlans();
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : `Failed to execute ${action} action`);
      } finally {
        setLoading(false);
      }
    },
    [loadRemediationPlans, setError, setLoading]
  );

  const resolveAlert = useCallback(
    async (alertId: string) => {
      try {
        setLoading(true);
        await apiService.resolveAlert(alertId);

        setState(prev => ({
          ...prev,
          alerts: prev.alerts.filter(a => a.alert_id !== alertId),
          lastUpdated: new Date()
        }));

        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to resolve alert');
      } finally {
        setLoading(false);
      }
    },
    [setError, setLoading]
  );

  const clearError = useCallback(() => {
    setError(null);
  }, [setError]);

  const refreshAll = useCallback(async () => {
    await loadAll();
  }, [loadAll]);

  return {
    ...state,
    loadZombies,
    loadRemediationPlans,
    loadHealth,
    loadAlerts,
    loadAll,
    executeRemediationAction,
    resolveAlert,
    clearError,
    refreshAll
  };
}
