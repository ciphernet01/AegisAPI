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
import { useTheme } from '@context/ThemeContext';

const ApiInventory: React.FC = () => {
  const { theme } = useTheme();
  const [apis, setApis] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");

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

  const filteredApis = apis.filter(api => 
    api.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    api.endpoint.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-8 animate-in slide-in-from-bottom-4 duration-500">
      <div className="flex items-center justify-between">
        <div>
          <h1 className={clsx("text-3xl font-bold mb-2", theme === 'dark' ? "text-white" : "text-black")}>API Inventory</h1>
          <p className={clsx(theme === 'dark' ? "text-slate-400" : "text-gray-600")}>Manage and monitor all discovered endpoints across repositories and registries.</p>
        </div>
        <div className="flex gap-3">
          <button className={clsx("px-4 py-2 rounded-xl transition-all border flex items-center gap-2 text-sm", theme === 'dark' ? "bg-slate-800 hover:bg-slate-700 text-slate-200 border-slate-700" : "bg-gray-200 hover:bg-gray-300 text-gray-800 border-gray-300")}>
            <Download size={16} /> Export
          </button>
          <button className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl transition-all shadow-lg shadow-indigo-600/20 flex items-center gap-2 text-sm font-semibold">
            Run Discovery
          </button>
        </div>
      </div>

      {/* Toolbar */}
      <div className={clsx("flex flex-col sm:flex-row gap-4 justify-between rounded-2xl p-4 shadow-xl border", theme === 'dark' ? "bg-slate-900 border-slate-800" : "bg-white border-gray-200")}>
        <div className="relative flex-1 max-w-md">
          <Search className={clsx("absolute left-3 top-1/2 -translate-y-1/2", theme === 'dark' ? "text-slate-500" : "text-gray-400")} size={18} />
          <input 
            type="text" 
            placeholder="Filter by name, endpoint or owner..." 
            className={clsx("w-full rounded-xl py-2 pl-10 pr-4 text-sm focus:outline-none focus:ring-2 border", theme === 'dark' ? "bg-slate-800/80 border-slate-700 text-white focus:ring-indigo-500/50" : "bg-gray-100 border-gray-300 text-black focus:ring-indigo-600/50")}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <div className="flex gap-2">
          <button className={clsx("px-4 py-2 rounded-xl transition-all border text-xs flex items-center gap-2", theme === 'dark' ? "bg-slate-800/50 hover:bg-slate-800 text-slate-400 hover:text-slate-200 border-slate-700" : "bg-gray-200/50 hover:bg-gray-200 text-gray-600 hover:text-gray-800 border-gray-300")}>
            <Filter size={14} /> Status
          </button>
          <button className={clsx("px-4 py-2 rounded-xl transition-all border text-xs flex items-center gap-2", theme === 'dark' ? "bg-slate-800/50 hover:bg-slate-800 text-slate-400 hover:text-slate-200 border-slate-700" : "bg-gray-200/50 hover:bg-gray-200 text-gray-600 hover:text-gray-800 border-gray-300")}>
            <ArrowUpDown size={14} /> Risk Score
          </button>
        </div>
      </div>

      {/* Table */}
      <div className={clsx("rounded-2xl overflow-hidden shadow-2xl border", theme === 'dark' ? "bg-slate-900 border-slate-800" : "bg-white border-gray-200")}>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className={clsx("border-b", theme === 'dark' ? "bg-slate-800/30 border-slate-800" : "bg-gray-100 border-gray-300")}>
                <th className={clsx("px-6 py-4 text-xs font-bold uppercase tracking-widest", theme === 'dark' ? "text-slate-500" : "text-gray-600")}>API Name & Endpoint</th>
                <th className={clsx("px-6 py-4 text-xs font-bold uppercase tracking-widest", theme === 'dark' ? "text-slate-500" : "text-gray-600")}>Method</th>
                <th className={clsx("px-6 py-4 text-xs font-bold uppercase tracking-widest text-center", theme === 'dark' ? "text-slate-500" : "text-gray-600")}>Security</th>
                <th className={clsx("px-6 py-4 text-xs font-bold uppercase tracking-widest", theme === 'dark' ? "text-slate-500" : "text-gray-600")}>Risk Score</th>
                <th className={clsx("px-6 py-4 text-xs font-bold uppercase tracking-widest", theme === 'dark' ? "text-slate-500" : "text-gray-600")}>Status</th>
                <th className={clsx("px-6 py-4 text-xs font-bold uppercase tracking-widest text-right", theme === 'dark' ? "text-slate-500" : "text-gray-600")}>Actions</th>
              </tr>
            </thead>
            <tbody className={clsx("border-t", theme === 'dark' ? "divide-y divide-slate-800 bg-slate-900/40" : "divide-y divide-gray-200 bg-white/40")}>
              {loading ? (
                <tr>
                  <td colSpan={6} className={clsx("px-6 py-12 text-center", theme === 'dark' ? "text-slate-500" : "text-gray-600")}>Scanning inventory...</td>
                </tr>
              ) : filteredApis.length === 0 ? (
                <tr>
                  <td colSpan={6} className={clsx("px-6 py-12 text-center", theme === 'dark' ? "text-slate-500" : "text-gray-600")}>No APIs found matching your criteria.</td>
                </tr>
              ) : (
                filteredApis.map((api) => (
                  <tr key={api.id} className={clsx("transition-colors group", theme === 'dark' ? "hover:bg-slate-800/30" : "hover:bg-gray-100")}>
                    <td className="px-6 py-5">
                      <div className="flex flex-col">
                        <span className={clsx("font-semibold transition-colors capitalize", theme === 'dark' ? "text-slate-200 group-hover:text-white" : "text-gray-900")}>{api.name.replace(/-/g, ' ')}</span>
                        <span className={clsx("text-[10px] font-mono tracking-tight mt-1", theme === 'dark' ? "text-slate-500" : "text-gray-500")}>{api.endpoint}</span>
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
                         <div className={clsx("p-1.5 rounded-full", api.is_documented ? "bg-emerald-500/10 text-emerald-500" : theme === 'dark' ? "bg-slate-800 text-slate-600" : "bg-gray-300 text-gray-600")}>
                           <Tag size={12} />
                         </div>
                         <div className={clsx("p-1.5 rounded-full", api.risk_score < 40 ? "bg-emerald-500/10 text-emerald-500" : "bg-rose-500/10 text-rose-500")}>
                           {api.risk_score < 40 ? <ShieldCheck size={12} /> : <ShieldAlert size={12} />}
                         </div>
                      </div>
                    </td>
                    <td className="px-6 py-5">
                      <div className="flex items-center gap-3">
                        <div className={clsx("flex-1 h-1.5 w-16 rounded-full overflow-hidden", theme === 'dark' ? "bg-slate-800" : "bg-gray-300")}>
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
                      <button className={clsx("p-2 rounded-lg transition-all", theme === 'dark' ? "text-slate-500 hover:text-white hover:bg-slate-700" : "text-gray-600 hover:text-black hover:bg-gray-200")}>
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
    </div>
  );
};

export default ApiInventory;
