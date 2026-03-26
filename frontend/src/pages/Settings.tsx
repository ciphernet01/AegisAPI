import React from 'react';
import { 
   Shield, 
   Database, 
   Github, 
   Lock,
   RefreshCw,
   Save
} from 'lucide-react';
import { clsx } from 'clsx';
import { useTheme } from '@context/ThemeContext';

const Settings: React.FC = () => {
  const { theme } = useTheme();
  return (
    <div className="space-y-8 max-w-4xl animate-in fade-in duration-500">
      <div>
        <h1 className={clsx("text-3xl font-bold mb-2", theme === 'dark' ? "text-white" : "text-black")}>Platform Settings</h1>
        <p className={clsx(theme === 'dark' ? "text-slate-400" : "text-gray-600")}>Configure discovery sources, security thresholds, and system preferences.</p>
      </div>

      <div className="space-y-6">
        {/* Discovery Sources */}
        <section className={clsx("rounded-2xl p-6 shadow-xl border", theme === 'dark' ? "bg-slate-900 border-slate-800" : "bg-white border-gray-200")}>
          <h3 className={clsx("text-lg font-bold mb-6 flex items-center gap-2", theme === 'dark' ? "text-white" : "text-black")}>
            <RefreshCw size={20} className="text-indigo-400" />
            Discovery Sources
          </h3>
          <div className="space-y-4">
            <SourceToggle 
               icon={<Github size={18} />} 
               name="GitHub Integration" 
               desc="Scan organization repositories for API definitions and routes." 
               enabled={true}
               theme={theme}
            />
            <SourceToggle 
               icon={<Database size={18} />} 
               name="AWS API Gateway" 
               desc="Automatically discover endpoints from cloud infrastructure." 
               enabled={false}
               theme={theme}
            />
            <SourceToggle 
               icon={<Shield size={18} />} 
               name="Kubernetes Ingress" 
               desc="Monitor cluster ingress for exposed services." 
               enabled={true}
               theme={theme}
            />
          </div>
        </section>

        {/* Security Thresholds */}
        <section className={clsx("rounded-2xl p-6 shadow-xl border", theme === 'dark' ? "bg-slate-900 border-slate-800" : "bg-white border-gray-200")}>
          <h3 className={clsx("text-lg font-bold mb-6 flex items-center gap-2", theme === 'dark' ? "text-white" : "text-black")}>
            <Lock size={20} className="text-rose-400" />
            Security Assessment Thresholds
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-4">
             <div>
                <label className={clsx("block text-xs font-bold uppercase tracking-widest mb-2", theme === 'dark' ? "text-slate-500" : "text-gray-600")}>Zombie Threshold (Days)</label>
                <input type="number" defaultValue={90} className={clsx("w-full rounded-xl px-4 py-2 focus:outline-none focus:ring-1 border", theme === 'dark' ? "bg-slate-800/50 border-slate-700 text-white focus:ring-rose-500" : "bg-gray-100 border-gray-300 text-black focus:ring-rose-600")} />
                <p className={clsx("mt-2 text-[10px] italic", theme === 'dark' ? "text-slate-500" : "text-gray-600")}>APIs with zero traffic for this duration are flagged as zombie.</p>
             </div>
             <div>
                <label className={clsx("block text-xs font-bold uppercase tracking-widest mb-2", theme === 'dark' ? "text-slate-500" : "text-gray-600")}>Default Risk Level</label>
                <select className={clsx("w-full rounded-xl px-4 py-2 focus:outline-none focus:ring-1 appearance-none border", theme === 'dark' ? "bg-slate-800/50 border-slate-700 text-white focus:ring-rose-500" : "bg-gray-100 border-gray-300 text-black focus:ring-rose-600")}>
                   <option>High</option>
                   <option selected>Medium</option>
                   <option>Low</option>
                </select>
             </div>
          </div>
        </section>

        <div className="flex justify-end gap-4 mt-8">
           <button className={clsx("px-6 py-3 rounded-xl font-bold transition-all text-sm", theme === 'dark' ? "bg-slate-800 hover:bg-slate-700 text-slate-300" : "bg-gray-200 hover:bg-gray-300 text-gray-800")}>
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

const SourceToggle = ({ icon, name, desc, enabled, theme }: any) => {
  return (
    <div className={clsx("flex items-center justify-between p-4 rounded-xl border transition-all", theme === 'dark' ? "border-slate-800 bg-slate-800/30 hover:border-slate-700" : "border-gray-300 bg-gray-100 hover:border-gray-400")}>
       <div className="flex gap-4">
          <div className={clsx("w-10 h-10 rounded-lg flex items-center justify-center", theme === 'dark' ? "bg-slate-800 text-slate-400" : "bg-gray-300 text-gray-600")}>{icon}</div>
          <div>
             <h4 className={clsx("text-sm font-bold", theme === 'dark' ? "text-slate-200" : "text-gray-900")}>{name}</h4>
             <p className={clsx("text-xs leading-relaxed max-w-md", theme === 'dark' ? "text-slate-500" : "text-gray-600")}>{desc}</p>
          </div>
       </div>
       <div className={`w-12 h-6 rounded-full p-1 cursor-pointer transition-all duration-300 ${enabled ? 'bg-indigo-600' : theme === 'dark' ? 'bg-slate-700' : 'bg-gray-400'}`}>
          <div className={`w-4 h-4 bg-white rounded-full shadow-md transition-all duration-300 ${enabled ? 'translate-x-6' : 'translate-x-0'}`}></div>
       </div>
    </div>
  );
};

export default Settings;
