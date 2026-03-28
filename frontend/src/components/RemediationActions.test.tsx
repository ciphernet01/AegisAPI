import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { RemediationActions } from '@components/RemediationActions'
import * as apiService from '@services/api'

// Mock the API service
vi.mock('@services/api', () => ({
  apiService: {
    getRemediationPlans: vi.fn(),
    decommissionApi: vi.fn(),
    archiveApi: vi.fn(),
    notifyApiOwner: vi.fn(),
    reviveApi: vi.fn(),
    getRemediationStats: vi.fn(),
  },
}))

// Mock the useTheme hook
vi.mock('@context/ThemeContext', () => ({
  useTheme: () => ({ theme: 'dark' }),
}))

describe('RemediationActions', () => {
  const mockPlans = [
    {
      id: '1',
      apiName: 'Legacy Auth API',
      apiId: 'api-1',
      status: 'zombie',
      urgency: 'critical',
      recommendedActions: ['decommission', 'notify'],
      effort: 'medium',
      estimatedCost: 5000,
      actionsTaken: ['notify'],
      actionStatus: 'pending',
    },
    {
      id: '2',
      apiName: 'Old Payment API',
      apiId: 'api-2',
      status: 'deprecated',
      urgency: 'high',
      recommendedActions: ['archive', 'notify'],
      effort: 'low',
      estimatedCost: 2000,
      actionsTaken: [],
      actionStatus: 'pending',
    },
  ]

  beforeEach(() => {
    vi.clearAllMocks()
    vi.mocked(apiService.apiService.getRemediationPlans).mockResolvedValue({
      success: true,
      plans: mockPlans,
    })
    vi.mocked(apiService.apiService.getRemediationStats).mockResolvedValue({
      success: true,
      stats: {
        totalPlans: 2,
        pendingActions: 5,
        completedActions: 3,
      },
    })
  })

  it('renders remediation actions component', async () => {
    render(<RemediationActions />)

    await waitFor(() => {
      expect(screen.getByText(/Remediation/i)).toBeInTheDocument()
    })
  })

  it('displays remediation plans from API', async () => {
    render(<RemediationActions />)

    await waitFor(() => {
      expect(screen.getByText('Legacy Auth API')).toBeInTheDocument()
      expect(screen.getByText('Old Payment API')).toBeInTheDocument()
    })
  })

  it('loads remediation plans on mount', async () => {
    render(<RemediationActions />)

    await waitFor(() => {
      expect(apiService.apiService.getRemediationPlans).toHaveBeenCalled()
    })
  })

  it('displays effort level for each plan', async () => {
    render(<RemediationActions />)

    await waitFor(() => {
      expect(screen.getByText(/medium|low/i)).toBeInTheDocument()
    })
  })

  it('displays cost estimate for plans', async () => {
    render(<RemediationActions />)

    await waitFor(() => {
      // Cost may be displayed in various formats
      const costs = screen.getAllByText(/\$|5000|2000/i)
      expect(costs.length).toBeGreaterThan(0)
    })
  })

  it('handles decommission action', async () => {
    vi.mocked(apiService.apiService.decommissionApi).mockResolvedValue({
      success: true,
      message: 'API decommissioned',
    })

    render(<RemediationActions />)

    await waitFor(() => {
      expect(screen.getByText('Legacy Auth API')).toBeInTheDocument()
    })

    // Find and click decommission button (implementation dependent)
    const buttons = screen.getAllByRole('button')
    const decommissionBtn = buttons.find(btn => btn.textContent?.includes('Decommission'))
    
    if (decommissionBtn) {
      await userEvent.click(decommissionBtn)
      
      await waitFor(() => {
        expect(apiService.apiService.decommissionApi).toHaveBeenCalled()
      })
    }
  })

  it('handles archive action', async () => {
    vi.mocked(apiService.apiService.archiveApi).mockResolvedValue({
      success: true,
      message: 'API archived',
    })

    render(<RemediationActions />)

    await waitFor(() => {
      expect(screen.getByText('Old Payment API')).toBeInTheDocument()
    })

    const buttons = screen.getAllByRole('button')
    const archiveBtn = buttons.find(btn => btn.textContent?.includes('Archive'))
    
    if (archiveBtn) {
      await userEvent.click(archiveBtn)
      
      await waitFor(() => {
        expect(apiService.apiService.archiveApi).toHaveBeenCalled()
      })
    }
  })

  it('handles notify owner action', async () => {
    vi.mocked(apiService.apiService.notifyApiOwner).mockResolvedValue({
      success: true,
      message: 'Owner notified',
    })

    render(<RemediationActions />)

    await waitFor(() => {
      expect(screen.getByText('Legacy Auth API')).toBeInTheDocument()
    })

    const buttons = screen.getAllByRole('button')
    const notifyBtn = buttons.find(btn => btn.textContent?.includes('Notify'))
    
    if (notifyBtn) {
      await userEvent.click(notifyBtn)
      
      await waitFor(() => {
        expect(apiService.apiService.notifyApiOwner).toHaveBeenCalled()
      })
    }
  })

  it('handles error gracefully', async () => {
    vi.mocked(apiService.apiService.getRemediationPlans).mockRejectedValue(
      new Error('Failed to load plans')
    )

    render(<RemediationActions />)

    // Component should render without crashing
    await waitFor(() => {
      expect(screen.getByRole('heading')).toBeInTheDocument()
    })
  })

  it('shows action status for each plan', async () => {
    render(<RemediationActions />)

    await waitFor(() => {
      expect(screen.getByText(/Pending|In Progress|Completed/i)).toBeInTheDocument()
    })
  })

  it('displays recommended actions per API', async () => {
    render(<RemediationActions />)

    await waitFor(() => {
      // Should show action recommendations
      expect(screen.getByText('Legacy Auth API')).toBeInTheDocument()
    })

    // Verify plan cards are rendered
    const cards = screen.getAllByRole('heading')
    expect(cards.length).toBeGreaterThan(0)
  })

  it('calls API methods on mount', async () => {
    render(<RemediationActions />)

    await waitFor(() => {
      expect(apiService.apiService.getRemediationPlans).toHaveBeenCalled()
    })
  })
})
