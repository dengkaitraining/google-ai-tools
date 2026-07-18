# Django on Docker 指定工具細部資訊 (Tools)

本文件詳細記載用於建置、管理、維護與自動化測試 Django on Docker 容器堆疊之指定工具與命令。

---

## 1. 容器編排管理工具 (Docker Compose Tools)

### A. 編譯並啟動容器群 (`docker compose up --build -d`)
- **功能**：重新讀取 [docker-compose.yaml](file:///home/dengkai/projects/django-on-docker/docker-compose.yaml) 與 [.env](file:///home/dengkai/projects/django-on-docker/.env)，並編譯 `web` (Apache)、`backend` (Django)、`frontend` (Vue) 與拉取 `db` (MariaDB 12.3) 與 `redis` (Redis 8.8) 映像檔後以背景模式啟動。
- **使用範例**：
  ```bash
  docker compose up --build -d
  # 或具備權限問題時
  sudo docker compose up --build -d
  ```

### B. 停止與清理容器資源 (`docker compose down -v`)
- **功能**：停止所有運行中之容器，並移除 Docker 橋接網路 `django-net` 與容器專屬 Volume。
- **使用範例**：
  ```bash
  docker compose down -v --rmi all
  ```

---

## 2. 自動化與內建檢查工具 (Automation & Built-in Tools)

### A. TCP 連線檢測工具 (`netcat-openbsd / nc`)
- **位置**：[backend/entrypoint.sh](file:///home/dengkai/projects/django-on-docker/backend/entrypoint.sh)
- **功能**：在 Django 容器初始化時，對 MariaDB 3306 Port 進行 TCP 連線測試，確保資料庫啟動完成後才執行 `migrate`。
- **指令**：
  ```sh
  while ! nc -z $DB_HOST $DB_PORT; do sleep 0.5; done
  ```

### B. Django 超級管理員自動初始化指令
- **位置**：[backend/entrypoint.sh](file:///home/dengkai/projects/django-on-docker/backend/entrypoint.sh)
- **功能**：執行 Python Shell snippet 自動查詢 MariaDB 12.3 中的 `auth_user` 表，若無帳號則自動建立 `DJANGO_SUPERUSER_USERNAME`。

---

## 3. 端點驗證與健康檢查工具 (API & HTTP Verification Tools)

### A. 端點健康測試指令 (`curl`)
- **測試 1：根目錄純文字回應**
  ```bash
  curl -s http://localhost/
  # 預期輸出：Django + Vue.js Web 資訊系統開發環境的服務已啟用。
  ```

- **測試 2：健康檢查 JSON API (MariaDB & Redis)**
  ```bash
  curl -s http://localhost/api/status/
  # 預期輸出：{"status": "online", "database": {"status": "connected"}, "redis": {"status": "connected"}}
  ```

- **測試 3：Vue 3.5 資訊系統儀表板**
  ```bash
  curl -sI http://localhost/tech-stack/
  # 預期輸出：HTTP/1.1 200 OK (Content-Type: text/html)
  ```
