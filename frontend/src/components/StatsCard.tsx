import React from 'react';
import { TrendingUp, TrendingDown, ArrowUpRight, ArrowDownRight } from 'lucide-react';
import { clsx } from 'clsx';

interface StatsCardProps {
  label: string;
  value: number | string;
  icon: React.ReactNode;
  trend?: string;
  trendDirection?: 'up' | 'down' | 'neutral';
  color: 'indigo' | 'emerald' | 'rose' | 'amber' | 'cyan';
  onClick?: () => void;
  change?: number;
}

export const StatsCard: React.FC<StatsCardProps> = ({
  label,
  value,
  icon,
  trend,
  trendDirection = 'neutral',
  color,
  onClick,
  change
}) => {
  const colorClasses = {
    indigo: {
      bg: 'from-indigo-500/15 to-indigo-600/5',
      border: 'border-indigo-500/30',
      icon: 'text-indigo-400',
      accent: 'bg-indigo-500/10',
      glow: 'group-hover:shadow-[0_0_30px_rgba(99,102,241,0.3)]'
    },
    emerald: {
      bg: 'from-emerald-500/15 to-emerald-600/5',
      border: 'border-emerald-500/30',
      icon: 'text-emerald-400',
      accent: 'bg-emerald-500/10',
      glow: 'group-hover:shadow-[0_0_30px_rgba(16,185,129,0.3)]'
    },
    rose: {
      bg: 'from-rose-500/15 to-rose-600/5',
      border: 'border-rose-500/30',
      icon: 'text-rose-400',
      accent: 'bg-rose-500/10',
      glow: 'group-hover:shadow-[0_0_30px_rgba(244,63,94,0.3)]'
    },
    amber: {
      bg: 'from-amber-500/15 to-amber-600/5',
      border: 'border-amber-500/30',
      icon: 'text-amber-400',
      accent: 'bg-amber-500/10',
      glow: 'group-hover:shadow-[0_0_30px_rgba(245,158,11,0.3)]'
    },
    cyan: {
      bg: 'from-cyan-500/15 to-cyan-600/5',
      border: 'border-cyan-500/30',
      icon: 'text-cyan-400',
      accent: 'bg-cyan-500/10',
      glow: 'group-hover:shadow-[0_0_30px_rgba(6,182,212,0.3)]'
    }
  };

  const trendColors = {
    up: 'text-emerald-400',
    down: 'text-rose-400',
    neutral: 'text-slate-500'
  };

  const colorScheme = colorClasses[color];

  return (
    <div
      onClick={onClick}
      className={clsx(
        'relative overflow-hidden rounded-2xl p-6 transition-all duration-300 cursor-pointer',
        'bg-gradient-to-br border backdrop-blur-xl',
        'hover:shadow-card-hover',
        colorScheme.bg,
        colorScheme.border,
        colorScheme.glow,
        'group'
      )}
    >
      {/* Animated gradient background */}
      <div className="absolute inset-0 overflow-hidden rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500">
        <div className={clsx(
          'absolute inset-0',
          colorScheme.accent,
          'opacity-0 group-hover:opacity-20 transition-opacity'
        )} />
      </div>

      {/* Top decorative line */}
      <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent group-hover:via-white/40 transition-all" />

      <div className="relative z-10">
        {/* Header with icon */}
        <div className="flex items-start justify-between mb-4">
          <div>
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">{label}</p>
          </div>
          <div className={clsx(
            'p-2.5 rounded-lg transition-all duration-300',
            colorScheme.accent,
            'group-hover:scale-110 group-hover:shadow-lg'
          )}>
            <div className={clsx(colorScheme.icon, 'group-hover:scale-110 transition-transform duration-300')}>
              {icon}
            </div>
          </div>
        </div>

        {/* Main value */}
        <div className="mb-4">
          <span className="text-4xl font-bold text-white font-mono tracking-tight">
            {typeof value === 'number' ? value.toLocaleString() : value}
          </span>
        </div>

        {/* Trend indicator */}
        {trend && (
          <div className="flex items-center justify-between">
            <div className={clsx('flex items-center gap-1.5 text-sm font-semibold', trendColors[trendDirection])}>
              {trendDirection === 'up' && <ArrowUpRight size={16} className="animate-pulse-subtle" />}
              {trendDirection === 'down' && <ArrowDownRight size={16} className="animate-pulse-subtle" />}
              <span>{trend}</span>
            </div>
            {change !== undefined && (
              <span className={clsx(
                'text-xs font-mono px-2 py-1 rounded-md transition-all',
                change >= 0
                  ? 'bg-emerald-500/10 text-emerald-400'
                  : 'bg-rose-500/10 text-rose-400'
              )}>
                {change >= 0 ? '+' : ''}{change}%
              </span>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
