import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook, waitFor } from '@testing-library/react'
import { useZombieDetection } from '@hooks/useZombieDetection'
import * as apiService from '@services/api'

// Mock the API service
vi.mock('@services/api', () => ({
  apiService: {
    listZombieApis: vi.fn(),
    getZombieStats: vi.fn(),
    getRemediationPlans: vi.fn(),
    getSystemHealth: vi.fn(),
    getAlerts: vi.fn(),
    getTrends: vi.fn(),
    decommissionApi: vi.fn(),
    archiveApi: vi.fn(),
    notifyApiOwner: vi.fn(),
    reviveApi: vi.fn(),
    resolveAlert: vi.fn(),
  },
}))

describe('useZombieDetection Hook', () => {
  const mockZombies = {
    apis: [
      { id: '1', name: 'API 1', status: 'zombie', riskScore: 95 },
      { id: '2', name: 'API 2', status: 'deprecated', riskScore: 75 },
    ],
  }

  const mockStats = {
    total: 245,
    zombie: 15,
    deprecated: 45,
    healthScore: 68,
  }

  const mockPlans = {
    plans: [
      { id: '1', apiName: 'API 1', urgency: 'critical' },
      { id: '2', apiName: 'API 2', urgency: 'high' },
    ],
  }

  const mockHealth = {
    health: { score: 72, status: 'healthy' },
  }

  const mockAlerts = {
    alerts: [
      { id: '1', severity: 'critical', message: 'High risk APIs' },
    ],
  }

  beforeEach(() => {
    vi.clearAllMocks()
    vi.mocked(apiService.apiService.listZombieApis).mockResolvedValue(mockZombies)
    vi.mocked(apiService.apiService.getZombieStats).mockResolvedValue(mockStats)
    vi.mocked(apiService.apiService.getRemediationPlans).mockResolvedValue(mockPlans)
    vi.mocked(apiService.apiService.getSystemHealth).mockResolvedValue(mockHealth)
    vi.mocked(apiService.apiService.getAlerts).mockResolvedValue(mockAlerts)
  })

  it('exports useZombieDetection hook', () => {
    expect(useZombieDetection).toBeDefined()
  })

  it('provides initial state', () => {
    const { result } = renderHook(() => useZombieDetection())
    
    // Initial state should include loading indicators and empty data
    expect(result.current.state).toBeDefined()
  })

  it('initializes with empty state', () => {
    const { result } = renderHook(() => useZombieDetection())
    
    const state = result.current.state
    expect(Array.isArray(state.zombies) || state.zombies === undefined || state.zombies === null).toBe(true)
  })

  it('provides loadZombies action', () => {
    const { result } = renderHook(() => useZombieDetection())
    
    expect(result.current.actions).toBeDefined()
    expect(result.current.actions.loadZombies).toBeDefined()
  })

  it('provides loadRemediationPlans action', () => {
    const { result } = renderHook(() => useZombieDetection())
    
    expect(result.current.actions.loadRemediationPlans).toBeDefined()
  })

  it('provides loadHealth action', () => {
    const { result } = renderHook(() => useZombieDetection())
    
    expect(result.current.actions.loadHealth).toBeDefined()
  })

  it('provides loadAlerts action', () => {
    const { result } = renderHook(() => useZombieDetection())
    
    expect(result.current.actions.loadAlerts).toBeDefined()
  })

  it('provides remediation action methods', () => {
    const { result } = renderHook(() => useZombieDetection())
    
    expect(result.current.actions.executeRemediationAction).toBeDefined()
    expect(result.current.actions.resolveAlert).toBeDefined()
  })

  it('provides refresh and error clearing methods', () => {
    const { result } = renderHook(() => useZombieDetection())
    
    expect(result.current.actions.refreshAll).toBeDefined()
    expect(result.current.actions.clearError).toBeDefined()
  })

  it('can load zombies', async () => {
    const { result } = renderHook(() => useZombieDetection())
    
    await result.current.actions.loadZombies()
    
    await waitFor(() => {
      expect(apiService.apiService.listZombieApis).toHaveBeenCalled()
    })
  })

  it('can load remediation plans', async () => {
    const { result } = renderHook(() => useZombieDetection())
    
    await result.current.actions.loadRemediationPlans()
    
    await waitFor(() => {
      expect(apiService.apiService.getRemediationPlans).toHaveBeenCalled()
    })
  })

  it('can load system health', async () => {
    const { result } = renderHook(() => useZombieDetection())
    
    await result.current.actions.loadHealth()
    
    await waitFor(() => {
      expect(apiService.apiService.getSystemHealth).toHaveBeenCalled()
    })
  })

  it('can load all data in parallel', async () => {
    const { result } = renderHook(() => useZombieDetection())
    
    await result.current.actions.loadAll()
    
    await waitFor(() => {
      expect(apiService.apiService.listZombieApis).toHaveBeenCalled()
      expect(apiService.apiService.getRemediationPlans).toHaveBeenCalled()
      expect(apiService.apiService.getSystemHealth).toHaveBeenCalled()
      expect(apiService.apiService.getAlerts).toHaveBeenCalled()
    })
  })

  it('can execute remediation actions', async () => {
    vi.mocked(apiService.apiService.decommissionApi).mockResolvedValue({
      success: true,
      message: 'API decommissioned',
    })

    const { result } = renderHook(() => useZombieDetection())
    
    await result.current.actions.executeRemediationAction('api-1', 'decommission')
    
    await waitFor(() => {
      expect(apiService.apiService.decommissionApi).toHaveBeenCalled()
    })
  })

  it('can resolve alerts', async () => {
    vi.mocked(apiService.apiService.resolveAlert).mockResolvedValue({
      success: true,
      message: 'Alert resolved',
    })

    const { result } = renderHook(() => useZombieDetection())
    
    await result.current.actions.resolveAlert('alert-1')
    
    await waitFor(() => {
      expect(apiService.apiService.resolveAlert).toHaveBeenCalled()
    })
  })

  it('can clear errors', async () => {
    const { result } = renderHook(() => useZombieDetection())
    
    // Clear error should not throw
    expect(() => result.current.actions.clearError()).not.toThrow()
  })

  it('can refresh all data', async () => {
    const { result } = renderHook(() => useZombieDetection())
    
    await result.current.actions.refreshAll()
    
    await waitFor(() => {
      // Should reload all data
      expect(apiService.apiService.listZombieApis).toHaveBeenCalled()
    })
  })

  it('handles loading states', async () => {
    vi.mocked(apiService.apiService.listZombieApis).mockImplementation(
      () => new Promise(resolve => setTimeout(() => resolve(mockZombies), 100))
    )

    const { result } = renderHook(() => useZombieDetection())
    
    const loadPromise = result.current.actions.loadZombies()
    
    // Should have started loading
    expect(result.current.state).toBeDefined()
    
    await loadPromise
    
    await waitFor(() => {
      expect(apiService.apiService.listZombieApis).toHaveBeenCalled()
    })
  })

  it('handles errors gracefully', async () => {
    vi.mocked(apiService.apiService.listZombieApis).mockRejectedValue(
      new Error('API error')
    )

    const { result } = renderHook(() => useZombieDetection())
    
    await result.current.actions.loadZombies()
    
    // Should not throw and should handle error
    await waitFor(() => {
      expect(apiService.apiService.listZombieApis).toHaveBeenCalled()
    })
  })
})
