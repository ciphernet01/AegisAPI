import React from 'react';
import { clsx } from 'clsx';

interface ChartCardProps {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  actions?: React.ReactNode;
  className?: string;
}

export const ChartCard: React.FC<ChartCardProps> = ({
  title,
  subtitle,
  children,
  actions,
  className
}) => {
  return (
    <div className={clsx(
      'relative overflow-hidden rounded-2xl backdrop-blur-xl transition-all duration-300',
      'bg-gradient-to-br from-slate-900/60 to-slate-900/40 border border-slate-800/50',
      'hover:border-slate-700 hover:shadow-[0_0_30px_rgba(99,102,241,0.1)] hover:from-slate-900/70 hover:to-slate-900/50',
      'shadow-card',
      className
    )}>
      {/* Gradient decoration line */}
      <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-indigo-500/30 to-transparent" />

      <div className="relative z-10 p-6">
        <div className="flex items-start justify-between mb-6">
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-white">{title}</h3>
            {subtitle && (
              <p className="text-sm text-slate-400 mt-1 font-medium">{subtitle}</p>
            )}
          </div>
          {actions && (
            <div className="flex gap-2 ml-4">
              {actions}
            </div>
          )}
        </div>
        {children}
      </div>
    </div>
  );
};
