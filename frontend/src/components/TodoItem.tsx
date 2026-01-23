'use client';

import React, { useState, memo } from 'react';
import { AdvancedTodo, Priority } from '@/types/todo';
import PriorityIndicator from './ui/PriorityIndicator';
import TagChip from './ui/TagChip';
import DueDateDisplay from './ui/DueDateDisplay';
import { getRecurrenceDescription } from '@/utils/recurrence';

interface TodoItemProps {
  todo: AdvancedTodo;
  onUpdate: (id: string, updates: Partial<AdvancedTodo>) => void;
  onDelete: (id: string) => void;
  onToggleComplete: (id: string, completed: boolean) => void;
}

const TodoItem: React.FC<TodoItemProps> = ({ todo, onUpdate, onDelete, onToggleComplete }) => {
  const [isEditing, setIsEditing] = useState<boolean>(false);
  const [title, setTitle] = useState<string>(todo.title);
  const [description, setDescription] = useState<string>(todo.description || '');
  const [priority, setPriority] = useState<Priority>(todo.priority || 'medium');
  const [dueDate, setDueDate] = useState<string>(todo.dueDate || '');

  // Function to check if current user has specific permission for this task
  const hasPermission = (permission: 'read' | 'write' | 'delete' | 'manage_access'): boolean => {
    // If task has no shares, the owner has all permissions
    if (!todo.shares || todo.shares.length === 0) {
      return true;
    }

    // In a real application, we'd check the current user's permissions
    // For now, we'll assume the current user is the owner (who has all permissions)
    // In a full implementation, we'd check the current user's role in the shares
    return true;
  };

  const handleSave = () => {
    onUpdate(todo.id, { title, description, priority, dueDate });
    setIsEditing(false);
  };

  const handleCancel = () => {
    setTitle(todo.title);
    setDescription(todo.description || '');
    setPriority(todo.priority || 'medium');
    setDueDate(todo.dueDate || '');
    setIsEditing(false);
  };

  const handleDelete = () => {
    onDelete(todo.id);
  };

  const handleToggleComplete = () => {
    onToggleComplete(todo.id, todo.completed);
  };

  return (
    <div
      className={`bg-white/10 backdrop-blur-sm border border-white/20 rounded-lg p-4 transition-all duration-200 ${todo.completed ? 'bg-green-900/20' : 'bg-white/10'} hover:bg-white/20`}
      role="article"
      aria-labelledby={`todo-title-${todo.id}`}
    >
      {isEditing ? (
        <div className="space-y-3 animate-fadeIn">
          <input
            type="text"
            id={`edit-title-${todo.id}`}
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 text-white placeholder-gray-400"
            maxLength={500}
            aria-label="Edit todo title"
            autoFocus
          />
          <textarea
            id={`edit-desc-${todo.id}`}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 text-white placeholder-gray-400"
            rows={2}
            aria-label="Edit todo description"
          />
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            <div>
              <label htmlFor={`edit-priority-${todo.id}`} className="block text-xs text-gray-400 mb-1">Priority</label>
              <select
                id={`edit-priority-${todo.id}`}
                value={priority}
                onChange={(e) => setPriority(e.target.value as Priority)}
                className="w-full px-2 py-1 bg-white/10 border border-white/20 rounded focus:outline-none focus:ring-1 focus:ring-purple-500 text-gray-800 text-sm"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
            <div>
              <label htmlFor={`edit-due-date-${todo.id}`} className="block text-xs text-gray-400 mb-1">Due Date</label>
              <input
                type="date"
                id={`edit-due-date-${todo.id}`}
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
                className="w-full px-2 py-1 bg-white/10 border border-white/20 rounded focus:outline-none focus:ring-1 focus:ring-purple-500 text-gray-800 text-sm"
                min={new Date().toISOString().split('T')[0]}
              />
            </div>
          </div>
          <div className="flex space-x-2">
            <button
              onClick={handleSave}
              className="bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white text-sm py-2 px-4 rounded-lg transition-all duration-200"
              aria-label="Save changes"
            >
              Save
            </button>
            <button
              onClick={handleCancel}
              className="bg-gradient-to-r from-gray-600 to-gray-700 hover:from-gray-700 hover:to-gray-800 text-white text-sm py-2 px-4 rounded-lg transition-all duration-200"
              aria-label="Cancel editing"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div className="space-y-2">
          <div className="flex items-start">
            <input
              type="checkbox"
              id={`complete-${todo.id}`}
              checked={todo.completed}
              onChange={handleToggleComplete}
              className="mt-1 mr-3 h-5 w-5 cursor-pointer accent-pink-500 transition-transform duration-150 hover:scale-110"
              aria-label={todo.completed ? `Mark "${todo.title}" as incomplete` : `Mark "${todo.title}" as complete`}
              aria-describedby={`todo-desc-${todo.id}`}
            />
            <div className="flex-1">
              <h3
                id={`todo-title-${todo.id}`}
                className={`${todo.completed ? 'line-through text-gray-400' : 'text-gray-200'} font-medium transition-colors duration-200`}
                tabIndex={0}
              >
                {todo.title}
              </h3>
              {todo.description && (
                <p
                  id={`todo-desc-${todo.id}`}
                  className={`text-gray-400 text-sm mt-1 ${todo.completed ? 'line-through' : ''} transition-colors duration-200`}
                  tabIndex={0}
                >
                  {todo.description}
                </p>
              )}

              
              <div
                className="flex flex-wrap items-center gap-2 mt-2"
                role="group"
                aria-label="Task properties"
              >
                <PriorityIndicator priority={todo.priority} />

                {todo.dueDate && (
                  <DueDateDisplay dueDate={todo.dueDate} />
                )}

                {todo.tags && todo.tags.length > 0 && (
                  <div className="flex flex-wrap gap-1" aria-label="Tags">
                    {todo.tags.map((tag) => (
                      <TagChip key={tag.id} tag={tag} />
                    ))}
                  </div>
                )}

                {/* Recurrence indicator if the task has recurrence */}
                {todo.recurrenceRule && (
                  <span
                    className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800 border border-purple-200"
                    aria-label={`Recurring task: ${getRecurrenceDescription(todo.recurrenceRule)}`}
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    {getRecurrenceDescription(todo.recurrenceRule)}
                  </span>
                )}

                {/* Shared indicator if the task has shares */}
                {todo.shares && todo.shares.length > 0 && (
                  <span
                    className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 border border-blue-200"
                    aria-label="Shared task"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                    Shared
                  </span>
                )}
              </div>

              <div className="text-xs text-gray-500 mt-2" aria-label={`Created on ${new Date(todo.createdAt).toLocaleDateString()}`}>
                Created: {new Date(todo.createdAt).toLocaleDateString()}
              </div>
            </div>
          </div>
          <div className="flex justify-end space-x-2" role="group" aria-label="Task actions">
            {/* Show Edit button if user has write permissions */}
            {(!todo.shares || todo.shares.length === 0 || hasPermission('write')) && (
              <button
                onClick={() => setIsEditing(true)}
                className="text-pink-400 hover:text-pink-300 text-sm transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-pink-500 focus:rounded-sm"
                aria-label={`Edit "${todo.title}"`}
                tabIndex={0}
              >
                Edit
              </button>
            )}

            {/* Show Delete button if user has delete permissions */}
            {(!todo.shares || todo.shares.length === 0 || hasPermission('delete')) && (
              <button
                onClick={handleDelete}
                className="text-red-400 hover:text-red-300 text-sm transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-red-500 focus:rounded-sm"
                aria-label={`Delete "${todo.title}"`}
                tabIndex={0}
              >
                Delete
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default memo(TodoItem);