'use client';

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';
import { useAuth } from '@/context/auth-context';

// Define the priority enum
type Priority = 'low' | 'medium' | 'high';

// Define the tag type
interface Tag {
  id: string;
  name: string;
  color: string;
  createdAt: string;
}

// Define the todo type
interface Todo {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  userId: string;
  priority: Priority;
  dueDate?: string;
  recurrenceRule?: string;
  tags: Tag[];
  createdAt: string;
  updatedAt: string;
}

// Mock data for the demo - reduced number for better visibility
const initialDemoTasks: Todo[] = [
{
  id: '1',
  title: 'Pay utility bills',
  description: 'Pay electricity and internet bills before the due date',
  completed: false,
  userId: 'demo',
  priority: 'high',
  dueDate: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000).toISOString(),
  tags: [
    {
      id: 'tag1',
      name: 'Personal',
      color: '#10B981',
      createdAt: new Date().toISOString(),
    }
  ],
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
},
  {
    id: '2',
    title: 'Team meeting',
    description: 'Weekly team sync meeting',
    completed: false,
    userId: 'demo',
    priority: 'medium',
    dueDate: new Date(Date.now() + 1 * 24 * 60 * 60 * 1000).toISOString(),
    tags: [{ id: 'tag2', name: 'Meeting', color: '#3B82F6', createdAt: new Date().toISOString() }],
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  },
];

const HeroSection = () => {
  const [tasks, setTasks] = useState<Todo[]>(initialDemoTasks);
  const [newTask, setNewTask] = useState('');
  const [priority, setPriority] = useState<Priority>('medium');
  const [tags, setTags] = useState<string>('');
  const [timeGreeting, setTimeGreeting] = useState('Good morning');
  const [demoStep, setDemoStep] = useState(0);
  const [currentMessage, setCurrentMessage] = useState('Adding tasks is now easier than ever');
  const inputRef = useRef<HTMLInputElement>(null);
  const demoTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const { user } = useAuth();

  // Auto-demo sequence
  const demoSequence = [
    { action: 'add', message: 'Adding tasks is now easier than ever' },
    { action: 'edit', message: 'Edit and manage your tasks seamlessly' },
    { action: 'delete', message: 'Delete tasks with one click' },
    { action: 'prioritize', message: 'Prioritize your tasks effectively' },
    { action: 'organize', message: 'Make your tasks manageable and organized' },
  ];

  useEffect(() => {
    // Set time-based greeting
    const hour = new Date().getHours();
    if (hour < 12) setTimeGreeting('Good morning');
    else if (hour < 18) setTimeGreeting('Good afternoon');
    else setTimeGreeting('Good evening');
  }, []);

  // Auto-demo sequence with visual indicators
  useEffect(() => {
    if (demoStep < demoSequence.length) {
      const currentStep = demoSequence[demoStep];
      setCurrentMessage(currentStep.message);

      demoTimeoutRef.current = setTimeout(() => {
        switch (currentStep.action) {
          case 'add':
            // Add the same demo task that's shown in the typing effect, but limit total tasks
            if (tasks.length < 6) { // Limit to 6 tasks for better visibility
              const newTodo: Todo = {
                id: `demo-${Date.now()}`,
                title: 'Complete the project proposal',
                completed: false,
                userId: 'demo',
                priority: 'high',
                tags: [{ id: 'tag-auto', name: 'work', color: '#F59E0B', createdAt: new Date().toISOString() }],
                createdAt: new Date().toISOString(),
                updatedAt: new Date().toISOString(),
              };
              setTasks(prev => [...prev, newTodo]);
            }
            break;

          case 'edit':
            // Ensure there are tasks to edit before attempting to edit
            if (tasks.length > 0) {
              const tasksCopy = [...tasks]; // Create a copy to avoid closure issues
              const firstTask = tasksCopy[0];
              if (firstTask) {
                setEditingTaskVisual(firstTask.id);
                // Toggle the completion status of the first task
                setTasks(prev => prev.map(task =>
                  task.id === firstTask.id ? { ...task, completed: !task.completed } : task
                ));
                setTimeout(() => {
                  setEditingTaskVisual(null);
                }, 500);
              }
            } else {
              // If no tasks exist, add a task first then edit it
              const tempTask: Todo = {
                id: `temp-${Date.now()}`,
                title: 'Temporary task for edit demo',
                completed: false,
                userId: 'demo',
                priority: 'medium',
                tags: [],
                createdAt: new Date().toISOString(),
                updatedAt: new Date().toISOString(),
              };
              setTasks(prev => [...prev, tempTask]);

              // Then edit it after a short delay
              setTimeout(() => {
                setEditingTaskVisual(tempTask.id);
                setTasks(prev => prev.map(task =>
                  task.id === tempTask.id ? { ...task, completed: true } : task
                ));
                setTimeout(() => {
                  setEditingTaskVisual(null);
                }, 500);
              }, 300);
            }
            break;

          case 'delete':
            // Ensure there are tasks to delete before attempting to delete
            if (tasks.length > 0) {
              const tasksCopy = [...tasks]; // Create a copy to avoid closure issues
              const lastTask = tasksCopy[tasksCopy.length - 1];
              if (lastTask) {
                setDeletingTaskId(lastTask.id);
                setTimeout(() => {
                  setTasks(prev => prev.filter(task => task.id !== lastTask.id)); // Use filter to ensure correct task is removed
                  setDeletingTaskId(null);
                }, 500);
              }
            } else {
              // If no tasks exist, add a task first then delete it
              const tempTask: Todo = {
                id: `temp-${Date.now()}`,
                title: 'Temporary task for delete demo',
                completed: false,
                userId: 'demo',
                priority: 'medium',
                tags: [],
                createdAt: new Date().toISOString(),
                updatedAt: new Date().toISOString(),
              };
              setTasks(prev => [...prev, tempTask]);

              // Then delete it after a short delay
              setTimeout(() => {
                setDeletingTaskId(tempTask.id);
                setTimeout(() => {
                  setTasks(prev => prev.filter(task => task.id !== tempTask.id));
                  setDeletingTaskId(null);
                }, 500);
              }, 300);
            }
            break;

          case 'prioritize':
            // Ensure there are tasks to prioritize before attempting to prioritize
            if (tasks.length > 0) {
              const tasksCopy = [...tasks]; // Create a copy to avoid closure issues
              const firstTask = tasksCopy[0];
              if (firstTask) {
                setTasks(prev => prev.map(task =>
                  task.id === firstTask.id ? { ...task, priority: task.priority === 'medium' ? 'high' : 'medium' } : task
                ));
              }
            } else if (tasks.length < 6) {
              // If no tasks exist and we're under the limit, add a task first then prioritize it
              const tempTask: Todo = {
                id: `temp-${Date.now()}`,
                title: 'Temporary task for prioritize demo',
                completed: false,
                userId: 'demo',
                priority: 'medium',
                tags: [],
                createdAt: new Date().toISOString(),
                updatedAt: new Date().toISOString(),
              };
              setTasks(prev => [...prev, tempTask]);

              // Then prioritize it after a short delay
              setTimeout(() => {
                setTasks(prev => prev.map(task =>
                  task.id === tempTask.id ? { ...task, priority: 'high' } : task
                ));
              }, 300);
            }
            break;

          case 'organize':
            setTasks(prev => [...prev]); // Trigger re-render to show current state
            break;
        }

        setDemoStep(prev => prev + 1);
      }, 2500);
    } else {
      // Restart demo after a pause
      demoTimeoutRef.current = setTimeout(() => {
        setDemoStep(0);
        setCurrentMessage('Adding tasks is now easier than ever');
        setTasks(initialDemoTasks);
      }, 3000);
    }

    return () => {
      if (demoTimeoutRef.current) {
        clearTimeout(demoTimeoutRef.current);
      }
    };
  }, [demoStep, tasks]);

  // Auto-fill behavior for the demo - only run once when component mounts
  useEffect(() => {
    // Auto-fill the form for the 'add' action after a delay
    const addTaskTimer = setTimeout(() => {
      setIsAutoFillActive(true);

      // Use typing effect to fill the task
      startTypingEffect('Complete the project proposal').then(() => {
        // Simulate selecting a priority (after typing completes)
        setTimeout(() => {
          setPriority('high');

          // Simulate adding tags (after priority selection)
          setTimeout(() => {
            setTags('work,important');

            // Finally simulate clicking the add button (after tags)
            setTimeout(() => {
              // Create and add the task
              const newTodo: Todo = {
                id: `demo-${Date.now()}`,
                title: 'Complete the project proposal',
                completed: false,
                userId: 'demo',
                priority: 'high',
                tags: [{ id: 'tag-auto', name: 'work', color: '#F59E0B', createdAt: new Date().toISOString() }],
                createdAt: new Date().toISOString(),
                updatedAt: new Date().toISOString(),
              };
              setTasks(prev => [...prev, newTodo]);

              setIsAutoFillActive(false); // Reset auto-fill state
            }, 800);
          }, 1000);
        }, 1000);
      });
    }, 3000); // Delay to let initial demo messages show

    return () => clearTimeout(addTaskTimer);
  }, []); // Only run once when component mounts

  const [showAddSuccess, setShowAddSuccess] = useState(false);
  const [successMessage, setSuccessMessage] = useState(''); // Still needed for edit/delete success messages
  const [editingTaskId, setEditingTaskId] = useState<string | null>(null);
  const [editingTaskTitle, setEditingTaskTitle] = useState('');
  const [isAutoFillActive, setIsAutoFillActive] = useState(false);
  const [deletingTaskId, setDeletingTaskId] = useState<string | null>(null);
  const [editingTaskVisual, setEditingTaskVisual] = useState<string | null>(null);
  const [typingText, setTypingText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [addSuccessTimeoutId, setAddSuccessTimeoutId] = useState<NodeJS.Timeout | null>(null);

  const addTask = () => {
    if (newTask.trim() === '') return;

    const newTodo: Todo = {
      id: Date.now().toString(),
      title: newTask,
      completed: false,
      userId: 'demo',
      priority,
      tags: tags.split(',').filter(tag => tag.trim()).map((tag, idx) => ({
        id: `tag-${Date.now()}-${idx}`,
        name: tag.trim(),
        color: getRandomColor(),
        createdAt: new Date().toISOString(),
      })),
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    // Update tasks first
    setTasks([...tasks, newTodo]);

    // Then reset fields
    setNewTask('');
    setTags('');
    setPriority('medium'); // Reset priority to default
    setTypingText(''); // Clear typing text if any
    setIsTyping(false); // Stop typing effect if active

    // Clear any existing timeout to prevent conflicts
    if (addSuccessTimeoutId) {
      clearTimeout(addSuccessTimeoutId);
    }

    // Show success indicator near the button
    setShowAddSuccess(true);

    // Use a more reliable timeout approach
    const timer = setTimeout(() => {
      setShowAddSuccess(false);
    }, 2500); // Slightly longer to ensure visibility

    // Store the timeout ID to clear it if needed
    setAddSuccessTimeoutId(timer);
  };

  // Function to simulate word-by-word typing effect for task addition
  const startTypingEffect = async (fullText: string) => {
    setIsTyping(true);
    setTypingText('');
    setNewTask('');

    const words = fullText.split(' ');

    for (let i = 0; i <= words.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 300)); // Pause between words
      const currentText = words.slice(0, i).join(' ');
      setTypingText(currentText);
      setNewTask(currentText);

      // Small additional delay after each word for better visibility
      if (i < words.length) {
        await new Promise(resolve => setTimeout(resolve, 100));
      }
    }

    setIsTyping(false);
  };

  const startEditing = (task: Todo) => {
    setEditingTaskId(task.id);
    setEditingTaskTitle(task.title);
  };

  const saveEdit = () => {
    if (editingTaskId && editingTaskTitle.trim()) {
      setEditingTaskVisual(editingTaskId); // Show visual feedback for editing

      setTasks(tasks.map(task =>
        task.id === editingTaskId
          ? { ...task, title: editingTaskTitle, updatedAt: new Date().toISOString() }
          : task
      ));

      // Show visual feedback for editing
      setTimeout(() => {
        setEditingTaskVisual(null);
      }, 500);

      cancelEdit();
    }
  };

  const cancelEdit = () => {
    setEditingTaskId(null);
    setEditingTaskTitle('');
  };

  const toggleTask = (id: string) => {
    setTasks(tasks.map(task =>
      task.id === id ? { ...task, completed: !task.completed } : task
    ));
  };

  const deleteTask = (id: string) => {
    setDeletingTaskId(id);
    // Briefly show deletion effect, then remove the task
    setTimeout(() => {
      setTasks(tasks.filter(task => task.id !== id));
      setDeletingTaskId(null);
    }, 500);
  };

  const getRandomColor = () => {
    const colors = ['#EF4444', '#F59E0B', '#10B981', '#3B82F6', '#8B5CF6', '#EC4899'];
    return colors[Math.floor(Math.random() * colors.length)];
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      addTask();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-pink-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-indigo-500 rounded-full mix-blend-multiply filter blur-xl opacity-10 animate-pulse delay-500"></div>
      </div>

      <div className="relative z-10 container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Left Side - Promotional Text */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center lg:text-left"
          >
            <motion.h1
              className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 bg-gradient-to-r from-purple-400 via-pink-400 to-purple-400 bg-clip-text text-transparent"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
            >
              Organize Your Tasks Effortlessly
            </motion.h1>

            <motion.div
              className="space-y-4 mb-8"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              <p className="text-xl text-gray-300 max-w-lg mx-auto lg:mx-0">
                {timeGreeting}! Add, track, and complete your daily goals — fast, elegant, distraction-free.
              </p>

              {/* Dynamic feature highlights that change with demo */}
              {/* <div className="mt-8 p-6 bg-white/5 rounded-xl border border-white/10">
                <div className="flex items-center justify-center lg:justify-start">
                  <div className="w-3 h-3 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full mr-3 animate-pulse"></div>
                  <span className="text-xl font-medium text-gray-200 text-center lg:text-left">
                    {currentMessage}
                  </span>
                </div>
              </div> */}
            </motion.div>

            <motion.div
              className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
            >
              <Link href="/signup" className="px-8 py-3.5 bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-medium rounded-lg hover:from-purple-700 hover:to-indigo-700 transition-all transform hover:scale-105 shadow-lg shadow-purple-500/20">
                Get Started
              </Link>

              {user ? (
                <Link href="/dashboard" className="px-8 py-3.5 bg-white/10 backdrop-blur-sm border border-white/20 text-white font-medium rounded-lg hover:bg-white/20 transition-all">
                  View Your Dashboard
                </Link>
              ) : (
                <Link href="/login" className="px-8 py-3.5 bg-white/10 backdrop-blur-sm border border-white/20 text-white font-medium rounded-lg hover:bg-white/20 transition-all">
                  Sign In
                </Link>
              )}
            </motion.div>

            {/* Stats */}
            <motion.div
              className="mt-12 grid grid-cols-3 gap-6 max-w-md mx-auto lg:mx-0"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
            >
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-400">{tasks.length}</div>
                <div className="text-sm text-gray-400">Tasks</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-400">{tasks.filter(t => t.completed).length}</div>
                <div className="text-sm text-gray-400">Completed</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-yellow-400">{tasks.filter(t => t.priority === 'high').length}</div>
                <div className="text-sm text-gray-400">Priority</div>
              </div>
            </motion.div>
          </motion.div>

          {/* Right Side - Auto Demo Panel */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="bg-white/10 backdrop-blur-sm rounded-2xl border border-white/20 p-6 shadow-xl"
          >
            <div className="flex justify-between items-center mb-6">
              <div className="flex flex-col">
                {/* <h3 className="text-xl font-semibold text-gray-200">Live Demo</h3> */}
                <div className="flex items-center justify-center lg:justify-start">
                  <div className="w-3 h-3 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full mr-3 animate-pulse"></div>
                  <span className="text-xl font-medium text-gray-200 mt-2">
                    {currentMessage}
                  </span>
                </div>
                {/* <div className="mt-2 text-xl font-semibold text-gray-200">
                  {currentMessage}
                </div> */}
              </div>
              <div className="flex space-x-2">
                <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              </div>
            </div>

            {/* Task Input Form - Shows what would be happening during auto demo */}
            <div className="mb-6 space-y-4">
              <div className={`flex gap-2 ${isAutoFillActive ? 'animate-pulse' : ''}`}>
                <input
                  ref={inputRef}
                  type="text"
                  value={isTyping ? typingText : newTask}
                  onChange={(e) => {
                    if (!isTyping) { // Only allow manual input when not typing
                      setNewTask(e.target.value);
                    }
                  }}
                  onKeyDown={handleKeyPress}
                  placeholder="Add a new task..."
                  className="flex-1 px-4 py-2.5 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-white placeholder-gray-400"
                />
                <div className="relative">
                  <button
                    onClick={addTask}
                    className={`px-4 py-2.5 rounded-lg transition-all ${
                      showAddSuccess
                        ? 'bg-green-500 hover:bg-green-600'
                        : 'bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700'
                    } text-white`}
                  >
                    {showAddSuccess ? (
                      <div className="flex items-center justify-center">
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                        </svg>
                      </div>
                    ) : (
                      '+'
                    )}
                  </button>
                </div>
              </div>

              <div className={`flex gap-2 ${isAutoFillActive ? 'animate-pulse' : ''}`}>
                <select
                  value={priority}
                  onChange={(e) => setPriority(e.target.value as Priority)}
                  className="flex-1 px-3 py-2 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-white"
                >
                  <option value="low" className="bg-gray-800 text-white">Low Priority</option>
                  <option value="medium" className="bg-gray-800 text-white">Medium Priority</option>
                  <option value="high" className="bg-gray-800 text-white">High Priority</option>
                </select>

                <input
                  type="text"
                  value={tags}
                  onChange={(e) => setTags(e.target.value)}
                  placeholder="Tags (comma separated)"
                  className="flex-1 px-3 py-2 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-white placeholder-gray-400"
                />
              </div>
            </div>

            {/* Task List - Auto demo running */}
            <div className="space-y-3 max-h-96 overflow-y-visible pr-2">
              <AnimatePresence>
                {tasks.map((task, index) => (
                  <motion.div
                    key={task.id}
                    initial={{ opacity: 0, y: -10 }}
                    animate={{
                      opacity: 1,
                      y: 0,
                      scale: deletingTaskId === task.id ? 0.8 : 1,
                      backgroundColor: deletingTaskId === task.id ? 'rgba(239, 68, 68, 0.2)' : '',
                      borderColor: deletingTaskId === task.id ? 'rgba(239, 68, 68, 0.3)' : ''
                    }}
                    exit={{ opacity: 0, scale: 0.8 }}
                    transition={{ duration: deletingTaskId === task.id ? 0.5 : 0.3, delay: index * 0.05 }}
                    className={`p-4 rounded-lg backdrop-blur-sm border transition-all duration-300 ${
                      task.completed
                        ? 'bg-green-500/10 border-green-500/30'
                        : 'bg-white/5 border-white/10'
                    } ${
                      editingTaskVisual === task.id ? 'ring-2 ring-blue-500/50 bg-blue-500/10' : ''
                    }`}
                  >
                    <div className="flex items-start gap-3">
                      <button
                        onClick={() => toggleTask(task.id)}
                        className={`flex-shrink-0 w-5 h-5 rounded-full border-2 flex items-center justify-center mt-1 ${
                          task.completed
                            ? 'bg-green-500 border-green-500'
                            : 'border-gray-400 hover:border-purple-400'
                        }`}
                      >
                        {task.completed && (
                          <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                          </svg>
                        )}
                      </button>

                      <div className="flex-1 min-w-0">
                        {editingTaskId === task.id ? (
                          <div className="space-y-2">
                            <input
                              type="text"
                              value={editingTaskTitle}
                              onChange={(e) => setEditingTaskTitle(e.target.value)}
                              onKeyDown={(e) => {
                                if (e.key === 'Enter') saveEdit();
                                if (e.key === 'Escape') cancelEdit();
                              }}
                              className="w-full px-2 py-1 bg-white/10 border border-white/20 rounded focus:outline-none focus:ring-2 focus:ring-purple-500 text-white"
                              autoFocus
                            />
                            <div className="flex gap-2">
                              <button
                                onClick={saveEdit}
                                className="px-2 py-1 bg-green-500/20 text-green-300 rounded text-xs hover:bg-green-500/30"
                              >
                                Save
                              </button>
                              <button
                                onClick={cancelEdit}
                                className="px-2 py-1 bg-gray-500/20 text-gray-300 rounded text-xs hover:bg-gray-500/30"
                              >
                                Cancel
                              </button>
                            </div>
                          </div>
                        ) : (
                          <>
                            <div className={`font-medium ${task.completed ? 'text-gray-400 line-through' : 'text-gray-200'}`}>
                              {task.title}
                            </div>
                            {task.description && (
                              <div className="text-sm text-gray-400 mt-1">{task.description}</div>
                            )}

                            <div className="flex flex-wrap gap-2 mt-2">
                              <span className={`px-2 py-1 rounded-full text-xs ${
                                task.priority === 'low' ? 'bg-green-500/20 text-green-400' :
                                task.priority === 'medium' ? 'bg-yellow-500/20 text-yellow-400' :
                                'bg-red-500/20 text-red-400'
                              }`}>
                                {task.priority}
                              </span>

                              {task.tags.map(tag => (
                                <span
                                  key={tag.id}
                                  className="px-2 py-1 rounded-full text-xs"
                                  style={{ backgroundColor: `${tag.color}20`, color: tag.color }}
                                >
                                  {tag.name}
                                </span>
                              ))}

                              {task.dueDate && (
                                <span className="px-2 py-1 rounded-full text-xs bg-blue-500/20 text-blue-400">
                                  {new Date(task.dueDate).toLocaleDateString()}
                                </span>
                              )}
                            </div>
                          </>
                        )}
                      </div>

                      {editingTaskId !== task.id && (
                        <div className="flex gap-1 ml-2">
                          <button
                            onClick={() => startEditing(task)}
                            className="flex-shrink-0 text-gray-400 hover:text-blue-400 transition-colors"
                            title="Edit task"
                          >
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                            </svg>
                          </button>
                          <button
                            onClick={() => deleteTask(task.id)}
                            className="flex-shrink-0 text-gray-400 hover:text-red-400 transition-colors"
                            title="Delete task"
                          >
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                            </svg>
                          </button>
                        </div>
                      )}
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default HeroSection;