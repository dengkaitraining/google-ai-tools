---
description: 【階段三】引導學生驗證交付的程式碼與 walkthrough.md 報告，並引導複盤與沉澱知識（Evolution）
---

1. 執行測試與驗證 (Verification)
   依據 `implementation_plan.md` 中的驗證計畫，由 Agent 執行測試指令或引導學生啟動程式進行手動功能驗證，確保程式如預期運作。

2. 撰寫交付報告 (Walkthrough)
   測試通過後，由 Agent 建立專案根目錄的 `walkthrough.md` 檔案，內容包含：
   - 本次開發完成的功能清單與變更說明
   - 驗證測試結果、指令輸出或執行的 logs
   - 請學生操作驗證的指引與說明
   > [!NOTE]
   > 請學生閱讀 `walkthrough.md` 並進行最後的驗證確認。

3. 沉澱進化 (Evolution)
   在專案順利完成後，引導學生進行學習複盤與知識沉澱：
   - 詢問學生此次開發過程中有哪些程式設計習慣或規則需要留存（例如：特別的排版、特定的套件使用限制）。引導學生使用 `/learn` 指令將其記錄於全域或專案的 `AGENTS.md` 中。
   - 評估本次開發出的功能是否具備高度重複實用性。若是，引導學生利用 `workflow-skill-creator` 技能將其蒸餾並封裝為自訂的 Custom Skill（技能套件），以供未來的專案直接調用。