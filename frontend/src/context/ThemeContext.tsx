'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';

type Theme = 'dark' | 'light' | 'auto';

interface ThemeContextType {
  theme: Theme;
  setTheme: (theme: Theme) => void;
  resolvedTheme: 'dark' | 'light';
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setThemeState] = useState<Theme>('auto');
  const [resolvedTheme, setResolvedTheme] = useState<'dark' | 'light'>('light');

  // Load theme from localStorage on mount, with fallback to system preference
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') as Theme | null;
    if (savedTheme) {
      setThemeState(savedTheme);
    } else {
      // Default to auto based on system preference
      setThemeState('auto');
    }
  }, []);

  // Apply theme changes to document
  useEffect(() => {
    const root = document.documentElement;

    // Remove existing theme classes
    root.classList.remove('dark', 'light');

    // Determine actual theme based on selection and system preference
    let actualTheme: 'dark' | 'light';
    if (theme === 'auto') {
      actualTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    } else {
      actualTheme = theme;
    }

    // Apply the theme class
    root.classList.add(actualTheme);
    setResolvedTheme(actualTheme);

    // Store the selected theme (not the resolved one) in localStorage
    if (theme !== 'auto') {
      localStorage.setItem('theme', theme);
    } else {
      localStorage.removeItem('theme'); // Remove saved theme when using auto
    }
  }, [theme]);

  // Listen for system theme changes when in auto mode
  useEffect(() => {
    if (theme !== 'auto') return;

    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = () => {
      const newTheme = mediaQuery.matches ? 'dark' : 'light';
      setResolvedTheme(newTheme);
    };

    handleChange(); // Set initial value
    mediaQuery.addEventListener('change', handleChange);

    return () => mediaQuery.removeEventListener('change', handleChange);
  }, [theme]);

  const setTheme = (newTheme: Theme) => {
    setThemeState(newTheme);
  };

  return (
    <ThemeContext.Provider value={{ theme, setTheme, resolvedTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}