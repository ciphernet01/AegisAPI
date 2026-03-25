import React from 'react';
import { 
  Settings as SettingsIcon, 
  Shield, 
  Database, 
  Github, 
  Bell, 
  Eye, 
  Lock,
  RefreshCw,
  Save
} from 'lucide-react';

const Settings: React.FC = () => {
  return (
    <div className="space-y-8 max-w-4xl animate-in fade-in duration-500">
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Platform Settings</h1>
        <p className="text-slate-400">Configure discovery sources, security thresholds, and system preferences.</p>
      </div>

      <div className="space-y-6">
        {/* Discovery Sources */}
        <section className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
          <h3 className="text-lg font-bold text-white mb-6 flex items-center gap-2">
            <RefreshCw size={20} className="text-indigo-400" />
            Discovery Sources
          </h3>
          <div className="space-y-4">
            <SourceToggle 
               icon={<Github size={18} />} 
               name="GitHub Integration" 
               desc="Scan organization repositories for API definitions and routes." 
               enabled={true} 
            />
            <SourceToggle 
               icon={<Database size={18} />} 
               name="AWS API Gateway" 
               desc="Automatically discover endpoints from cloud infrastructure." 
               enabled={false} 
            />
            <SourceToggle 
               icon={<Shield size={18} />} 
               name="Kubernetes Ingress" 
               desc="Monitor cluster ingress for exposed services." 
               enabled={true} 
            />
          </div>
        </section>

        {/* Security Thresholds */}
        <section className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
          <h3 className="text-lg font-bold text-white mb-6 flex items-center gap-2">
            <Lock size={20} className="text-rose-400" />
            Security Assessment Thresholds
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-4">
             <div>
                <label className="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">Zombie Threshold (Days)</label>
                <input type="number" defaultValue={90} className="w-full bg-slate-800/50 border border-slate-700 rounded-xl px-4 py-2 text-white focus:outline-none focus:ring-1 focus:ring-rose-500" />
                <p className="mt-2 text-[10px] text-slate-500 italic">APIs with zero traffic for this duration are flagged as zombie.</p>
             </div>
             <div>
                <label className="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">Default Risk Level</label>
                <select className="w-full bg-slate-800/50 border border-slate-700 rounded-xl px-4 py-2 text-white focus:outline-none focus:ring-1 focus:ring-rose-500 appearance-none">
                   <option>High</option>
                   <option selected>Medium</option>
                   <option>Low</option>
                </select>
             </div>
          </div>
        </section>

        <div className="flex justify-end gap-4 mt-8">
           <button className="px-6 py-3 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl font-bold transition-all text-sm">
              Discard Changes
           </button>
           <button className="px-8 py-3 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl font-bold transition-all shadow-lg shadow-indigo-600/20 flex items-center gap-2 text-sm">
              <Save size={18} /> Save Configurations
           </button>
        </div>
      </div>
    </div>
  );
};

const SourceToggle = ({ icon, name, desc, enabled }: any) => {
  return (
    <div className="flex items-center justify-between p-4 rounded-xl border border-slate-800 bg-slate-800/30 hover:border-slate-700 transition-all">
       <div className="flex gap-4">
          <div className="w-10 h-10 rounded-lg bg-slate-800 flex items-center justify-center text-slate-400">{icon}</div>
          <div>
             <h4 className="text-sm font-bold text-slate-200">{name}</h4>
             <p className="text-xs text-slate-500 leading-relaxed max-w-md">{desc}</p>
          </div>
       </div>
       <div className={`w-12 h-6 rounded-full p-1 cursor-pointer transition-all duration-300 ${enabled ? 'bg-indigo-600' : 'bg-slate-700'}`}>
          <div className={`w-4 h-4 bg-white rounded-full shadow-md transition-all duration-300 ${enabled ? 'translate-x-6' : 'translate-x-0'}`}></div>
       </div>
    </div>
  );
};

export default Settings;
