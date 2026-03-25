import React, { useEffect, useState } from 'react';
import { 
  Activity, 
  ShieldAlert, 
  ShieldCheck, 
  AlertTriangle, 
  Zap, 
  Globe, 
  Database,
  ArrowUpRight
} from 'lucide-react';
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
        console.error("Dashboard stats failed:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  if (loading) return <div className="text-slate-400">Loading analytics...</div>;

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Platform Overview</h1>
        <p className="text-slate-400">Real-time security posture and API inventory discovery analytics.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard 
          label="Total Discovered APIs" 
          value={stats?.total_apis || 0} 
          icon={<Globe size={20} className="text-indigo-400" />} 
          trend="+12% this month"
          color="indigo"
        />
        <StatCard 
          label="Zombie APIs Detected" 
          value={stats?.by_status?.zombie || 0} 
          icon={<Zap size={20} className="text-rose-400" />} 
          trend="Action required"
          color="rose"
        />
        <StatCard 
          label="Critical Findings" 
          value={8} 
          icon={<ShieldAlert size={20} className="text-amber-400" />} 
          trend="High risk"
          color="amber"
        />
        <StatCard 
          label="Secure APIs" 
          value={stats?.documented || 0} 
          icon={<ShieldCheck size={20} className="text-emerald-400" />} 
          trend="Vulnerability-free"
          color="emerald"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Status Distribution */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
          <div className="flex items-center justify-between mb-8">
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <Activity size={20} className="text-indigo-400" />
              API Lifecycle Status
            </h3>
            <button className="text-indigo-400 text-xs font-semibold hover:text-indigo-300 transition-colors uppercase tracking-widest">Details</button>
          </div>
          
          <div className="space-y-6">
            <ProgressBar label="Active" value={stats?.by_status?.active || 0} max={stats?.total_apis || 1} color="indigo" />
            <ProgressBar label="Deprecated" value={stats?.by_status?.deprecated || 0} max={stats?.total_apis || 1} color="amber" />
            <ProgressBar label="Orphaned" value={stats?.by_status?.orphaned || 0} max={stats?.total_apis || 1} color="slate" />
            <ProgressBar label="Zombie" value={stats?.by_status?.zombie || 0} max={stats?.total_apis || 1} color="rose" />
          </div>
        </div>

        {/* Quick Insights */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
          <h3 className="text-lg font-bold text-white mb-6 flex items-center gap-2">
            <AlertTriangle size={20} className="text-amber-400" />
            Priority Risks
          </h3>
          <div className="space-y-4">
            <InsightItem 
              title="Auth Missing" 
              desc="15 APIs identified without active authentication." 
              severity="high" 
            />
            <InsightItem 
              title="Shadow APIs" 
              desc="8 undocument endpoints found in cluster." 
              severity="medium" 
            />
            <InsightItem 
              title="Sensitive Data" 
              desc="PII exposure likely on /v1/profiles." 
              severity="critical" 
            />
          </div>
          <button className="w-full mt-6 py-3 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl font-medium transition-all text-sm">
            View All Assessments
          </button>
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ label, value, icon, trend, color }: any) => {
  const colorMap: any = {
    indigo: "border-indigo-500/20 shadow-indigo-500/5",
    rose: "border-rose-500/20 shadow-rose-500/5",
    amber: "border-amber-500/20 shadow-amber-500/5",
    emerald: "border-emerald-500/20 shadow-emerald-500/5",
  };

  return (
    <div className={`bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl transition-all hover:scale-[1.02] hover:bg-slate-800/80 group ${colorMap[color] || ""}`}>
      <div className="flex items-center justify-between mb-4">
        <div className="p-2 bg-slate-800/50 rounded-lg group-hover:bg-slate-800 transition-colors">
          {icon}
        </div>
        <ArrowUpRight size={18} className="text-slate-600 group-hover:text-slate-400 transition-colors" />
      </div>
      <div>
        <p className="text-slate-500 text-sm font-medium mb-1">{label}</p>
        <div className="flex items-baseline gap-2">
          <h2 className="text-3xl font-bold text-white tracking-tight">{value}</h2>
        </div>
        <p className="text-[10px] uppercase tracking-wider font-bold text-slate-600 mt-2">{trend}</p>
      </div>
    </div>
  );
};

const ProgressBar = ({ label, value, max, color }: any) => {
  const percentage = Math.round((value / max) * 100) || 0;
  const colorMap: any = {
    indigo: "bg-indigo-600 shadow-indigo-500/20",
    rose: "bg-rose-600 shadow-rose-500/20",
    amber: "bg-amber-600 shadow-amber-500/20",
    slate: "bg-slate-400 shadow-slate-400/20",
  };

  return (
    <div className="space-y-2">
      <div className="flex justify-between text-sm font-medium">
        <span className="text-slate-300">{label}</span>
        <span className="text-slate-500">{value} <span className="text-xs text-slate-700">({percentage}%)</span></span>
      </div>
      <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div 
          className={`h-full rounded-full transition-all duration-1000 ${colorMap[color] || "bg-slate-600"}`}
          style={{ width: `${percentage}%` }}
        ></div>
      </div>
    </div>
  );
};

const InsightItem = ({ title, desc, severity }: any) => {
  const ringColor: any = {
    critical: "border-rose-500 text-rose-500 bg-rose-500/10",
    high: "border-amber-500 text-amber-500 bg-amber-500/10",
    medium: "border-indigo-500 text-indigo-500 bg-indigo-500/10",
  };

  return (
    <div className="flex gap-4 p-4 rounded-xl border border-slate-800 hover:border-slate-700 bg-slate-800/30 transition-all cursor-pointer">
      <div className={`mt-1 shrink-0 w-2 h-2 rounded-full ${severity === 'critical' ? 'bg-rose-500 shadow-rose-500/50 shadow-sm' : severity === 'high' ? 'bg-amber-500' : 'bg-indigo-500'}`}></div>
      <div>
        <h4 className="text-sm font-bold text-slate-100 mb-1">{title}</h4>
        <p className="text-xs text-slate-500 leading-relaxed line-clamp-2">{desc}</p>
      </div>
    </div>
  );
};

export default Dashboard;
