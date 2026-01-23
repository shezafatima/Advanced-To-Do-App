import { defineRouting } from 'next-intl/routing';
import { createNavigation } from 'next-intl/navigation';

export const routing = defineRouting({
  // A list of all locales that are supported
  locales: ['en', 'ur'],

  // Used when no locale matches
  defaultLocale: 'en',

  // If you set this to true, only URLs with a locale prefix will be handled
  localePrefix: 'always', // Default
});

// Lightweight navigation wrapper:
// If locales are configured, `navigate` and `useParams` are already i18n-aware
// This is only needed to make them work if no locales are configured
export const { Link, redirect, usePathname, useRouter } = createNavigation(routing);