'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '@/context/auth-context';
import LoginForm from '@/components/auth/LoginForm';
import { useRouter } from 'next/navigation';

const LoginPage: React.FC = () => {
  const { isAuthenticated } = useAuth();
  const router = useRouter();

  // Redirect if already authenticated
  React.useEffect(() => {
    if (isAuthenticated) {
      router.push('/dashboard');
    }
  }, [isAuthenticated, router]);

  if (isAuthenticated) {
    return null; // Or a loading indicator while redirecting
  }

  return (
    <div className="flex items-center justify-center p-4 min-h-[calc(100vh-120px)]">
      <div className="w-full max-w-md">
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 shadow-2xl">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-white mb-2">Welcome Back</h1>
            <p className="text-gray-300">Sign in to your account to continue</p>
          </div>

          <LoginForm />

          <div className="mt-6 text-center">
            <p className="text-gray-300">
              Don't have an account?{' '}
              <Link
                href="/signup"
                className="text-pink-400 hover:text-pink-300 font-medium transition-colors duration-300"
              >
                Sign up
              </Link>
            </p>
          </div>

          <div className="mt-6 text-center">
            <Link
              href="/"
              className="text-gray-400 hover:text-gray-300 text-sm transition-colors duration-300"
            >
              ← Back to home
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;