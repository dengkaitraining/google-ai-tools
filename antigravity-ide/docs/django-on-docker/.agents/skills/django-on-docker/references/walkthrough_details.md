# Django on Docker 逐步解說細部資訊 (Walkthrough Reference)

本參考文件詳細記載 **Python Django 5.2 + Vue 3.5 + Apache HTTPD + MariaDB 12.3 + Redis 8.8** 容器化系統架構與各元件之協作細節。

---

## 1. 系統架構與反向代理機制

```text
User Request (Port 80)
   │
   ▼
[apache_web Container] Apache HTTPD 2.4 (Reverse Proxy)
   ├── http://localhost/           ──► [django_backend Container] Django 5.2 (Plain Text Response)
   ├── http://localhost/tech-stack/ ──► [vue_frontend Container] Vue 3.5 + Vite (Base: /tech-stack/)
   ├── http://localhost/admin/      ──► [django_backend Container] Django Unfold Admin
   └── http://localhost/api/status/ ──► [django_backend Container] Django Health Check API
                                          │
                                          ├──► [django_db Container] MariaDB 12.3 (mysqlclient C-Extension)
                                          └──► [django_redis Container] Redis 8.8 (django-redis Cache)
```

---

## 2. MariaDB 12.3 與 Django 5.2 協作運作細節

1. **底層驅動層 binding**：
   - Django 5.2 使用 `django.db.backends.mysql` 搭配原生 C 擴充套件 `mysqlclient`。
   - 配置 `charset: utf8mb4` 對應 MariaDB 12.3 最佳化全字元集。
2. **TCP 等待機制**：
   - `entrypoint.sh` 透過 `nc -z db 3306` 進行健康等待輪詢，確保 MariaDB 3306 可連線才開始 ORM 遷移。
3. **schema Migration 與 Superuser 自動化**：
   - 執行 `python manage.py migrate --noinput` 自動建置 `auth_user` 等資料表。
   - 執行 Python Shell 自動查詢 `auth_user`，若無帳號則自動建立 `DJANGO_SUPERUSER_USERNAME`。
4. **自定義設定檔與 Command Options**：
   - MariaDB 載入 `MARIADB_CUSTOM_CONF=./db_conf/my_custom.cnf`，調校 `innodb_buffer_pool_size = 256M` 與最大連線數 `250`。
5. **即時檢測與持久化**：
   - `/api/status/` 透過 `connection.cursor().execute("SELECT 1")` 測試數據庫動態查詢能力。
   - 實體 Volume 掛載 `./db_data:/var/lib/mysql` 保障數據持久化。

---

## 3. Vue 3.5 前端 HMR 與 10 分鐘自動檢測機制

- **路徑與 Base 配置**：`http://localhost/tech-stack/` 映射至 Vue 3.5。Vite 於 [frontend/vite.config.ts](file:///home/dengkai/projects/django-on-docker/frontend/vite.config.ts) 設定 `base: '/tech-stack/'`。
- **WebSocket HMR 代理**：Apache 代理 `/tech-stack/_hmr` 至 `ws://frontend:5173/tech-stack/_hmr`。
- **10 分鐘自動檢測**：[frontend/src/App.vue](file:///home/dengkai/projects/django-on-docker/frontend/src/App.vue) 於 `onMounted` 階段發送 1 次 API 連線檢測，並透過 `setInterval(fetchStatus, 600000)` 設定每 10 分鐘自動重新檢測 1 次狀態，於 `onUnmounted` 階段自動清理定時器。
