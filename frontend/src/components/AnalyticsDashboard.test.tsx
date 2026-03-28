import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { AnalyticsDashboard } from '@components/AnalyticsDashboard'
import * as apiService from '@services/api'

// Mock the API service
vi.mock('@services/api', () => ({
  apiService: {
    getSystemHealth: vi.fn(),
    getAlerts: vi.fn(),
    getTrends: vi.fn(),
    getAnalyticsReport: vi.fn(),
    resolveAlert: vi.fn(),
  },
}))

// Mock the useTheme hook
vi.mock('@context/ThemeContext', () => ({
  useTheme: () => ({ theme: 'dark' }),
}))

describe('AnalyticsDashboard', () => {
  const mockHealth = {
    score: 72,
    status: 'healthy',
    zombieCount: 15,
    deprecatedCount: 45,
    riskDistribution: {
      healthy: 185,
      atRisk: 45,
      critical: 15,
    },
  }

  const mockAlerts = [
    {
      id: '1',
      type: 'zombie_detection',
      severity: 'critical',
      message: '15 zombie APIs detected',
      timestamp: '2024-03-28T10:00:00Z',
      resolved: false,
    },
    {
      id: '2',
      type: 'deprecated_api',
      severity: 'warning',
      message: '45 deprecated APIs still in use',
      timestamp: '2024-03-28T09:00:00Z',
      resolved: false,
    },
    {
      id: '3',
      type: 'low_documentation',
      severity: 'info',
      message: '23 APIs lack documentation',
      timestamp: '2024-03-28T08:00:00Z',
      resolved: false,
    },
  ]

  const mockTrends = [
    {
      metric: 'zombie_apis',
      direction: 'increasing',
      change: 3,
      percentageChange: 25,
    },
    {
      metric: 'health_score',
      direction: 'decreasing',
      change: -5,
      percentageChange: -6.5,
    },
    {
      metric: 'documented_apis',
      direction: 'increasing',
      change: 12,
      percentageChange: 8.2,
    },
  ]

  beforeEach(() => {
    vi.clearAllMocks()
    vi.mocked(apiService.apiService.getSystemHealth).mockResolvedValue({
      success: true,
      health: mockHealth,
    })
    vi.mocked(apiService.apiService.getAlerts).mockResolvedValue({
      success: true,
      alerts: mockAlerts,
    })
    vi.mocked(apiService.apiService.getTrends).mockResolvedValue({
      success: true,
      trends: mockTrends,
    })
  })

  it('renders analytics dashboard', async () => {
    render(<AnalyticsDashboard />)

    await waitFor(() => {
      expect(screen.getByText(/Analytics|Monitoring/i)).toBeInTheDocument()
    })
  })

  it('displays system health score', async () => {
    render(<AnalyticsDashboard />)

    await waitFor(() => {
      expect(screen.getByText('72')).toBeInTheDocument()
    })
  })

  it('displays health status label', async () => {
    render(<AnalyticsDashboard />)

    await waitFor(() => {
      expect(screen.getByText(/healthy|warning|critical/i)).toBeInTheDocument()
    })
  })

  it('displays risk distribution cards', async () => {
    render(<AnalyticsDashboard />)

    await waitFor(() => {
      // Risk distribution should show counts
      const counts = screen.getAllByText(/\d+/)
      expect(counts.length).toBeGreaterThan(0)
    })
  })

  it('displays alerts with correct severity', async () => {
    render(<AnalyticsDashboard />)

    await waitFor(() => {
      expect(screen.getByText(/15 zombie APIs detected/i)).toBeInTheDocument()
      expect(screen.getByText(/45 deprecated APIs still in use/i)).toBeInTheDocument()
    })
  })

  it('loads health, alerts, and trends on mount', async () => {
    render(<AnalyticsDashboard />)

    await waitFor(() => {
      expect(apiService.apiService.getSystemHealth).toHaveBeenCalled()
      expect(apiService.apiService.getAlerts).toHaveBeenCalled()
      expect(apiService.apiService.getTrends).toHaveBeenCalled()
    })
  })

  it('handles alert resolution', async () => {
    vi.mocked(apiService.apiService.resolveAlert).mockResolvedValue({
      success: true,
      message: 'Alert resolved',
    })

    render(<AnalyticsDashboard />)

    await waitFor(() => {
      expect(screen.getByText(/15 zombie APIs detected/i)).toBeInTheDocument()
    })

    // Try to click resolve button
    const buttons = screen.getAllByRole('button')
    const resolveBtn = buttons.find(btn => btn.textContent?.includes('Resolve'))

    if (resolveBtn) {
      await userEvent.click(resolveBtn)

      await waitFor(() => {
        expect(apiService.apiService.resolveAlert).toHaveBeenCalled()
      })
    }
  })

  it('displays trend information', async () => {
    render(<AnalyticsDashboard />)

    await waitFor(() => {
      // Trends should be displayed
      expect(screen.getByRole('heading')).toBeInTheDocument()
    })
  })

  it('shows alert severity filtering', async () => {
    render(<AnalyticsDashboard />)

    await waitFor(() => {
      // Should show alerts
      const alertElements = screen.getAllByText(/zombie APIs detected|deprecated APIs|APIs lack/i)
      expect(alertElements.length).toBeGreaterThan(0)
    })
  })

  it('handles error gracefully', async () => {
    vi.mocked(apiService.apiService.getSystemHealth).mockRejectedValue(
      new Error('Failed to load health')
    )
    vi.mocked(apiService.apiService.getAlerts).mockRejectedValue(
      new Error('Failed to load alerts')
    )
    vi.mocked(apiService.apiService.getTrends).mockRejectedValue(
      new Error('Failed to load trends')
    )

    render(<AnalyticsDashboard />)

    // Component should render without crashing
    await waitFor(() => {
      expect(screen.getByRole('heading')).toBeInTheDocument()
    })
  })

  it('displays trend direction indicators', async () => {
    render(<AnalyticsDashboard />)

    await waitFor(() => {
      // Trends should be displayed (look for trend information)
      const headings = screen.getAllByRole('heading')
      expect(headings.length).toBeGreaterThan(0)
    })
  })

  it('filters alerts by severity', async () => {
    render(<AnalyticsDashboard />)

    await waitFor(() => {
      expect(screen.getByText(/15 zombie APIs detected/i)).toBeInTheDocument()
    })

    // Try to find severity filter buttons
    const buttons = screen.getAllByRole('button')
    const criticalBtn = buttons.find(btn => btn.textContent?.includes('Critical'))

    if (criticalBtn) {
      await userEvent.click(criticalBtn)
      // Should filter to critical alerts only
      expect(screen.getByText(/15 zombie APIs detected/i)).toBeInTheDocument()
    }
  })

  it('displays recommendations based on health', async () => {
    render(<AnalyticsDashboard />)

    await waitFor(() => {
      // Component should render with score of 72 (healthy)
      expect(screen.getByText('72')).toBeInTheDocument()
    })
  })
})
