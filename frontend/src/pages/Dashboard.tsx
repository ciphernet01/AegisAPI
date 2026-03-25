import React, { useEffect, useState } from 'react';
import {
  ShieldAlert,
  ShieldCheck,
  AlertTriangle,
  Zap,
  Globe,
  TrendingUp,
  ArrowRight,
  Lock,
  Activity,
  Users
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
  ResponsiveContainer,
  AreaChart,
  Area,
  ComposedChart
} from 'recharts';
import { StatsCard } from '@components/StatsCard';
import { ChartCard } from '@components/ChartCard';
import { Badge } from '@components/Badge';
import { FilterBar } from '@components/FilterBar';
import { SummaryCard } from '@components/SummaryCard';
import { apiService } from '@services/api';

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState('7d');

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

  const handleExport = (format: 'csv' | 'pdf' | 'json') => {
    console.log(`Exporting dashboard as ${format}`);
    // TODO: Implement export functionality
  };

  // Mock data for charts (replace with real data when API ready)
  const discoveryTrend = [
    { date: 'Mon', discovered: 12, verified: 9, documented: 8 },
    { date: 'Tue', discovered: 19, verified: 15, documented: 12 },
    { date: 'Wed', discovered: 8, verified: 6, documented: 5 },
    { date: 'Thu', discovered: 24, verified: 18, documented: 15 },
    { date: 'Fri', discovered: 31, verified: 28, documented: 25 },
    { date: 'Sat', discovered: 18, verified: 16, documented: 14 },
    { date: 'Sun', discovered: 22, verified: 19, documented: 17 }
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

  const complianceMetrics = [
    { name: 'Week 1', compliance: 75, target: 85 },
    { name: 'Week 2', compliance: 78, target: 85 },
    { name: 'Week 3', compliance: 82, target: 85 },
    { name: 'Week 4', compliance: 88, target: 85 }
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
      {/* Header with filters */}
      <div className="space-y-4">
        <div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent mb-2">
            Platform Overview
          </h1>
          <p className="text-slate-400 font-medium">Real-time security posture and API inventory discovery analytics</p>
        </div>
        <FilterBar 
          onTimeRangeChange={setTimeRange}
          onExport={handleExport}
          selectedTimeRange={timeRange}
        />
      </div>

      {/* Key Metrics with enhanced design */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard
          label="Total APIs"
          value={stats?.total_apis || 188}
          icon={<Globe size={24} />}
          trend="+12% from last month"
          trendDirection="up"
          color="indigo"
          change={12}
        />
        <StatsCard
          label="Critical Risks"
          value={8}
          icon={<ShieldAlert size={24} />}
          trend="Requires immediate action"
          trendDirection="down"
          color="rose"
          change={-3}
        />
        <StatsCard
          label="Documented APIs"
          value={89}
          icon={<ShieldCheck size={24} />}
          trend="47% of total"
          trendDirection="up"
          color="emerald"
          change={8}
        />
        <StatsCard
          label="This Week"
          value={73}
          icon={<Zap size={24} />}
          trend="New discoveries"
          trendDirection="up"
          color="amber"
          change={25}
        />
      </div>

      {/* Quick Insights Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <SummaryCard
          title="Top Risk"
          value="JWT Weakness"
          description="Detected in payment-gateway service"
          icon={<AlertTriangle size={20} />}
          variant="warning"
          actionText="View Details"
        />
        <SummaryCard
          title="Most Accessed"
          value="auth-service"
          description="2,847 calls in last 7 days"
          icon={<Users size={20} />}
          variant="info"
          actionText="Analyze"
        />
        <SummaryCard
          title="Security Score"
          value="8.2/10"
          description="↑ 0.5 from last period"
          icon={<Lock size={20} />}
          variant="success"
          actionText="Improve"
        />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Discovery Trend - Enhanced */}
        <div className="lg:col-span-2">
          <ChartCard 
            title="Discovery & Verification Trend" 
            subtitle="APIs discovered, verified, and documented this week"
          >
            <ResponsiveContainer width="100%" height={320}>
              <AreaChart data={discoveryTrend}>
                <defs>
                  <linearGradient id="colorDiscovered" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorVerified" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                  </linearGradient>
                </defs>
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
                <Area
                  type="monotone"
                  dataKey="discovered"
                  stroke="#6366f1"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#colorDiscovered)"
                />
                <Area
                  type="monotone"
                  dataKey="verified"
                  stroke="#10b981"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#colorVerified)"
                />
              </AreaChart>
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
                    className="w-3 h-3 rounded-full shadow-lg"
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
        <div className="relative overflow-hidden rounded-2xl backdrop-blur-xl transition-all duration-300 bg-gradient-to-br from-slate-900/60 to-slate-900/40 border border-slate-800/50 hover:border-slate-700 hover:shadow-[0_0_30px_rgba(99,102,241,0.1)] shadow-card">
          <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-amber-500/30 to-transparent" />
          
          <div className="relative z-10 p-6">
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
            <button className="w-full mt-6 px-4 py-2.5 bg-gradient-to-r from-indigo-600 to-indigo-500 hover:from-indigo-500 hover:to-indigo-400 text-white rounded-xl font-medium transition-all text-sm flex items-center justify-center gap-2 group shadow-lg hover:shadow-indigo-600/50">
              <span>View All Alerts</span>
              <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
            </button>
          </div>
        </div>
      </div>

      {/* Compliance Metrics */}
      <ChartCard title="Security Compliance Trend" subtitle="Weekly progress towards compliance targets">
        <ResponsiveContainer width="100%" height={280}>
          <ComposedChart data={complianceMetrics}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis stroke="#64748b" />
            <YAxis stroke="#64748b" />
            <Tooltip
              contentStyle={{
                backgroundColor: '#0f172a',
                border: '1px solid #1e293b'
              }}
            />
            <Legend />
            <Bar dataKey="compliance" fill="#10b981" radius={[8, 8, 0, 0]} />
            <Line
              type="monotone"
              dataKey="target"
              stroke="#f59e0b"
              strokeWidth={2}
              strokeDasharray="5 5"
              dot={{ fill: '#f59e0b' }}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </ChartCard>

      {/* Recent Activity */}
      <ChartCard title="Recent Activity" subtitle="Latest API discoveries and findings">
        <div className="space-y-3">
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
    low: 'border-cyan-500/30 bg-cyan-500/10 hover:bg-cyan-500/15',
    medium: 'border-amber-500/30 bg-amber-500/10 hover:bg-amber-500/15',
    high: 'border-orange-500/30 bg-orange-500/10 hover:bg-orange-500/15',
    critical: 'border-rose-500/30 bg-rose-500/10 hover:bg-rose-500/15'
  };

  return (
    <div className={`border rounded-lg p-3 transition-all ${severityColors[severity]}`}>
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
    deprecation: <Activity className="w-5 h-5 text-amber-500" />
  };

  return (
    <div className="flex gap-4 p-4 rounded-xl bg-slate-800/30 hover:bg-slate-800/50 transition-all duration-300 border border-slate-700/30 hover:border-slate-600/50">
      <div className="flex-shrink-0 mt-1">{icons[type]}</div>
      <div className="flex-1 min-w-0">
        <p className="font-semibold text-white text-sm">{title}</p>
        <p className="text-xs text-slate-400 mt-0.5 line-clamp-2">{description}</p>
        <p className="text-xs text-slate-500 mt-2">{time}</p>
      </div>
    </div>
  );
};

export default Dashboard;

