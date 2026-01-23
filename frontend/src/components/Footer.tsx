import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-slate-900/80 backdrop-blur-md border-t border-white/10 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <p className="text-gray-400 text-sm">
            © {new Date().getFullYear()} Todo App. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;