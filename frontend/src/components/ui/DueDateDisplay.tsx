'use client';

import React from 'react';
import { format, isToday, isTomorrow } from 'date-fns';

interface DueDateDisplayProps {
  dueDate: string; // ISO date string
  className?: string;
  overdueClassName?: string;
  todayClassName?: string;
  tomorrowClassName?: string;
}

const DueDateDisplay: React.FC<DueDateDisplayProps> = ({
  dueDate,
  className = '',
  overdueClassName = 'text-red-600 bg-red-50',
  todayClassName = 'text-blue-600 bg-blue-50',
  tomorrowClassName = 'text-orange-600 bg-orange-50'
}) => {
  const date = new Date(dueDate);
  const now = new Date();
  const isOverdue = date < now && !isToday(date);
  const isTodayDue = isToday(date);
  const isTomorrowDue = isTomorrow(date);

  let displayClass = className;
  if (isOverdue) {
    displayClass += ` ${overdueClassName}`;
  } else if (isTodayDue) {
    displayClass += ` ${todayClassName}`;
  } else if (isTomorrowDue) {
    displayClass += ` ${tomorrowClassName}`;
  } else {
    displayClass += ' text-gray-600 bg-gray-50';
  }

  const formattedDate = format(date, 'MMM dd, yyyy');
  const dayDifference = Math.ceil((date.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));

  let label = formattedDate;
  if (isTodayDue) {
    label = 'Today';
  } else if (isTomorrowDue) {
    label = 'Tomorrow';
  } else if (isOverdue) {
    if (dayDifference === -1) {
      label = 'Yesterday';
    } else {
      label = `${Math.abs(dayDifference)} days ago`;
    }
  } else if (dayDifference === 2) {
    label = 'In 2 days';
  } else if (dayDifference <= 7) {
    label = `In ${dayDifference} days`;
  }

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${displayClass}`}>
      <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
      </svg>
      {label}
    </span>
  );
};

export default DueDateDisplay;