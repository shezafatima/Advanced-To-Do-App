'use client';

import { notFound } from 'next/navigation';
import { createNavigation } from 'next-intl/navigation';
import { routing } from './routing';

// Create the navigation functions based on the routing config
export const { Link, redirect, usePathname, useRouter } = createNavigation(routing);

// Define the available locales
export const locales = ['en', 'ur'] as const;

// Default locale
export const defaultLocale = 'en';

// Helper functions
export const getLocale = async () => {
  // This would typically come from a context or header
  return defaultLocale;
};