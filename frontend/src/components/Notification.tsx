import React, { useState, useCallback } from 'react';
import { X, AlertCircle, Check, Info, AlertTriangle } from 'lucide-react';
import { clsx } from 'clsx';

export type NotificationType = 'success' | 'error' | 'warning' | 'info';

export interface Notification {
  id: string;
  type: NotificationType;
  title: string;
  message?: string;
  duration?: number;
}

interface NotificationContextType {
  notifications: Notification[];
  notify: (notification: Omit<Notification, 'id'>) => void;
  dismiss: (id: string) => void;
}

export const NotificationContext = React.createContext<NotificationContextType | undefined>(undefined);

export const useNotification = () => {
  const context = React.useContext(NotificationContext);
  if (!context) {
    throw new Error('useNotification must be used within NotificationProvider');
  }
  return context;
};

export const NotificationProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [notifications, setNotifications] = useState<Notification[]>([]);

  const notify = useCallback((notification: Omit<Notification, 'id'>) => {
    const id = Math.random().toString(36).substr(2, 9);
    const newNotification: Notification = { ...notification, id };

    setNotifications((prev) => [...prev, newNotification]);

    if (notification.duration !== 0) {
      const timeout = setTimeout(() => {
        dismiss(id);
      }, notification.duration || 4000);

      return () => clearTimeout(timeout);
    }
  }, []);

  const dismiss = useCallback((id: string) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id));
  }, []);

  return (
    <NotificationContext.Provider value={{ notifications, notify, dismiss }}>
      {children}
      <NotificationContainer notifications={notifications} onDismiss={dismiss} />
    </NotificationContext.Provider>
  );
};

interface NotificationContainerProps {
  notifications: Notification[];
  onDismiss: (id: string) => void;
}

const NotificationContainer: React.FC<NotificationContainerProps> = ({ notifications, onDismiss }) => {
  return (
    <div className="fixed bottom-6 right-6 z-50 space-y-3 pointer-events-none">
      {notifications.map((notification) => (
        <NotificationItem
          key={notification.id}
          notification={notification}
          onDismiss={() => onDismiss(notification.id)}
        />
      ))}
    </div>
  );
};

interface NotificationItemProps {
  notification: Notification;
  onDismiss: () => void;
}

const NotificationItem: React.FC<NotificationItemProps> = ({ notification, onDismiss }) => {
  const typeStyles = {
    success: {
      bg: 'from-emerald-900/50 to-emerald-950/50 border-emerald-700/50',
      icon: <Check className="w-5 h-5 text-emerald-400" />,
      accent: 'bg-emerald-500/10'
    },
    error: {
      bg: 'from-rose-900/50 to-rose-950/50 border-rose-700/50',
      icon: <AlertCircle className="w-5 h-5 text-rose-400" />,
      accent: 'bg-rose-500/10'
    },
    warning: {
      bg: 'from-amber-900/50 to-amber-950/50 border-amber-700/50',
      icon: <AlertTriangle className="w-5 h-5 text-amber-400" />,
      accent: 'bg-amber-500/10'
    },
    info: {
      bg: 'from-blue-900/50 to-blue-950/50 border-blue-700/50',
      icon: <Info className="w-5 h-5 text-blue-400" />,
      accent: 'bg-blue-500/10'
    }
  };

  const style = typeStyles[notification.type];

  return (
    <div
      className={clsx(
        'pointer-events-auto',
        'animate-slide-in',
        'overflow-hidden rounded-xl backdrop-blur-xl transition-all duration-300',
        `bg-gradient-to-br ${style.bg} border`,
        'shadow-lg'
      )}
    >
      <div className="p-4 flex items-start gap-3">
        <div className={clsx('flex-shrink-0 mt-0.5', 'flex items-center')}>{style.icon}</div>

        <div className="flex-1">
          <h3 className="font-semibold text-white">{notification.title}</h3>
          {notification.message && (
            <p className="text-sm text-slate-300 mt-1">{notification.message}</p>
          )}
        </div>

        <button
          onClick={onDismiss}
          className="flex-shrink-0 text-slate-400 hover:text-slate-200 transition-colors"
        >
          <X className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};
