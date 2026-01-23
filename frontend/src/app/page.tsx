'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '../context/auth-context';
import HeroSection from '@/components/HeroSection';

const HomePage: React.FC = () => {
  const { isAuthenticated } = useAuth();

  return (
    <div className="min-h-screen">
      {/* Enhanced Hero Section with Live Demo */}
      <HeroSection />

      {/* Features Section */}
      <div className="relative z-10 px-4 py-20 sm:px-8">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center text-white mb-16">
            Powerful Features for Maximum Productivity
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {/* Feature 1 */}
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all duration-300 transform hover:scale-105">
              <div className="w-12 h-12 bg-gradient-to-r from-pink-500 to-purple-600 rounded-lg mb-4 flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Organize Your Tasks</h3>
              <p className="text-gray-300">Effortlessly categorize and prioritize your tasks with our intuitive drag-and-drop interface.</p>
            </div>

            {/* Feature 2 */}
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all duration-300 transform hover:scale-105">
              <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-blue-600 rounded-lg mb-4 flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Stay Productive</h3>
              <p className="text-gray-300">Focus on what matters most with smart notifications and productivity insights.</p>
            </div>

            {/* Feature 3 */}
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all duration-300 transform hover:scale-105">
              <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-cyan-600 rounded-lg mb-4 flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Simple & Secure</h3>
              <p className="text-gray-300">Enterprise-grade security with a clean, minimalist interface that stays out of your way.</p>
            </div>

            {/* Feature 4 */}
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all duration-300 transform hover:scale-105">
              <div className="w-12 h-12 bg-gradient-to-r from-cyan-500 to-pink-600 rounded-lg mb-4 flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zM21 5a2 2 0 00-2-2h-4a2 2 0 00-2 2v12a4 4 0 004 4h4a2 2 0 002-2V5z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Personalized Experience</h3>
              <p className="text-gray-300">Custom themes, layouts, and preferences tailored to your unique workflow.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;