import React from 'react';
import { clsx } from 'clsx';

type BadgeVariant = 'default' | 'success' | 'warning' | 'error' | 'info';

interface BadgeProps {
  variant?: BadgeVariant;
  children: React.ReactNode;
  icon?: React.ReactNode;
  size?: 'sm' | 'md';
}

const variantClasses: Record<BadgeVariant, string> = {
  default: 'bg-slate-900/50 text-slate-300 border-slate-700/50 hover:bg-slate-900/70 hover:border-slate-600',
  success: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30 hover:bg-emerald-500/25 hover:border-emerald-400',
  warning: 'bg-amber-500/15 text-amber-300 border-amber-500/30 hover:bg-amber-500/25 hover:border-amber-400',
  error: 'bg-rose-500/15 text-rose-300 border-rose-500/30 hover:bg-rose-500/25 hover:border-rose-400',
  info: 'bg-cyan-500/15 text-cyan-300 border-cyan-500/30 hover:bg-cyan-500/25 hover:border-cyan-400',
};

const sizeClasses = {
  sm: 'px-1.5 py-0.5 text-xs',
  md: 'px-2.5 py-1 text-xs'
};

export const Badge: React.FC<BadgeProps> = ({
  variant = 'default',
  children,
  icon,
  size = 'md'
}) => {
  return (
    <span className={clsx(
      'inline-flex items-center gap-1.5 rounded-full font-semibold border transition-all duration-200 cursor-default',
      variantClasses[variant],
      sizeClasses[size]
    )}>
      {icon && <span className="flex-shrink-0 flex items-center">{icon}</span>}
      <span className="font-medium">{children}</span>
    </span>
  );
};
