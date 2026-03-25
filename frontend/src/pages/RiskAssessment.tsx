import React from 'react';
import { 
  ShieldAlert, 
  Search, 
  AlertCircle, 
  ChevronRight, 
  Zap, 
  Info,
  ExternalLink
} from 'lucide-react';
import { clsx } from 'clsx';

const RiskAssessment: React.FC = () => {
  const risks = [
    { id: 1, api: "Auth-Service", endpoint: "/v1/login", risk: "Critical", score: 92, issue: "JWT Secret Weakness", status: "Open" },
    { id: 2, api: "Payment-Gateway", endpoint: "/v2/charge", risk: "High", score: 78, issue: "Insufficient Rate Limiting", status: "In Progress" },
    { id: 3, api: "User-Profile", endpoint: "/api/users/me", risk: "Medium", score: 45, issue: "PII Exposure in Logs", status: "Open" },
    { id: 4, api: "Inventory-Sync", endpoint: "/hooks/sync", risk: "Low", score: 22, issue: "Undocumented Endpoint", status: "Resolved" },
  ];

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-right-4 duration-500">
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Security Risk Assessment</h1>
        <p className="text-slate-400">Detailed breakdown of security findings, vulnerabilities, and compliance gaps across the platform.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="lg:col-span-3 space-y-6">
          {/* Risk List */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
            <div className="p-6 border-b border-slate-800 flex justify-between items-center">
              <h3 className="font-bold text-white flex items-center gap-2">
                <ShieldAlert size={20} className="text-rose-500" />
                Active Security Findings
              </h3>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={16} />
                <input 
                  type="text" 
                  placeholder="Filter findings..." 
                  className="bg-slate-800 border-none rounded-lg py-1.5 pl-10 pr-4 text-xs focus:ring-1 focus:ring-indigo-500"
                />
              </div>
            </div>

            <div className="divide-y divide-slate-800">
              {risks.map((risk) => (
                <div key={risk.id} className="p-6 hover:bg-slate-800/30 transition-all cursor-pointer group">
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
                          <h4 className="font-bold text-slate-100 group-hover:text-white transition-colors">{risk.issue}</h4>
                          <span className={clsx(
                            "px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider",
                            risk.risk === 'Critical' ? 'bg-rose-500/10 text-rose-500' :
                            risk.risk === 'High' ? 'bg-amber-500/10 text-amber-500' :
                            'bg-indigo-500/10 text-indigo-500'
                          )}>{risk.risk}</span>
                        </div>
                        <p className="text-xs text-slate-500 font-medium">
                          Impacts <span className="text-slate-300">{risk.api}</span> <span className="text-slate-600 mx-1">•</span> <span className="font-mono">{risk.endpoint}</span>
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-xl font-bold text-white mb-1">{risk.score}</div>
                      <div className="text-[10px] text-slate-500 font-bold uppercase tracking-widest">Risk Score</div>
                    </div>
                  </div>
                  <div className="mt-4 flex items-center justify-between">
                    <div className="flex gap-2">
                       <span className="px-2 py-1 bg-slate-800 text-slate-400 rounded-md text-[10px] border border-slate-700">CWE-327</span>
                       <span className="px-2 py-1 bg-slate-800 text-slate-400 rounded-md text-[10px] border border-slate-700">OWASP A2</span>
                    </div>
                    <div className="flex items-center gap-2 group/btn cursor-pointer">
                      <span className="text-xs font-semibold text-slate-500 group-hover/btn:text-indigo-400 transition-colors">View Details</span>
                      <ChevronRight size={14} className="text-slate-700 group-hover/btn:text-indigo-400 transition-all group-hover/btn:translate-x-1" />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Sidebar info */}
        <div className="space-y-6">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
             <h3 className="font-bold text-white mb-4 flex items-center gap-2 text-sm">
                <ShieldAlert size={18} className="text-indigo-400" />
                Score Distribution
             </h3>
             <div className="space-y-4">
                <div className="flex justify-between items-end">
                   <div className="text-xs text-slate-500">Critical (90+)</div>
                   <div className="text-sm font-bold text-rose-500">2</div>
                </div>
                <div className="w-full h-1 bg-slate-800 rounded-full overflow-hidden">
                   <div className="w-[15%] h-full bg-rose-500"></div>
                </div>
                
                <div className="flex justify-between items-end pt-2">
                   <div className="text-xs text-slate-500">High (70-90)</div>
                   <div className="text-sm font-bold text-amber-500">5</div>
                </div>
                <div className="w-full h-1 bg-slate-800 rounded-full overflow-hidden">
                   <div className="w-[35%] h-full bg-amber-500"></div>
                </div>

                <div className="flex justify-between items-end pt-2">
                   <div className="text-xs text-slate-500">Medium (40-70)</div>
                   <div className="text-sm font-bold text-indigo-500">12</div>
                </div>
                <div className="w-full h-1 bg-slate-800 rounded-full overflow-hidden">
                   <div className="w-[60%] h-full bg-indigo-500"></div>
                </div>
             </div>
          </div>

          <div className="bg-gradient-to-br from-indigo-900/50 to-slate-900 border border-indigo-500/20 rounded-2xl p-6 shadow-xl">
             <Zap size={24} className="text-indigo-400 mb-4" />
             <h3 className="font-bold text-white mb-2 text-sm leading-tight">Comprehensive Security Audit</h3>
             <p className="text-xs text-slate-400 leading-relaxed mb-4">You have 12 APIs that haven't been scanned in over 30 days.</p>
             <button className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-bold transition-all shadow-lg shadow-indigo-600/20">
                Rescan Infrastructure
             </button>
          </div>

          <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6">
             <div className="flex items-center gap-2 text-slate-400 mb-3 hover:text-slate-200 transition-colors cursor-pointer">
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
