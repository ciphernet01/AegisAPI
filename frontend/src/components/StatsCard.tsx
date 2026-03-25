import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';
import { clsx } from 'clsx';

interface StatsCardProps {
  label: string;
  value: number | string;
  icon: React.ReactNode;
  trend?: string;
  trendDirection?: 'up' | 'down' | 'neutral';
  color: 'indigo' | 'emerald' | 'rose' | 'amber' | 'cyan';
  onClick?: () => void;
}

export const StatsCard: React.FC<StatsCardProps> = ({
  label,
  value,
  icon,
  trend,
  trendDirection = 'neutral',
  color,
  onClick
}) => {
  const colorClasses = {
    indigo: 'from-indigo-500/10 to-indigo-600/5 border-indigo-500/20',
    emerald: 'from-emerald-500/10 to-emerald-600/5 border-emerald-500/20',
    rose: 'from-rose-500/10 to-rose-600/5 border-rose-500/20',
    amber: 'from-amber-500/10 to-amber-600/5 border-amber-500/20',
    cyan: 'from-cyan-500/10 to-cyan-600/5 border-cyan-500/20',
  };

  const trendColors = {
    up: 'text-emerald-500',
    down: 'text-rose-500',
    neutral: 'text-slate-400'
  };

  return (
    <div
      onClick={onClick}
      className={clsx(
        'relative overflow-hidden rounded-2xl p-6 transition-all duration-300 cursor-pointer',
        'bg-gradient-to-br border backdrop-blur-xl',
        'hover:shadow-lg hover:scale-105',
        colorClasses[color],
        'group'
      )}
    >
      {/* Background glow effect */}
      <div className="absolute inset-0 bg-gradient-to-br opacity-0 group-hover:opacity-10 transition-opacity" />

      <div className="relative z-10 flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-slate-400 mb-2">{label}</p>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-bold text-white font-mono">
              {typeof value === 'number' ? value.toLocaleString() : value}
            </span>
          </div>
          {trend && (
            <div className={clsx('mt-4 flex items-center gap-1 text-sm font-medium', trendColors[trendDirection])}>
              {trendDirection === 'up' && <TrendingUp size={16} />}
              {trendDirection === 'down' && <TrendingDown size={16} />}
              <span>{trend}</span>
            </div>
          )}
        </div>
        <div className="text-slate-500 group-hover:text-slate-400 transition-colors ml-4">
          {icon}
        </div>
      </div>
    </div>
  );
};
