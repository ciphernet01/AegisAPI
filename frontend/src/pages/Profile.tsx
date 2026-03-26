import React, { useState } from 'react';
import { User, ShieldCheck, Mail, Lock, Smartphone, LogOut } from 'lucide-react';
import { clsx } from 'clsx';
import { useTheme } from '@context/ThemeContext';

const Profile: React.FC = () => {
  const { theme } = useTheme();
  const [notifySecurity, setNotifySecurity] = useState(true);
  const [notifyOps, setNotifyOps] = useState(false);

  const cardBg = theme === 'dark' ? 'bg-dark-surface-1 border-dark-border' : 'bg-light-bg border-light-border';
  const textPrimary = theme === 'dark' ? 'text-dark-text-primary' : 'text-light-text-primary';
  const textSecondary = theme === 'dark' ? 'text-dark-text-secondary' : 'text-light-text-secondary';

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-right-4 duration-500">
      <div>
        <h1 className={clsx('text-3xl font-bold mb-2', textPrimary)}>Profile</h1>
        <p className={clsx(textSecondary)}>Manage your account, security preferences, and notifications.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <section className={clsx('rounded-2xl border p-6 shadow-sm lg:col-span-2', cardBg)}>
          <div className="flex items-center gap-4 mb-6">
            <div className={clsx('w-14 h-14 rounded-xl flex items-center justify-center text-lg font-bold border', theme === 'dark' ? 'bg-dark-surface-2 border-dark-border' : 'bg-light-surface-1 border-light-border')}>
              <User />
            </div>
            <div>
              <p className={clsx('text-lg font-semibold', textPrimary)}>Admin User</p>
              <p className={clsx('text-sm', textSecondary)}>Security Team</p>
            </div>
          </div>

          <div className="space-y-4">
            <ProfileRow icon={<Mail size={16} />} label="Email" value="admin@example.com" theme={theme} />
            <ProfileRow icon={<Smartphone size={16} />} label="MFA" value="Enabled" theme={theme} />
            <ProfileRow icon={<ShieldCheck size={16} />} label="Role" value="Administrator" theme={theme} />
          </div>
        </section>

        <section className={clsx('rounded-2xl border p-6 shadow-sm space-y-4', cardBg)}>
          <h3 className={clsx('text-lg font-semibold', textPrimary)}>Quick Actions</h3>
          <button className={clsx('w-full px-4 py-3 rounded-xl font-semibold transition-all flex items-center gap-2 justify-center', theme === 'dark' ? 'bg-dark-surface-2 hover:bg-dark-surface-2/80 text-dark-text-primary border border-dark-border' : 'bg-light-surface-1 hover:bg-light-surface-1 text-light-text-primary border border-light-border')}>
            <Lock size={16} /> Reset Password
          </button>
          <button className={clsx('w-full px-4 py-3 rounded-xl font-semibold transition-all flex items-center gap-2 justify-center', theme === 'dark' ? 'bg-rose-600 hover:bg-rose-500 text-white' : 'bg-rose-600 hover:bg-rose-500 text-white')}>
            <LogOut size={16} /> Sign Out
          </button>
        </section>
      </div>

      <section className={clsx('rounded-2xl border p-6 shadow-sm space-y-6', cardBg)}>
        <div className="flex items-center justify-between">
          <div>
            <h3 className={clsx('text-lg font-semibold', textPrimary)}>Notifications</h3>
            <p className={clsx('text-sm', textSecondary)}>Choose what alerts you receive.</p>
          </div>
        </div>
        <div className="space-y-4">
          <ToggleRow
            checked={notifySecurity}
            onChange={() => setNotifySecurity((v) => !v)}
            title="Security events"
            description="Critical findings, new zombie API detections, decommission approvals."
            theme={theme}
          />
          <ToggleRow
            checked={notifyOps}
            onChange={() => setNotifyOps((v) => !v)}
            title="Operations"
            description="Deployments, job status, background discovery runs."
            theme={theme}
          />
        </div>
      </section>
    </div>
  );
};

const ProfileRow = ({ icon, label, value, theme }: any) => (
  <div className={clsx('flex items-center justify-between rounded-xl px-4 py-3 border', theme === 'dark' ? 'border-dark-border bg-dark-surface-2/40' : 'border-light-border bg-light-surface-1')}>
    <div className="flex items-center gap-3">
      <span className={clsx('p-2 rounded-lg border', theme === 'dark' ? 'border-dark-border bg-dark-surface-2 text-dark-text-secondary' : 'border-light-border bg-light-surface-1 text-light-text-secondary')}>{icon}</span>
      <div>
        <p className={clsx('text-sm font-semibold', theme === 'dark' ? 'text-dark-text-primary' : 'text-light-text-primary')}>{label}</p>
        <p className={clsx('text-xs', theme === 'dark' ? 'text-dark-text-secondary' : 'text-light-text-secondary')}>{value}</p>
      </div>
    </div>
  </div>
);

const ToggleRow = ({ checked, onChange, title, description, theme }: any) => (
  <div className={clsx('flex items-center justify-between rounded-xl px-4 py-3 border', theme === 'dark' ? 'border-dark-border bg-dark-surface-2/40' : 'border-light-border bg-light-surface-1')}>
    <div>
      <p className={clsx('text-sm font-semibold', theme === 'dark' ? 'text-dark-text-primary' : 'text-light-text-primary')}>{title}</p>
      <p className={clsx('text-xs', theme === 'dark' ? 'text-dark-text-secondary' : 'text-light-text-secondary')}>{description}</p>
    </div>
    <button
      onClick={onChange}
      className={clsx(
        'w-12 h-6 rounded-full p-1 transition-all duration-200 flex items-center',
        checked ? 'bg-indigo-600' : theme === 'dark' ? 'bg-dark-surface-2' : 'bg-gray-300'
      )}
      aria-pressed={checked}
    >
      <span
        className={clsx(
          'w-4 h-4 rounded-full bg-white shadow-sm transform transition-all duration-200',
          checked ? 'translate-x-6' : 'translate-x-0'
        )}
      />
    </button>
  </div>
);

export default Profile;
