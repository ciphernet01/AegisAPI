import React from 'react';
import { clsx } from 'clsx';
import { ArrowRight, AlertCircle, Zap, Star } from 'lucide-react';

interface SummaryCardProps {
  title: string;
  value: string;
  description: string;
  icon: React.ReactNode;
  variant?: 'default' | 'warning' | 'success' | 'info';
  actionText?: string;
  onAction?: () => void;
}

export const SummaryCard: React.FC<SummaryCardProps> = ({
  title,
  value,
  description,
  icon,
  variant = 'default',
  actionText,
  onAction
}) => {
  const variantStyles = {
    default: {
      bg: 'from-slate-800/50 to-slate-900/50 border-slate-700',
      iconBg: 'bg-slate-700/30',
      iconColor: 'text-slate-400'
    },
    warning: {
      bg: 'from-amber-900/20 to-amber-950/20 border-amber-700/40',
      iconBg: 'bg-amber-700/20',
      iconColor: 'text-amber-400'
    },
    success: {
      bg: 'from-emerald-900/20 to-emerald-950/20 border-emerald-700/40',
      iconBg: 'bg-emerald-700/20',
      iconColor: 'text-emerald-400'
    },
    info: {
      bg: 'from-indigo-900/20 to-indigo-950/20 border-indigo-700/40',
      iconBg: 'bg-indigo-700/20',
      iconColor: 'text-indigo-400'
    }
  };

  const style = variantStyles[variant];

  return (
    <div className={clsx(
      'relative overflow-hidden rounded-xl p-5 backdrop-blur-sm',
      `bg-gradient-to-br ${style.bg} border`,
      'hover:shadow-lg transition-all duration-300 group'
    )}>
      {/* Top accent line */}
      <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-white/10 to-transparent" />

      <div className="relative z-10 flex items-start gap-4">
        <div className={clsx('p-2.5 rounded-lg transition-all', style.iconBg)}>
          <div className={style.iconColor}>
            {icon}
          </div>
        </div>

        <div className="flex-1">
          <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">
            {title}
          </p>
          <p className="text-2xl font-bold text-white mb-1">
            {value}
          </p>
          <p className="text-sm text-slate-400 leading-tight">
            {description}
          </p>

          {actionText && (
            <button
              onClick={onAction}
              className="mt-3 inline-flex items-center gap-1 text-xs font-semibold text-indigo-400 hover:text-indigo-300 transition-colors group"
            >
              {actionText}
              <ArrowRight size={12} className="group-hover:translate-x-0.5 transition-transform" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
