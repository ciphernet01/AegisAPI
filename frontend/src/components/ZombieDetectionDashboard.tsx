import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import { ZombieDetectionResult, ZombieStats } from '../types';

export function ZombieDetectionDashboard() {
  const [zombies, setZombies] = useState<ZombieDetectionResult[]>([]);
  const [stats, setStats] = useState<ZombieStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedZombie, setSelectedZombie] = useState<ZombieDetectionResult | null>(null);

  useEffect(() => {
    loadZombieData();
  }, []);

  const loadZombieData = async () => {
    try {
      setLoading(true);
      const [zombieList, statsData] = await Promise.all([
        apiService.listZombieApis(),
        apiService.getZombieStats()
      ]);
      setZombies(zombieList.apis || []);
      setStats(statsData);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load zombie APIs');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="p-6 text-center text-gray-500">Loading zombie detection data...</div>;
  }

  return (
    <div className="space-y-6">
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard
          label="Total APIs"
          value={stats?.total_apis || 0}
          color="blue"
        />
        <StatCard
          label="Zombie APIs"
          value={stats?.zombie_count || 0}
          color="red"
          highlight={true}
        />
        <StatCard
          label="Deprecated"
          value={stats?.deprecated_count || 0}
          color="yellow"
        />
        <StatCard
          label="Health Score"
          value={stats?.health_score?.toFixed(1) || '0'}
          color="green"
          suffix="%"
        />
      </div>

      {/* Zombie List */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-800">Detected Zombie APIs</h2>
          <p className="text-sm text-gray-500 mt-1">
            {zombies.length} zombie API(s) detected in your infrastructure
          </p>
        </div>

        {error && (
          <div className="p-4 bg-red-50 border-l-4 border-red-500 text-red-700">
            {error}
          </div>
        )}

        {zombies.length === 0 ? (
          <div className="p-8 text-center text-gray-500">
            No zombie APIs detected! Your API inventory is healthy.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">API Name</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Status</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Risk Score</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Confidence</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Action</th>
                </tr>
              </thead>
              <tbody>
                {zombies.map((zombie) => (
                  <tr key={zombie.id} className="border-b border-gray-200 hover:bg-gray-50">
                    <td className="px-6 py-4 text-sm text-gray-900">{zombie.name}</td>
                    <td className="px-6 py-4 text-sm">
                      <StatusBadge status={zombie.status} />
                    </td>
                    <td className="px-6 py-4 text-sm">
                      <RiskScoreBadge score={zombie.risk_score} />
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">
                      {(zombie.confidence * 100).toFixed(0)}%
                    </td>
                    <td className="px-6 py-4 text-sm">
                      <button
                        onClick={() => setSelectedZombie(zombie)}
                        className="text-blue-600 hover:text-blue-800 font-medium"
                      >
                        View Details
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Detail Modal */}
      {selectedZombie && (
        <ZombieDetailModal
          zombie={selectedZombie}
          onClose={() => setSelectedZombie(null)}
        />
      )}
    </div>
  );
}

function StatCard({
  label,
  value,
  color = 'blue',
  highlight = false,
  suffix = ''
}: {
  label: string;
  value: string | number;
  color?: 'blue' | 'red' | 'yellow' | 'green';
  highlight?: boolean;
  suffix?: string;
}) {
  const colorClass = {
    blue: 'bg-blue-50 border-blue-200',
    red: 'bg-red-50 border-red-200',
    yellow: 'bg-yellow-50 border-yellow-200',
    green: 'bg-green-50 border-green-200'
  }[color];

  const valueColorClass = {
    blue: 'text-blue-900',
    red: 'text-red-900',
    yellow: 'text-yellow-900',
    green: 'text-green-900'
  }[color];

  return (
    <div className={`p-4 border rounded-lg ${colorClass} ${highlight ? 'ring-2 ring-' + color + '-300' : ''}`}>
      <p className="text-sm text-gray-600">{label}</p>
      <p className={`text-3xl font-bold mt-2 ${valueColorClass}`}>
        {value}{suffix}
      </p>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const colorClass = {
    'ZOMBIE': 'bg-red-100 text-red-800',
    'DEPRECATED': 'bg-yellow-100 text-yellow-800',
    'ORPHANED': 'bg-orange-100 text-orange-800',
    'ACTIVE': 'bg-green-100 text-green-800'
  }[status] || 'bg-gray-100 text-gray-800';

  return (
    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${colorClass}`}>
      {status}
    </span>
  );
}

function RiskScoreBadge({ score }: { score: number }) {
  let color = 'text-green-600';
  if (score >= 70) color = 'text-red-600 font-bold';
  else if (score >= 50) color = 'text-yellow-600';

  return <span className={color}>{score.toFixed(0)}</span>;
}

function ZombieDetailModal({
  zombie,
  onClose
}: {
  zombie: ZombieDetectionResult;
  onClose: () => void;
}) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-lg max-w-2xl w-full mx-4 max-h-96 overflow-y-auto">
        <div className="p-6 border-b border-gray-200">
          <div className="flex justify-between items-start">
            <div>
              <h3 className="text-xl font-semibold text-gray-900">{zombie.name}</h3>
              <p className="text-sm text-gray-500 mt-1">{zombie.endpoint}</p>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600"
            >
              ✕
            </button>
          </div>
        </div>

        <div className="p-6 space-y-4">
          <div className="grid grid-cols-3 gap-4">
            <div>
              <p className="text-sm text-gray-600">Status</p>
              <StatusBadge status={zombie.status} />
            </div>
            <div>
              <p className="text-sm text-gray-600">Risk Score</p>
              <RiskScoreBadge score={zombie.risk_score} />
            </div>
            <div>
              <p className="text-sm text-gray-600">Confidence</p>
              <p className="text-lg font-semibold">{(zombie.confidence * 100).toFixed(0)}%</p>
            </div>
          </div>

          {zombie.zombie_factors && (
            <div className="border-t pt-4">
              <h4 className="font-semibold text-gray-900 mb-3">Risk Factors</h4>
              <div className="grid grid-cols-2 gap-3">
                <FactorBar label="Traffic Activity" value={zombie.zombie_factors.traffic_activity} />
                <FactorBar label="Documentation" value={zombie.zombie_factors.documentation_status} />
                <FactorBar label="Ownership" value={zombie.zombie_factors.ownership} />
                <FactorBar label="Age/Deprecation" value={zombie.zombie_factors.age_deprecation} />
              </div>
            </div>
          )}

          {zombie.reasoning && zombie.reasoning.length > 0 && (
            <div className="border-t pt-4">
              <h4 className="font-semibold text-gray-900 mb-2">Classification Reasoning</h4>
              <ul className="space-y-1">
                {zombie.reasoning.map((reason, idx) => (
                  <li key={idx} className="text-sm text-gray-700 flex items-start">
                    <span className="text-blue-500 mr-2">•</span>
                    {reason}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

        <div className="p-6 border-t border-gray-200 flex justify-end gap-3">
          <button
            onClick={onClose}
            className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
          >
            Close
          </button>
          <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            View Remediation
          </button>
        </div>
      </div>
    </div>
  );
}

function FactorBar({ label, value }: { label: string; value: number }) {
  return (
    <div>
      <p className="text-xs text-gray-600 mb-1">{label}</p>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div
          className="bg-red-500 h-2 rounded-full"
          style={{ width: `${Math.min(value * 100, 100)}%` }}
        />
      </div>
      <p className="text-xs text-gray-500 mt-1">{(value * 100).toFixed(0)}%</p>
    </div>
  );
}
