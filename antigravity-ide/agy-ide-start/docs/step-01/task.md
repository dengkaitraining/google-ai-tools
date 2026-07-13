# 執行任務清單

- [x] 建立 Python 虛擬環境與安裝套件
  - [x] 執行 `uv venv` 建立虛擬環境
  - [x] 安裝 `pypdf` 與 `reportlab` 套件
- [x] 實作車票處理腳本 (`process_tickets.py`)
  - [x] 讀取 PDF 並使用 Regex 解析日期、時間、票款
  - [x] 複製並重新命名檔案到 `Tickets-[今日日期]` 資料夾
  - [x] 合併 PDF 檔案
  - [x] 使用 `reportlab` 疊加總金額於合併後 PDF 的最後一頁底端
- [x] 執行並驗證
  - [x] 執行腳本，確認是否產生 `Tickets-[今日日期]` 資料夾與其內的檔案
  - [x] 確認是否產生 `Tickets[今日日期]-merge.pdf` 且最下方有總金額
  - [x] 建立 `walkthrough.md` 說明變更與結果
