'use client';

import { createI18nClient } from 'next-intl';
import { notFound } from 'next/navigation';
import { routing } from './routing';

export const { getTranslations, getLocale, getRequestConfig } = createI18nClient({
  // Provide all locales that are supported
  locales: ['en', 'ur'],

  // If a locale is not provided, use this as the default
  defaultLocale: 'en',

  // If a locale is not found, use this as the fallback
  onError: (error) => {
    if (error.code === 'MISSING_NAMESPACE') {
      // Safely ignore this error
      return;
    }

    console.error(error);
  },

  // Used to redirect to the root page when a locale is detected
  routing,

  // Used to load translations
  loadLocale: async (locale) => {
    const messages = (await import(`../messages/${locale}.json`)).default;
    return messages;
  }
});