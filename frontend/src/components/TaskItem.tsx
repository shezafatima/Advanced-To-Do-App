import React from 'react';
import { motion } from 'framer-motion';
import { PriorityIndicator } from './ui/PriorityIndicator';
import { TagChip } from './ui/TagChip';
import { AdvancedTodo, Tag } from '@/types/todo';

interface TaskItemProps {
  todo: AdvancedTodo;
  onToggleComplete: (todo: AdvancedTodo) => void;
  onDelete: (id: string) => void;
  viewMode: 'expanded' | 'compact';
}

const TaskItem: React.FC<TaskItemProps> = ({ todo, onToggleComplete, onDelete, viewMode }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.8 }}
      transition={{ duration: 0.3 }}
      whileHover={{ y: -2, boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.25)' }}
      className={`p-4 rounded-xl backdrop-blur-sm border ${
        todo.completed
          ? 'bg-green-500/10 border-green-500/30'
          : viewMode === 'expanded'
            ? 'bg-white/10 border-white/20'
            : 'bg-white/5 border-white/10'
      } transition-all duration-200`}
    >
      <div className={`flex items-start gap-3 ${viewMode === 'compact' ? 'items-center' : ''}`}>
        <button
          onClick={() => onToggleComplete(todo)}
          className={`flex-shrink-0 w-5 h-5 rounded-full border-2 flex items-center justify-center mt-1 transition-all ${
            todo.completed
              ? 'bg-green-500 border-green-500 scale-110'
              : 'border-gray-400 hover:border-purple-400 hover:scale-110'
          }`}
        >
          {todo.completed && (
            <motion.svg
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              className="w-3 h-3 text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
            </motion.svg>
          )}
        </button>

        <div className="flex-1 min-w-0">
          <div className={`font-medium ${todo.completed ? 'text-gray-400 line-through' : 'text-gray-200'}`}>
            {todo.title}
          </div>

          {viewMode === 'expanded' && todo.description && (
            <div className="text-sm text-gray-400 mt-1">{todo.description}</div>
          )}

          <div className="flex flex-wrap gap-2 mt-2">
            <PriorityIndicator priority={todo.priority} />

            {todo.tags.map((tag: Tag) => (
              <TagChip key={tag.id} tag={tag} />
            ))}

            {todo.dueDate && (
              <span className={`px-2 py-1 rounded-full text-xs ${
                new Date(todo.dueDate) < new Date() && !todo.completed
                  ? 'bg-red-500/20 text-red-400'
                  : 'bg-blue-500/20 text-blue-400'
              }`}>
                {new Date(todo.dueDate).toLocaleDateString()}
              </span>
            )}

            {todo.recurrenceRule && (
              <span className="px-2 py-1 rounded-full text-xs bg-purple-500/20 text-purple-400">
                🔁 Recurring
              </span>
            )}
          </div>
        </div>

        <div className="flex items-center gap-2">
          {viewMode === 'expanded' && (
            <span className="text-xs text-gray-500">
              {new Date(todo.createdAt).toLocaleDateString()}
            </span>
          )}
          <button
            onClick={() => onDelete(todo.id)}
            className="flex-shrink-0 text-gray-400 hover:text-red-400 transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
            </svg>
          </button>
        </div>
      </div>
    </motion.div>
  );
};

export default TaskItem;