'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User, UserRegistration, UserLogin, AuthResponse } from '../../../shared/types/user';
import { authService } from '../services/api';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: UserLogin) => Promise<void>;
  register: (userData: UserRegistration) => Promise<void>;
  logout: () => void;
  checkAuthStatus: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);

  // Check authentication status and set up token refresh
  useEffect(() => {
    checkAuthStatus();

    // Set up interval to check token validity periodically (every 10 minutes)
    const interval = setInterval(() => {
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          // Decode JWT to check expiration
          const tokenParts = token.split('.');
          if (tokenParts.length === 3) {
            const payload = JSON.parse(atob(tokenParts[1]));
            const currentTime = Math.floor(Date.now() / 1000);

            // If token expires in less than 5 minutes, refresh it
            if (payload.exp - currentTime < 300) {
              // In a real app, we would call a refresh token endpoint
              // For now, we'll just redirect to login
              logout();
            }
          }
        } catch (error) {
          console.error('Error decoding token:', error);
          logout();
        }
      }
    }, 600000); // 10 minutes

    return () => clearInterval(interval);
  }, []);

  const checkAuthStatus = async () => {
    const token = localStorage.getItem('access_token');

    if (!token) {
      setIsLoading(false);
      setIsAuthenticated(false);
      return;
    }

    try {
      const response = await authService.getCurrentUser();
      setUser(response.data);
      setIsAuthenticated(true);
    } catch (error) {
      console.error('Failed to verify authentication:', error);
      localStorage.removeItem('access_token');
      setIsAuthenticated(false);
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (credentials: UserLogin) => {
    try {
      const response = await authService.login(credentials.email, credentials.password);

      if (response.data.access_token) {
        localStorage.setItem('access_token', response.data.access_token);

        // Get user info after login
        const userInfo = await authService.getCurrentUser();
        setUser(userInfo.data);
        setIsAuthenticated(true);
      }
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };

  const register = async (userData: UserRegistration) => {
    try {
      const response = await authService.register(userData.email, userData.password);

      if (response.data.access_token) {
        localStorage.setItem('access_token', response.data.access_token);

        // Get user info after registration
        const userInfo = await authService.getCurrentUser();
        setUser(userInfo.data);
        setIsAuthenticated(true);
      }
    } catch (error) {
      console.error('Registration failed:', error);
      throw error;
    }
  };

  const logout = () => {
    authService.logout();
    setUser(null);
    setIsAuthenticated(false);
  };

  const value = {
    user,
    isAuthenticated,
    isLoading,
    login,
    register,
    logout,
    checkAuthStatus
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};