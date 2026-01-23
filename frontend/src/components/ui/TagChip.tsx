'use client';

import React from 'react';
import { Tag } from '@/types/todo';

interface TagChipProps {
  tag: Tag;
  className?: string;
  onClick?: () => void;
}

const TagChip: React.FC<TagChipProps> = ({ tag, className = '', onClick }) => {
  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${className}`}
      style={{ backgroundColor: `${tag.color}20`, color: tag.color, border: `1px solid ${tag.color}` }} // Add 20% opacity to background
      onClick={onClick}
    >
      {tag.name}
    </span>
  );
};

export default TagChip;