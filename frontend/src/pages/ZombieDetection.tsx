import React from 'react';
import { Zap } from 'lucide-react';
import { ZombieDetectionDashboard } from '@components/ZombieDetectionDashboard';
import { useTheme } from '@context/ThemeContext';
import { clsx } from 'clsx';

const ZombieDetection: React.FC = () => {
  const { theme } = useTheme();

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-3">
            <Zap className="text-rose-500" size={28} />
            <h1 className={clsx("text-3xl font-bold", theme === 'dark' ? "text-white" : "text-black")}>
              Zombie API Detection
            </h1>
          </div>
          <p className={clsx("mt-2", theme === 'dark' ? "text-slate-400" : "text-gray-600")}>
            Detect and monitor inactive, deprecated, and forgotten APIs in your infrastructure
          </p>
        </div>
      </div>

      {/* Zombie Detection Dashboard */}
      <ZombieDetectionDashboard />
    </div>
  );
};

export default ZombieDetection;
