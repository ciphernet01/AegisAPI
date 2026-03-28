import React from 'react';
import { Wrench } from 'lucide-react';
import { RemediationActions } from '@components/RemediationActions';
import { useTheme } from '@context/ThemeContext';
import { clsx } from 'clsx';

const Remediation: React.FC = () => {
  const { theme } = useTheme();

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-3">
            <Wrench className="text-blue-500" size={28} />
            <h1 className={clsx("text-3xl font-bold", theme === 'dark' ? "text-white" : "text-black")}>
              Remediation Workflows
            </h1>
          </div>
          <p className={clsx("mt-2", theme === 'dark' ? "text-slate-400" : "text-gray-600")}>
            Execute remediation actions for zombie and deprecated APIs with effort and cost estimation
          </p>
        </div>
      </div>

      {/* Remediation Actions Component */}
      <RemediationActions />
    </div>
  );
};

export default Remediation;
