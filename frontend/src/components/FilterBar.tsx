import React, { useState } from 'react';
import { Filter, Download, Calendar, ChevronDown } from 'lucide-react';
import { clsx } from 'clsx';

interface FilterBarProps {
  onTimeRangeChange?: (range: string) => void;
  onExport?: (format: 'csv' | 'pdf' | 'json') => void;
  selectedTimeRange?: string;
}

export const FilterBar: React.FC<FilterBarProps> = ({
  onTimeRangeChange,
  onExport,
  selectedTimeRange = '7d'
}) => {
  const [isTimeRangeOpen, setIsTimeRangeOpen] = useState(false);
  const [isExportOpen, setIsExportOpen] = useState(false);

  const timeRanges = [
    { label: 'Last 24 Hours', value: '24h' },
    { label: 'Last 7 Days', value: '7d' },
    { label: 'Last 30 Days', value: '30d' },
    { label: 'Last 90 Days', value: '90d' },
    { label: 'This Year', value: 'year' }
  ];

  const exportFormats = [
    { label: 'Export as CSV', format: 'csv' as const },
    { label: 'Export as PDF', format: 'pdf' as const },
    { label: 'Export as JSON', format: 'json' as const }
  ];

  const getTimeRangeLabel = () => {
    return timeRanges.find(r => r.value === selectedTimeRange)?.label || 'Last 7 Days';
  };

  return (
    <div className="flex flex-col sm:flex-row gap-3">
      {/* Time Range Selector */}
      <div className="relative">
        <button
          onClick={() => {
            setIsTimeRangeOpen(!isTimeRangeOpen);
            setIsExportOpen(false);
          }}
          className={clsx(
            'flex items-center gap-2 px-4 py-2.5 rounded-xl font-medium',
            'bg-slate-900/50 border border-slate-800 text-slate-200',
            'hover:border-slate-700 hover:bg-slate-900/70 transition-all',
            'focus:outline-none focus:ring-2 focus:ring-indigo-500/50'
          )}
        >
          <Calendar size={16} />
          <span className="hidden sm:inline">{getTimeRangeLabel()}</span>
          <span className="sm:hidden">{selectedTimeRange}</span>
          <ChevronDown size={14} />
        </button>

        {isTimeRangeOpen && (
          <div className="absolute top-full left-0 mt-2 w-48 bg-slate-900 border border-slate-800 rounded-xl shadow-xl z-20 overflow-hidden">
            {timeRanges.map((range) => (
              <button
                key={range.value}
                onClick={() => {
                  onTimeRangeChange?.(range.value);
                  setIsTimeRangeOpen(false);
                }}
                className={clsx(
                  'w-full px-4 py-3 text-left text-sm font-medium transition-all',
                  'hover:bg-indigo-600/20 hover:border-l-2 hover:border-indigo-500',
                  selectedTimeRange === range.value
                    ? 'bg-indigo-600/30 text-indigo-300 border-l-2 border-indigo-500'
                    : 'text-slate-300'
                )}
              >
                {range.label}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Export Button */}
      <div className="relative">
        <button
          onClick={() => {
            setIsExportOpen(!isExportOpen);
            setIsTimeRangeOpen(false);
          }}
          className={clsx(
            'flex items-center gap-2 px-4 py-2.5 rounded-xl font-medium',
            'bg-gradient-to-r from-indigo-600/80 to-indigo-600 hover:from-indigo-600 hover:to-indigo-500',
            'text-white transition-all shadow-lg hover:shadow-indigo-600/50',
            'focus:outline-none focus:ring-2 focus:ring-indigo-500/50'
          )}
        >
          <Download size={16} />
          <span>Export</span>
          <ChevronDown size={14} />
        </button>

        {isExportOpen && (
          <div className="absolute top-full right-0 mt-2 w-48 bg-slate-900 border border-slate-800 rounded-xl shadow-xl z-20 overflow-hidden">
            {exportFormats.map((item) => (
              <button
                key={item.format}
                onClick={() => {
                  onExport?.(item.format);
                  setIsExportOpen(false);
                }}
                className={clsx(
                  'w-full px-4 py-3 text-left text-sm font-medium transition-all',
                  'hover:bg-indigo-600/20 text-slate-300'
                )}
              >
                {item.label}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Filter Indicator */}
      <button
        className={clsx(
          'flex items-center gap-2 px-4 py-2.5 rounded-xl font-medium',
          'bg-slate-900/50 border border-slate-800 text-slate-300',
          'hover:border-slate-700 hover:bg-slate-900/70 transition-all',
          'focus:outline-none focus:ring-2 focus:ring-indigo-500/50'
        )}
      >
        <Filter size={16} />
        <span className="hidden sm:inline">More Filters</span>
        <span className="sm:hidden">Filter</span>
      </button>
    </div>
  );
};
