# Django on Docker 完成後的檢查清單 (Final Inspection)

本文件提供開發者或自動化測試流程於系統完成建置與修補後的最終檢核清單與測試指引。

---

## 1. 服務啟動與容器狀態檢查

- [ ] 執行 `sudo docker ps` 或 `docker compose ps`，確認 5 大容器狀態均為 `Up` 且無無故重啟（Crash Loop）：
  - [ ] `apache_web` (Apache HTTPD 2.4 - Port 80)
  - [ ] `vue_frontend` (Vue 3.5 Dev Server - Port 5173)
  - [ ] `django_backend` (Django 5.2 - Port 8000)
  - [ ] `django_db` (MariaDB 12.3 - Port 3306)
  - [ ] `django_redis` (Redis 8.8 - Port 6379)

---

## 2. 路由與回應內容檢查

- [ ] **根目錄文字檢查**：
  - 存取 `http://localhost/`，回應 Header 狀態 `200 OK`，純文字內容為 `Django + Vue.js Web 資訊系統開發環境的服務已啟用。`
- [ ] **Vue 前端儀表板檢查**：
  - 存取 `http://localhost/tech-stack/`，回應 Header 狀態 `200 OK`，順利載入深色擬態 Dashboard。
  - 驗證頁面顯示「*首次連線自動檢查 1 次 • 爾後每 10 分鐘自動重新檢測 1 次*」標示。
- [ ] **Django Unfold 後台檢查**：
  - 存取 `http://localhost/admin/`，順利顯示 Django Unfold 後台登入畫面。
  - 使用 [.env](file:///home/dengkai/projects/django-on-docker/.env) 之 `DJANGO_SUPERUSER_USERNAME` 與 `DJANGO_SUPERUSER_PASSWORD` 登入成功。
- [ ] **健康檢查 API 檢查**：
  - 存取 `http://localhost/api/status/`，JSON 中 `database.status` 為 `"connected"`，`redis.status` 為 `"connected"`。

---

## 3. 設定檔與全專案註解檢查

- [ ] **繁體中文註解**：專案內全數 27 個核心程式與設定檔（`.py`, `.yaml`, `.cnf`, `.conf`, `.env`, `.json`, `.ts`, `.sh`, `Dockerfile`, `.vue`）皆具備清晰的繁體中文說明。
- [ ] **換行規範**：檢查所有 `.sh` 與 Docker 相關檔案均採用 Unix `LF` 換行符號（由 [.gitattributes](file:///home/dengkai/projects/django-on-docker/.gitattributes) 強制約束）。
- [ ] **獨立自定義設定檔映射**：
  - [ ] Apache 自定義檔：`APACHE_CUSTOM_CONF=./apache/httpd-custom.conf`
  - [ ] MariaDB 自定義檔：`MARIADB_CUSTOM_CONF=./db_conf/my_custom.cnf`
  - [ ] Redis 自定義檔：`REDIS_CUSTOM_CONF=./redis_conf/redis.conf`
