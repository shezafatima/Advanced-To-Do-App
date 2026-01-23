'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNotification } from '@/context/NotificationContext';
import { useAuth } from '@/context/auth-context';
import { todoService } from '@/services/api';
import { AdvancedTodo } from '@/types/todo';
import { useRouter } from 'next/navigation';
import TaskForm from '@/components/TaskForm';
// import TaskItem from '@/components/TaskItem';
import FilterToolbar from '@/components/FilterToolbar';
import SummaryBar from '@/components/SummaryBar';
import ProgressBar from '@/components/ProgressBar';

// Define filter types
type StatusFilter = 'all' | 'completed' | 'pending';
type PriorityFilter = 'all' | 'low' | 'medium' | 'high';

const DashboardPage = () => {
  const [todos, setTodos] = useState<AdvancedTodo[]>([]);
  const [filteredTodos, setFilteredTodos] = useState<AdvancedTodo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Form states
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<'low' | 'medium' | 'high'>('medium');
  const [dueDate, setDueDate] = useState('');
  const [recurrenceRule, setRecurrenceRule] = useState('');
  const [tags, setTags] = useState('');
  const [isAdding, setIsAdding] = useState(false);

  // Filter states
  const [statusFilter, setStatusFilter] = useState<StatusFilter>('all');
  const [priorityFilter, setPriorityFilter] = useState<PriorityFilter>('all');
  const [sortBy, setSortBy] = useState<'createdAt' | 'dueDate' | 'priority'>('createdAt');

  // View mode
  const [viewMode, setViewMode] = useState<'expanded' | 'compact'>('expanded');

  const { showSuccess, showError } = useNotification();
  const { user, isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  // Define functions before useEffect hooks
  const fetchTodos = async () => {
    try {
      setLoading(true);
      const response = await todoService.getAdvanced();
      setTodos(response.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching todos:', err);
      setError('Failed to load tasks. Please try again later.');
      showError('Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const applyFiltersAndSort = () => {
    let result = [...todos];

    // Apply status filter
    if (statusFilter === 'completed') {
      result = result.filter(todo => todo.completed);
    } else if (statusFilter === 'pending') {
      result = result.filter(todo => !todo.completed);
    }

    // Apply priority filter
    if (priorityFilter !== 'all') {
      result = result.filter(todo => todo.priority === priorityFilter);
    }

    // Apply sorting
    result.sort((a, b) => {
      if (sortBy === 'dueDate') {
        if (!a.dueDate && !b.dueDate) return 0;
        if (!a.dueDate) return 1;
        if (!b.dueDate) return -1;
        return new Date(a.dueDate).getTime() - new Date(b.dueDate).getTime();
      } else if (sortBy === 'priority') {
        const priorityOrder: Record<'low' | 'medium' | 'high', number> = { high: 3, medium: 2, low: 1 };
        return priorityOrder[b.priority] - priorityOrder[a.priority];
      } else {
        return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime();
      }
    });

    setFilteredTodos(result);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      showError('Title is required');
      return;
    }

    try {
      setIsAdding(true);

      const tagArray = tags.split(',').map(tag => tag.trim()).filter(tag => tag);

      const newTodo = await todoService.create({
        title,
        description,
        priority,
        dueDate: dueDate || undefined,
        recurrenceRule: recurrenceRule || undefined,
        tags: tagArray
      });

      setTodos([newTodo.data, ...todos]);
      showSuccess('Task added successfully!');

      // Reset form
      setTitle('');
      setDescription('');
      setPriority('medium');
      setDueDate('');
      setRecurrenceRule('');
      setTags('');
    } catch (err) {
      console.error('Error creating todo:', err);
      showError('Failed to add task');
    } finally {
      setIsAdding(false);
    }
  };

  const toggleComplete = async (todo: AdvancedTodo) => {
    try {
      const updatedTodo = await todoService.toggleComplete(todo.id, !todo.completed);
      setTodos(todos.map(t => t.id === todo.id ? updatedTodo.data : t));

      if (todo.completed) {
        showSuccess('Task marked as incomplete');
      } else {
        showSuccess('Task completed!');
      }
    } catch (err) {
      console.error('Error toggling task:', err);
      showError('Failed to update task');
    }
  };

  const deleteTodo = async (id: string) => {
    try {
      await todoService.delete(id);
      setTodos(todos.filter(todo => todo.id !== id));
      showSuccess('Task deleted successfully!');
    } catch (err) {
      console.error('Error deleting todo:', err);
      showError('Failed to delete task');
    }
  };

  const getProgressPercentage = () => {
    if (todos.length === 0) return 0;
    const completedCount = todos.filter(todo => todo.completed).length;
    return Math.round((completedCount / todos.length) * 100);
  };

  const getDailyStreak = () => {
    // Calculate daily streak based on completed tasks
    // For demo purposes, we'll return a random number
    return Math.floor(Math.random() * 10) + 1;
  };

  // Effects must be placed after all functions are defined
  useEffect(() => {
    fetchTodos();
  }, []);

  useEffect(() => {
    applyFiltersAndSort();
  }, [todos, statusFilter, priorityFilter, sortBy]);

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, isLoading, router]);

  // Handle loading and authentication in the main return
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <div className="text-xl text-white">Loading...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null; // Will redirect via useEffect above
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          className="w-12 h-12 border-4 border-purple-500 border-t-transparent rounded-full"
        />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-4 sm:p-6">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-10 animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-pink-500 rounded-full mix-blend-multiply filter blur-xl opacity-10 animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-indigo-500 rounded-full mix-blend-multiply filter blur-xl opacity-5 animate-pulse delay-500"></div>
      </div>

      <div className="max-w-6xl mx-auto relative z-10">
        {/* Welcome Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8 text-center"
        >
          <h1 className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-pink-400 via-purple-400 to-blue-400 bg-clip-text text-transparent mb-2">
            Welcome back, {user?.email}!
          </h1>
          <p className="text-gray-300 text-lg">Organize your tasks efficiently</p>
        </motion.div>

        {/* Top Summary Bar */}
        <SummaryBar
          totalTasks={todos.length}
          completedTasks={todos.filter(t => t.completed).length}
          progressPercentage={getProgressPercentage()}
          dailyStreak={getDailyStreak()}
        />

        {/* Progress Bar */}
        <ProgressBar percentage={getProgressPercentage()} />

        {/* Main Section */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left: Task Input Form */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="lg:col-span-1"
          >
            <div className="sticky top-6">
              <TaskForm
                title={title}
                setTitle={setTitle}
                description={description}
                setDescription={setDescription}
                priority={priority}
                setPriority={setPriority}
                dueDate={dueDate}
                setDueDate={setDueDate}
                recurrenceRule={recurrenceRule}
                setRecurrenceRule={setRecurrenceRule}
                tags={tags}
                setTags={setTags}
                onSubmit={handleSubmit}
                isAdding={isAdding}
              />
            </div>
          </motion.div>

          {/* Right: Task List */}
          <div className="lg:col-span-2">
            {/* Filter Toolbar */}
            <FilterToolbar
              statusFilter={statusFilter}
              setStatusFilter={setStatusFilter}
              priorityFilter={priorityFilter}
              setPriorityFilter={setPriorityFilter}
              sortBy={sortBy}
              setSortBy={setSortBy}
              viewMode={viewMode}
              setViewMode={setViewMode}
            />

            {/* Task List */}
            {error && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
                className="bg-red-500/20 border border-red-500/30 rounded-xl p-4 mb-6 flex items-center justify-between"
              >
                <div className="flex items-center">
                  <svg className="w-5 h-5 text-red-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <span className="text-red-400">{error}</span>
                </div>
                <button
                  onClick={fetchTodos}
                  className="px-3 py-1 bg-red-500/30 text-red-400 rounded-lg hover:bg-red-500/40 transition-colors"
                >
                  Retry
                </button>
              </motion.div>
            )}

            {filteredTodos.length === 0 ? (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.5 }}
                className="bg-white/10 backdrop-blur-sm rounded-2xl border border-white/20 p-12 text-center"
              >
                <div className="text-6xl mb-4">📋</div>
                <h3 className="text-xl font-semibold text-gray-200 mb-2">No tasks found</h3>
                <p className="text-gray-400 mb-4">
                  {statusFilter === 'all'
                    ? "Get started by adding your first task!"
                    : `No ${statusFilter} tasks match your filters.`}
                </p>
                <button
                  onClick={() => {
                    setStatusFilter('all');
                    setPriorityFilter('all');
                  }}
                  className="px-4 py-2 bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-lg hover:from-purple-700 hover:to-indigo-700 transition-all"
                >
                  Clear Filters
                </button>
              </motion.div>
            ) : (
              <AnimatePresence>
                <div className="space-y-3">
                  {filteredTodos.map((todo, index) => (
                    <div key={todo.id} className="p-4 bg-white/10 backdrop-blur-sm rounded-xl border border-white/20">
                      <h3 className={`text-lg font-medium ${todo.completed ? 'line-through text-gray-400' : 'text-gray-200'}`}>
                        {todo.title}
                      </h3>
                      {todo.description && (
                        <p className="text-gray-400 mt-1">{todo.description}</p>
                      )}
                      <div className="flex items-center justify-between mt-3">
                        <span className={`px-2 py-1 rounded-full text-xs ${
                          todo.priority === 'low' ? 'bg-green-500/20 text-green-400' :
                          todo.priority === 'medium' ? 'bg-yellow-500/20 text-yellow-400' :
                          'bg-red-500/20 text-red-400'
                        }`}>
                          {todo.priority}
                        </span>
                        <div className="flex space-x-2">
                          <button
                            onClick={() => toggleComplete(todo)}
                            className={`px-3 py-1 rounded-lg text-sm ${
                              todo.completed
                                ? 'bg-green-500/20 text-green-400'
                                : 'bg-blue-500/20 text-blue-400'
                            }`}
                          >
                            {todo.completed ? 'Undo' : 'Complete'}
                          </button>
                          <button
                            onClick={() => deleteTodo(todo.id)}
                            className="px-3 py-1 bg-red-500/20 text-red-400 rounded-lg text-sm"
                          >
                            Delete
                          </button>
                        </div>
                      </div>
                      {todo.dueDate && (
                        <div className="text-xs text-gray-500 mt-2">
                          Due: {new Date(todo.dueDate).toLocaleDateString()}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </AnimatePresence>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;