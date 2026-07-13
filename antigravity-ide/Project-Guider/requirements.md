# 需求文件 (requirements.md) - 車票合併作業 (Ticket Merger)

本文件定義「車票合併作業」專案的開發目標、功能與技術需求，作為後續實作與驗證的依據。

---

## 1. 專案目標與背景 (Project Goal)

在日常報帳或整理財務憑證時，手動讀取 PDF 車票、修改檔名、歸檔並合併是一件繁瑣且容易出錯的工作。
本專案旨在開發一個 **自動化車票處理工具**。該工具能自動從 `Tickets/` 資料夾內的 PDF 車票中擷取「搭乘日期」、「搭乘時間」與「票價」，複製並重新命名檔案，將複製後的檔案移至 `Tickets-[current_timestamp]` 歸檔資料夾，最後將這些 PDF 合併為單一 PDF 檔，並在合併檔最下方加入總金額。

---

## 2. 功能性需求 (Functional Requirements)

*   **PDF 車票解析與複製命名**：
    *   讀取 `Tickets/` 資料夾內的所有 PDF 檔案。
    *   解析 PDF 內容，擷取其中的 **乘車日期** (格式如：`YYYYMMDD`)、**乘車時間** (格式如：`HHMM`) 與 **票價** (數字，如 `1200`)。
    *   複製原始 PDF，並將複製的檔案命名為：`[日期][時間][票價]原檔名.pdf`（例如：`[20260713][1430][1200]original_name.pdf`）。
*   **檔案歸檔與移動**：
    *   在專案目錄下建立名為 `Tickets-[current_timestamp]` 的資料夾，其中 `current_timestamp` 為執行腳本時的當前時間戳記（格式為 `YYYYMMDD_HHMMSS`，如 `Tickets-20260713_151700`）。
    *   將上述所有重新命名後的複製檔案，移動到該 `Tickets-[current_timestamp]` 資料夾中。
*   **PDF 合併與加總**：
    *   將這批重新命名後的 PDF 檔案合併為一個單一 PDF 檔。
    *   合併後的 PDF 檔命名為：`Tickets-[日期][時間][總金額]-merge.pdf`。
        *   其中 `[日期][時間]` 為執行腳本當下的時間（格式為 `YYYYMMDD-HHMM`），`[總金額]` 為該批車票的票價總和（例如：`Tickets-20260713-1517-2170-merge.pdf`）。
    *   在合併後的 PDF 最下方，動態增加標示該次合併的總費用 `[總金額]`。

---

## 3. 技術要求 (Technical Requirements)

*   **開發語言**：Python 3.10+
*   **環境管理**：強制使用 `uv` 建立與管理虛擬環境（包含產生 `.venv`、使用 `uv pip install` 安裝套件）。
*   **PDF 處理套件**：
    *   文字擷取與解析：使用 `pdfplumber` 或 `pypdf`。
    *   PDF 合併與標記：使用 `pypdf` 合併 PDF。對於底部金額標記，使用 `reportlab` 繪製總金額文字，並透過 `pypdf` 的 PageOverlay 功能將其疊加在合併 PDF 的最後一頁底部。

---

## 4. 非功能性需求 (Non-functional Requirements)

*   **異常處理 (Robustness)**：
    *   若 PDF 檔案毀損、或非標準車票，應跳過該檔案，在終端機輸出警告，並繼續處理其他檔案。
    *   若無法成功解析日期、時間或票價，使用 `[UNKNOWN_DATE]`、`[UNKNOWN_TIME]` 或 `[UNKNOWN_PRICE]` 作為檔名占位符，並將票價計為 0。
*   **日誌輸出**：
    *   執行時在終端機輸出詳細日誌，明確列出每個檔案的解析結果、歸檔位置與合併結果。
*   **原始檔案保護**：
    *   `Tickets/` 資料夾底下的原始 PDF 檔案不可被修改或刪除，所有操作皆針對「複製並重新命名的檔案」進行。

---

## 5. 使用者情境 (User Scenarios)

1.  使用者將數個電子車票 PDF 放進專案根目錄的 `Tickets/` 資料夾下。
2.  執行 `python process_tickets.py`。
3.  程式在專案根目錄下建立歸檔資料夾（如 `Tickets-20260713_151700`），並將重新命名後的車票（如 `[20260713][1430][1200]thsr.pdf`）移入。
4.  程式在根目錄下輸出合併後的 PDF（如 `Tickets-20260713-1517-1200-merge.pdf`），且該 PDF 最下方會顯示總金額。
