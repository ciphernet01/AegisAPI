import React, { useState } from 'react';
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
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
  const navigate = useNavigate();
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
        ? "bg-dark-bg text-dark-text-primary" 
        : "bg-light-bg text-light-text-primary"
    )}>
      {/* Top Navbar */}
      <nav className={clsx(
        "backdrop-blur-md border-b z-50 transition-colors duration-300",
        theme === 'dark'
          ? "bg-dark-surface-1 border-dark-border"
          : "bg-light-bg border-light-border shadow-sm"
      )}>
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <Link to="/" className="flex items-center gap-3 group pr-4 md:pr-6">
              <div className={clsx(
                "w-9 h-9 rounded-md flex items-center justify-center font-bold text-sm transition-all",
                theme === 'dark'
                  ? "bg-dark-surface-2 text-dark-text-primary border border-dark-border"
                  : "bg-light-surface-1 text-light-text-primary border border-light-border"
              )}>
                <ShieldAlert className="w-5 h-5" />
              </div>
              <span className={clsx(
                "font-bold text-lg tracking-tight hidden sm:inline",
                theme === 'dark'
                  ? "text-dark-text-primary"
                  : "text-light-text-primary"
              )}>
                Aegis API
              </span>
            </Link>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center gap-2">
              {navItems.map((item) => {
                const isActive = location.pathname === item.path;
                const Icon = item.icon;
                
                return (
                  <Link
                    key={item.name}
                    to={item.path}
                    className={clsx(
                      "flex items-center gap-2 px-3 py-2 rounded-md transition-all duration-200 font-medium text-sm",
                      isActive 
                        ? theme === 'dark'
                          ? "bg-dark-surface-2 text-dark-text-primary border border-dark-border"
                          : "bg-light-surface-1 text-light-text-primary border border-light-border"
                        : theme === 'dark'
                          ? "text-dark-text-secondary hover:bg-dark-surface-2"
                          : "text-light-text-secondary hover:bg-light-surface-1"
                    )}
                  >
                    <Icon size={16} />
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
                    ? "text-dark-text-secondary"
                    : "text-light-text-secondary"
                )} size={16} />
                <input 
                  type="text" 
                  placeholder="Search..." 
                  className={clsx(
                    "w-full rounded-md py-2 pl-10 pr-4 text-sm focus:outline-none focus:ring-1 transition-all border",
                    theme === 'dark'
                      ? "bg-dark-surface-2 border-dark-border text-dark-text-primary focus:ring-dark-text-secondary focus:border-dark-text-secondary placeholder:text-dark-text-secondary"
                      : "bg-light-surface-1 border-light-border text-light-text-primary focus:ring-light-text-secondary focus:border-light-text-secondary placeholder:text-light-text-secondary"
                  )}
                />
              </div>
            </div>

            {/* Right Actions */}
            <div className="flex items-center gap-3">
              {/* Notifications */}
              <button className={clsx(
                "p-2 rounded-md transition-colors relative hidden sm:flex items-center justify-center",
                theme === 'dark'
                  ? "hover:bg-dark-surface-2 text-dark-text-secondary hover:text-dark-text-primary"
                  : "hover:bg-light-surface-1 text-light-text-secondary hover:text-light-text-primary"
              )}>
                <Bell size={18} />
                <span className={clsx("absolute top-1 right-1 w-2 h-2 rounded-full", theme === 'dark' ? "bg-dark-text-secondary" : "bg-light-text-secondary")}></span>
              </button>

              {/* Theme Toggle */}
              <button 
                onClick={toggleTheme}
                className={clsx(
                  "p-2 rounded-md transition-colors flex items-center justify-center",
                  theme === 'dark'
                    ? "hover:bg-dark-surface-2 text-dark-text-secondary hover:text-dark-text-primary"
                    : "hover:bg-light-surface-1 text-light-text-secondary hover:text-light-text-primary"
                )}
                title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
              >
                {theme === 'dark' ? <Sun size={18} /> : <Moon size={18} />}
              </button>

              {/* Profile Dropdown */}
              <div className="relative">
                <button 
                  onClick={() => setIsProfileMenuOpen(!isProfileMenuOpen)}
                  className={clsx(
                    "flex items-center gap-2 px-3 py-2 rounded-md transition-all group",
                    theme === 'dark'
                      ? "hover:bg-dark-surface-2"
                      : "hover:bg-light-surface-1"
                  )}
                >
                  <div className={clsx(
                    "w-8 h-8 rounded-md border flex items-center justify-center",
                    theme === 'dark'
                      ? "bg-dark-surface-2 border-dark-border text-dark-text-secondary"
                      : "bg-light-surface-1 border-light-border text-light-text-secondary"
                  )}>
                    <User size={16} />
                  </div>
                  <div className="hidden sm:flex flex-col items-start">
                    <p className={clsx("text-sm font-semibold", theme === 'dark' ? "text-dark-text-primary" : "text-light-text-primary")}>Admin</p>
                    <p className={clsx("text-[10px] uppercase tracking-wider", theme === 'dark' ? "text-dark-text-secondary" : "text-light-text-secondary")}>Security</p>
                  </div>
                  <ChevronDown size={16} className={clsx("transition-transform", theme === 'dark' ? "text-dark-text-secondary" : "text-light-text-secondary", isProfileMenuOpen && "rotate-180")} />
                </button>

                {/* Profile Dropdown Menu */}
                {isProfileMenuOpen && (
                  <div className={clsx(
                    "absolute right-0 mt-2 w-48 rounded-md shadow-lg overflow-hidden z-50 border",
                    theme === 'dark'
                      ? "bg-dark-surface-1 border-dark-border"
                      : "bg-light-bg border-light-border"
                  )}>
                    <Link
                      to="/profile"
                      onClick={() => setIsProfileMenuOpen(false)}
                      className={clsx(
                        "w-full text-left px-4 py-3 transition-colors flex items-center gap-2 border-b",
                        theme === 'dark'
                          ? "hover:bg-dark-surface-2 text-dark-text-primary border-dark-border"
                          : "hover:bg-light-surface-1 text-light-text-primary border-light-border"
                      )}
                    >
                      <User size={16} />
                      <span className="text-sm">View Profile</span>
                    </Link>
                    <button 
                      onClick={() => {
                        setIsProfileMenuOpen(false);
                        // Placeholder sign-out hook; replace with real auth flow
                        localStorage.removeItem('auth_token');
                        navigate('/');
                      }}
                      className={clsx(
                        "w-full text-left px-4 py-3 transition-colors flex items-center gap-2",
                        theme === 'dark'
                          ? "hover:bg-dark-surface-2 text-dark-text-primary"
                          : "hover:bg-light-surface-1 text-light-text-primary"
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
                className={clsx(
                  "md:hidden p-2 rounded-md transition-colors",
                  theme === 'dark'
                    ? "hover:bg-dark-surface-2 text-dark-text-secondary hover:text-dark-text-primary"
                    : "hover:bg-light-surface-1 text-light-text-secondary hover:text-light-text-primary"
                )}
              >
                {isMobileMenuOpen ? <X size={18} /> : <Menu size={18} />}
              </button>
            </div>
          </div>

          {/* Mobile Navigation */}
          {isMobileMenuOpen && (
            <div className={clsx(
              "md:hidden mt-4 pb-4 space-y-2 border-t pt-4",
              theme === 'dark' ? "border-dark-border" : "border-light-border"
            )}>
              {navItems.map((item) => {
                const isActive = location.pathname === item.path;
                const Icon = item.icon;
                
                return (
                  <Link
                    key={item.name}
                    to={item.path}
                    onClick={() => setIsMobileMenuOpen(false)}
                    className={clsx(
                      "flex items-center gap-3 px-4 py-2 rounded-md transition-all duration-200 font-medium",
                      isActive 
                        ? theme === 'dark'
                          ? "bg-dark-surface-2 text-dark-text-primary border border-dark-border"
                          : "bg-light-surface-1 text-light-text-primary border border-light-border"
                        : theme === 'dark'
                          ? "text-dark-text-secondary hover:bg-dark-surface-2"
                          : "text-light-text-secondary hover:bg-light-surface-1"
                    )}
                  >
                    <Icon size={16} />
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
        <main className={clsx(
          "flex-1 overflow-y-auto p-8 custom-scrollbar",
          theme === 'dark' ? "bg-dark-bg" : "bg-light-bg"
        )}>
          <div className="max-w-7xl mx-auto">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;
