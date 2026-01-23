import React from 'react';
import { motion } from 'framer-motion';

interface SummaryBarProps {
  totalTasks: number;
  completedTasks: number;
  progressPercentage: number;
  dailyStreak: number;
}

const SummaryBar: React.FC<SummaryBarProps> = ({
  totalTasks,
  completedTasks,
  progressPercentage,
  dailyStreak
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.1 }}
      className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6"
    >
      <div className="bg-white/10 backdrop-blur-sm rounded-xl border border-white/20 p-4">
        <div className="text-2xl font-bold text-purple-400">{totalTasks}</div>
        <div className="text-sm text-gray-400">Total Tasks</div>
      </div>

      <div className="bg-white/10 backdrop-blur-sm rounded-xl border border-white/20 p-4">
        <div className="text-2xl font-bold text-green-400">{completedTasks}</div>
        <div className="text-sm text-gray-400">Completed</div>
      </div>

      <div className="bg-white/10 backdrop-blur-sm rounded-xl border border-white/20 p-4">
        <div className="text-2xl font-bold text-yellow-400">{progressPercentage}%</div>
        <div className="text-sm text-gray-400">Progress</div>
      </div>

      <div className="bg-white/10 backdrop-blur-sm rounded-xl border border-white/20 p-4">
        <div className="text-2xl font-bold text-blue-400">{dailyStreak}</div>
        <div className="text-sm text-gray-400">Day Streak</div>
      </div>
    </motion.div>
  );
};

export default SummaryBar;