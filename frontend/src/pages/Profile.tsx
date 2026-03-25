import React, { useEffect, useState } from 'react';
import { RefreshCcw, UserCircle2, Database, Clock4 } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { apiService } from '@services/api';
import type { DatabaseHistoryEntry } from '@/types/auth';
import { Badge } from '@components/Badge';

const Profile: React.FC = () => {
  const { user } = useAuth();
  const [history, setHistory] = useState<DatabaseHistoryEntry[]>([]);
  const [loading, setLoading] = useState(false);

  const loadHistory = async () => {
    setLoading(true);
    try {
      const rows = await apiService.getDatabaseHistory();
      setHistory(rows);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  return (
    <div className="space-y-6 animate-fade-up">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Profile</h1>
          <p className="text-slate-400 mt-1">Account details and database activity history.</p>
        </div>
        <button
          onClick={loadHistory}
          className="px-4 py-2 rounded-xl border border-slate-700 bg-slate-900 hover:bg-slate-800 text-slate-200 text-sm flex items-center gap-2"
        >
          <RefreshCcw size={16} className={loading ? 'animate-spin' : ''} /> Refresh History
        </button>
      </div>

      <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="md:col-span-2 rounded-2xl border border-slate-800 bg-slate-900/70 p-5">
          <div className="flex items-center gap-3 mb-4">
            <UserCircle2 className="text-indigo-400" size={24} />
            <h2 className="text-lg font-semibold text-white">User Information</h2>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
            <div>
              <p className="text-slate-500">Name</p>
              <p className="text-slate-200">{user?.name ?? 'N/A'}</p>
            </div>
            <div>
              <p className="text-slate-500">Email</p>
              <p className="text-slate-200">{user?.email ?? 'N/A'}</p>
            </div>
            <div>
              <p className="text-slate-500">Role</p>
              <p className="text-slate-200">{user?.role ?? 'N/A'}</p>
            </div>
            <div>
              <p className="text-slate-500">Session Status</p>
              <Badge variant="success">Authenticated</Badge>
            </div>
          </div>
        </div>

        <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-5">
          <div className="flex items-center gap-2 mb-3">
            <Database className="text-cyan-400" size={20} />
            <h3 className="text-base font-semibold text-white">History Summary</h3>
          </div>
          <p className="text-3xl font-bold text-white">{history.length}</p>
          <p className="text-xs text-slate-500 mt-1">Recent database actions</p>
        </div>
      </section>

      <section className="rounded-2xl border border-slate-800 bg-slate-900/70 overflow-hidden">
        <div className="px-5 py-4 border-b border-slate-800 flex items-center gap-2">
          <Clock4 className="text-indigo-400" size={18} />
          <h2 className="text-base font-semibold text-white">Database History</h2>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-slate-950/50 text-slate-400">
                <th className="text-left px-5 py-3">Timestamp</th>
                <th className="text-left px-5 py-3">Action</th>
                <th className="text-left px-5 py-3">Table</th>
                <th className="text-left px-5 py-3">Rows</th>
                <th className="text-left px-5 py-3">Status</th>
                <th className="text-left px-5 py-3">Source IP</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan={6} className="px-5 py-6 text-center text-slate-400">Loading history...</td>
                </tr>
              ) : history.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-5 py-6 text-center text-slate-400">No history available.</td>
                </tr>
              ) : (
                history.map((item) => (
                  <tr key={item.id} className="border-t border-slate-800 hover:bg-slate-800/40 transition-colors">
                    <td className="px-5 py-3 text-slate-300">{new Date(item.timestamp).toLocaleString()}</td>
                    <td className="px-5 py-3 text-slate-200 font-medium">{item.action}</td>
                    <td className="px-5 py-3 text-slate-300">{item.table}</td>
                    <td className="px-5 py-3 text-slate-300">{item.rowsAffected}</td>
                    <td className="px-5 py-3">
                      <Badge variant={item.status === 'success' ? 'success' : 'error'}>
                        {item.status}
                      </Badge>
                    </td>
                    <td className="px-5 py-3 text-slate-400">{item.sourceIp}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
};

export default Profile;
