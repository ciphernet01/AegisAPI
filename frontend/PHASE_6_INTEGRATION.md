# Phase 6: Frontend Integration Guide

## Overview

Phase 6 provides complete frontend integration for the Zombie API Detection system with three main components:

1. **Zombie Detection Dashboard** - Visualize detected zombie APIs
2. **Remediation Actions** - Manage remediation workflows
3. **Analytics Dashboard** - Monitor system health and trends

## Components

### 1. ZombieDetectionDashboard

Displays all detected zombie APIs with detailed classification information.

```tsx
import { ZombieDetectionDashboard } from '@/components/ZombieDetectionDashboard';

function MyPage() {
  return <ZombieDetectionDashboard />;
}
```

**Features:**
- Status cards: Total APIs, Zombie count, Deprecated, Health Score
- Zombie API list with sortable columns
- Risk score visualization
- Confidence metrics
- Detail modal for individual APIs with risk factors
- Reason explanations for classifications

### 2. RemediationActions

Manage remediation workflows for detected zombie APIs.

```tsx
import { RemediationActions } from '@/components/RemediationActions';

function MyPage() {
  return <RemediationActions />;
}
```

**Features:**
- List remediation plans by urgency
- Execute actions: Decommission, Archive, Notify Owner, Revive
- Recommended actions per API
- Effort and cost estimates
- Action status tracking (Pending, In Progress, Completed, Failed)
- Bulk action capabilities

### 3. AnalyticsDashboard

Monitor system health, trends, and alerts.

```tsx
import { AnalyticsDashboard } from '@/components/AnalyticsDashboard';

function MyPage() {
  return <AnalyticsDashboard />;
}
```

**Features:**
- System health score (0-100)
- Risk distribution (Healthy, At Risk, Critical)
- Active and critical alerts with resolution
- 7-day trend analysis
- Trend direction indicators (Improving/Declining)
- Recommendations based on current state
- Alert filtering by severity

## API Integration

### Service Methods

The `apiService` module provides all zombie detection, remediation, and analytics endpoints:

```typescript
// Zombie Detection
apiService.listZombieApis()          // GET /zombies
apiService.analyzeAllApis()          // POST /analyze
apiService.analyzeApiById(id)        // GET /apis/{id}/analysis
apiService.getZombieStats()          // GET /stats

// Remediation
apiService.getRemediationPlans(id?)  // GET /remediation/plans[/{id}]
apiService.decommissionApi(id)       // POST /remediation/decommission/{id}
apiService.archiveApi(id)            // POST /remediation/archive/{id}
apiService.notifyApiOwner(id)        // POST /remediation/notify-owner/{id}
apiService.reviveApi(id)             // POST /remediation/revive/{id}
apiService.bulkRemediation(ids, action) // POST /remediation/bulk
apiService.getRemediationStats()     // GET /remediation/stats

// Analytics
apiService.getMetrics(type?, hours)  // GET /analytics/metrics
apiService.getAlerts(severity?, unresolved) // GET /analytics/alerts
apiService.resolveAlert(id)          // POST /analytics/alerts/{id}/resolve
apiService.getSystemHealth()         // GET /analytics/health
apiService.getTrends(days)           // GET /analytics/trends
apiService.getAnalyticsReport()      // GET /analytics/report
apiService.setAlertThreshold(type, value) // POST /analytics/thresholds/{type}
```

## Custom Hook: useZombieDetection

For state management across components, use the `useZombieDetection` hook:

```typescript
import { useZombieDetection } from '@/hooks/useZombieDetection';

function MyComponent() {
  const {
    zombies,
    plans,
    health,
    alerts,
    loading,
    error,
    lastUpdated,
    loadAll,
    executeRemediationAction,
    resolveAlert,
    refreshAll
  } = useZombieDetection();

  // Load all data on mount
  useEffect(() => {
    loadAll();
  }, []);

  // Execute remediation action
  const handleDecommission = async (apiId: number) => {
    await executeRemediationAction(apiId, 'decommission');
  };

  // Resolve an alert
  const handleResolveAlert = async (alertId: string) => {
    await resolveAlert(alertId);
  };

  // Refresh all data
  const handleRefresh = async () => {
    await refreshAll();
  };

  return (
    <div>
      {loading && <p>Loading...</p>}
      {error && <p>Error: {error}</p>}
      {/* Render data */}
    </div>
  );
}
```

**Hook Methods:**
- `loadZombies()` - Load zombie API list
- `loadRemediationPlans()` - Load remediation plans
- `loadHealth()` - Load system health
- `loadAlerts()` - Load active alerts
- `loadAll()` - Load all data in parallel
- `executeRemediationAction(apiId, action)` - Execute remediation
- `resolveAlert(alertId)` - Mark alert resolved
- `refreshAll()` - Re-fetch all data
- `clearError()` - Clear error message

## Type Definitions

All TypeScript types are available from `@/types`:

```typescript
import {
  API,
  ZombieDetectionResult,
  RemediationPlan,
  RemediationAction,
  SystemHealth,
  Alert,
  Metric,
  TrendAnalysis,
  AnalyticsReport,
  ZombieStats
} from '@/types';
```

## Usage Examples

### Complete Dashboard Page

```tsx
import { ZombieDetectionDashboard } from '@/components/ZombieDetectionDashboard';
import { RemediationActions } from '@/components/RemediationActions';
import { AnalyticsDashboard } from '@/components/AnalyticsDashboard';
import { useZombieDetection } from '@/hooks/useZombieDetection';
import { useEffect } from 'react';

export default function ZombieManagementPage() {
  const { loadAll, refreshAll } = useZombieDetection();

  useEffect(() => {
    loadAll();
    // Refresh every 30 seconds
    const interval = setInterval(refreshAll, 30000);
    return () => clearInterval(interval);
  }, [loadAll, refreshAll]);

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold">Zombie API Management</h1>
      
      <ZombieDetectionDashboard />
      <RemediationActions />
      <AnalyticsDashboard />
    </div>
  );
}
```

### Custom Implementation

```tsx
import { useZombieDetection } from '@/hooks/useZombieDetection';
import { useEffect } from 'react';

export function CustomZombieView() {
  const {
    zombies,
    health,
    loading,
    error,
    loadAll,
    executeRemediationAction
  } = useZombieDetection();

  useEffect(() => {
    loadAll();
  }, [loadAll]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h2>Found {zombies.length} zombie APIs</h2>
      
      {health && (
        <div>
          <p>System Health: {health.health_score}%</p>
          <p>Status: {health.overall_status}</p>
        </div>
      )}

      {zombies.map(zombie => (
        <div key={zombie.id}>
          <h3>{zombie.name}</h3>
          <p>Risk: {zombie.risk_score}</p>
          <p>Status: {zombie.status}</p>
          <button
            onClick={() => executeRemediationAction(zombie.id, 'archive')}
          >
            Archive API
          </button>
        </div>
      ))}
    </div>
  );
}
```

## Styling

All components use Tailwind CSS with a consistent design system:

- **Colors**: Blue (primary), Red (zombie/critical), Yellow (warning), Green (healthy)
- **Layout**: Grid-based, responsive (mobile-first)
- **Cards**: White background, subtle shadows, rounded corners
- **Badges**: Color-coded status indicators
- **Tables**: Hover states, sortable columns
- **Modals**: Overlay with rounded dialog

## Error Handling

Components gracefully handle errors:

```tsx
{error && (
  <div className="p-4 bg-red-50 border-l-4 border-red-500 text-red-700">
    ✗ {error}
  </div>
)}
```

## Loading States

All components show loading indicators:

```tsx
{loading && (
  <div className="p-6 text-center text-gray-500">
    Loading...
  </div>
)}
```

## Auto-Refresh

For real-time updates, use intervals:

```tsx
useEffect(() => {
  const interval = setInterval(() => {
    refreshAll();
  }, 30000); // 30 seconds
  
  return () => clearInterval(interval);
}, [refreshAll]);
```

## Integration Checklist

- [ ] Install all components in pages
- [ ] Configure API base URL in `.env.local`
- [ ] Add routes for zombie management pages
- [ ] Set up auto-refresh intervals
- [ ] Test API connectivity
- [ ] Configure error boundaries
- [ ] Add success notifications
- [ ] Test all remediation actions
- [ ] Test alert resolution
- [ ] Configure analytics dashboards

## API Proxy Setup

For development, configure proxy in `vite.config.ts`:

```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    }
  }
}
```

Or set `VITE_API_URL` in `.env.local`:

```
VITE_API_URL=http://localhost:8000
```

## Performance Tips

1. Use the `useZombieDetection` hook for shared state
2. Implement pagination for large zombie lists
3. Set appropriate refresh intervals (30-60 seconds)
4. Cache metric data with timestamps
5. Lazy-load components below the fold
6. Memoize expensive computations

## Support & Debugging

Check browser console for detailed error logs. All API calls include:
- Error messages with context
- Timestamps for debugging
- Request/response logging
- Network error details

Monitor the `/analytics/health` endpoint for system status before making other requests.
