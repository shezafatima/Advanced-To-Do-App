'use client';

import React from 'react';
import { Priority } from '@/types/todo';

interface PriorityIndicatorProps {
  priority: Priority;
  className?: string;
}

const PriorityIndicator: React.FC<PriorityIndicatorProps> = ({ priority, className = '' }) => {
  const priorityStyles = {
    low: 'bg-green-100 text-green-800 border border-green-200',
    medium: 'bg-yellow-100 text-yellow-800 border border-yellow-200',
    high: 'bg-red-100 text-red-800 border border-red-200',
  };

  const priorityLabels = {
    low: 'Low',
    medium: 'Medium',
    high: 'High',
  };

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${priorityStyles[priority]} ${className}`}>
      {priorityLabels[priority]}
    </span>
  );
};

export default PriorityIndicator;