# Django on Docker 準則細部資訊 (Rules)

本檔案詳細記錄維護與開發本專案時必須嚴格遵守的規範與準則。

---

## 1. 全專案繁體中文註解規範
- 專案內所有代碼（包含 `.py`, `.ts`, `.vue`, `.sh`）與服務設定檔（包含 `.yaml`, `.cnf`, `.conf`, `.env`, `.json`, `Dockerfile`）必須維持完整且詳細的繁體中文註解與功能描述。
- 每項設定參數、視圖處理函式與組件生命週期必須詳述其用途與運作機制。

---

## 2. 跨平台防錯與字元集規範
- **LF 換行符號**：所有 `.sh` 腳本與 Docker 設定必須維持 Unix `LF` 換行格式（受 [.gitattributes](file:///home/dengkai/projects/django-on-docker/.gitattributes) 強制約束），防止 Windows CRLF 導致容器執行失敗。
- **實體 Volume 掛載**：MariaDB 與 Redis 之 Volume 對應採相對路徑 `./db_data` 與 `./redis_data`，確保相容 Linux 與 Windows Docker Desktop。
- **Vite 熱更新**：Vite 於 `vite.config.ts` 內必須啟用 `watch: { usePolling: true }` 檔案輪詢機制。

---

## 3. 服務獨立自定義設定檔規範 (User-Defined Configs)
- **Apache HTTPD**：`APACHE_CUSTOM_CONF=./apache/httpd-custom.conf` 自 `.env` 宣告並掛載至 `/usr/local/apache2/conf/httpd-custom.conf`。
- **MariaDB 12.3**：`MARIADB_CUSTOM_CONF=./db_conf/my_custom.cnf` 自 `.env` 宣告並掛載至 `/etc/mysql/conf.d/my_custom.cnf`。
- **Redis 8.8**：`REDIS_CUSTOM_CONF=./redis_conf/redis.conf` 自 `.env` 宣告並掛載至 `/usr/local/etc/redis/redis.conf`。

---

## 4. URL 路由與回應規範
- **`http://localhost/`**：轉接至 Django Backend (`/`)，回應純文字：`Django + Vue.js Web 資訊系統開發環境的服務已啟用。`
- **`http://localhost/tech-stack/`**：轉接至 Vue 3.5 Frontend (`/tech-stack/`) 資訊系統儀表板 (首次自動檢查，爾後每 10 分鐘 `600,000 ms` 定時自動重新檢測 1 次)。
- **`http://localhost/admin/`**：轉接至 Django Unfold 後台 (資料存於 MariaDB 12.3 `auth_user` 表)。
- **`http://localhost/api/status/`**：健康檢查 JSON API (對 MariaDB 執行 `SELECT 1` 檢測與 Redis 寫入測試)。
