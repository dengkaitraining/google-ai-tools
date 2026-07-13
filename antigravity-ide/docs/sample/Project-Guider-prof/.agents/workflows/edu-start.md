---
description: 【階段一】引導學生描述專案目標，由 Agent 撰寫並建立 requirements.md 文件，並以問答對齊細節
---

1. 獲取專案描述
   請學生提供他們的開發構想、專案目標或問題描述。如果學生沒有提供足夠資訊，請主動詢問引導。

2. 撰寫需求文件 (requirements.md)
   根據學生的描述，由 Agent 建立並撰寫專案根目錄的 `requirements.md` 檔案，內容應包含：
   - 專案目標與背景 (Project Goal)
   - 功能性需求 (Functional Requirements)
   - 技術要求 (Technical Requirements)：包含所採用的程式語言、技術棧或框架。
   - 非功能性需求（如環境與限制）(Non-functional Requirements)
   - 使用者情境 (User Scenarios)
   - 若學生對以上無法回答，則採取 AI Agent 的專業建議。

3. 需求對齊 (Alignment)
   對學生提出 2~3 個具體的澄清問題（例如：「輸入資料的格式是什麼？」、「需要支援哪些錯誤處理？」），引導學生思考細節，並根據學生的回覆更新 `requirements.md`。

4. 學生審查與確認
   引導學生審查 `requirements.md`。確認無誤後，提醒學生輸入 `/edu-plan` 進入下一個實作計畫階段。