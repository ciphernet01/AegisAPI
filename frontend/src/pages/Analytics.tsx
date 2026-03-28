import React from 'react';
import { TrendingUp } from 'lucide-react';
import { AnalyticsDashboard } from '@components/AnalyticsDashboard';
import { useTheme } from '@context/ThemeContext';
import { clsx } from 'clsx';

const Analytics: React.FC = () => {
  const { theme } = useTheme();

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-3">
            <TrendingUp className="text-emerald-500" size={28} />
            <h1 className={clsx("text-3xl font-bold", theme === 'dark' ? "text-white" : "text-black")}>
              Analytics & Monitoring
            </h1>
          </div>
          <p className={clsx("mt-2", theme === 'dark' ? "text-slate-400" : "text-gray-600")}>
            Monitor system health, track trends, and manage alerts for your API platform
          </p>
        </div>
      </div>

      {/* Analytics Dashboard Component */}
      <AnalyticsDashboard />
    </div>
  );
};

export default Analytics;
