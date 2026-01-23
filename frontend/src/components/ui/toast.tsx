/**
 * Toast notifications for user feedback in the Todo Full-Stack Web Application.
 *
 * This component provides visual feedback for user actions and system events.
 */

import React from 'react';
import { Toaster, toast } from 'react-hot-toast';

interface ToastProps {
  position?: 'top-left' | 'top-center' | 'top-right' | 'bottom-left' | 'bottom-center' | 'bottom-right';
}

const ToastProvider: React.FC<ToastProps> = ({ position = 'top-right' }) => {
  return (
    <Toaster
      position={position}
      toastOptions={{
        // Define default options
        className: '',
        duration: 4000,
        style: {
          background: '#363636',
          color: '#fff',
        },

        // Default options for specific types
        success: {
          duration: 3000,
          style: {
            background: '#28a745',
            color: '#fff',
          },
        },

        error: {
          duration: 5000,
          style: {
            background: '#dc3545',
            color: '#fff',
          },
        },

        loading: {
          style: {
            background: '#6c757d',
            color: '#fff',
          },
        },
      }}
    />
  );
};

// Export toast functions for use in other components
export { toast, ToastProvider };

export default ToastProvider;