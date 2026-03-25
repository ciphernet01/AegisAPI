import React from 'react';
import { 
  Wrench, 
  Clock, 
  CheckCircle2, 
  Play, 
  Trash2, 
  Plus,
  ArrowRight,
  ShieldAlert
} from 'lucide-react';
import { clsx } from 'clsx';

const Remediations: React.FC = () => {
  const workflows = [
    { id: 1, target: "Orphaned-Service-v1", action: "Decommission", status: "In Progress", progress: 65, initiated: "2024-01-20" },
    { id: 2, target: "Old-Billing-API", action: "Deprecate", status: "Proposed", progress: 0, initiated: "2024-01-22" },
    { id: 3, target: "Auth-Legacy-Fix", action: "Update Config", status: "Completed", progress: 100, initiated: "2024-01-15" },
  ];

  return (
    <div className="space-y-8 animate-in zoom-in-95 duration-500">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Remediation & Decommissioning</h1>
          <p className="text-slate-400">Track and manage the lifecycle of vulnerable or outdated API services.</p>
        </div>
        <button className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl transition-all shadow-lg shadow-indigo-600/20 flex items-center gap-2 text-sm font-semibold">
          <Plus size={18} /> New Workflow
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatusOverviewCard label="Proposed" count={2} color="slate" />
        <StatusOverviewCard label="In Execution" count={1} color="indigo" />
        <StatusOverviewCard label="Completed" count={14} color="emerald" />
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
        <div className="p-6 border-b border-slate-800 bg-slate-800/30">
          <h3 className="font-bold text-white flex items-center gap-2">
            <Clock size={20} className="text-indigo-400" />
            Active Workflows
          </h3>
        </div>

        <div className="divide-y divide-slate-800">
          {workflows.map((wf) => (
            <div key={wf.id} className="p-6 hover:bg-slate-800/30 transition-all group">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
                <div className="flex gap-4">
                  <div className={clsx(
                    "w-12 h-12 rounded-xl flex items-center justify-center shrink-0 border",
                    wf.status === 'In Progress' ? 'bg-indigo-500/10 border-indigo-500/20 text-indigo-400 shadow-indigo-500/10 shadow-lg' :
                    wf.status === 'Completed' ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-500' :
                    'bg-slate-800 border-slate-700 text-slate-500'
                  )}>
                    {wf.status === 'Completed' ? <CheckCircle2 size={24} /> : <Wrench size={24} />}
                  </div>
                  <div>
                    <h4 className="font-bold text-slate-100 mb-1 flex items-center gap-2">
                       {wf.target}
                       {wf.status === 'In Progress' && <span className="flex h-2 w-2 rounded-full bg-indigo-500 animate-pulse"></span>}
                    </h4>
                    <div className="flex items-center gap-2 text-xs font-medium text-slate-500">
                      <span className="uppercase tracking-widest bg-slate-800 px-1.5 py-0.5 rounded text-[9px] text-slate-400">{wf.action}</span>
                      <span>•</span>
                      <span>Initiated {wf.initiated}</span>
                    </div>
                  </div>
                </div>

                <div className="flex-1 max-w-xs px-4">
                   <div className="flex justify-between text-[10px] font-bold text-slate-500 mb-1 uppercase tracking-wider">
                      <span>Progress</span>
                      <span>{wf.progress}%</span>
                   </div>
                   <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                      <div 
                        className={clsx(
                          "h-full rounded-full transition-all duration-1000",
                          wf.status === 'Completed' ? 'bg-emerald-500' : 'bg-indigo-500'
                        )}
                        style={{ width: `${wf.progress}%` }}
                      ></div>
                   </div>
                </div>

                <div className="flex items-center gap-3">
                  {wf.status === 'Proposed' && (
                    <button className="p-2 bg-emerald-500/10 text-emerald-500 hover:bg-emerald-500 hover:text-white rounded-lg transition-all border border-emerald-500/20">
                      <Play size={18} fill="currentColor" />
                    </button>
                  )}
                  <button className="p-2 text-slate-500 hover:text-rose-500 hover:bg-rose-500/10 rounded-lg transition-all">
                    <Trash2 size={18} />
                  </button>
                  <button className="p-2 text-slate-500 hover:text-white hover:bg-slate-800 rounded-lg transition-all">
                    <ArrowRight size={18} />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        <div className="p-4 bg-slate-900/50 text-center">
           <button className="text-xs font-bold text-slate-500 hover:text-indigo-400 transition-colors uppercase tracking-widest">
              View Historical Workflows
           </button>
        </div>
      </div>

      <div className="bg-rose-950/20 border border-rose-500/20 rounded-2xl p-6 flex flex-col md:flex-row items-center gap-6">
         <div className="p-4 bg-rose-500/10 rounded-2xl">
            <ShieldAlert size={32} className="text-rose-500" />
         </div>
         <div className="flex-1 text-center md:text-left">
            <h3 className="text-lg font-bold text-white mb-1">Zombie API Alert</h3>
            <p className="text-sm text-slate-400 leading-relaxed">The 'Legacy-Auth-Proxy' service has had 0 traffic for 90 days but remains active. Decommissioning is highly recommended.</p>
         </div>
         <button className="px-6 py-3 bg-rose-600 hover:bg-rose-500 text-white rounded-xl font-bold transition-all shadow-lg shadow-rose-600/20 whitespace-nowrap">
            Initiate Decommission
         </button>
      </div>
    </div>
  );
};

const StatusOverviewCard = ({ label, count, color }: any) => {
  const colorMap: any = {
    indigo: "border-indigo-500/20 bg-indigo-500/5 text-indigo-400",
    emerald: "border-emerald-500/20 bg-emerald-500/5 text-emerald-400",
    slate: "border-slate-800 bg-slate-800/20 text-slate-400",
  };

  return (
    <div className={clsx("p-6 rounded-2xl border flex flex-col items-center justify-center transition-all hover:scale-[1.03]", colorMap[color])}>
       <div className="text-4xl font-black mb-1 leading-none tracking-tight">{count}</div>
       <div className="text-[10px] font-bold uppercase tracking-[0.2em] opacity-80">{label}</div>
    </div>
  );
};

export default Remediations;
