'use client';

import React, { useState, useEffect, useMemo } from 'react';
import { AdvancedTodo } from '@/types/todo';
import TodoItem from './TodoItem';
import TodoForm from './TodoForm';
import Loading from './Loading';
import { todoService } from '../services/api';
import { useNotification } from '../context/NotificationContext';

interface TodoListProps {}

const TodoList: React.FC<TodoListProps> = () => {
  const { showSuccess, showError, showInfo } = useNotification();
  const [todos, setTodos] = useState<AdvancedTodo[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Filter and sort state
  const [filterPriority, setFilterPriority] = useState<string>('all');
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [filterDueDate, setFilterDueDate] = useState<string>('all');
  const [sortBy, setSortBy] = useState<string>('created_date');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

  useEffect(() => {
    fetchTodos();
  }, [filterPriority, filterStatus, filterDueDate, sortBy, sortOrder]); // Add dependencies for filter/sort

  const fetchTodos = async () => {
    try {
      setLoading(true);
      // Fetch all todos from the API
      const response = await todoService.getAdvanced({});
      const allTodos = response.data;

      // Apply client-side filtering and sorting
      let filteredTodos = allTodos;

      // Apply filters
      if (filterPriority !== 'all') {
        filteredTodos = filteredTodos.filter(todo => todo.priority === filterPriority);
      }

      if (filterStatus !== 'all') {
        if (filterStatus === 'pending') {
          filteredTodos = filteredTodos.filter(todo => !todo.completed);
        } else if (filterStatus === 'completed') {
          filteredTodos = filteredTodos.filter(todo => todo.completed);
        }
      }

      if (filterDueDate !== 'all') {
        const now = new Date();
        if (filterDueDate === 'overdue') {
          filteredTodos = filteredTodos.filter(todo =>
            todo.dueDate && new Date(todo.dueDate) < now && !todo.completed
          );
        } else if (filterDueDate === 'today') {
          const today = new Date();
          today.setHours(0, 0, 0, 0);
          const tomorrow = new Date(today);
          tomorrow.setDate(tomorrow.getDate() + 1);

          filteredTodos = filteredTodos.filter(todo =>
            todo.dueDate &&
            new Date(todo.dueDate) >= today &&
            new Date(todo.dueDate) < tomorrow
          );
        } else if (filterDueDate === 'this_week') {
          const today = new Date();
          const endOfWeek = new Date(today);
          endOfWeek.setDate(today.getDate() + 7); // Next 7 days

          filteredTodos = filteredTodos.filter(todo =>
            todo.dueDate &&
            new Date(todo.dueDate) >= today &&
            new Date(todo.dueDate) <= endOfWeek
          );
        }
      }

      // Apply sorting
      let sortedTodos = [...filteredTodos]; // Create a copy to avoid mutating the original array

      if (sortBy === 'priority') {
        sortedTodos.sort((a, b) => {
          const priorityOrder = { high: 3, medium: 2, low: 1 };
          return sortOrder === 'asc'
            ? priorityOrder[a.priority] - priorityOrder[b.priority]
            : priorityOrder[b.priority] - priorityOrder[a.priority];
        });
      } else if (sortBy === 'due_date') {
        sortedTodos.sort((a, b) => {
          const dateA = a.dueDate ? new Date(a.dueDate).getTime() : Infinity;
          const dateB = b.dueDate ? new Date(b.dueDate).getTime() : Infinity;

          if (sortOrder === 'asc') {
            return dateA - dateB;
          } else {
            return dateB - dateA;
          }
        });
      } else if (sortBy === 'created_date') {
        sortedTodos.sort((a, b) => {
          const timeA = new Date(a.createdAt).getTime();
          const timeB = new Date(b.createdAt).getTime();

          if (sortOrder === 'asc') {
            return timeA - timeB;
          } else {
            return timeB - timeA;
          }
        });
      }

      setTodos(sortedTodos);
      setError(null);
    } catch (err) {
      console.error('Error fetching todos:', err);
      setError('Failed to load todos. Please try again.');
      showError('Failed to load tasks. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleAddTodo = async (title: string, description?: string, priority?: 'low' | 'medium' | 'high', dueDate?: string, tags?: string[], recurrenceRule?: string) => {
    try {
      const newTodo = await todoService.create({ title, description, priority, dueDate, tags, recurrenceRule });
      // Refresh the entire todo list to ensure all filters and sorts are applied correctly
      fetchTodos();
      showSuccess('Task added successfully!');
    } catch (err) {
      console.error('Error adding todo:', err);
      showError('Failed to add task. Please try again.');
    }
  };

  const handleUpdateTodo = async (id: string, updates: Partial<AdvancedTodo>) => {
    try {
      const updatedTodo = await todoService.update(id, updates);
      setTodos(todos.map(todo => (todo.id === id ? updatedTodo.data : todo)));
      showSuccess('Task updated successfully!');
    } catch (err) {
      console.error('Error updating todo:', err);
      showError('Failed to update task. Please try again.');
    }
  };

  const handleDeleteTodo = async (id: string) => {
    try {
      await todoService.delete(id);
      setTodos(todos.filter(todo => todo.id !== id));
      showSuccess('Task deleted successfully!');
    } catch (err) {
      console.error('Error deleting todo:', err);
      showError('Failed to delete task. Please try again.');
    }
  };

  const handleToggleComplete = async (id: string, completed: boolean) => {
    try {
      const updatedTodo = await todoService.toggleComplete(id, !completed);
      setTodos(todos.map(todo => (todo.id === id ? updatedTodo.data : todo)));
      showSuccess(completed ? 'Task marked as pending!' : 'Task completed!');
    } catch (err) {
      console.error('Error toggling todo:', err);
      showError('Failed to update task status. Please try again.');
    }
  };

  if (loading) {
    return <Loading type="spinner" />;
  }

  return (
    <div className="w-full">
      <div className="max-w-2xl mx-auto">
        <h2 className="text-2xl font-bold mb-6 text-center md:text-left text-gray-200">My Todos</h2>

        {error && (
          <div className="bg-red-500/20 border border-red-500 text-red-200 px-4 py-3 rounded-lg mb-6 backdrop-blur-sm">
            {error}
          </div>
        )}

        <TodoForm onAddTodo={handleAddTodo} />

        {/* Filter and Sort Controls */}
        <div className="flex flex-wrap gap-4 mt-6 p-4 bg-white/5 backdrop-blur-sm rounded-xl border border-white/10">
          <div className="flex-1 min-w-[150px]">
            <label className="block text-sm font-medium text-gray-300 mb-1">Priority</label>
            <select
              value={filterPriority}
              onChange={(e) => setFilterPriority(e.target.value)}
              className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-gray-800"
            >
              <option value="all">All Priorities</option>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>

          <div className="flex-1 min-w-[150px]">
            <label className="block text-sm font-medium text-gray-300 mb-1">Status</label>
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-gray-800"
            >
              <option value="all">All Statuses</option>
              <option value="pending">Pending</option>
              <option value="completed">Completed</option>
            </select>
          </div>

          <div className="flex-1 min-w-[150px]">
            <label className="block text-sm font-medium text-gray-300 mb-1">Due Date</label>
            <select
              value={filterDueDate}
              onChange={(e) => setFilterDueDate(e.target.value)}
              className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-gray-800"
            >
              <option value="all">All Dates</option>
              <option value="today">Today</option>
              <option value="this_week">This Week</option>
              <option value="overdue">Overdue</option>
            </select>
          </div>

          <div className="flex-1 min-w-[150px]">
            <label className="block text-sm font-medium text-gray-300 mb-1">Sort By</label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-gray-800"
            >
              <option value="created_date">Created Date</option>
              <option value="due_date">Due Date</option>
              <option value="priority">Priority</option>
            </select>
          </div>

          <div className="flex-1 min-w-[150px]">
            <label className="block text-sm font-medium text-gray-300 mb-1">Order</label>
            <select
              value={sortOrder}
              onChange={(e) => setSortOrder(e.target.value as 'asc' | 'desc')}
              className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-gray-800"
            >
              <option value="desc">Descending</option>
              <option value="asc">Ascending</option>
            </select>
          </div>
        </div>

        {todos.length === 0 ? (
          <div className="text-center py-8 text-gray-400 mt-6">
            No todos match your filters. Add one to get started!
          </div>
        ) : (
          <div className="space-y-3 mt-6">
            {todos.map(todo => (
              <TodoItem
                key={todo.id}
                todo={todo}
                onUpdate={handleUpdateTodo}
                onDelete={handleDeleteTodo}
                onToggleComplete={handleToggleComplete}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default TodoList;