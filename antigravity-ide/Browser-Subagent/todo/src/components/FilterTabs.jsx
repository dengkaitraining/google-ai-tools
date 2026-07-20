import React from 'react';

export const FilterTabs = ({ 
  currentFilter, 
  onFilterChange, 
  totalCount, 
  activeCount, 
  completedCount, 
  onClearCompleted 
}) => {
  return (
    <section className="toolbar-section">
      <div className="filter-tabs" role="tablist" aria-label="事項篩選">
        <button 
          type="button" 
          className={`filter-tab ${currentFilter === 'all' ? 'active' : ''}`}
          onClick={() => onFilterChange('all')}
          role="tab" 
          aria-selected={currentFilter === 'all'}
        >
          全部 <span className="badge">{totalCount}</span>
        </button>
        <button 
          type="button" 
          className={`filter-tab ${currentFilter === 'active' ? 'active' : ''}`}
          onClick={() => onFilterChange('active')}
          role="tab" 
          aria-selected={currentFilter === 'active'}
        >
          未完成 <span className="badge">{activeCount}</span>
        </button>
        <button 
          type="button" 
          className={`filter-tab ${currentFilter === 'completed' ? 'active' : ''}`}
          onClick={() => onFilterChange('completed')}
          role="tab" 
          aria-selected={currentFilter === 'completed'}
        >
          已完成 <span className="badge">{completedCount}</span>
        </button>
      </div>

      <button 
        type="button" 
        className="btn btn-ghost" 
        onClick={onClearCompleted}
        style={{
          opacity: completedCount > 0 ? 1 : 0.4,
          pointerEvents: completedCount > 0 ? 'auto' : 'none'
        }}
        aria-label="清除已完成事項"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <polyline points="3 6 5 6 21 6"></polyline>
          <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
        </svg>
        <span>清除已完成</span>
      </button>
    </section>
  );
};
