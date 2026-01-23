'use client';

import React, { useState } from 'react';
import { UserLogin } from '../../../../shared/types/user';
import { useAuth } from '../../context/auth-context';

interface LoginFormProps {
  onSwitchToSignup?: () => void;
}

const LoginForm: React.FC<LoginFormProps> = ({ onSwitchToSignup }) => {
  const [formData, setFormData] = useState<UserLogin>({
    email: '',
    password: ''
  });
  const [error, setError] = useState<string | null>(null);
  const { login } = useAuth();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      await login(formData);
      setError(null);
    } catch (err) {
      setError('Invalid email or password. Please try again.');
      console.error('Login error:', err);
    }
  };

  return (
    <>
      {error && (
        <div className="bg-red-500/20 border border-red-500 text-red-200 px-4 py-3 rounded-lg mb-6 backdrop-blur-sm">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="mb-6">
          <label htmlFor="email" className="block text-gray-300 text-sm font-medium mb-2">
            Email
          </label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 text-white placeholder-gray-400"
            placeholder="your@email.com"
          />
        </div>

        <div className="mb-6">
          <label htmlFor="password" className="block text-gray-300 text-sm font-medium mb-2">
            Password
          </label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 text-white placeholder-gray-400"
            placeholder="••••••••"
          />
        </div>

        <button
          type="submit"
          className="w-full bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white font-semibold py-3 px-4 rounded-lg transition-all duration-300 transform hover:scale-[1.02]"
        >
          Sign In
        </button>
      </form>

      {onSwitchToSignup && (
        <div className="mt-6 text-center">
          <p className="text-gray-400">
            Don't have an account?{' '}
            <button
              onClick={onSwitchToSignup}
              className="text-pink-400 hover:text-pink-300 font-medium transition-colors duration-300"
            >
              Sign up
            </button>
          </p>
        </div>
      )}
    </>
  );
};

export default LoginForm;