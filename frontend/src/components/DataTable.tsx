import React, { useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';
import { clsx } from 'clsx';

interface Column<T> {
  key: keyof T | string;
  label: string;
  render?: (value: any, row: T) => React.ReactNode;
  sortable?: boolean;
  width?: string;
}

interface DataTableProps<T> {
  columns: Column<T>[];
  data: T[];
  loading?: boolean;
  emptyMessage?: string;
  onRowClick?: (row: T) => void;
}

export function DataTable<T extends { id?: string | number }>(
  {
    columns,
    data,
    loading,
    emptyMessage = 'No data available',
    onRowClick
  }: DataTableProps<T>
) {
  const [sortKey, setSortKey] = useState<string | null>(null);
  const [sortDir, setSortDir] = useState<'asc' | 'desc'>('asc');

  const handleSort = (key: string) => {
    if (sortKey === key) {
      setSortDir(sortDir === 'asc' ? 'desc' : 'asc');
    } else {
      setSortKey(key);
      setSortDir('asc');
    }
  };

  return (
    <div className="overflow-x-auto rounded-lg border border-slate-800">
      <table className="w-full">
        <thead>
          <tr className="border-b border-slate-800 bg-slate-900/50">
            {columns.map((col) => (
              <th
                key={String(col.key)}
                className={clsx(
                  'px-6 py-4 text-left text-sm font-semibold text-slate-300',
                  col.width,
                  col.sortable && 'cursor-pointer hover:text-slate-200'
                )}
                onClick={() => col.sortable && handleSort(String(col.key))}
              >
                <div className="flex items-center gap-2">
                  {col.label}
                  {col.sortable && sortKey === String(col.key) && (
                    <div>{sortDir === 'asc' ? <ChevronUp size={16} /> : <ChevronDown size={16} />}</div>
                  )}
                </div>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {loading ? (
            <tr>
              <td colSpan={columns.length} className="px-6 py-12 text-center text-slate-400">
                Loading...
              </td>
            </tr>
          ) : data.length === 0 ? (
            <tr>
              <td colSpan={columns.length} className="px-6 py-12 text-center text-slate-400">
                {emptyMessage}
              </td>
            </tr>
          ) : (
            data.map((row, idx) => (
              <tr
                key={(row as any).id || idx}
                onClick={() => onRowClick?.(row)}
                className="border-b border-slate-800 hover:bg-slate-800/30 transition-colors cursor-pointer"
              >
                {columns.map((col) => (
                  <td key={String(col.key)} className="px-6 py-4 text-sm text-slate-300">
                    {col.render
                      ? col.render((row as any)[col.key as keyof T], row)
                      : String((row as any)[col.key as keyof T] || '-')}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
