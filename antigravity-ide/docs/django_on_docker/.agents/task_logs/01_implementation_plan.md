# Django + Vue.js (TS/Tailwind) 資訊系統容器化開發環境實作計畫 (Implementation Plan)

本實作計畫詳細記載基於 Docker Compose 建立之 Python Django (整合 Django Unfold 後台)、Vue.js 3.5 (整合 TypeScript 與 Tailwind CSS 4.3)、Apache HTTPD 反向代理、MariaDB 12.3 與 Redis 8.8 完整 Stack 之架構與服務設計。

---

## 1. 架構設計與服務配置

### A. 系統服務佈局 (Service Layout)
```text
/home/dengkai/projects/django-on-docker/
├── .env                              # 全局環境變數與自定義設定檔路徑
├── .gitattributes                    # 強制 LF 換行符號 (Linux/Windows 跨平台支援)
├── .gitignore                        # 忽略本地 Volume 資料與 Node/Python 暫存檔
├── docker-compose.yaml               # Docker Compose 5 大服務與 Bridge 網路定義
├── agents/
│   └── task_logs/                    # 專案任務與計畫紀錄目錄
│       ├── 01_implementation_plan.md
│       ├── 02_task_list.md
│       └── 03_walkthrough.md
├── apache/                           # Apache HTTPD 反向代理服務
│   ├── Dockerfile
│   └── httpd-custom.conf             # 使用者自定義設定檔 (APACHE_CUSTOM_CONF)
├── db_conf/                          # MariaDB 自定義設定檔目錄
│   └── my_custom.cnf                 # 使用者自定義設定檔 (MARIADB_CUSTOM_CONF)
├── redis_conf/                       # Redis 自定義設定檔目錄
│   └── redis.conf                    # 使用者自定義設定檔 (REDIS_CUSTOM_CONF)
├── backend/                          # Django 5.2 後端應用服務
│   ├── Dockerfile
│   ├── requirements.txt              # Django 5.2, django-unfold, mysqlclient, django-redis
│   ├── entrypoint.sh                 # 等待資料庫、自動 Migration 與自動 Superuser
│   ├── manage.py
│   └── core/                         # Django 核心模組 (settings, urls, views, wsgi, asgi)
├── frontend/                         # Vue 3.5 前端應用服務
│   ├── Dockerfile
│   ├── package.json                  # Vue 3.5, @tailwindcss/vite 4.3, TypeScript
│   ├── vite.config.ts                # Vite 5 (base: /tech-stack/), HMR WebSocket 配置
│   ├── tsconfig.json
│   ├── index.html
│   └── src/
│       ├── style.css                 # Tailwind CSS v4 `@import "tailwindcss";`
│       ├── main.ts
│       ├── vite-env.d.ts
│       └── App.vue                   # 資訊系統儀表板 (含 10 分鐘自動連線檢測)
├── db_data/                          # MariaDB 實體持久化目錄 (Git 忽略)
└── redis_data/                       # Redis 實體持久化目錄 (Git 忽略)
```

---

## 2. 服務技術細節與 Option 命令設定

| 服務名稱 | 技術堆疊與版本 | 自定義設定檔 (.env 定義) | 容器 command 運行選項 (Options) |
| :--- | :--- | :--- | :--- |
| **`web`** | Apache HTTPD `2.4-alpine` | `APACHE_CUSTOM_CONF=./apache/httpd-custom.conf` | `["httpd-foreground"]` |
| **`db`** | MariaDB `12.3` | `MARIADB_CUSTOM_CONF=./db_conf/my_custom.cnf` | `--character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci --max-connections=250 --default-storage-engine=InnoDB` |
| **`redis`** | Redis `8.8` | `REDIS_CUSTOM_CONF=./redis_conf/redis.conf` | `["redis-server", "/usr/local/etc/redis/redis.conf"]` |
| **`backend`** | Python `3.11` + Django `5.2 LTS` | 不適用 | 自動執行 `entrypoint.sh` (含 `python manage.py runserver 0.0.0.0:8000`) |
| **`frontend`** | Node `20` + Vue `3.5` + Tailwind `4.3` | 不適用 | 執行 `npm run dev` (Vite `base: /tech-stack/`) |

---

## 3. URL 路由映射與功能規劃

1. **`http://localhost/` (根路由)**：
   - 轉接至 Django Backend (`/`)，回應純文字訊息：`Django + Vue.js Web 資訊系統開發環境的服務已啟用。`
2. **`http://localhost/tech-stack/` (系統儀表板)**：
   - 轉接至 Vue 3.5 Frontend (`/tech-stack/`)，展示 5 大容器節點狀態儀表板。
   - **檢測機制**：首次連線自動檢查 1 次，爾後每 10 分鐘 (`600,000 ms`) 自動重新檢測各服務狀態。
3. **`http://localhost/admin/` (Unfold 後台)**：
   - 轉接至 Django Unfold 管理員介面 (`/admin/`)，可使用預設帳號登入。
4. **`http://localhost/api/status/` (連線檢測 API)**：
   - 轉接至 Django Backend (`/api/status/`)，動態檢測 MariaDB 與 Redis 連線並回傳 JSON 數據。

---

## 4. 跨平台相容性規劃 (Linux & Windows)

- **腳本換行符號**：設定 [.gitattributes](file:///home/dengkai/projects/django-on-docker/.gitattributes) 強制 `*.sh` 與 `Dockerfile` 為 Unix `LF` 格式。
- **實體目錄掛載**：採用相對路徑 `./db_data` 與 `./redis_data` 相容 Linux 與 Windows Docker Desktop。
- **Vite 檔案輪詢**：設定 `vite.config.ts` 內 `watch: { usePolling: true }`，確保 Windows 掛載時熱更新監聽不受影響。
