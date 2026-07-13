# 高鐵 PDF 車票解析與合併實作計畫

此計畫的目的在於自動化處理 `Tickets` 資料夾內的所有 PDF 高鐵車票，解析出乘車時間與票價，複製並重命名，移動到今日日期的資料夾下，並合併成一份 PDF 且在最後一頁底部加上總金額。

## User Review Required

> [!IMPORTANT]
> - 本實作將使用 **Python 3.14** 與 `uv` 建立虛擬環境，並安裝 `pypdf` 及 `reportlab` 套件。
> - 為了避免中文字型亂碼，我們將使用系統內建的 `DroidSansFallbackFull.ttf` 字型來繪製最底部的「費用：[總金額]」文字。
> - 處理時間的格式化：例如 `2025/08/24 08:41` 將格式化為 `20250824-0841`，以確保能作為合法檔名使用。

## Proposed Changes

### [Python Script & Environment Setup]

我們將在專案根目錄下建立虛擬環境，並新增一個腳本 `process_tickets.py` 來執行所有邏輯。

#### [NEW] [process_tickets.py](file:///home/dengkai/projects/google-ai-tools/antigravity-ide/agy-ide-start/process_tickets.py)

此腳本將會執行以下步驟：
1. **載入今天日期**：格式化為 `YYYYMMDD`（例如 `20260713`）。
2. **解析 PDF**：
   - 讀取 `Tickets` 資料夾中的所有 `.pdf` 檔案。
   - 使用 Regex 提取「乘車日期」（Travel Date）、「起程時間」與「票款」（Fare）。
   - 產生新檔名格式：`[時間][票價]原檔名`，如 `[20250824-0841][1160]ticket_A.pdf`。
3. **複製與移動**：
   - 建立資料夾 `Tickets-YYYYMMDD`（例如 `Tickets-20260713`）。
   - 將複製且重新命名的 PDF 檔案寫入 `Tickets-YYYYMMDD` 目錄中。
4. **合併 PDF**：
   - 依據時間順序將 `Tickets-YYYYMMDD` 下的 PDF 檔案排序。
   - 使用 `pypdf.PdfWriter` 進行合併。
   - 計算總金額。
5. **添加費用總額**：
   - 使用 `reportlab` 建立一頁透明的 A4 PDF，並在底部 (y=30) 繪製「`費用：[總金額]`」或「`費用 2320`」等中文字樣。
   - 將此透明 PDF 頁面疊加（overlay）至合併 PDF 的最後一頁底端。
   - 輸出為 `TicketsYYYYMMDD-merge.pdf`（例如 `Tickets20260713-merge.pdf`）。

## Verification Plan

### Automated Tests & Executions
- 執行以下指令建立環境並執行腳本：
  ```bash
  # 1. 建立虛擬環境
  ~/.local/bin/uv venv
  # 2. 安裝套件
  ~/.local/bin/uv pip install pypdf reportlab
  # 3. 執行主程式
  .venv/bin/python process_tickets.py
  ```

### Manual Verification
- 確認是否成功建立了 `Tickets-[日期]` 資料夾。
- 確認該資料夾內包含重新命名的 `[時間][票價]原檔名.pdf`。
- 確認根目錄生成了 `Tickets[日期]-merge.pdf` 且最後一頁的最下方有顯示正確的總金額。
