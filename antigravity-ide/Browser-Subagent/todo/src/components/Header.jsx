import React from 'react';

export const Header = () => {
  return (
    <header className="app-header">
      <div className="brand">
        <div className="brand-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="9 11 12 14 22 4"></polyline>
            <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>
          </svg>
        </div>
        <div className="brand-title">
          <h1>我的待辦事項</h1>
          <p>清爽淡藍風格 • 優雅管理日常任務與目標</p>
        </div>
      </div>
    </header>
  );
};

