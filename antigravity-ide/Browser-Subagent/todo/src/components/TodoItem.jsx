import React, { useState } from 'react';

export const TodoItem = ({ todo, onToggle, onDelete }) => {
  const [isRemoving, setIsRemoving] = useState(false);

  const handleDelete = (e) => {
    e.stopPropagation();
    setIsRemoving(true);
    setTimeout(() => {
      onDelete(todo.id);
    }, 250); // Matches CSS slideOut animation duration
  };

  return (
    <li 
      className={`todo-item ${todo.completed ? 'completed' : ''} ${isRemoving ? 'removing' : ''}`}
      onClick={() => onToggle(todo.id)}
    >
      <div className="todo-content">
        <div 
          className="custom-checkbox" 
          role="checkbox" 
          aria-checked={todo.completed}
          aria-label="切換完成狀態"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
        </div>
        <span className="todo-text">{todo.text}</span>
      </div>
      <button 
        type="button" 
        className="delete-btn" 
        onClick={handleDelete}
        aria-label="刪除事項" 
        title="刪除"
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <polyline points="3 6 5 6 21 6"></polyline>
          <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
          <line x1="10" y1="11" x2="10" y2="17"></line>
          <line x1="14" y1="11" x2="14" y2="17"></line>
        </svg>
      </button>
    </li>
  );
};
