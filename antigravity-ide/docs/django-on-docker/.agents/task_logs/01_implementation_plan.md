# Django 5.2 + Vue.js 3.5 資訊系統容器化開發環境實作計畫 (Implementation Plan)

本實作計畫詳細記載基於 Docker Compose 建立之 **Python Django 5.2 (整合 Django Unfold 後台)**、**MariaDB 12.3 關聯式資料庫**、**Vue.js 3.5 (整合 TypeScript 與 Tailwind CSS 4.3)**、**Apache HTTPD 反向代理** 與 **Redis 8.8** 完整 Stack 之架構與服務設計。

---

## 1. MariaDB 12.3 與 Django 5.2 協作與運作機制說明

在本專案的容器化架構中，**MariaDB 12.3 關聯式資料庫**與 **Django 5.2 LTS 後端框架** 透過以下 6 大核心機制緊密協作與高效率運作：

### A. 原生 C-Extension 驅動與引擎轉接層 (Driver & Engine Layer)
- **驅動套件**：Django 5.2 透過 `mysqlclient` 套件（專案內 `backend/Dockerfile` 於 Python 3.11 Slim 映像檔中以 `default-libmysqlclient-dev` 與 `build-essential` 編譯）與 MariaDB 進行高效率原生 C 語言層級通訊。
- **ORM 設定檔**：在 [backend/core/settings.py](file:///home/dengkai/projects/django-on-docker/backend/core/settings.py) 中，將 `DATABASES['default']['ENGINE']` 設定為 `'django.db.backends.mysql'`，並啟用 `'charset': 'utf8mb4'`，完美對應 MariaDB 12.3 之全 Unicode / Emoji 儲存需求。
- **動態憑證注入**：資料庫連線參數 (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`) 透過 [.env](file:///home/dengkai/projects/django-on-docker/.env) 全局注入，雙方於 Docker Bridge 網路 (`django-net`) 內透過 Service Name `db:3306` 溝通。

### B. 容器初始化與健康狀態等待協定 (TCP Health Waiting Protocol)
- 在 [backend/entrypoint.sh](file:///home/dengkai/projects/django-on-docker/backend/entrypoint.sh) 啟動腳本中，編寫了 `nc -z $DB_HOST $DB_PORT` 的 TCP 輪詢等待機制。
- 當 MariaDB 12.3 容器啟動並完成數據庫初始化且開啟 3306 Port 時，Django 才開始執行後續 ORM 指令，避免資料庫未就緒導致 Django 連線失敗。

### C. 自動化 Migration 與資料表 Schema 建置
- 資料庫就緒後，`entrypoint.sh` 自動執行 `python manage.py migrate --noinput`。
- Django 5.2 的 ORM 自動檢查 MariaDB 12.3 中的 `django_migrations` 資料表，自動執行 DDL SQL 建表指令，建立包括 `auth_user`、`django_session` 等關聯資料表結構。

### D. 自動化超級管理員帳號建立 (Auto Superuser Creation)
- Migration 完成後，`entrypoint.sh` 自動執行內嵌 Python Shell 腳本，查詢 MariaDB 12.3 的 `auth_user` 資料表。
- 若偵測到憑證設定檔中 (`DJANGO_SUPERUSER_USERNAME`) 的帳號不存在，自動執行 `User.objects.create_superuser()` 將超級管理員資料寫入 MariaDB 12.3 中，實現啟動即可以 Unfold 後台登入。

### E. 資料庫自定義調校與 Command Options
- **Docker Compose Command Options**：MariaDB 容器在 [docker-compose.yaml](file:///home/dengkai/projects/django-on-docker/docker-compose.yaml) 中設定有顯式 command：
  ```yaml
  command:
    - --character-set-server=utf8mb4
    - --collation-server=utf8mb4_unicode_ci
    - --max-connections=250
    - --default-storage-engine=InnoDB
  ```
- **User-Defined Config Mount**：載入 [db_conf/my_custom.cnf](file:///home/dengkai/projects/django-on-docker/db_conf/my_custom.cnf)，調校 `innodb_buffer_pool_size = 256M`、最大連線數 `250` 與慢查詢日誌，確保高併發下與 Django 5.2 ORM 通訊無瓶頸。

### F. 即時連線檢測與實體持久化 (Health Check & Persistence)
- **即時 SQL 檢測**：[backend/core/views.py](file:///home/dengkai/projects/django-on-docker/backend/core/views.py) 的 `/api/status/` 視圖執行 `connection.cursor().execute("SELECT 1")` 測試 SQL 查詢能力。
- **持久化機制**：MariaDB 12.3 之 `/var/lib/mysql` 目錄透過 Volume 映射至宿主機實體路徑 `./db_data`，確保容器重啟時 SQL 資料完全保留。

---

## 2. 系統服務佈局 (Service Layout)

```text
/home/dengkai/projects/django-on-docker/
├── .env                              # 全局環境變數與自定義設定檔路徑
├── .gitattributes                    # 強制 LF 換行符號 (Linux/Windows 跨平台支援)
├── .gitignore                        # 忽略本地 Volume 資料與 Node/Python 暫存檔
├── docker-compose.yaml               # Docker Compose 5 大服務與 Bridge 網路定義
├── README.md                         # 專案詳細說明文件
├── .agents/
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
│   ├── entrypoint.sh                 # 等待 MariaDB 3306、自動 Migration 與自動 Superuser
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
├── db_data/                          # MariaDB 12.3 實體持久化目錄 (Git 忽略)
└── redis_data/                       # Redis 8.8 實體持久化目錄 (Git 忽略)
```

---

## 3. URL 路由映射與功能規劃

1. **`http://localhost/` (根路由)**：
   - 轉接至 Django Backend (`/`)，回應純文字訊息：`Django + Vue.js Web 資訊系統開發環境的服務已啟用。`
2. **`http://localhost/tech-stack/` (系統儀表板)**：
   - 轉接至 Vue 3.5 Frontend (`/tech-stack/`)，展示 5 大容器節點狀態儀表板。
   - **檢測機制**：首次連線自動檢查 1 次，爾後每 10 分鐘 (`600,000 ms`) 自動重新檢測各服務狀態。
3. **`http://localhost/admin/` (Unfold 後台)**：
   - 轉接至 Django Unfold 管理員介面 (`/admin/`)，資料儲存於 MariaDB 12.3 `auth_user` 表。
4. **`http://localhost/api/status/` (連線檢測 API)**：
   - 轉接至 Django Backend (`/api/status/`)，動態對 MariaDB 12.3 執行 `SELECT 1` 查詢與 Redis 寫入測試並回傳 JSON。
