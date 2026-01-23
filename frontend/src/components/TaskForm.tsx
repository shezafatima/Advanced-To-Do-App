import React from 'react';
import { motion } from 'framer-motion';
import PriorityIndicator from './ui/PriorityIndicator';

interface TaskFormProps {
  title: string;
  setTitle: (title: string) => void;
  description: string;
  setDescription: (description: string) => void;
  priority: 'low' | 'medium' | 'high';
  setPriority: (priority: 'low' | 'medium' | 'high') => void;
  dueDate: string;
  setDueDate: (dueDate: string) => void;
  recurrenceRule: string;
  setRecurrenceRule: (recurrenceRule: string) => void;
  tags: string;
  setTags: (tags: string) => void;
  onSubmit: (e: React.FormEvent) => void;
  isAdding: boolean;
}

const TaskForm: React.FC<TaskFormProps> = ({
  title,
  setTitle,
  description,
  setDescription,
  priority,
  setPriority,
  dueDate,
  setDueDate,
  recurrenceRule,
  setRecurrenceRule,
  tags,
  setTags,
  onSubmit,
  isAdding
}) => {
  return (
    <div className="bg-white/10 backdrop-blur-sm rounded-2xl border border-white/20 p-6">
      <h2 className="text-xl font-semibold text-gray-200 mb-4">Add New Task</h2>

      <form onSubmit={onSubmit}>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Title *</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="What needs to be done?"
              className="w-full px-4 py-2.5 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-white placeholder-gray-400 transition-all duration-200 hover:scale-[1.02]"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Description</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Add details..."
              rows={3}
              className="w-full px-4 py-2.5 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-white placeholder-gray-400 resize-none transition-all duration-200 hover:scale-[1.02]"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Priority</label>
            <div className="flex gap-2">
              {(['low', 'medium', 'high'] as const).map((prio) => (
                <button
                  key={prio}
                  type="button"
                  onClick={() => setPriority(prio)}
                  className={`flex-1 py-2 rounded-lg transition-all ${
                    priority === prio
                      ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white'
                      : 'bg-white/10 text-gray-300 hover:bg-white/20'
                  }`}
                >
                  <PriorityIndicator priority={prio} />
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Due Date</label>
            <input
              type="date"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
              className="w-full px-4 py-2.5 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-white"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Recurrence</label>
            <select
              value={recurrenceRule}
              onChange={(e) => setRecurrenceRule(e.target.value)}
              className="w-full px-4 py-2.5 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-gray-800"
            >
              <option value="">No recurrence</option>
              <option value="FREQ=DAILY">Daily</option>
              <option value="FREQ=WEEKLY">Weekly</option>
              <option value="FREQ=MONTHLY">Monthly</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Tags</label>
            <input
              type="text"
              value={tags}
              onChange={(e) => setTags(e.target.value)}
              placeholder="work, personal, urgent (comma separated)"
              className="w-full px-4 py-2.5 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-white placeholder-gray-400"
            />
          </div>

          <motion.button
            type="submit"
            disabled={isAdding}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="w-full px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white font-medium rounded-lg hover:from-green-600 hover:to-emerald-700 transition-all disabled:opacity-50"
          >
            {isAdding ? 'Adding...' : 'Add Task'}
          </motion.button>
        </div>
      </form>
    </div>
  );
};

export default TaskForm;