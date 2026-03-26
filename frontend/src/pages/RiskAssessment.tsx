import React from 'react';
import { 
  ShieldAlert, 
  Search, 
  AlertCircle, 
  ChevronRight, 
  Lock, 
  Zap, 
  Info,
  ExternalLink
} from 'lucide-react';
import { clsx } from 'clsx';
import { useTheme } from '@contexts/ThemeContext';

const RiskAssessment: React.FC = () => {
  const { theme } = useTheme();
  const risks = [
    { id: 1, api: "Auth-Service", endpoint: "/v1/login", risk: "Critical", score: 92, issue: "JWT Secret Weakness", status: "Open" },
    { id: 2, api: "Payment-Gateway", endpoint: "/v2/charge", risk: "High", score: 78, issue: "Insufficient Rate Limiting", status: "In Progress" },
    { id: 3, api: "User-Profile", endpoint: "/api/users/me", risk: "Medium", score: 45, issue: "PII Exposure in Logs", status: "Open" },
    { id: 4, api: "Inventory-Sync", endpoint: "/hooks/sync", risk: "Low", score: 22, issue: "Undocumented Endpoint", status: "Resolved" },
  ];

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-right-4 duration-500">
      <div>
        <h1 className={clsx("text-3xl font-bold mb-2", theme === 'dark' ? "text-white" : "text-black")}>Security Risk Assessment</h1>
        <p className={clsx(theme === 'dark' ? "text-slate-400" : "text-gray-600")}>Detailed breakdown of security findings, vulnerabilities, and compliance gaps across the platform.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="lg:col-span-3 space-y-6">
          {/* Risk List */}
          <div className={clsx("rounded-2xl overflow-hidden shadow-xl border", theme === 'dark' ? "bg-slate-900 border-slate-800" : "bg-white border-gray-200")}>
            <div className={clsx("p-6 border-b flex justify-between items-center", theme === 'dark' ? "border-slate-800" : "border-gray-200")}>
              <h3 className={clsx("font-bold flex items-center gap-2", theme === 'dark' ? "text-white" : "text-black")}>
                <ShieldAlert size={20} className="text-rose-500" />
                Active Security Findings
              </h3>
              <div className="relative">
                <Search className={clsx("absolute left-3 top-1/2 -translate-y-1/2", theme === 'dark' ? "text-slate-500" : "text-gray-400")} size={16} />
                <input 
                  type="text" 
                  placeholder="Filter findings..." 
                  className={clsx("rounded-lg py-1.5 pl-10 pr-4 text-xs focus:ring-1 border", theme === 'dark' ? "bg-slate-800 border-slate-700 focus:ring-indigo-500 text-white" : "bg-gray-100 border-gray-300 focus:ring-indigo-600 text-black")}
                />
              </div>
            </div>

            <div className={clsx("divide-y", theme === 'dark' ? "divide-slate-800" : "divide-gray-200")}>
              {risks.map((risk) => (
                <div key={risk.id} className={clsx("p-6 transition-all cursor-pointer group", theme === 'dark' ? "hover:bg-slate-800/30" : "hover:bg-gray-100")}>
                  <div className="flex items-start justify-between">
                    <div className="flex gap-4">
                      <div className={clsx(
                        "w-12 h-12 rounded-xl flex items-center justify-center shrink-0 border",
                        risk.risk === 'Critical' ? 'bg-rose-500/10 border-rose-500/20 text-rose-500' :
                        risk.risk === 'High' ? 'bg-amber-500/10 border-amber-500/20 text-amber-500' :
                        'bg-indigo-500/10 border-indigo-500/20 text-indigo-500'
                      )}>
                        <AlertCircle size={24} />
                      </div>
                      <div>
                        <div className="flex items-center gap-3 mb-1">
                          <h4 className={clsx("font-bold transition-colors", theme === 'dark' ? "text-slate-100 group-hover:text-white" : "text-gray-900")}>{risk.issue}</h4>
                          <span className={clsx(
                            "px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider",
                            risk.risk === 'Critical' ? 'bg-rose-500/10 text-rose-500' :
                            risk.risk === 'High' ? 'bg-amber-500/10 text-amber-500' :
                            'bg-indigo-500/10 text-indigo-500'
                          )}>{risk.risk}</span>
                        </div>
                        <p className={clsx("text-xs font-medium", theme === 'dark' ? "text-slate-500" : "text-gray-600")}>
                          Impacts <span className={theme === 'dark' ? "text-slate-300" : "text-gray-800"}>{risk.api}</span> <span className={clsx("mx-1", theme === 'dark' ? "text-slate-600" : "text-gray-400")}>•</span> <span className="font-mono">{risk.endpoint}</span>
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className={clsx("text-xl font-bold mb-1", theme === 'dark' ? "text-white" : "text-black")}>{risk.score}</div>
                      <div className={clsx("text-[10px] font-bold uppercase tracking-widest", theme === 'dark' ? "text-slate-500" : "text-gray-600")}>Risk Score</div>
                    </div>
                  </div>
                  <div className="mt-4 flex items-center justify-between">
                    <div className="flex gap-2">
                       <span className={clsx("px-2 py-1 rounded-md text-[10px] border", theme === 'dark' ? "bg-slate-800 text-slate-400 border-slate-700" : "bg-gray-200 text-gray-600 border-gray-300")}>CWE-327</span>
                       <span className={clsx("px-2 py-1 rounded-md text-[10px] border", theme === 'dark' ? "bg-slate-800 text-slate-400 border-slate-700" : "bg-gray-200 text-gray-600 border-gray-300")}>OWASP A2</span>
                    </div>
                    <div className="flex items-center gap-2 group/btn cursor-pointer">
                      <span className={clsx("text-xs font-semibold transition-colors", theme === 'dark' ? "text-slate-500 group-hover/btn:text-indigo-400" : "text-gray-600 group-hover/btn:text-indigo-600")}>View Details</span>
                      <ChevronRight size={14} className={clsx("transition-all group-hover/btn:translate-x-1", theme === 'dark' ? "text-slate-700 group-hover/btn:text-indigo-400" : "text-gray-400 group-hover/btn:text-indigo-600")} />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Sidebar info */}
        <div className="space-y-6">
          <div className={clsx("rounded-2xl p-6 shadow-xl border", theme === 'dark' ? "bg-slate-900 border-slate-800" : "bg-white border-gray-200")}>
             <h3 className={clsx("font-bold mb-4 flex items-center gap-2 text-sm", theme === 'dark' ? "text-white" : "text-black")}>
                <ShieldAlert size={18} className="text-indigo-400" />
                Score Distribution
             </h3>
             <div className="space-y-4">
                <div className="flex justify-between items-end">
                   <div className={clsx("text-xs", theme === 'dark' ? "text-slate-500" : "text-gray-600")}>Critical (90+)</div>
                   <div className={clsx("text-sm font-bold", theme === 'dark' ? "text-rose-400" : "text-rose-600")}>2</div>
                </div>
                <div className={clsx("w-full h-1 rounded-full overflow-hidden", theme === 'dark' ? "bg-slate-800" : "bg-gray-300")}>
                   <div className="w-[15%] h-full bg-rose-500"></div>
                </div>
                
                <div className="flex justify-between items-end pt-2">
                   <div className={clsx("text-xs", theme === 'dark' ? "text-slate-500" : "text-gray-600")}>High (70-90)</div>
                   <div className={clsx("text-sm font-bold", theme === 'dark' ? "text-amber-400" : "text-amber-600")}>5</div>
                </div>
                <div className={clsx("w-full h-1 rounded-full overflow-hidden", theme === 'dark' ? "bg-slate-800" : "bg-gray-300")}>
                   <div className="w-[35%] h-full bg-amber-500"></div>
                </div>

                <div className="flex justify-between items-end pt-2">
                   <div className={clsx("text-xs", theme === 'dark' ? "text-slate-500" : "text-gray-600")}>Medium (40-70)</div>
                   <div className={clsx("text-sm font-bold", theme === 'dark' ? "text-indigo-400" : "text-indigo-600")}>12</div>
                </div>
                <div className={clsx("w-full h-1 rounded-full overflow-hidden", theme === 'dark' ? "bg-slate-800" : "bg-gray-300")}>
                   <div className="w-[60%] h-full bg-indigo-500"></div>
                </div>
             </div>
          </div>

          <div className={clsx("rounded-2xl p-6 shadow-xl border", theme === 'dark' ? "bg-gradient-to-br from-indigo-900/50 to-slate-900 border-indigo-500/20" : "bg-indigo-50 border-indigo-200")}>
             <Zap size={24} className={clsx("mb-4", theme === 'dark' ? "text-indigo-400" : "text-indigo-600")} />
             <h3 className={clsx("font-bold mb-2 text-sm leading-tight", theme === 'dark' ? "text-white" : "text-indigo-900")}>Comprehensive Security Audit</h3>
             <p className={clsx("text-xs leading-relaxed mb-4", theme === 'dark' ? "text-slate-400" : "text-indigo-700")}>You have 12 APIs that haven't been scanned in over 30 days.</p>
             <button className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-bold transition-all shadow-lg shadow-indigo-600/20">
                Rescan Infrastructure
             </button>
          </div>

          <div className={clsx("rounded-2xl p-6 border", theme === 'dark' ? "bg-slate-900/50 border-slate-800" : "bg-gray-100 border-gray-200")}>
             <div className={clsx("flex items-center gap-2 mb-3 hover:transition-colors cursor-pointer", theme === 'dark' ? "text-slate-400 hover:text-slate-200" : "text-gray-600 hover:text-gray-900")}>
                <Info size={16} />
                <span className="text-xs font-medium">Risk Scoring Methodology</span>
                <ExternalLink size={12} className="ml-auto" />
             </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RiskAssessment;
