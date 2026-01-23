'use client';

import React, { useState, useEffect } from 'react';
import Modal from './Modal';
import { TaskShare, Role } from '@/types/todo';

interface TaskSharingModalProps {
  isOpen: boolean;
  onClose: () => void;
  taskId: string;
  currentShares: TaskShare[];
  onShare: (taskId: string, userEmail: string, role: Role) => Promise<void>;
  onRemoveShare: (taskId: string, userId: string) => Promise<void>;
}

const TaskSharingModal: React.FC<TaskSharingModalProps> = ({
  isOpen,
  onClose,
  taskId,
  currentShares,
  onShare,
  onRemoveShare
}) => {
  const [email, setEmail] = useState<string>('');
  const [role, setRole] = useState<Role>('viewer');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!email.trim()) {
      setError('Email is required');
      return;
    }

    setLoading(true);
    try {
      await onShare(taskId, email.trim(), role);
      setEmail('');
      setRole('viewer');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to share task');
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveShare = async (userId: string) => {
    try {
      await onRemoveShare(taskId, userId);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to remove share');
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <div className="p-6">
        <h2 className="text-2xl font-bold text-gray-200 mb-6">Share Task</h2>

        <form onSubmit={handleSubmit} className="mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-1">
                User Email
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="user@example.com"
                className="w-full px-4 py-2.5 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-white placeholder-gray-400"
                required
              />
            </div>

            <div>
              <label htmlFor="role" className="block text-sm font-medium text-gray-300 mb-1">
                Role
              </label>
              <select
                id="role"
                value={role}
                onChange={(e) => setRole(e.target.value as Role)}
                className="w-full px-4 py-2.5 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-gray-800"
              >
                <option value="viewer">Viewer</option>
                <option value="editor">Editor</option>
                <option value="owner">Owner</option>
              </select>
            </div>
          </div>

          {error && (
            <div className="mt-4 p-3 bg-red-500/20 border border-red-500 text-red-200 rounded-lg">
              {error}
            </div>
          )}

          <div className="mt-6 flex justify-end">
            <button
              type="submit"
              disabled={loading}
              className="px-6 py-2.5 bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-medium rounded-lg hover:from-purple-700 hover:to-indigo-700 transition-all disabled:opacity-50"
            >
              {loading ? 'Sharing...' : 'Share Task'}
            </button>
          </div>
        </form>

        {currentShares.length > 0 && (
          <div>
            <h3 className="text-lg font-medium text-gray-200 mb-4">Shared With</h3>
            <div className="space-y-3">
              {currentShares.map((share) => (
                <div key={share.id} className="flex items-center justify-between p-3 bg-white/5 rounded-lg border border-white/10">
                  <div>
                    <p className="font-medium text-gray-200">User ID: {share.userId}</p>
                    <div className="flex items-center mt-1">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        share.role === 'owner' ? 'bg-purple-100 text-purple-800' :
                        share.role === 'editor' ? 'bg-blue-100 text-blue-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {share.role.charAt(0).toUpperCase() + share.role.slice(1)}
                      </span>
                      <span className="ml-2 text-xs text-gray-400">
                        Shared: {new Date(share.sharedAt).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                  <button
                    onClick={() => handleRemoveShare(share.userId)}
                    className="text-red-400 hover:text-red-300 text-sm"
                  >
                    Remove
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </Modal>
  );
};

export default TaskSharingModal;