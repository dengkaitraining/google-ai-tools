# 車票處理任務完成說明

我們已成功實作並執行了高鐵車票 PDF 解析、複製、改名、移動與合併的自動化腳本。

## 變更項目

1. **環境建立**：
   - 使用 `uv` 建立了 Python 虛擬環境 `.venv`。
   - 安裝了 `pypdf` 與 `reportlab` 套件。
2. **實作核心腳本**：
   - 建立並實作了 [process_tickets.py](file:///home/dengkai/projects/google-ai-tools/antigravity-ide/agy-ide-start/process_tickets.py)。
   - **時間與票價提取**：利用 `pypdf` 讀取 PDF 內容，並結合精準區塊匹配與正則表達式（Regex），解析出乘車日期、出發時間與票款。
   - **改名與複製**：複製原始檔案至 [Tickets-20260713](file:///home/dengkai/projects/google-ai-tools/antigravity-ide/agy-ide-start/Tickets-20260713) 資料夾，並重新命名為 `[時間][票價]原檔名` 的格式。
   - **PDF 合併與疊加**：
     - 將複製後的所有 PDF 依照時間順序排序並進行合併。
     - 使用 `reportlab` 繪製「`費用：`」和「`2320`」（拆分繪製以避開字型編碼產生的 NUL 亂碼字元）。
     - 將繪製的費用透明頁面疊加至合併 PDF 的最後一頁底部。
     - 輸出為 [Tickets20260713-merge.pdf](file:///home/dengkai/projects/google-ai-tools/antigravity-ide/agy-ide-start/Tickets20260713-merge.pdf)。

## 驗證結果

### 產出檔案清單
1. **複製與改名之檔案資料夾**：[Tickets-20260713](file:///home/dengkai/projects/google-ai-tools/antigravity-ide/agy-ide-start/Tickets-20260713)
   - `[20250824-0841][1160]ticket_A.pdf` (台南 08:41 出發，票價 1160)
   - `[20250824-2119][1160]ticket_B.pdf` (板橋 21:19 出發，票價 1160)
2. **合併後之 PDF**：[Tickets20260713-merge.pdf](file:///home/dengkai/projects/google-ai-tools/antigravity-ide/agy-ide-start/Tickets20260713-merge.pdf)

### 總金額驗證
經程式運算，車票總金額為 `1160 + 1160 = 2320`。
使用 `pypdf` 讀取合併後 PDF 最後一頁，成功提取出字串 `費用：\n2320`，且無 NUL 亂碼字元。
在 PDF 檢視器中，最後一頁最底部已完美呈現「費用：2320」。
