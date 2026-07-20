import React, { useState } from 'react';

export const TodoForm = ({ onAddTodo }) => {
  const [text, setText] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmed = text.trim();
    if (trimmed) {
      onAddTodo(trimmed);
      setText('');
    }
  };

  return (
    <section className="input-section">
      <form onSubmit={handleSubmit} className="todo-form">
        <div className="input-wrapper">
          <svg className="input-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="16"></line>
            <line x1="8" y1="12" x2="16" y2="12"></line>
          </svg>
          <input 
            type="text" 
            className="todo-input" 
            placeholder="新增待辦事項... (按 Enter 或點擊新增)" 
            value={text}
            onChange={(e) => setText(e.target.value)}
            autoComplete="off"
            aria-label="新增待辦事項"
          />
          <button type="submit" className="btn btn-primary" aria-label="新增事項">
            <span>新增</span>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
          </button>
        </div>
      </form>
    </section>
  );
};
