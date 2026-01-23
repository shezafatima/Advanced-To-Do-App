import React from 'react';
import { motion } from 'framer-motion';

interface ProgressBarProps {
  percentage: number;
}

const ProgressBar: React.FC<ProgressBarProps> = ({ percentage }) => {
  return (
    <motion.div
      initial={{ opacity: 0, scaleX: 0 }}
      animate={{ opacity: 1, scaleX: 1 }}
      transition={{ delay: 0.2 }}
      className="mb-6 bg-white/10 backdrop-blur-sm rounded-xl border border-white/20 p-4"
    >
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm text-gray-300">Your Progress</span>
        <span className="text-sm text-gray-300">{percentage}%</span>
      </div>
      <div className="w-full bg-gray-700 rounded-full h-2.5">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="bg-gradient-to-r from-purple-500 to-pink-500 h-2.5 rounded-full"
        ></motion.div>
      </div>
    </motion.div>
  );
};

export default ProgressBar;