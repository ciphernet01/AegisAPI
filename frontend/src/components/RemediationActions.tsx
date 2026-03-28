import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import { RemediationPlan } from '../types';

export function RemediationActions() {
  const [plans, setPlans] = useState<RemediationPlan[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [executing, setExecuting] = useState<number | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  useEffect(() => {
    loadRemediationPlans();
  }, []);

  const loadRemediationPlans = async () => {
    try {
      setLoading(true);
      const response = await apiService.getRemediationPlans();
      setPlans(response.plans || []);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load remediation plans');
    } finally {
      setLoading(false);
    }
  };

  const executeAction = async (
    apiId: number,
    action: 'decommission' | 'archive' | 'notify' | 'revive'
  ) => {
    try {
      setExecuting(apiId);
      
      let response;
      switch (action) {
        case 'decommission':
          response = await apiService.decommissionApi(apiId);
          break;
        case 'archive':
          response = await apiService.archiveApi(apiId);
          break;
        case 'notify':
          response = await apiService.notifyApiOwner(apiId);
          break;
        case 'revive':
          response = await apiService.reviveApi(apiId);
          break;
      }

      setSuccessMessage(`${action} action executed successfully`);
      setTimeout(() => setSuccessMessage(null), 3000);
      await loadRemediationPlans();
    } catch (err) {
      setError(err instanceof Error ? err.message : `Failed to execute ${action} action`);
    } finally {
      setExecuting(null);
    }
  };

  if (loading) {
    return <div className="p-6 text-center text-gray-500">Loading remediation plans...</div>;
  }

  return (
    <div className="space-y-6">
      {/* Success Message */}
      {successMessage && (
        <div className="p-4 bg-green-50 border-l-4 border-green-500 text-green-700 rounded">
          ✓ {successMessage}
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="p-4 bg-red-50 border-l-4 border-red-500 text-red-700 rounded">
          ✗ {error}
        </div>
      )}

      {/* Remediation Plans */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-800">Remediation Plans</h2>
          <p className="text-sm text-gray-500 mt-1">
            {plans.length} API(s) have recommended remediation actions
          </p>
        </div>

        {plans.length === 0 ? (
          <div className="p-8 text-center text-gray-500">
            No remediation plans available. All APIs are healthy!
          </div>
        ) : (
          <div className="divide-y divide-gray-200">
            {plans.map((plan) => (
              <RemediationPlanCard
                key={plan.api_id}
                plan={plan}
                onExecuteAction={executeAction}
                isExecuting={executing === plan.api_id}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function RemediationPlanCard({
  plan,
  onExecuteAction,
  isExecuting
}: {
  plan: RemediationPlan;
  onExecuteAction: (apiId: number, action: string) => Promise<void>;
  isExecuting: boolean;
}) {
  const urgencyColor = {
    low: 'bg-green-100 text-green-800',
    medium: 'bg-yellow-100 text-yellow-800',
    high: 'bg-orange-100 text-orange-800',
    critical: 'bg-red-100 text-red-800'
  }[plan.urgency_level];

  const actionButtons = (action: RemediationPlan['recommended_actions'][0]) => {
    const actionMap: Record<string, 'decommission' | 'archive' | 'notify' | 'revive'> = {
      'DECOMMISSION': 'decommission',
      'ARCHIVE': 'archive',
      'NOTIFY_OWNER': 'notify',
      'REVIVE': 'revive'
    };

    return actionMap[action.action_type] || 'notify';
  };

  return (
    <div className="p-6">
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">{plan.api_name}</h3>
          <p className="text-sm text-gray-500 mt-1">Status: {plan.current_status}</p>
        </div>
        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${urgencyColor}`}>
          {plan.urgency_level.toUpperCase()}
        </span>
      </div>

      <div className="grid grid-cols-3 gap-4 mb-4">
        <div>
          <p className="text-xs text-gray-600">Estimated Effort</p>
          <p className="text-sm font-medium text-gray-900">{plan.estimated_effort}</p>
        </div>
        <div>
          <p className="text-xs text-gray-600">Cost Estimate</p>
          <p className="text-sm font-medium text-gray-900">{plan.cost_estimate}</p>
        </div>
        <div>
          <p className="text-xs text-gray-600">Actions Available</p>
          <p className="text-sm font-medium text-gray-900">{plan.recommended_actions.length}</p>
        </div>
      </div>

      <div className="mb-4 space-y-2">
        <p className="text-sm font-medium text-gray-700">Recommended Actions:</p>
        {plan.recommended_actions.map((action, idx) => (
          <div key={idx} className="flex items-start gap-3">
            <span className={`px-2 py-1 text-xs rounded font-medium ${
              action.status === 'COMPLETED' ? 'bg-green-100 text-green-800' :
              action.status === 'IN_PROGRESS' ? 'bg-blue-100 text-blue-800' :
              'bg-gray-100 text-gray-800'
            }`}>
              {action.action_type}
            </span>
            <div className="flex-1">
              <p className="text-sm text-gray-700">{action.description}</p>
              <p className="text-xs text-gray-500 mt-1">Priority: {action.priority}/5 | Status: {action.status}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="flex gap-2 pt-4 border-t border-gray-200">
        <button
          onClick={() => onExecuteAction(plan.api_id, 'decommission')}
          disabled={isExecuting}
          className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium"
        >
          {isExecuting ? 'Processing...' : 'Decommission'}
        </button>
        <button
          onClick={() => onExecuteAction(plan.api_id, 'archive')}
          disabled={isExecuting}
          className="px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium"
        >
          {isExecuting ? 'Processing...' : 'Archive'}
        </button>
        <button
          onClick={() => onExecuteAction(plan.api_id, 'notify')}
          disabled={isExecuting}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium"
        >
          {isExecuting ? 'Processing...' : 'Notify Owner'}
        </button>
        <button
          onClick={() => onExecuteAction(plan.api_id, 'revive')}
          disabled={isExecuting}
          className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium"
        >
          {isExecuting ? 'Processing...' : 'Revive'}
        </button>
      </div>
    </div>
  );
}
