'use client';

import React, { useState } from 'react';
import { Priority } from '@/types/todo';
import PriorityIndicator from './ui/PriorityIndicator';
import TagChip from './ui/TagChip';

interface TodoFormProps {
  onAddTodo: (title: string, description?: string, priority?: Priority, dueDate?: string, tags?: string[], recurrenceRule?: string) => void;
}

const TodoForm: React.FC<TodoFormProps> = ({ onAddTodo }) => {
  const [title, setTitle] = useState<string>('');
  const [description, setDescription] = useState<string>('');
  const [priority, setPriority] = useState<Priority>('medium');
  const [dueDate, setDueDate] = useState<string>('');
  const [recurrenceRule, setRecurrenceRule] = useState<string>('');
  const [tagInput, setTagInput] = useState<string>('');
  const [tags, setTags] = useState<string[]>([]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (title.trim()) {
      onAddTodo(title, description, priority, dueDate, tags, recurrenceRule);
      // Reset form
      resetForm();
    }
  };

  const resetForm = () => {
    setTitle('');
    setDescription('');
    setPriority('medium');
    setDueDate('');
    setRecurrenceRule('');
    setTags([]);
  };

  const handleAddTag = () => {
    if (tagInput.trim() && !tags.includes(tagInput.trim())) {
      setTags([...tags, tagInput.trim()]);
      setTagInput('');
    }
  };

  const handleRemoveTag = (tagToRemove: string) => {
    setTags(tags.filter(tag => tag !== tagToRemove));
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddTag();
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-6 p-4 bg-white/5 backdrop-blur-sm rounded-xl border border-white/10 shadow-lg">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div className="space-y-2">
          <label htmlFor="title" className="block text-sm font-medium text-gray-300">Title *</label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Add a new task..."
            className="w-full px-4 py-2.5 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-white placeholder-gray-400"
            maxLength={500}
            required
            aria-label="Task title"
          />
        </div>

        <div className="space-y-2">
          <label htmlFor="priority" className="block text-sm font-medium text-gray-300">Priority</label>
          <select
            id="priority"
            value={priority}
            onChange={(e) => setPriority(e.target.value as Priority)}
            className="w-full px-4 py-2.5 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-gray-800"
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
          <div className="mt-1">
            <PriorityIndicator priority={priority} />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div className="space-y-2">
          <label htmlFor="dueDate" className="block text-sm font-medium text-gray-300">Due Date</label>
          <input
            id="dueDate"
            type="date"
            value={dueDate}
            onChange={(e) => setDueDate(e.target.value)}
            className="w-full px-4 py-2.5 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-white"
            min={new Date().toISOString().split('T')[0]} // Only allow future dates
            aria-describedby="dueDateHelp"
          />
          <small id="dueDateHelp" className="text-xs text-gray-400">Leave blank for no due date</small>
        </div>

        <div className="space-y-2">
          <label htmlFor="recurrence" className="block text-sm font-medium text-gray-300">Recurrence</label>
          <select
            id="recurrence"
            value={recurrenceRule}
            onChange={(e) => setRecurrenceRule(e.target.value)}
            className="w-full px-4 py-2.5 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-gray-800"
            aria-describedby="recurrenceHelp"
          >
            <option value="">No recurrence</option>
            <option value="FREQ=DAILY;INTERVAL=1">Daily</option>
            <option value="FREQ=WEEKLY;INTERVAL=1">Weekly</option>
            <option value="FREQ=MONTHLY;INTERVAL=1">Monthly</option>
            <option value="FREQ=DAILY;INTERVAL=7">Every 7 days</option>
            <option value="FREQ=WEEKLY;INTERVAL=2">Bi-weekly</option>
            <option value="FREQ=MONTHLY;INTERVAL=3">Quarterly</option>
          </select>
          <small id="recurrenceHelp" className="text-xs text-gray-400">Select recurrence pattern</small>
        </div>
      </div>

      <div className="space-y-2 mb-4">
        <label htmlFor="tags" className="block text-sm font-medium text-gray-300">Tags</label>
        <div className="flex">
          <input
            id="tags"
            type="text"
            value={tagInput}
            onChange={(e) => setTagInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Add a tag..."
            className="flex-1 px-4 py-2.5 bg-white/10 border border-white/20 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-white placeholder-gray-400"
            aria-label="Add tag"
          />
          <button
            type="button"
            onClick={handleAddTag}
            className="bg-gradient-to-r from-purple-600 to-indigo-600 text-white px-4 py-2.5 rounded-r-lg hover:from-purple-700 hover:to-indigo-700 transition-colors"
            aria-label="Add tag"
          >
            +
          </button>
        </div>
        {tags.length > 0 && (
          <div className="flex flex-wrap gap-2 mt-2" role="group" aria-label="Added tags">
            {tags.map((tag, index) => (
              <div key={index} className="relative inline-block" role="group" aria-label={`Tag: ${tag}`}>
                <TagChip
                  tag={{ id: index.toString(), name: tag, color: '#8b5cf6', createdAt: new Date().toISOString() }}
                  className="mr-1"
                />
                <button
                  type="button"
                  onClick={() => handleRemoveTag(tag)}
                  className="absolute -top-1.5 -right-1.5 bg-red-500 text-white rounded-full w-4 h-4 flex items-center justify-center text-xs hover:bg-red-600 transition-colors"
                  aria-label={`Remove tag ${tag}`}
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="space-y-2 mb-4">
        <label htmlFor="description" className="block text-sm font-medium text-gray-300">Description</label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Task details (optional)"
          className="w-full px-4 py-2.5 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-white placeholder-gray-400"
          rows={2}
          aria-label="Task description"
        />
      </div>

      <button
        type="submit"
        className="w-full md:w-auto bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-300 transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
        disabled={!title.trim()}
      >
        Add Task
      </button>
    </form>
  );
};

export default TodoForm;