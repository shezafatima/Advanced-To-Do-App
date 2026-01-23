'use client';

import React from 'react';
import { useAuth } from '../context/auth-context';
import { useRouter, usePathname } from 'next/navigation';
import { useEffect } from 'react';

interface AuthGuardProps {
  children: React.ReactNode;
  requireAuth?: boolean; // If true, requires authentication; if false, redirects away if authenticated
}

const AuthGuard: React.FC<AuthGuardProps> = ({ children, requireAuth = true }) => {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (!isLoading) {
      // If this is an auth-guarded route but user is not authenticated
      if (requireAuth && !isAuthenticated) {
        router.push('/login');
      }
      // If this is a non-auth-guarded route (like login/signup) but user is authenticated
      else if (!requireAuth && isAuthenticated) {
        router.push('/dashboard');
      }
    }
  }, [isAuthenticated, isLoading, requireAuth, router]);

  // Show loading state while checking auth
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  // If auth requirements are met, render children
  if (
    (requireAuth && isAuthenticated) ||
    (!requireAuth && !isAuthenticated)
  ) {
    return <>{children}</>;
  }

  // Otherwise, return nothing while redirecting
  return null;
};

export default AuthGuard;