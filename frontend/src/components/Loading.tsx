import React from 'react';

interface LoadingProps {
  type?: 'spinner' | 'skeleton' | 'skeleton-list';
  count?: number; // Number of skeleton items for skeleton-list type
}

const Loading: React.FC<LoadingProps> = ({ type = 'spinner', count = 3 }) => {
  switch (type) {
    case 'spinner':
      return (
        <div className="flex justify-center items-center py-8">
          <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-blue-500"></div>
        </div>
      );

    case 'skeleton':
      return (
        <div className="animate-pulse p-4 border rounded-lg bg-gray-100">
          <div className="h-4 bg-gray-300 rounded w-3/4 mb-2"></div>
          <div className="h-4 bg-gray-300 rounded w-1/2"></div>
        </div>
      );

    case 'skeleton-list':
      return (
        <div className="space-y-4">
          {Array.from({ length: count }).map((_, index) => (
            <div key={index} className="animate-pulse p-4 border rounded-lg bg-gray-100">
              <div className="flex items-center space-x-3">
                <div className="h-5 w-5 bg-gray-300 rounded"></div>
                <div className="flex-1 space-y-2">
                  <div className="h-4 bg-gray-300 rounded w-3/4"></div>
                  <div className="h-4 bg-gray-300 rounded w-1/2"></div>
                </div>
              </div>
            </div>
          ))}
        </div>
      );

    default:
      return (
        <div className="flex justify-center items-center py-8">
          <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-blue-500"></div>
        </div>
      );
  }
};

export default Loading;