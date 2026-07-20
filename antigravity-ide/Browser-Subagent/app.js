/**
 * TaskFlow - 現代化待辦事項應用程式 Core Engine
 * 語法標準：ES6+ (Class, Arrow Functions, Destructuring, Template Literals)
 * 特色：零外部框架、localStorage 持久化、XSS 防護、全 DOM 動態更新
 */

class TodoApp {
  /**
   * 建構子：初始化應用狀態與儲存鍵名
   */
  constructor() {
    // LocalStorage 儲存 Key 名稱
    this.STORAGE_KEY = 'taskflow_todos_v1';

    // 應用狀態 State
    this.todos = [];
    this.currentFilter = 'all'; // 預設篩選模式：'all' | 'active' | 'completed'

    // DOM 元素快取 (Element Cache)
    this.todoForm = document.getElementById('todo-form');
    this.todoInput = document.getElementById('todo-input');
    this.todoList = document.getElementById('todo-list');
    this.emptyState = document.getElementById('empty-state');
    this.emptyTitle = document.getElementById('empty-title');
    this.emptyDesc = document.getElementById('empty-desc');

    // 進度條與計數器 DOM 元素
    this.progressFill = document.getElementById('progress-fill');
    this.progressText = document.getElementById('progress-text');
    this.statsSummary = document.getElementById('stats-summary');

    // 徽章計數器 (Badges)
    this.badgeAll = document.getElementById('badge-all');
    this.badgeActive = document.getElementById('badge-active');
    this.badgeCompleted = document.getElementById('badge-completed');

    // 批次按鈕與篩選頁籤
    this.filterTabs = document.querySelectorAll('.filter-tab');
    this.clearCompletedBtn = document.getElementById('clear-completed-btn');

    // 初始化啟動
    this.init();
  }

  /**
   * 初始化應用程式：載入資料與註冊事件監聽
   */
  init() {
    // 1. 從 LocalStorage 載入歷史資料
    this.loadTodos();

    // 2. 註冊事件監聽器 (Event Listeners)
    this.registerEventListeners();

    // 3. 初始渲染畫面
    this.render();
  }

  /**
   * 註冊所有 DOM 事件處理器
   */
  registerEventListeners() {
    // 提交表單（點擊新增按鈕或按下 Enter 鍵）
    this.todoForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const text = this.todoInput.value.trim();
      if (text) {
        this.addTodo(text);
        this.todoInput.value = ''; // 新增後清空輸入框
      }
    });

    // 待辦事項清單點擊事件代理 (Event Delegation)
    this.todoList.addEventListener('click', (e) => {
      const todoItem = e.target.closest('.todo-item');
      if (!todoItem) return;

      const id = todoItem.dataset.id;

      // 判斷是否點擊刪除按鈕
      if (e.target.closest('.delete-btn')) {
        this.deleteTodo(id, todoItem);
        return;
      }

      // 點擊勾選框或卡片本體切換完成狀態
      this.toggleTodo(id);
    });

    // 篩選頁籤點擊事件
    this.filterTabs.forEach((tab) => {
      tab.addEventListener('click', () => {
        const filter = tab.dataset.filter;
        this.setFilter(filter);
      });
    });

    // 清除已完成事項按鈕
    this.clearCompletedBtn.addEventListener('click', () => {
      this.clearCompleted();
    });
  }

  /**
   * 自 localStorage 讀取待辦事項
   */
  loadTodos() {
    try {
      const storedData = localStorage.getItem(this.STORAGE_KEY);
      this.todos = storedData ? JSON.parse(storedData) : [];
    } catch (error) {
      console.error('讀取 localStorage 失敗:', error);
      this.todos = [];
    }
  }

  /**
   * 將待辦事項寫入 localStorage
   */
  saveTodos() {
    try {
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(this.todos));
    } catch (error) {
      console.error('寫入 localStorage 失敗:', error);
    }
  }

  /**
   * 新增一筆待辦事項
   * @param {string} text 事項內容
   */
  addTodo(text) {
    const newTodo = {
      id: Date.now().toString(), // 以時間戳記生成唯一 ID
      text: text,
      completed: false,
      createdAt: new Date().toISOString()
    };

    // 新增至列表頂部（新事項優先顯示）
    this.todos.unshift(newTodo);
    this.saveTodos();
    this.render();
  }

  /**
   * 切換特定事項的完成/未完成狀態
   * @param {string} id 事項 ID
   */
  toggleTodo(id) {
    this.todos = this.todos.map((todo) => {
      if (todo.id === id) {
        return { ...todo, completed: !todo.completed };
      }
      return todo;
    });

    this.saveTodos();
    this.render();
  }

  /**
   * 刪除特定待辦事項（帶滑出離場動畫）
   * @param {string} id 事項 ID
   * @param {HTMLElement} element DOM 節點元素
   */
  deleteTodo(id, element) {
    // 觸發 CSS 離場動畫類別
    element.classList.add('removing');

    // 等待動畫結束後自陣列刪除並更新 UI
    setTimeout(() => {
      this.todos = this.todos.filter((todo) => todo.id !== id);
      this.saveTodos();
      this.render();
    }, 250); // 對應 style.css 中的 slideOut 時間 0.25s
  }

  /**
   * 設定當前顯示的篩選模式
   * @param {string} filter 篩選類別 ('all' | 'active' | 'completed')
   */
  setFilter(filter) {
    this.currentFilter = filter;

    // 更新頁籤按鈕 active 狀態
    this.filterTabs.forEach((tab) => {
      const isActive = tab.dataset.filter === filter;
      tab.classList.toggle('active', isActive);
      tab.setAttribute('aria-selected', isActive ? 'true' : 'false');
    });

    this.render();
  }

  /**
   * 清除所有已完成的事項
   */
  clearCompleted() {
    const activeCount = this.todos.filter((t) => !t.completed).length;
    if (activeCount === this.todos.length) return; // 若沒有已完成事項則無需處理

    this.todos = this.todos.filter((todo) => !todo.completed);
    this.saveTodos();
    this.render();
  }

  /**
   * 根據當前篩選條件過濾待辦事項
   * @returns {Array} 過濾後的事項陣列
   */
  getFilteredTodos() {
    switch (this.currentFilter) {
      case 'active':
        return this.todos.filter((todo) => !todo.completed);
      case 'completed':
        return this.todos.filter((todo) => todo.completed);
      case 'all':
      default:
        return this.todos;
    }
  }

  /**
   * XSS 防護字串轉義函式
   * @param {string} str 未過濾文字
   * @returns {string} 安全 HTML 字串
   */
  escapeHTML(str) {
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  /**
   * 更新進度條與數據統計顯示
   */
  updateStats() {
    const total = this.todos.length;
    const completedCount = this.todos.filter((t) => t.completed).length;
    const activeCount = total - completedCount;

    // 1. 計算完成百分比
    const percentage = total === 0 ? 0 : Math.round((completedCount / total) * 100);
    this.progressFill.style.width = `${percentage}%`;
    this.progressText.textContent = `${percentage}%`;

    // 2. 更新摘要數字
    this.statsSummary.textContent = `${activeCount} 個項目待完成`;

    // 3. 更新篩選列徽章數字
    this.badgeAll.textContent = total;
    this.badgeActive.textContent = activeCount;
    this.badgeCompleted.textContent = completedCount;

    // 4. 控制「清除已完成」按鈕顯示
    this.clearCompletedBtn.style.opacity = completedCount > 0 ? '1' : '0.4';
    this.clearCompletedBtn.style.pointerEvents = completedCount > 0 ? 'auto' : 'none';
  }

  /**
   * 主渲染函式 (Render Function)
   */
  render() {
    // 1. 更新統計指標與進度
    this.updateStats();

    // 2. 取得過濾後的事項
    const filteredTodos = this.getFilteredTodos();

    // 3. 控制空白狀態 (Empty State) 的呈現
    if (filteredTodos.length === 0) {
      this.todoList.innerHTML = '';
      this.emptyState.classList.remove('hidden');

      if (this.todos.length === 0) {
        this.emptyTitle.textContent = '沒有待辦事項';
        this.emptyDesc.textContent = '在上方輸入框新增第一個事項開始記錄吧！';
      } else if (this.currentFilter === 'active') {
        this.emptyTitle.textContent = '太棒了！所有事項皆已完成';
        this.emptyDesc.textContent = '目前沒有任何未完成的待辦任務。';
      } else if (this.currentFilter === 'completed') {
        this.emptyTitle.textContent = '尚未有完成的事項';
        this.emptyDesc.textContent = '點擊事項邊緣的勾選框以完成第一個任務。';
      }
      return;
    }

    // 有內容時隱藏空白提示
    this.emptyState.classList.add('hidden');

    // 4. 繪製待辦事項列表 DOM
    const htmlString = filteredTodos
      .map((todo) => {
        const safeText = this.escapeHTML(todo.text);
        const completedClass = todo.completed ? 'completed' : '';

        return `
          <li class="todo-item ${completedClass}" data-id="${todo.id}">
            <div class="todo-content">
              <div class="custom-checkbox" aria-label="切換完成狀態" role="checkbox" aria-checked="${todo.completed}">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
              </div>
              <span class="todo-text">${safeText}</span>
            </div>
            <button type="button" class="delete-btn" aria-label="刪除事項" title="刪除">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                <line x1="10" y1="11" x2="10" y2="17"></line>
                <line x1="14" y1="11" x2="14" y2="17"></line>
              </svg>
            </button>
          </li>
        `;
      })
      .join('');

    this.todoList.innerHTML = htmlString;
  }
}

// 當 DOM 載入完成後初始化 TodoApp 實例
document.addEventListener('DOMContentLoaded', () => {
  window.app = new TodoApp();
});
