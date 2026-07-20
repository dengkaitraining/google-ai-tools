# 瀏覽器整合功能
 * Agent 可以直接操作瀏覽器
   * 開啟網頁、點擊按鈕、填寫表單、擷取畫面、錄製整個操作過程。
# 實作 Todo List 網頁應用
```markdown
# 請幫我建立一個 Todo List 網頁應用,需求如下:
## 功能需求:
 1.可以新增待辦事項(輸入文字後按 Enter 或點擊按鈕)
 2.可以標記事項為完成/未完成(點擊切換)
 3.可以刪除事項
 4.可以篩選顯示:全部、未完成、已完成
 5.使用 localStorage 儲存資料,重新整理不會遺失
## 技術要求:
 * 使用純 HTML、CSS、JavaScript(不使用框架)
 * CSS 使用現代化設計,支援響應式佈局
 * JavaScript 使用 ES6+ 語法
 * 程式碼要有適當的註解
 * 請先建立專案結構,然後逐步實作各個功能。
```
# 開啟瀏覽器預覽
# 查看程式碼
# 下測試任務prompt
```markdown
# 請開啟本地檔案 Browser-Subagent\index.html
# 並執行以下測試:
 1.檢查頁面標題是否為「我的待辦事項」。
 2.新增兩個任務:「完成網頁閱讀」與「完成查詢」。
 3.點擊「完成網頁閱讀」將其標記為完成。
 4.切換篩選器到「已完成」,確認只看到「完成網頁閱讀」。
 5.切換回「全部」。
 6.刪除「完成查詢」。
 7.重新整理頁面,確認「完成網頁閱讀」依然是完成狀態。
# 請在完成後回報結果與任何發現的問題。
```
# 爬蟲
```markdown
# 使用Browser Subagent,瀏覽URL 做重點整理,存成md檔。
 * 專案儲存在：「Browser-Subagent/crawl_results」。
 * Adaptive-RAG
 * GraphRAG
 * 配合skill 將md檔轉成pdf。
# 查詢
 * 使用Browser Subagent,瀏覽https://kpp.tbkc.gov.tw/ 輸入車號xxx-xxxx與驗證碼,確定送出。將結果畫面截圖下來，儲存成「Browser-Subagent/screenshots/車號xxx-xxxx-(日期-時間).png」檔案。
```