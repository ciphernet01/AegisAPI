import React, { useState } from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  ShieldAlert, 
  ListTree, 
  Wrench, 
  Settings as SettingsIcon,
  Menu,
  X,
  Search,
  Bell,
  User,
  LogOut
} from 'lucide-react';
import { clsx } from 'clsx';
import { useAuth } from '@/context/AuthContext';

const Layout: React.FC = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const location = useLocation();
  const { user, logout } = useAuth();

  const navItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'API Inventory', path: '/inventory', icon: ListTree },
    { name: 'Risk Assessment', path: '/risk-assessment', icon: ShieldAlert },
    { name: 'Remediations', path: '/remediations', icon: Wrench },
    { name: 'Settings', path: '/settings', icon: SettingsIcon },
  ];

  return (
    <div className="flex h-screen bg-slate-950 text-slate-200 font-sans overflow-hidden">
      {/* Sidebar */}
      <aside 
        className={clsx(
          "bg-slate-900 border-r border-slate-800 transition-all duration-300 ease-in-out z-30",
          isSidebarOpen ? "w-64" : "w-20"
        )}
      >
        <div className="flex items-center justify-between h-16 px-4 border-b border-slate-800 shadow-lg bg-slate-900/50 backdrop-blur-md">
          <div className={clsx("flex items-center gap-3 transition-opacity duration-300", !isSidebarOpen && "opacity-0 invisible")}>
            <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center shadow-indigo-500/20 shadow-lg">
              <ShieldAlert className="w-5 h-5 text-white" />
            </div>
            <span className="font-bold text-xl tracking-tight bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
              Aegis API
            </span>
          </div>
          <button 
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="p-2 rounded-md hover:bg-slate-800 text-slate-400 hover:text-white transition-colors"
          >
            {isSidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>

        <nav className="mt-6 px-3 space-y-1">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;
            const Icon = item.icon;
            
            return (
              <Link
                key={item.name}
                to={item.path}
                className={clsx(
                  "flex items-center gap-4 px-3 py-3 rounded-xl transition-all duration-200 group relative",
                  isActive 
                    ? "bg-indigo-600/10 text-indigo-400 shadow-sm" 
                    : "text-slate-400 hover:bg-slate-800/50 hover:text-slate-200"
                )}
              >
                <div className={clsx(
                  "transition-all duration-200",
                  isActive ? "text-indigo-400 scale-110" : "group-hover:scale-110"
                )}>
                  <Icon size={22} />
                </div>
                {isSidebarOpen && (
                  <span className="font-medium whitespace-nowrap">{item.name}</span>
                )}
                {isActive && (
                  <div className="absolute left-0 w-1 h-6 bg-indigo-500 rounded-r-full" />
                )}
              </Link>
            );
          })}
        </nav>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Header */}
        <header className="h-16 bg-slate-900/50 backdrop-blur-md border-b border-slate-800 flex items-center justify-between px-8 z-20">
          <div className="flex-1 max-w-xl">
            <div className="relative group">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-indigo-400 transition-colors" size={18} />
              <input 
                type="text" 
                placeholder="Search APIs, endpoints, or vulnerabilities..." 
                className="w-full bg-slate-800/50 border border-slate-700 rounded-full py-2 pl-10 pr-4 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500/50 transition-all placeholder:text-slate-600"
              />
            </div>
          </div>
          
          <div className="flex items-center gap-4 ml-8">
            <button className="p-2 rounded-full hover:bg-slate-800 text-slate-400 hover:text-indigo-400 transition-colors relative">
              <Bell size={20} />
              <span className="absolute top-2 right-2 w-2 h-2 bg-indigo-500 rounded-full border-2 border-slate-900"></span>
            </button>
            <button
              onClick={logout}
              className="p-2 rounded-full hover:bg-slate-800 text-slate-400 hover:text-rose-400 transition-colors"
              title="Sign out"
            >
              <LogOut size={18} />
            </button>
            <div className="h-8 w-px bg-slate-800 mx-1"></div>
            <Link to="/profile" className={clsx('flex items-center gap-3 pl-2 rounded-lg px-2 py-1.5 transition-colors', location.pathname === '/profile' ? 'bg-indigo-600/15 border border-indigo-500/30' : 'hover:bg-slate-800/60')}>
              <div className="text-right hidden sm:block">
                <p className="text-sm font-semibold text-slate-200 group-hover:text-white transition-colors leading-tight">{user?.name ?? 'Security Admin'}</p>
                <p className="text-[10px] text-slate-500 font-medium tracking-wider uppercase">Profile</p>
              </div>
              <div className="w-9 h-9 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-indigo-400 group-hover:border-indigo-500/50 transition-all shadow-lg overflow-hidden">
                <User size={20} />
              </div>
            </Link>
          </div>
        </header>

        {/* Page Area */}
        <main className="flex-1 overflow-y-auto p-8 custom-scrollbar">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;
