import React from 'react';
import { TodoItem } from './TodoItem';

export const TodoList = ({ todos, currentFilter, totalCount, onToggle, onDelete }) => {
  if (todos.length === 0) {
    let emptyTitle = '沒有待辦事項';
    let emptyDesc = '在上方輸入框新增第一個事項開始記錄吧！';

    if (totalCount > 0) {
      if (currentFilter === 'active') {
        emptyTitle = '太棒了！所有事項皆已完成';
        emptyDesc = '目前沒有任何未完成的待辦任務。';
      } else if (currentFilter === 'completed') {
        emptyTitle = '尚未有完成的事項';
        emptyDesc = '點擊事項邊緣的勾選框以完成第一個任務。';
      }
    }

    return (
      <main className="list-section">
        <div className="empty-state">
          <div className="empty-icon">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
          </div>
          <h3>{emptyTitle}</h3>
          <p>{emptyDesc}</p>
        </div>
      </main>
    );
  }

  return (
    <main className="list-section">
      <ul className="todo-list" aria-label="待辦事項列表">
        {todos.map((todo) => (
          <TodoItem 
            key={todo.id} 
            todo={todo} 
            onToggle={onToggle} 
            onDelete={onDelete} 
          />
        ))}
      </ul>
    </main>
  );
};
