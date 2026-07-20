import React from 'react';

export const ProgressCard = ({ total, completedCount, activeCount }) => {
  const percentage = total === 0 ? 0 : Math.round((completedCount / total) * 100);

  return (
    <section className="progress-card">
      <div className="progress-header">
        <div className="progress-info">
          <span className="progress-title">目前完成度</span>
          <span className="progress-percentage">{percentage}%</span>
        </div>
        <div className="stats-counters">
          <span className="counter-badge">{activeCount} 個項目待完成</span>
        </div>
      </div>
      <div className="progress-bar-bg">
        <div 
          className="progress-bar-fill" 
          style={{ width: `${percentage}%` }}
        ></div>
      </div>
    </section>
  );
};
