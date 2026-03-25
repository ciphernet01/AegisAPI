import React, { useEffect, useState } from 'react';
import { 
  Search, 
  Filter, 
  Download, 
  ArrowUpDown,
  ExternalLink,
  Tag,
  ShieldCheck,
  ShieldAlert
} from 'lucide-react';
import { apiService } from '@services/api';
import { clsx } from 'clsx';
import { Modal } from '@components/Modal';
import { Badge } from '@components/Badge';

const ApiInventory: React.FC = () => {
  const [apis, setApis] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'active' | 'deprecated' | 'orphaned' | 'zombie'>('all');
  const [sortByRisk, setSortByRisk] = useState(false);
  const [selectedApi, setSelectedApi] = useState<any | null>(null);

  useEffect(() => {
    const fetchApis = async () => {
      try {
        const response = await apiService.listApis();
        if (response.success) {
          setApis(response.data);
        }
      } catch (error) {
        console.error("Failed to fetch APIs:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchApis();
  }, []);

  const filteredApis = apis
    .filter((api) => {
      const matchesSearch =
        api.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        api.endpoint.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesStatus = statusFilter === 'all' ? true : api.status === statusFilter;
      return matchesSearch && matchesStatus;
    })
    .sort((a, b) => (sortByRisk ? b.risk_score - a.risk_score : 0));

  return (
    <div className="space-y-8 animate-in slide-in-from-bottom-4 duration-500">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">API Inventory</h1>
          <p className="text-slate-400">Manage and monitor all discovered endpoints across repositories and registries.</p>
        </div>
        <div className="flex gap-3">
          <button className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl transition-all border border-slate-700 flex items-center gap-2 text-sm">
            <Download size={16} /> Export
          </button>
          <button className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl transition-all shadow-lg shadow-indigo-600/20 flex items-center gap-2 text-sm font-semibold">
            Run Discovery
          </button>
        </div>
      </div>

      {/* Toolbar */}
      <div className="flex flex-col sm:flex-row gap-4 justify-between bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={18} />
          <input 
            type="text" 
            placeholder="Filter by name, endpoint or owner..." 
            className="w-full bg-slate-800/80 border border-slate-700 rounded-xl py-2 pl-10 pr-4 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setStatusFilter(statusFilter === 'all' ? 'active' : 'all')}
            className="px-4 py-2 bg-slate-800/50 hover:bg-slate-800 text-slate-400 hover:text-slate-200 rounded-xl transition-all border border-slate-700 text-xs flex items-center gap-2"
          >
            <Filter size={14} /> Status
          </button>
          <button
            onClick={() => setSortByRisk((prev) => !prev)}
            className="px-4 py-2 bg-slate-800/50 hover:bg-slate-800 text-slate-400 hover:text-slate-200 rounded-xl transition-all border border-slate-700 text-xs flex items-center gap-2"
          >
            <ArrowUpDown size={14} /> Risk Score
          </button>
        </div>
      </div>

      {/* Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-800/30 border-b border-slate-800">
                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-widest">API Name & Endpoint</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-widest">Method</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-widest text-center">Security</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-widest">Risk Score</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-widest">Status</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-widest text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 bg-slate-900/40">
              {loading ? (
                <tr>
                  <td colSpan={6} className="px-6 py-12 text-center text-slate-500">Scanning inventory...</td>
                </tr>
              ) : filteredApis.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-6 py-12 text-center text-slate-500">No APIs found matching your criteria.</td>
                </tr>
              ) : (
                filteredApis.map((api) => (
                  <tr key={api.id} onClick={() => setSelectedApi(api)} className="hover:bg-slate-800/30 transition-colors group cursor-pointer">
                    <td className="px-6 py-5">
                      <div className="flex flex-col">
                        <span className="text-slate-200 font-semibold group-hover:text-white transition-colors capitalize">{api.name.replace(/-/g, ' ')}</span>
                        <span className="text-[10px] text-slate-500 font-mono tracking-tight mt-1">{api.endpoint}</span>
                      </div>
                    </td>
                    <td className="px-6 py-5">
                      <span className={clsx(
                        "px-2.5 py-1 rounded-md text-[10px] font-bold tracking-widest",
                        api.method === 'GET' ? 'bg-emerald-500/10 text-emerald-500' :
                        api.method === 'POST' ? 'bg-indigo-500/10 text-indigo-500' :
                        'bg-amber-500/10 text-amber-500'
                      )}>
                        {api.method}
                      </span>
                    </td>
                    <td className="px-6 py-5">
                      <div className="flex justify-center gap-2">
                         <div className={clsx("p-1.5 rounded-full", api.is_documented ? "bg-emerald-500/10 text-emerald-500" : "bg-slate-800 text-slate-600")}>
                           <Tag size={12} />
                         </div>
                         <div className={clsx("p-1.5 rounded-full", api.risk_score < 40 ? "bg-emerald-500/10 text-emerald-500" : "bg-rose-500/10 text-rose-500")}>
                           {api.risk_score < 40 ? <ShieldCheck size={12} /> : <ShieldAlert size={12} />}
                         </div>
                      </div>
                    </td>
                    <td className="px-6 py-5">
                      <div className="flex items-center gap-3">
                        <div className="flex-1 h-1.5 w-16 bg-slate-800 rounded-full overflow-hidden">
                           <div 
                             className={clsx(
                               "h-full rounded-full transition-all duration-1000",
                               api.risk_score < 40 ? "bg-emerald-500" : api.risk_score < 70 ? "bg-amber-500" : "bg-rose-500"
                             )}
                             style={{ width: `${api.risk_score}%` }}
                           ></div>
                        </div>
                        <span className={clsx(
                          "text-xs font-bold",
                          api.risk_score < 40 ? "text-emerald-500" : api.risk_score < 70 ? "text-amber-500" : "text-rose-500"
                        )}>{api.risk_score}</span>
                      </div>
                    </td>
                    <td className="px-6 py-5">
                      <span className={clsx(
                        "flex items-center gap-2 text-xs font-semibold",
                        api.status === 'active' ? 'text-emerald-500' : api.status === 'zombie' ? 'text-rose-500' : 'text-slate-400'
                      )}>
                        <div className={clsx("w-1.5 h-1.5 rounded-full", api.status === 'active' ? 'bg-emerald-500' : 'bg-rose-500')}></div>
                        <span className="capitalize">{api.status}</span>
                      </span>
                    </td>
                    <td className="px-6 py-5 text-right">
                      <button onClick={() => setSelectedApi(api)} className="p-2 text-slate-500 hover:text-white hover:bg-slate-700 rounded-lg transition-all">
                        <ExternalLink size={18} />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      <Modal
        isOpen={!!selectedApi}
        onClose={() => setSelectedApi(null)}
        title={selectedApi ? `${selectedApi.name} Details` : 'API Details'}
        size="lg"
      >
        {selectedApi && (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <p className="text-xs text-slate-500">Endpoint</p>
                <p className="text-sm text-slate-200 font-mono">{selectedApi.endpoint}</p>
              </div>
              <div>
                <p className="text-xs text-slate-500">Method</p>
                <p className="text-sm text-slate-200">{selectedApi.method}</p>
              </div>
              <div>
                <p className="text-xs text-slate-500">Risk Score</p>
                <p className="text-sm text-slate-200">{selectedApi.risk_score}</p>
              </div>
              <div>
                <p className="text-xs text-slate-500">Status</p>
                <Badge variant={selectedApi.status === 'active' ? 'success' : selectedApi.status === 'zombie' ? 'error' : 'warning'}>
                  {selectedApi.status}
                </Badge>
              </div>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default ApiInventory;
