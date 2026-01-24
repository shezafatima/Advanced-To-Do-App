/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:3000",
    NEXT_PUBLIC_BETTER_AUTH_URL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || ""
  },
  // Don't use output: 'export' for dynamic apps
  // Images config for when needed
  images: {
    domains: ['lh3.googleusercontent.com', 'avatars.githubusercontent.com'], // Add any image domains you use
  },
};

module.exports = nextConfig;