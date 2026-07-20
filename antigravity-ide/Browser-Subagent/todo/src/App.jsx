import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { ProgressCard } from './components/ProgressCard';
import { TodoForm } from './components/TodoForm';
import { FilterTabs } from './components/FilterTabs';
import { TodoList } from './components/TodoList';

const STORAGE_KEY = 'taskflow_react_todos_v1';

export const App = () => {
  // 從 LocalStorage 載入初始數據
  const [todos, setTodos] = useState(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      return stored ? JSON.parse(stored) : [];
    } catch (error) {
      console.error('載入 localStorage 失敗:', error);
      return [];
    }
  });

  const [filter, setFilter] = useState('all'); // 'all' | 'active' | 'completed'

  // 當 todos 變更時自動同步至 LocalStorage
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(todos));
    } catch (error) {
      console.error('寫入 localStorage 失敗:', error);
    }
  }, [todos]);

  // 新增待辦事項
  const handleAddTodo = (text) => {
    const newTodo = {
      id: Date.now().toString(),
      text,
      completed: false,
      createdAt: new Date().toISOString()
    };
    setTodos((prev) => [newTodo, ...prev]);
  };

  // 切換完成狀態
  const handleToggleTodo = (id) => {
    setTodos((prev) =>
      prev.map((todo) =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
      )
    );
  };

  // 刪除待辦事項
  const handleDeleteTodo = (id) => {
    setTodos((prev) => prev.filter((todo) => todo.id !== id));
  };

  // 清除所有已完成事項
  const handleClearCompleted = () => {
    setTodos((prev) => prev.filter((todo) => !todo.completed));
  };

  // 數據統計計算
  const totalCount = todos.length;
  const completedCount = todos.filter((t) => t.completed).length;
  const activeCount = totalCount - completedCount;

  // 根據當前篩選器過濾任務
  const filteredTodos = todos.filter((todo) => {
    if (filter === 'active') return !todo.completed;
    if (filter === 'completed') return todo.completed;
    return true; // 'all'
  });

  return (
    <>
      <div className="bg-glow bg-glow-1"></div>
      <div className="bg-glow bg-glow-2"></div>

      <div className="app-container">
        <Header />

        <ProgressCard 
          total={totalCount} 
          completedCount={completedCount} 
          activeCount={activeCount} 
        />

        <TodoForm onAddTodo={handleAddTodo} />

        <FilterTabs 
          currentFilter={filter}
          onFilterChange={setFilter}
          totalCount={totalCount}
          activeCount={activeCount}
          completedCount={completedCount}
          onClearCompleted={handleClearCompleted}
        />

        <TodoList 
          todos={filteredTodos}
          currentFilter={filter}
          totalCount={totalCount}
          onToggle={handleToggleTodo}
          onDelete={handleDeleteTodo}
        />

        <footer className="app-footer">
          <p>React.js + LocalStorage 持久化 • 清爽淡藍主題</p>
        </footer>
      </div>
    </>
  );
};

export default App;
