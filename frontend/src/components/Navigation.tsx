'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useAuth } from '../context/auth-context';

const Navigation: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const { user, isAuthenticated, logout } = useAuth();

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const handleLogout = () => {
    logout();
  };

  return (
    <header className="bg-slate-900/80 backdrop-blur-md border-b border-white/10 z-50 relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link
              href="/"
              className="text-xl font-bold bg-gradient-to-r from-pink-400 via-purple-400 to-blue-400 bg-clip-text text-transparent cursor-pointer"
              onClick={() => setIsMenuOpen(false)}
            >
              Todo App
            </Link>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-6 z-50">
            {isAuthenticated ? (
              <>
                <Link
                  href="/dashboard"
                  className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors duration-300 cursor-pointer relative z-50"
                  prefetch={false}
                >
                  Dashboard
                </Link>
                <Link
                  href="/profile"
                  className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors duration-300 cursor-pointer relative z-50"
                  prefetch={false}
                >
                  Profile
                </Link>
                <span className="text-gray-400 text-sm relative z-50">Welcome, {user?.email}</span>
                <button
                  onClick={handleLogout}
                  className="bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-all duration-300 cursor-pointer relative z-50"
                  type="button"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link
                  href="/login"
                  className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors duration-300 cursor-pointer relative z-50"
                  prefetch={false}
                >
                  Login
                </Link>
                <Link
                  href="/signup"
                  className="bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-all duration-300 cursor-pointer relative z-50"
                  prefetch={false}
                >
                  Sign Up
                </Link>
              </>
            )}
          </nav>

          {/* Mobile menu button */}
          <div className="flex items-center md:hidden relative z-50">
            <button
              onClick={toggleMenu}
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-300 hover:text-white hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-pink-500 cursor-pointer relative z-50"
              aria-expanded="false"
              type="button"
            >
              <span className="sr-only">Open main menu</span>
              {/* Hamburger icon */}
              <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="md:hidden relative z-40">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-slate-800/90 backdrop-blur-md">
            {isAuthenticated ? (
              <>
                <Link
                  href="/dashboard"
                  className="block px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-white hover:bg-white/10 cursor-pointer"
                  onClick={() => setIsMenuOpen(false)}
                  prefetch={false}
                >
                  Dashboard
                </Link>
                <Link
                  href="/profile"
                  className="block px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-white hover:bg-white/10 cursor-pointer"
                  onClick={() => setIsMenuOpen(false)}
                  prefetch={false}
                >
                  Profile
                </Link>
                <div className="block px-3 py-2 text-base font-medium text-gray-400">
                  Welcome, {user?.email}
                </div>
                <button
                  onClick={() => {
                    handleLogout();
                    setIsMenuOpen(false);
                  }}
                  className="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-white bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 cursor-pointer"
                  type="button"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link
                  href="/login"
                  className="block px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-white hover:bg-white/10 cursor-pointer"
                  onClick={() => setIsMenuOpen(false)}
                  prefetch={false}
                >
                  Login
                </Link>
                <Link
                  href="/signup"
                  className="block px-3 py-2 rounded-md text-base font-medium text-white bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 cursor-pointer"
                  onClick={() => setIsMenuOpen(false)}
                  prefetch={false}
                >
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </header>
  );
};

export default Navigation;