'use client';

import React, { createContext, useContext } from 'react';
import toast, { Toaster } from 'react-hot-toast';

interface NotificationContextType {
  // Methods for triggering notifications
  showSuccess: (message: string, duration?: number) => void;
  showError: (message: string, duration?: number) => void;
  showInfo: (message: string, duration?: number) => void;
  showWarning: (message: string, duration?: number) => void;
}

const NotificationContext = createContext<NotificationContextType | undefined>(undefined);

export function NotificationProvider({ children }: { children: React.ReactNode }) {
  const showSuccess = (message: string, duration = 4000) => {
    toast.success(message, {
      duration,
      style: {
        background: '#10b981', // green-500
        color: '#ffffff',
      },
    });
  };

  const showError = (message: string, duration = 4000) => {
    toast.error(message, {
      duration,
      style: {
        background: '#ef4444', // red-500
        color: '#ffffff',
      },
    });
  };

  const showInfo = (message: string, duration = 4000) => {
    toast(message, {
      duration,
      style: {
        background: '#3b82f6', // blue-500
        color: '#ffffff',
      },
    });
  };

  const showWarning = (message: string, duration = 4000) => {
    toast(message, {
      duration,
      style: {
        background: '#f59e0b', // amber-500
        color: '#ffffff',
      },
    });
  };

  return (
    <NotificationContext.Provider value={{ showSuccess, showError, showInfo, showWarning }}>
      {children}
      <Toaster
        position="top-right"
        toastOptions={{
          style: {
            padding: '16px',
            borderRadius: '8px',
            fontSize: '14px',
          },
        }}
      />
    </NotificationContext.Provider>
  );
}

export function useNotification() {
  const context = useContext(NotificationContext);
  if (context === undefined) {
    throw new Error('useNotification must be used within a NotificationProvider');
  }
  return context;
}