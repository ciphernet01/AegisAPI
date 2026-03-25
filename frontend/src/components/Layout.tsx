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
  LogOut,
  ChevronDown
} from 'lucide-react';
import { clsx } from 'clsx';

const Layout: React.FC = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isProfileMenuOpen, setIsProfileMenuOpen] = useState(false);
  const location = useLocation();

  const navItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'API Inventory', path: '/inventory', icon: ListTree },
    { name: 'Risk Assessment', path: '/risk-assessment', icon: ShieldAlert },
    { name: 'Remediations', path: '/remediations', icon: Wrench },
    { name: 'Settings', path: '/settings', icon: SettingsIcon },
  ];

  return (
    <div className="flex h-screen bg-slate-950 text-slate-200 font-sans flex-col overflow-hidden">
      {/* Top Navbar */}
      <nav className="bg-slate-900/50 backdrop-blur-md border-b border-slate-800 z-50">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <Link to="/" className="flex items-center gap-3 group">
              <div className="w-9 h-9 rounded-lg bg-indigo-600 flex items-center justify-center shadow-indigo-500/20 shadow-lg group-hover:shadow-indigo-500/40 transition-all">
                <ShieldAlert className="w-5 h-5 text-white" />
              </div>
              <span className="font-bold text-xl tracking-tight bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent hidden sm:inline">
                Aegis API
              </span>
            </Link>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center gap-1">
              {navItems.map((item) => {
                const isActive = location.pathname === item.path;
                const Icon = item.icon;
                
                return (
                  <Link
                    key={item.name}
                    to={item.path}
                    className={clsx(
                      "flex items-center gap-2 px-4 py-2 rounded-lg transition-all duration-200 font-medium text-sm",
                      isActive 
                        ? "bg-indigo-600/20 text-indigo-400 border border-indigo-500/30" 
                        : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
                    )}
                  >
                    <Icon size={18} />
                    <span>{item.name}</span>
                  </Link>
                );
              })}
            </div>

            {/* Search Bar */}
            <div className="hidden lg:flex flex-1 mx-6 max-w-md">
              <div className="relative w-full group">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-indigo-400 transition-colors" size={16} />
                <input 
                  type="text" 
                  placeholder="Search..." 
                  className="w-full bg-slate-800/50 border border-slate-700 rounded-lg py-2 pl-10 pr-4 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500/50 transition-all placeholder:text-slate-600"
                />
              </div>
            </div>

            {/* Right Actions */}
            <div className="flex items-center gap-4">
              {/* Notifications */}
              <button className="p-2 rounded-lg hover:bg-slate-800/50 text-slate-400 hover:text-indigo-400 transition-colors relative hidden sm:flex items-center justify-center">
                <Bell size={20} />
                <span className="absolute top-1 right-1 w-2 h-2 bg-indigo-500 rounded-full"></span>
              </button>

              {/* Profile Dropdown */}
              <div className="relative">
                <button 
                  onClick={() => setIsProfileMenuOpen(!isProfileMenuOpen)}
                  className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-slate-800/50 transition-all group"
                >
                  <div className="w-8 h-8 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center text-indigo-400 group-hover:border-indigo-500/50">
                    <User size={18} />
                  </div>
                  <div className="hidden sm:flex flex-col items-start">
                    <p className="text-sm font-semibold text-slate-200">Admin</p>
                    <p className="text-[10px] text-slate-500 uppercase tracking-wider">Security</p>
                  </div>
                  <ChevronDown size={16} className={clsx("text-slate-500 transition-transform", isProfileMenuOpen && "rotate-180")} />
                </button>

                {/* Profile Dropdown Menu */}
                {isProfileMenuOpen && (
                  <div className="absolute right-0 mt-2 w-48 bg-slate-800 border border-slate-700 rounded-lg shadow-lg overflow-hidden z-50">
                    <button className="w-full text-left px-4 py-3 hover:bg-slate-700/50 transition-colors flex items-center gap-2 text-slate-200 border-b border-slate-700">
                      <User size={16} />
                      <span className="text-sm">View Profile</span>
                    </button>
                    <button 
                      onClick={() => {
                        setIsProfileMenuOpen(false);
                        // Add logout logic here
                      }}
                      className="w-full text-left px-4 py-3 hover:bg-slate-700/50 transition-colors flex items-center gap-2 text-red-400 hover:text-red-300"
                    >
                      <LogOut size={16} />
                      <span className="text-sm">Sign Out</span>
                    </button>
                  </div>
                )}
              </div>

              {/* Mobile Menu Button */}
              <button 
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="md:hidden p-2 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-white transition-colors"
              >
                {isMobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
              </button>
            </div>
          </div>

          {/* Mobile Navigation */}
          {isMobileMenuOpen && (
            <div className="md:hidden mt-4 pb-4 space-y-2 border-t border-slate-800 pt-4">
              {navItems.map((item) => {
                const isActive = location.pathname === item.path;
                const Icon = item.icon;
                
                return (
                  <Link
                    key={item.name}
                    to={item.path}
                    onClick={() => setIsMobileMenuOpen(false)}
                    className={clsx(
                      "flex items-center gap-3 px-4 py-2 rounded-lg transition-all duration-200 font-medium",
                      isActive 
                        ? "bg-indigo-600/20 text-indigo-400 border border-indigo-500/30" 
                        : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
                    )}
                  >
                    <Icon size={18} />
                    <span>{item.name}</span>
                  </Link>
                );
              })}
            </div>
          )}
        </div>
      </nav>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Page Area */}
        <main className="flex-1 overflow-y-auto p-8 custom-scrollbar">
          <div className="max-w-7xl mx-auto">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;
            </div>
          </div>
          
          <div className="flex items-center gap-4 ml-8">
            <button className="p-2 rounded-full hover:bg-slate-800 text-slate-400 hover:text-indigo-400 transition-colors relative">
              <Bell size={20} />
              <span className="absolute top-2 right-2 w-2 h-2 bg-indigo-500 rounded-full border-2 border-slate-900"></span>
            </button>
            <div className="h-8 w-px bg-slate-800 mx-1"></div>
            <div className="flex items-center gap-3 pl-2 group cursor-pointer">
              <div className="text-right hidden sm:block">
                <p className="text-sm font-semibold text-slate-200 group-hover:text-white transition-colors leading-tight">Security Admin</p>
                <p className="text-[10px] text-slate-500 font-medium tracking-wider uppercase">Risk Analysis Eng.</p>
              </div>
              <div className="w-9 h-9 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-indigo-400 group-hover:border-indigo-500/50 transition-all shadow-lg overflow-hidden">
                <User size={20} />
              </div>
            </div>
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
