# Django 5.2 + Vue.js 3.5 開發環境任務清單 (Task List)

- [x] 建立全局環境變數設定檔 (`.env`)，包含 Apache、MariaDB 與 Redis 之使用者自定義設定檔路徑
- [x] 建立服務自定義設定檔 (`apache/httpd-custom.conf`, `db_conf/my_custom.cnf`, `redis_conf/redis.conf`)
- [x] 配置 `docker-compose.yaml` 中 Apache、MariaDB 12.3 與 Redis 8.8 之顯式 `command` 運行選項 (Options)
- [x] 實作 MariaDB 12.3 與 Django 5.2 ORM 之原生 C 語言驅動 (`mysqlclient`) 與 `utf8mb4` 全字元集通訊機制
- [x] 實作 `entrypoint.sh` 之 MariaDB 3306 TCP 健康狀態等待、自動 Migration 與自動 Superuser 建立機制
- [x] 設定 Django 根路徑 (`/`) 回傳純文字訊息：`Django + Vue.js Web 資訊系統開發環境的服務已啟用。`
- [x] 移轉 Vue 3.5 前端資訊系統儀表板路徑至 `/tech-stack/` (`http://localhost/tech-stack/`)
- [x] 設定 `App.vue` 首次連線自動檢查服務狀態 1 次，爾後每 10 分鐘 (`600,000 ms`) 自動重新檢查機制
- [x] 建立 Django 後端服務檔案 (`Dockerfile`, `requirements.txt`, `entrypoint.sh`)
- [x] 初始化 Django 專案結構 (`manage.py`, `core/settings.py`, `core/urls.py`, `core/views.py`, `core/wsgi.py`, `core/asgi.py`)
- [x] 建立 Vue.js 前端服務檔案 (`Dockerfile`, `package.json`, `vite.config.ts`, `tsconfig.json`, `App.vue`, `style.css`, `main.ts`, `vite-env.d.ts`)
- [x] 補齊專案內全數 27 個程式與服務設定檔 (`.py`, `.yaml`, `.cnf`, `.conf`, `.env`, `.json`, `.ts`, `.sh`, `Dockerfile`, `.vue`) 之詳細繁體中文註解與功能描述
- [x] 建立 Linux/Windows 跨平台防錯配置 (`.gitattributes`, `LF` 換行符號, 相對 Volume 路徑, Vite 輪詢)
- [x] 重新啟動與驗證全新容器群 (`docker compose up --build -d`)
- [x] 輸出專案文件至 `./.agents/task_logs/` (`01_implementation_plan.md`, `02_task_list.md`, `03_walkthrough.md`)
- [x] 建立並維護最新版 [README.md](file:///home/dengkai/projects/django-on-docker/README.md) (含 3 大 Mermaid 架構/流程/時序圖與 MariaDB 12.3 + Django 5.2 協作運作說明)
