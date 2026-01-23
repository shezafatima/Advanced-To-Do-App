import React from 'react';
import { motion } from 'framer-motion';

type StatusFilter = 'all' | 'completed' | 'pending';
type PriorityFilter = 'all' | 'low' | 'medium' | 'high';

interface FilterToolbarProps {
  statusFilter: StatusFilter;
  setStatusFilter: (filter: StatusFilter) => void;
  priorityFilter: PriorityFilter;
  setPriorityFilter: (filter: PriorityFilter) => void;
  sortBy: 'createdAt' | 'dueDate' | 'priority';
  setSortBy: (sort: 'createdAt' | 'dueDate' | 'priority') => void;
  viewMode: 'expanded' | 'compact';
  setViewMode: (mode: 'expanded' | 'compact') => void;
}

const FilterToolbar: React.FC<FilterToolbarProps> = ({
  statusFilter,
  setStatusFilter,
  priorityFilter,
  setPriorityFilter,
  sortBy,
  setSortBy,
  viewMode,
  setViewMode
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      className="sticky top-6 z-10 bg-white/10 backdrop-blur-sm rounded-xl border border-white/20 p-4 mb-6"
    >
      <div className="flex flex-wrap gap-4 items-center justify-between">
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setStatusFilter('all')}
            className={`px-3 py-1.5 rounded-md text-sm font-medium ${
              statusFilter === 'all'
                ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white'
                : 'bg-white/10 text-gray-300 hover:bg-white/20'
            }`}
          >
            All
          </button>
          <button
            onClick={() => setStatusFilter('pending')}
            className={`px-3 py-1.5 rounded-md text-sm font-medium ${
              statusFilter === 'pending'
                ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white'
                : 'bg-white/10 text-gray-300 hover:bg-white/20'
            }`}
          >
            Pending
          </button>
          <button
            onClick={() => setStatusFilter('completed')}
            className={`px-3 py-1.5 rounded-md text-sm font-medium ${
              statusFilter === 'completed'
                ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white'
                : 'bg-white/10 text-gray-300 hover:bg-white/20'
            }`}
          >
            Completed
          </button>
        </div>

        <div className="flex flex-wrap gap-2">
          <select
            value={priorityFilter}
            onChange={(e) => setPriorityFilter(e.target.value as PriorityFilter)}
            className="px-3 py-1.5 bg-white/10 border border-white/20 rounded-md text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-purple-500"
          >
            <option value="all">All Priorities</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>

          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
            className="px-3 py-1.5 bg-white/10 border border-white/20 rounded-md text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-purple-500"
          >
            <option value="createdAt">Newest First</option>
            <option value="dueDate">Due Date</option>
            <option value="priority">Priority</option>
          </select>

          <button
            onClick={() => setViewMode(viewMode === 'expanded' ? 'compact' : 'expanded')}
            className="px-3 py-1.5 bg-white/10 text-gray-300 rounded-md text-sm hover:bg-white/20"
          >
            {viewMode === 'expanded' ? 'Compact View' : 'Expanded View'}
          </button>
        </div>
      </div>
    </motion.div>
  );
};

export default FilterToolbar;