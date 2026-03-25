import React, { useEffect, useState } from 'react';
import {
  ShieldAlert,
  ShieldCheck,
  AlertTriangle,
  Zap,
  Globe,
  TrendingUp,
  ArrowRight
} from 'lucide-react';
import {
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { StatsCard } from '@components/StatsCard';
import { ChartCard } from '@components/ChartCard';
import { Badge } from '@components/Badge';
import { apiService } from '@services/api';

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await apiService.getDashboardSummary();
        if (response.success) {
          setStats(response.data);
        }
      } catch (error) {
        console.error('Dashboard stats failed:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  // Mock data for charts (replace with real data when API ready)
  const discoveryTrend = [
    { date: 'Mon', discovered: 12, verified: 9 },
    { date: 'Tue', discovered: 19, verified: 15 },
    { date: 'Wed', discovered: 8, verified: 6 },
    { date: 'Thu', discovered: 24, verified: 18 },
    { date: 'Fri', discovered: 31, verified: 28 },
    { date: 'Sat', discovered: 18, verified: 16 },
    { date: 'Sun', discovered: 22, verified: 19 }
  ];

  const riskDistribution = [
    { name: 'Critical', value: 8, color: '#f43f5e' },
    { name: 'High', value: 24, color: '#f97316' },
    { name: 'Medium', value: 42, color: '#eab308' },
    { name: 'Low', value: 56, color: '#06b6d4' }
  ];

  const statusBreakdown = [
    { status: 'Active', count: 145 },
    { status: 'Deprecated', count: 23 },
    { status: 'Orphaned', count: 12 },
    { status: 'Zombie', count: 8 }
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-slate-700 border-t-indigo-500 rounded-full animate-spin mx-auto mb-4" />
          <p className="text-slate-400">Loading dashboard analytics...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent mb-2">
          Platform Overview
        </h1>
        <p className="text-slate-400">Real-time security posture and API inventory discovery analytics</p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard
          label="Total APIs"
          value={stats?.total_apis || 188}
          icon={<Globe size={24} />}
          trend="+12% from last month"
          trendDirection="up"
          color="indigo"
        />
        <StatsCard
          label="Critical Risks"
          value={8}
          icon={<ShieldAlert size={24} />}
          trend="Requires immediate action"
          trendDirection="down"
          color="rose"
        />
        <StatsCard
          label="Documented APIs"
          value={89}
          icon={<ShieldCheck size={24} />}
          trend="47% of total"
          trendDirection="up"
          color="emerald"
        />
        <StatsCard
          label="This Week"
          value={73}
          icon={<Zap size={24} />}
          trend="New discoveries"
          trendDirection="up"
          color="amber"
        />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Discovery Trend */}
        <div className="lg:col-span-2">
          <ChartCard title="Discovery Trend" subtitle="APIs discovered vs verified this week">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={discoveryTrend}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis stroke="#64748b" />
                <YAxis stroke="#64748b" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0f172a',
                    border: '1px solid #1e293b',
                    borderRadius: '8px'
                  }}
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="discovered"
                  stroke="#6366f1"
                  strokeWidth={2}
                  dot={{ fill: '#6366f1' }}
                  activeDot={{ r: 6 }}
                />
                <Line
                  type="monotone"
                  dataKey="verified"
                  stroke="#10b981"
                  strokeWidth={2}
                  dot={{ fill: '#10b981' }}
                  activeDot={{ r: 6 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </ChartCard>
        </div>

        {/* Risk Summary */}
        <ChartCard title="Risk Distribution" subtitle="By severity level">
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={riskDistribution}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={90}
                paddingAngle={2}
                dataKey="value"
              >
                {riskDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: '#0f172a',
                  border: '1px solid #1e293b'
                }}
              />
            </PieChart>
          </ResponsiveContainer>
          <div className="mt-4 space-y-2">
            {riskDistribution.map((risk) => (
              <div key={risk.name} className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-2">
                  <div
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: risk.color }}
                  />
                  <span className="text-slate-300">{risk.name}</span>
                </div>
                <span className="font-semibold text-white">{risk.value}</span>
              </div>
            ))}
          </div>
        </ChartCard>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* API Status Breakdown */}
        <div className="lg:col-span-2">
          <ChartCard title="API Lifecycle Status" subtitle="Current distribution across all endpoints">
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={statusBreakdown}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis stroke="#64748b" />
                <YAxis stroke="#64748b" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0f172a',
                    border: '1px solid #1e293b'
                  }}
                />
                <Bar dataKey="count" fill="#6366f1" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>
        </div>

        {/* Priority Alerts */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6 backdrop-blur-xl">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <AlertTriangle size={20} className="text-amber-500" />
            Priority Alerts
          </h3>
          <div className="space-y-3">
            <AlertItem
              title="Missing Authentication"
              description="15 APIs without active auth"
              severity="high"
            />
            <AlertItem
              title="Outdated Schemas"
              description="23 endpoints using deprecated specs"
              severity="medium"
            />
            <AlertItem
              title="Shadow APIs"
              description="8 undocumented endpoints found"
              severity="high"
            />
            <AlertItem
              title="Rate Limit Issues"
              description="3 services insufficient protection"
              severity="low"
            />
          </div>
          <button className="w-full mt-6 px-4 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl font-medium transition-all text-sm flex items-center justify-center gap-2 group">
            <span>View All Alerts</span>
            <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
          </button>
        </div>
      </div>

      {/* Recent Activity */}
      <ChartCard title="Recent Activity" subtitle="Latest API discoveries and findings">
        <div className="space-y-4">
          <ActivityItem
            type="discovered"
            title="New API Endpoint"
            description="/api/v2/users/profile discovered in auth-service"
            time="2 hours ago"
          />
          <ActivityItem
            type="risk"
            title="Critical Vulnerability"
            description="JWT secret weakness identified in payment-gateway"
            time="4 hours ago"
          />
          <ActivityItem
            type="resolved"
            title="Risk Remediated"
            description="Legacy OAuth implementation upgraded to OAuth 2.1"
            time="1 day ago"
          />
          <ActivityItem
            type="deprecation"
            title="API Decommissioning"
            description="v1 of billing-service marked for retirement"
            time="2 days ago"
          />
        </div>
      </ChartCard>
    </div>
  );
};

interface AlertItemProps {
  title: string;
  description: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
}

const AlertItem: React.FC<AlertItemProps> = ({ title, description, severity }) => {
  const severityColors = {
    low: 'border-cyan-500/20 bg-cyan-500/5',
    medium: 'border-amber-500/20 bg-amber-500/5',
    high: 'border-orange-500/20 bg-orange-500/5',
    critical: 'border-rose-500/20 bg-rose-500/5'
  };

  return (
    <div className={`border rounded-lg p-3 transition-all hover:border-opacity-100 ${severityColors[severity]}`}>
      <div className="flex items-start gap-2">
        <Badge variant={severity === 'critical' ? 'error' : severity === 'high' ? 'warning' : 'info'}>
          {severity.toUpperCase()}
        </Badge>
        <div className="flex-1">
          <p className="font-semibold text-white text-sm">{title}</p>
          <p className="text-xs text-slate-400 mt-1">{description}</p>
        </div>
      </div>
    </div>
  );
};

interface ActivityItemProps {
  type: 'discovered' | 'risk' | 'resolved' | 'deprecation';
  title: string;
  description: string;
  time: string;
}

const ActivityItem: React.FC<ActivityItemProps> = ({ type, title, description, time }) => {
  const icons = {
    discovered: <Zap className="w-5 h-5 text-indigo-500" />,
    risk: <ShieldAlert className="w-5 h-5 text-rose-500" />,
    resolved: <ShieldCheck className="w-5 h-5 text-emerald-500" />,
    deprecation: <TrendingUp className="w-5 h-5 text-amber-500" />
  };

  return (
      <div className="flex gap-4 p-4 rounded-xl bg-slate-800/30 hover:bg-slate-800/50 transition-colors">
      <div className="flex-shrink-0 mt-1">{icons[type]}</div>
      <div className="flex-1 min-w-0">
        <p className="font-semibold text-white text-sm">{title}</p>
        <p className="text-xs text-slate-400 mt-0.5 truncate">{description}</p>
        <p className="text-xs text-slate-500 mt-2">{time}</p>
      </div>
    </div>
  );
};

export default Dashboard;

