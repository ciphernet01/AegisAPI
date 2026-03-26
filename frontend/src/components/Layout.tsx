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
  ChevronDown,
  Sun,
  Moon
} from 'lucide-react';
import { clsx } from 'clsx';
import { useTheme } from '@/context/ThemeContext';

const Layout: React.FC = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isProfileMenuOpen, setIsProfileMenuOpen] = useState(false);
  const location = useLocation();
  const { theme, toggleTheme } = useTheme();

  const navItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'API Inventory', path: '/inventory', icon: ListTree },
    { name: 'Risk Assessment', path: '/risk-assessment', icon: ShieldAlert },
    { name: 'Remediations', path: '/remediations', icon: Wrench },
    { name: 'Settings', path: '/settings', icon: SettingsIcon },
  ];

  return (
    <div className={clsx(
      "flex h-screen font-sans flex-col overflow-hidden transition-colors duration-300",
      theme === 'dark' 
        ? "bg-slate-950 text-slate-200" 
        : "bg-slate-50 text-slate-900"
    )}>
      {/* Top Navbar */}
      <nav className={clsx(
        "backdrop-blur-md border-b z-50 transition-colors duration-300",
        theme === 'dark'
          ? "bg-slate-900/50 border-slate-800"
          : "bg-white/80 border-gray-300 shadow-sm"
      )}>
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <Link to="/" className="flex items-center gap-3 group">
              <div className={clsx(
                "w-9 h-9 rounded-lg flex items-center justify-center shadow-lg transition-all",
                theme === 'dark'
                  ? "bg-indigo-600 shadow-indigo-500/20 group-hover:shadow-indigo-500/40"
                  : "bg-indigo-500 shadow-indigo-400/30 group-hover:shadow-indigo-400/50"
              )}>
                <ShieldAlert className="w-5 h-5 text-white" />
              </div>
              <span className={clsx(
                "font-bold text-xl tracking-tight bg-clip-text text-transparent hidden sm:inline",
                theme === 'dark'
                  ? "bg-gradient-to-r from-white to-slate-400"
                  : "bg-gradient-to-r from-slate-900 to-slate-600"
              )}>
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
                        ? theme === 'dark'
                          ? "bg-indigo-600/20 text-indigo-400 border border-indigo-500/30"
                          : "bg-indigo-100 text-indigo-700 border border-indigo-300"
                        : theme === 'dark'
                          ? "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
                          : "text-gray-600 hover:text-black hover:bg-gray-200"
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
                <Search className={clsx(
                  "absolute left-3 top-1/2 -translate-y-1/2 transition-colors",
                  theme === 'dark' 
                    ? "text-slate-500 group-focus-within:text-indigo-400"
                    : "text-gray-400 group-focus-within:text-indigo-600"
                )} size={16} />
                <input 
                  type="text" 
                  placeholder="Search..." 
                  className={clsx(
                    "w-full rounded-lg py-2 pl-10 pr-4 text-sm focus:outline-none focus:ring-2 transition-all",
                    theme === 'dark'
                      ? "bg-slate-800/50 border border-slate-700 text-white focus:ring-indigo-500/50 focus:border-indigo-500/50 placeholder:text-slate-600"
                      : "bg-gray-200 border border-gray-300 text-black focus:ring-indigo-600/50 focus:border-indigo-600 placeholder:text-gray-500"
                  )}
                />
              </div>
            </div>

            {/* Right Actions */}
            <div className="flex items-center gap-4">
              {/* Notifications */}
              <button className={clsx(
                "p-2 rounded-lg transition-colors relative hidden sm:flex items-center justify-center",
                theme === 'dark'
                  ? "hover:bg-slate-800/50 text-slate-400 hover:text-indigo-400"
                  : "hover:bg-gray-200 text-gray-600 hover:text-indigo-600"
              )}>
                <Bell size={20} />
                <span className="absolute top-1 right-1 w-2 h-2 bg-indigo-500 rounded-full"></span>
              </button>

              {/* Theme Toggle */}
              <button 
                onClick={toggleTheme}
                className={clsx(
                  "p-2 rounded-lg transition-colors flex items-center justify-center",
                  theme === 'dark'
                    ? "hover:bg-slate-800/50 text-slate-400 hover:text-indigo-400"
                    : "hover:bg-gray-200 text-gray-600 hover:text-indigo-600"
                )}
                title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
              >
                {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
              </button>

              {/* Profile Dropdown */}
              <div className="relative">
                <button 
                  onClick={() => setIsProfileMenuOpen(!isProfileMenuOpen)}
                  className={clsx(
                    "flex items-center gap-2 px-3 py-2 rounded-lg transition-all group",
                    theme === 'dark'
                      ? "hover:bg-slate-800/50"
                      : "hover:bg-gray-200"
                  )}
                >
                  <div className={clsx(
                    "w-8 h-8 rounded-lg border flex items-center justify-center",
                    theme === 'dark'
                      ? "bg-slate-800 border-slate-700 text-indigo-400 group-hover:border-indigo-500/50"
                      : "bg-gray-200 border-gray-400 text-indigo-600 group-hover:border-indigo-600"
                  )}>
                    <User size={18} />
                  </div>
                  <div className="hidden sm:flex flex-col items-start">
                    <p className={clsx("text-sm font-semibold", theme === 'dark' ? "text-slate-200" : "text-black")}>Admin</p>
                    <p className={clsx("text-[10px] uppercase tracking-wider", theme === 'dark' ? "text-slate-500" : "text-gray-500")}>Security</p>
                  </div>
                  <ChevronDown size={16} className={clsx("transition-transform", theme === 'dark' ? "text-slate-500" : "text-gray-500", isProfileMenuOpen && "rotate-180")} />
                </button>

                {/* Profile Dropdown Menu */}
                {isProfileMenuOpen && (
                  <div className={clsx(
                    "absolute right-0 mt-2 w-48 rounded-lg shadow-lg overflow-hidden z-50",
                    theme === 'dark'
                      ? "bg-slate-800 border border-slate-700"
                      : "bg-white border border-gray-300"
                  )}>
                    <button className={clsx(
                      "w-full text-left px-4 py-3 transition-colors flex items-center gap-2",
                      theme === 'dark'
                        ? "hover:bg-slate-700/50 text-slate-200 border-b border-slate-700"
                        : "hover:bg-gray-100 text-black border-b border-gray-200"
                    )}>
                      <User size={16} />
                      <span className="text-sm">View Profile</span>
                    </button>
                    <button 
                      onClick={() => {
                        setIsProfileMenuOpen(false);
                        // Add logout logic here
                      }}
                      className={clsx(
                        "w-full text-left px-4 py-3 transition-colors flex items-center gap-2",
                        theme === 'dark'
                          ? "hover:bg-slate-700/50 text-red-400 hover:text-red-300"
                          : "hover:bg-red-50 text-red-600 hover:text-red-700"
                      )}
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
