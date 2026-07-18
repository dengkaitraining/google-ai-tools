# [Django + Vue.js (TS/Tailwind) 資訊系統容器化開發環境實作計畫 (Implementation Plan)]
------
# 使用 docker compose 建立 Python Django Web base 資訊系統開發環境。
## 1. 應用套件與技術堆疊：
 - 網頁伺服器：apache httpd 伺服器。
 - 資料庫伺服器：MariaDB 伺服器。
 - 前端技術堆疊：TypeScript、Vue.js 框架、Tailwind CSS UI 套件。
 - 後端技術堆疊：Python Django 框架、Python Django Unfold 後台管理套件。
 - 資料庫連線技術：使用 Redis 技術以避免高併發的問題。
## 2. 技術堆疊容器化：
 - 將「1. 應用套件與技術堆疊」容器化，轉換為 docker compose 並建立下列文件資訊：
   - Dockerfile
   - docker-compose.yaml
   - .env
   ...
   等 docker compose 文件。
 - docker-compose.yaml 內 volumes 資料儲存目錄指向專案內實體路徑。
 - docker-compose.yaml 內加入 docker network bridge 網路連線。
 
## 3. 檢查 docker compose 文件
 - 檢查 docker compose 相關文件在 Linux , Windows 運行是否正確，並協助修補文件內容。

------
1. Vue 更新至 3.5。
2. Redis 更新至 8.8。
3. MariaDB 更新至 12.3。
4. Django 更新至 5.2。
5. Tailwind CSS UI 更新至 4.3。

------
使用 sudo deocker compose up --build -d 發生錯誤資訊：Error response from daemon: failed to create task for container: failed to create shim task: OCI runtime create failed: runc create failed: unable to start container process: error during container init: exec: "/app/entrypoint.sh": permission denied

------
# 1. 移除所有容器 docker compose 資訊、空間 volumes 與 映像檔資訊。
# 2. 在 .env 加入 ：
 - Django Unfold 後台管理者的「帳戶」與「密碼」資訊。
 - MariaDB 使用者端自定義(user define)設定檔資訊。
# 3. 重新執行全新的容器 docker compose 作業 (如：docker compose up --build -d)。

------
# 1. 在 .env 加入 ：
 - Apache httpd 使用者端自定義(user define)設定檔資訊。
 - Redis 使用者端自定義(user define)設定檔資訊。
# 2. Apache httpd、MariaDB、Redis 請加入「option」的設定資訊。
# 3. 專案內的程式(.py 等程式)、服務設定檔(.yaml, .cnf, .conf, .env, .json, .ts, .sh, Dockerfile 等設定檔)加入詳細的說明與功能描述。

------
# 1. 將首頁「Django + Vue.js Web 資訊系統開發環境」的路徑「 http://localhost/」修改為「http://localhost/tech-stack」。
# 2. 原本路徑「 http://localhost/」改為顯示「Django + Vue.js Web 資訊系統開發環境的服務以啟用 。」的簡單文字資訊。
# 3. 修改後請更新專案內的程式(.py 等程式)、服務設定檔(.yaml, .cnf, .conf, .env, .json, .ts, .sh, Dockerfile 等設定檔)的詳細說明與功能描述。

------
# 1. 修改「Django + Vue.js Web 資訊系統開發環境」(http://localhost/tech-stack) 設定資訊：
 - 第一次連上「Django + Vue.js Web 資訊系統開發環境」(http://localhost/tech-stack) 自動檢查各項服務狀態一次。
 - 爾後 「Django + Vue.js Web 資訊系統開發環境」(http://localhost/tech-stack) 每 10 分鐘自動檢查各項服務狀態一次。
# 2. 修改後請更新專案內的程式(.py 等程式)、服務設定檔(.yaml, .cnf, .conf, .env, .json, .ts, .sh, Dockerfile 等設定檔)的詳細說明與功能描述。

------
# 1. 檢查「Django + Vue.js Web 資訊系統開發環境」的狀態資訊：
 - 檢查專案內的程式(.py 等程式)、服務設定檔(.yaml, .cnf, .conf, .env, .json, .ts, .sh, Dockerfile 等設定檔)的資訊是否正確。
 - 檢查 docker compose 建立後的運行狀態是否正確。
# 2. 檢查完成後修改後請更新專案內的程式(.py 等程式)、服務設定檔(.yaml, .cnf, .conf, .env, .json, .ts, .sh, Dockerfile 等設定檔)的詳細說明與功能描述。
# 3. 檢查與修改成後，依據專案內修正的資訊內容，例如：專案內的程式(.py 等程式)、服務設定檔(.yaml, .cnf, .conf, .env, .json, .ts, .sh, Dockerfile 等設定檔)等，修改以下內容：
 - 依據專案目前的結果，更新「實作計畫 (Implementation Plan)」、「任務清單 (Task List)」、「逐步解說 (Walkthrough)」詳細資訊
 - 更新完成後:
   - 「實作計畫 (Implementation Plan)」資訊儲存在專案內「./agents/task_logs/01_implementation_plan.md」的檔案。
   - 「任務清單 (Task List)」資訊儲存在專案內「./agents/task_logs/02_task_list.md」的檔案。
   - 「逐步解說 (Walkthrough)」資訊儲存在專案內「./agents/task_logs/03_walkthrough.md」的檔案。

------
# 1. 依據文件資訊<spec>建立以下資訊內容<info>：
 <spec>
 - 「實作計畫 (Implementation Plan)」的資訊(/home/dengkai/projects/django-on-docker/agents/task_logs/01_implementation_plan.md)。
 - 「任務清單 (Task List)」資訊儲存在專案內的資訊(/home/dengkai/projects/django-on-docker/agents/task_logs/02_task_list.md)。
 - 「逐步解說 (Walkthrough)」資訊儲存在專案內的資訊(/home/dengkai/projects/django-on-docker/agents/task_logs/03_walkthrough.md)。
 </spec>
 <info>
 - 建立詳細的 README.md 說明檔資訊包含：
   (1) 專案簡介 (Description)、mermaid 格式的「系統架構圖 (System Architecture)」、「系統流程圖 (System Flowchart」、「系統時序圖 (Sequence Diagram)」。
   (2) 安裝與建置指南 (Installation and Setup)。
   (3) 設定說明 (Configuration)。
   (4) 執行與啟動本地服務 (Usage / Getting Started)。
   (5) 資料夾結構與架構簡述 (Project Structure)。
   (6) 系統測試與驗證 (System Testing and Verification)。
   (7) 貢獻與授權 (Contributing and License)。
 </info>
# 2. 專案內的 agents 資料夾「/home/dengkai/projects/django-on-docker/agents」修改為「/home/dengkai/projects/django-on-docker/.agents」。

------
# 1. 詳細說明專案內「MariaDB 12.3 關聯式資料庫」與「Django 更新至 5.2」如何協作、運作？
# 2. 依據「1.」詳細說明的協作、運作結果更新「實作計畫 (Implementation Plan)」、「任務清單 (Task List)」、「逐步解說 (Walkthrough)」詳細資訊，也一併更新<data>內容：
 <data>
   (1) 「實作計畫 (Implementation Plan)」的資訊(/home/dengkai/projects/django-on-docker/.agents/task_logs/01_implementation_plan.md)。
   (2) 「任務清單 (Task List)」資訊儲存在專案內的資訊(/home/dengkai/projects/django-on-docker/.agents/task_logs/02_task_list.md)。
   (3) 「逐步解說 (Walkthrough)」資訊儲存在專案內的資訊(/home/dengkai/projects/django-on-docker/.agents/task_logs/03_walkthrough.md)。
 </data>
# 3. 依據「1.」詳細說明的協作、運作結果更新「 README.md」說明檔資訊，包含<info>內容：
 <info>
   (1) 專案簡介 (Description)、mermaid 格式的「系統架構圖 (System Architecture)」、「系統流程圖 (System Flowchart)」、「系統時序圖 (Sequence Diagram)」。
   (2) 安裝與建置指南 (Installation and Setup)。
   (3) 設定說明 (Configuration)。
   (4) 執行與啟動本地服務 (Usage / Getting Started)。
   (5) 資料夾結構與架構簡述 (Project Structure)。
   (6) 系統測試與驗證 (System Testing and Verification)。
   (7) 貢獻與授權 (Contributing and License)。
 </info>

------
# 1. 依據文件資訊<spec>建立 skills 資訊內容<skills>：
 <spec>
 - 「實作計畫 (Implementation Plan)」的資訊(/home/dengkai/projects/django-on-docker/.agents/task_logs/01_implementation_plan.md)。
 - 「任務清單 (Task List)」資訊儲存在專案內的資訊(/home/dengkai/projects/django-on-docker/.agents/task_logs/02_task_list.md)。
 - 「逐步解說 (Walkthrough)」資訊儲存在專案內的資訊(/home/dengkai/projects/django-on-docker/.agents/task_logs/03_walkthrough.md)。
 - 「README.md 說明檔資訊」(/home/dengkai/projects/django-on-docker/README.md)。
 </spec>
 <skills>
 - 建立的 /home/dengkai/projects/django-on-docker/.agents/skills/django-on-docker/SKILL.md 檔案資訊包含：
   (1) SKILL 飆頭描述 (name, description)。
   (2) 角色定位 (role)。
   (3) 準則 (rules)。
   (4) 指定工具 (tools)：指定工具細部資訊，以 markdown 檔案儲存在 /home/dengkai/projects/django-on-docker/.agents/skills/django-on-docker/scripts/ 的資料夾內。
   (5) 逐步解說 (Walkthrough)：逐步解說項目細部資訊，以 markdown 檔案儲存在 /home/dengkai/projects/django-on-docker/.agents/skills/django-on-docker/references/ 的資料夾內。
   (6) 完成後的檢查 (Final inspection)：檢查作業細部資訊，以 markdown 檔案儲存在 /home/dengkai/projects/django-on-docker/.agents/skills/django-on-docker/inspections/ 的資料夾內。
 </skills>

------
# 1. 移除「1. SKILL 表頭描述 (Header Description)」標題資訊，內容修改為：
---
name: django-on-docker
description: 提供基於 Docker Compose 容器化技術之 Python Django 5.2 LTS、Vue.js 3.5、MariaDB 12.3、Redis 8.8 與 Apache HTTPD 多容器開發環境建立、管理、維護與自動化檢查指南。
---
# 2. 準則 (rules)：準則細部資訊，以 markdown 檔案儲存在 /home/dengkai/projects/django-on-docker/.agents/skills/django-on-docker/rules/ 的資料夾內。