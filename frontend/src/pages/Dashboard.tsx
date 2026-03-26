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
import { clsx } from 'clsx';
import { apiService } from '@services/api';
import { useTheme } from '@contexts/ThemeContext';

const Dashboard: React.FC = () => {
  const { theme } = useTheme();
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

  if (loading) return <div className={clsx(theme === 'dark' ? "text-slate-400" : "text-gray-600")}>Loading analytics...</div>;

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div>
        <h1 className={clsx("text-3xl font-bold mb-2", theme === 'dark' ? "text-white" : "text-black")}>Platform Overview</h1>
        <p className={clsx(theme === 'dark' ? "text-slate-400" : "text-gray-600")}>Real-time security posture and API inventory discovery analytics.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard 
          theme={theme}
          label="Total Discovered APIs" 
          value={stats?.total_apis || 0} 
          icon={<Globe size={20} className="text-indigo-400" />} 
          trend="+12% this month"
          color="indigo"
        />
        <StatCard 
          theme={theme}
          label="Zombie APIs Detected" 
          value={stats?.by_status?.zombie || 0} 
          icon={<Zap size={20} className="text-rose-400" />} 
          trend="Action required"
          color="rose"
        />
        <StatCard 
          theme={theme}
          label="Critical Findings" 
          value={8} 
          icon={<ShieldAlert size={20} className="text-amber-400" />} 
          trend="High risk"
          color="amber"
        />
        <StatCard 
          theme={theme}
          label="Secure APIs" 
          value={stats?.documented || 0} 
          icon={<ShieldCheck size={20} className="text-emerald-400" />} 
          trend="Vulnerability-free"
          color="emerald"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Status Distribution */}
        <div className={clsx("lg:col-span-2 rounded-2xl p-6 shadow-xl border", theme === 'dark' ? "bg-slate-900 border-slate-800" : "bg-white border-gray-200")}>
          <div className="flex items-center justify-between mb-8">
            <h3 className={clsx("text-lg font-bold flex items-center gap-2", theme === 'dark' ? "text-white" : "text-black")}>
              <Activity size={20} className="text-indigo-400" />
              API Lifecycle Status
            </h3>
            <button className={clsx("text-xs font-semibold transition-colors uppercase tracking-widest", theme === 'dark' ? "text-indigo-400 hover:text-indigo-300" : "text-indigo-600 hover:text-indigo-700")}>Details</button>
          </div>
          
          <div className="space-y-6">
            <ProgressBar label="Active" value={stats?.by_status?.active || 0} max={stats?.total_apis || 1} color="indigo" theme={theme} />
            <ProgressBar label="Deprecated" value={stats?.by_status?.deprecated || 0} max={stats?.total_apis || 1} color="amber" theme={theme} />
            <ProgressBar label="Orphaned" value={stats?.by_status?.orphaned || 0} max={stats?.total_apis || 1} color="slate" theme={theme} />
            <ProgressBar label="Zombie" value={stats?.by_status?.zombie || 0} max={stats?.total_apis || 1} color="rose" theme={theme} />
          </div>
        </div>

        {/* Quick Insights */}
        <div className={clsx("rounded-2xl p-6 shadow-xl border", theme === 'dark' ? "bg-slate-900 border-slate-800" : "bg-white border-gray-200")}>
          <h3 className={clsx("text-lg font-bold mb-6 flex items-center gap-2", theme === 'dark' ? "text-white" : "text-black")}>
            <AlertTriangle size={20} className="text-amber-400" />
            Priority Risks
          </h3>
          <div className="space-y-4">
            <InsightItem 
              theme={theme}
              title="Auth Missing" 
              desc="15 APIs identified without active authentication." 
              severity="high" 
            />
            <InsightItem 
              theme={theme}
              title="Shadow APIs" 
              desc="8 undocument endpoints found in cluster." 
              severity="medium" 
            />
            <InsightItem 
              theme={theme}
              title="Sensitive Data" 
              desc="PII exposure likely on /v1/profiles." 
              severity="critical" 
            />
          </div>
          <button className={clsx("w-full mt-6 py-3 rounded-xl font-medium transition-all text-sm", theme === 'dark' ? "bg-slate-800 hover:bg-slate-700 text-slate-200" : "bg-gray-200 hover:bg-gray-300 text-gray-800")}>
            View All Assessments
          </button>
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ label, value, icon, trend, color, theme }: any) => {
  const colorMap: any = {
    indigo: "border-indigo-500/20 shadow-indigo-500/5",
    rose: "border-rose-500/20 shadow-rose-500/5",
    amber: "border-amber-500/20 shadow-amber-500/5",
    emerald: "border-emerald-500/20 shadow-emerald-500/5",
  };

  return (
    <div className={clsx("rounded-2xl p-6 shadow-xl transition-all hover:scale-[1.02] border", theme === 'dark' ? `bg-slate-900 border-slate-800 hover:bg-slate-800/80 ${colorMap[color] || ""}` : "bg-white border-gray-200 hover:bg-gray-50")}>
      <div className="flex items-center justify-between mb-4">
        <div className={clsx("p-2 rounded-lg transition-colors", theme === 'dark' ? "bg-slate-800/50 group-hover:bg-slate-800" : "bg-gray-200 group-hover:bg-gray-300")}>
          {icon}
        </div>
        <ArrowUpRight size={18} className={clsx("transition-colors", theme === 'dark' ? "text-slate-600 group-hover:text-slate-400" : "text-gray-500 group-hover:text-gray-600")} />
      </div>
      <div>
        <p className={clsx("text-sm font-medium mb-1", theme === 'dark' ? "text-slate-500" : "text-gray-600")}>{label}</p>
        <div className="flex items-baseline gap-2">
          <h2 className={clsx("text-3xl font-bold tracking-tight", theme === 'dark' ? "text-white" : "text-black")}>{value}</h2>
        </div>
        <p className={clsx("text-[10px] uppercase tracking-wider font-bold mt-2", theme === 'dark' ? "text-slate-600" : "text-gray-500")}>{trend}</p>
      </div>
    </div>
  );
};
};

const ProgressBar = ({ label, value, max, color, theme }: any) => {
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
        <span className={theme === 'dark' ? "text-slate-300" : "text-gray-700"}>{label}</span>
        <span className={clsx(theme === 'dark' ? "text-slate-500" : "text-gray-600", "text-xs")}>{value} <span className={clsx("text-xs", theme === 'dark' ? "text-slate-700" : "text-gray-500")}>({percentage}%)</span></span>
      </div>
      <div className={clsx("w-full h-1.5 rounded-full overflow-hidden", theme === 'dark' ? "bg-slate-800" : "bg-gray-300")}>
        <div 
          className={`h-full rounded-full transition-all duration-1000 ${colorMap[color] || "bg-slate-600"}`}
          style={{ width: `${percentage}%` }}
        ></div>
      </div>
    </div>
  );
};
};

const InsightItem = ({ title, desc, severity, theme }: any) => {
  const ringColor: any = {
    critical: "border-rose-500 text-rose-500 bg-rose-500/10",
    high: "border-amber-500 text-amber-500 bg-amber-500/10",
    medium: "border-indigo-500 text-indigo-500 bg-indigo-500/10",
  };

  return (
    <div className={clsx("flex gap-4 p-4 rounded-xl border transition-all cursor-pointer", theme === 'dark' ? "border-slate-800 hover:border-slate-700 bg-slate-800/30" : "border-gray-300 hover:border-gray-400 bg-gray-100")}>
      <div className={`mt-1 shrink-0 w-2 h-2 rounded-full ${severity === 'critical' ? 'bg-rose-500 shadow-rose-500/50 shadow-sm' : severity === 'high' ? 'bg-amber-500' : 'bg-indigo-500'}`}></div>
      <div>
        <h4 className={clsx("text-sm font-bold mb-1", theme === 'dark' ? "text-slate-100" : "text-black")}>{title}</h4>
        <p className={clsx("text-xs leading-relaxed line-clamp-2", theme === 'dark' ? "text-slate-500" : "text-gray-600")}>{desc}</p>
      </div>
    </div>
  );
};
};

export default Dashboard;
