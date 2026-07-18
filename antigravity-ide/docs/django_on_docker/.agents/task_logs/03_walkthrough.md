# Django + Vue.js 開發環境逐步解說與驗證報告 (Walkthrough)

本報告記載 **Python Django 5.2 + Vue 3.5 + Apache HTTPD + MariaDB 12.3 + Redis 8.8** 容器化環境之完整測試驗證結果、檔案架構與註解說明。

---

## 1. 服務運行狀態與 HTTP 端點測試結果

已透過實際 `curl` 測試驗證所有服務端點運作正常：

| 測試網址 | 預期 HTTP 狀態與回應內容 | 實測驗證結果 |
| :--- | :--- | :--- |
| **`http://localhost/`** | 回應 200 OK 純文字：`Django + Vue.js Web 資訊系統開發環境的服務已啟用。` | **成功 (200 OK)** |
| **`http://localhost/tech-stack/`** | 回應 200 OK HTML 頁面，載入 Vue 3.5 資訊系統儀表板 (含 10 分鐘自動檢測) | **成功 (200 OK)** |
| **`http://localhost/admin/`** | 回應 200 OK HTML 頁面，載入 Django Unfold 後台管理介面 | **成功 (200 OK)** |
| **`http://localhost/api/status/`** | 回應 200 OK JSON 數據：`{"status": "online", "database": {"status": "connected"}, "redis": {"status": "connected"}}` | **成功 (200 OK)** |

---

## 2. 專案內全數檔案與中文註解說明目錄

專案內全數 27 個核心檔案均已加上詳細的繁體中文註解與功能描述：

### A. 全局與環境變數設定檔
- **[.env](file:///home/dengkai/projects/django-on-docker/.env)**：全局變數，包含 `APACHE_CUSTOM_CONF`、`MARIADB_CUSTOM_CONF`、`REDIS_CUSTOM_CONF`、超級管理員帳密與 Ports。
- **[docker-compose.yaml](file:///home/dengkai/projects/django-on-docker/docker-compose.yaml)**：5 大服務編排檔，包含各服務之 `command` 運行選項與 Volumes 掛載。
- **[.gitattributes](file:///home/dengkai/projects/django-on-docker/.gitattributes)**：強制 LF 換行符號規範。
- **[.gitignore](file:///home/dengkai/projects/django-on-docker/.gitignore)**：Git 忽略規則。

### B. 服務獨立自定義設定檔 (User-Defined Configs)
- **[apache/httpd-custom.conf](file:///home/dengkai/projects/django-on-docker/apache/httpd-custom.conf)**：Apache 反向代理與 WebSocket 轉接設定。
- **[db_conf/my_custom.cnf](file:///home/dengkai/projects/django-on-docker/db_conf/my_custom.cnf)**：MariaDB 字元集 (`utf8mb4`)、連線池 (250) 與 InnoDB 記憶體調校。
- **[redis_conf/redis.conf](file:///home/dengkai/projects/django-on-docker/redis_conf/redis.conf)**：Redis 記憶體上限 (256MB)、LRU 快取淘汰與 snapshot 寫入設定。

### C. Django 後端專案檔
- **[backend/Dockerfile](file:///home/dengkai/projects/django-on-docker/backend/Dockerfile)** & **[backend/entrypoint.sh](file:///home/dengkai/projects/django-on-docker/backend/entrypoint.sh)**：Python 3.11 環境構建、MariaDB 連線等待、自動 Migration 與自動 Superuser。
- **[backend/requirements.txt](file:///home/dengkai/projects/django-on-docker/backend/requirements.txt)**：相依套件清單說明。
- **[backend/manage.py](file:///home/dengkai/projects/django-on-docker/backend/manage.py)**：命令行管理工具腳本。
- **[backend/core/settings.py](file:///home/dengkai/projects/django-on-docker/backend/core/settings.py)**：MariaDB、Redis 快取與 Unfold 後台配置。
- **[backend/core/views.py](file:///home/dengkai/projects/django-on-docker/backend/core/views.py)**：根目錄純文字回應 (`home_view`) 與動態健康檢測 API (`health_check`)。
- **[backend/core/urls.py](file:///home/dengkai/projects/django-on-docker/backend/core/urls.py)**：路由映設設定。
- **[backend/core/wsgi.py](file:///home/dengkai/projects/django-on-docker/backend/core/wsgi.py)** & **[backend/core/asgi.py](file:///home/dengkai/projects/django-on-docker/backend/core/asgi.py)**：網關介面設定。

### D. Vue.js 前端專案檔
- **[frontend/Dockerfile](file:///home/dengkai/projects/django-on-docker/frontend/Dockerfile)** & **[frontend/package.json](file:///home/dengkai/projects/django-on-docker/frontend/package.json)**：Node 20 開發環境與 Vue 3.5 套件設定。
- **[frontend/vite.config.ts](file:///home/dengkai/projects/django-on-docker/frontend/vite.config.ts)**：Vite 5 (base: `/tech-stack/`)、Tailwind CSS v4 插件與 HMR 設定。
- **[frontend/tsconfig.json](file:///home/dengkai/projects/django-on-docker/frontend/tsconfig.json)**：TypeScript 編譯選項。
- **[frontend/index.html](file:///home/dengkai/projects/django-on-docker/frontend/index.html)**：HTML 入口與 Google Fonts 字體載入。
- **[frontend/src/App.vue](file:///home/dengkai/projects/django-on-docker/frontend/src/App.vue)**：前端 Dashboard 儀表板，具備首次連線檢測 1 次與爾後每 10 分鐘自動檢測 1 次之定時器機制。
- **[frontend/src/style.css](file:///home/dengkai/projects/django-on-docker/frontend/src/style.css)**：Tailwind CSS v4 `@import "tailwindcss";` 指令。
- **[frontend/src/main.ts](file:///home/dengkai/projects/django-on-docker/frontend/src/main.ts)** & **[frontend/src/vite-env.d.ts](file:///home/dengkai/projects/django-on-docker/frontend/src/vite-env.d.ts)**：進入點腳本與型態宣告。

---

## 3. 系統存取資訊

- **Vue.js 儀表板 (每10分鐘自動檢測)**：[http://localhost/tech-stack/](http://localhost/tech-stack/)
- **啟用純文字回應**：[http://localhost/](http://localhost/)
- **Django Unfold 後台管理介面**：[http://localhost/admin/](http://localhost/admin/) (預設帳號：`admin`)
- **健康檢查 JSON API**：[http://localhost/api/status/](http://localhost/api/status/)
