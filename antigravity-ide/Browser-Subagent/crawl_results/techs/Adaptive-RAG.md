# Adaptive-RAG 技術重點整理與架構分析

## 概述 (Overview)

**Adaptive-RAG** (Adaptive Retrieval-Augmented Generation，自適應檢索增強生成) 是一種依據**查詢複雜度 (Question Complexity)** 動態調整檢索策略的 LLM 增強框架。此論文發表於 arXiv (arXiv:2403.14403)。

傳統的 RAG 系統大多採取「單一模式 fits all」的設計——對所有問題均執行固定次數的向量檢索，或者完全不檢索。Adaptive-RAG 的目標是在**計算效率 (Computational Efficiency)** 與**回答準確度 (Response Accuracy)** 之間取得最佳平衡。

---

## 核心架構與元件 (Core Architecture & Components)

Adaptive-RAG 的架構主要由以下三大模組構成：

### 1. 複雜度分類器 / 路由 (Complexity Classifier / Router)
* 使用輕量級的語言模型作為 Classifier。
* 當使用者輸入 Query 時，分類器首先評估該查詢的複雜程度。
* 將問題分類為不同的複雜度層級（如簡單事實、中等複雜度、多跳/跨文檔複雜問題）。

### 2. 多階層檢索策略 (Multi-Tiered Retrieval Strategies)
依據分類器的判定結果，系統自動切換至相應的處理解法：
* **無須檢索 (No-Retrieval)**：若問題屬於 LLM 內部參數知識即可解答的簡單常識或基礎問答，直接由 LLM 生成回答，省去外部檢索開銷。
* **單步檢索 (Single-Step Retrieval)**：若問題需要單一外部事實佐證，執行標準的單次向量檢索並結合 Context 生成回答。
* **多步/疊代檢索 (Multi-Step / Iterative Retrieval)**：針對複雜、多跳 (Multi-hop) 或需綜合推理的問題，啟動多輪疊代檢索與推論鏈，逐步收集所需上下文。

### 3. 自動化標籤訓練機制 (Automatic Labeling)
* 為了解決缺乏「查詢與最佳 RAG 策略對應」標註資料的問題，作者設計了自動生成訓練集的標註機制。
* 將訓練問題通過各種策略測試，紀錄能正確回答問題且資源消耗最少的策略作為 Ground Truth 標籤，用以訓練分類器。

---

## 策略對比與優劣勢 (Pros & Cons)

| 評估維度 | Naive RAG (傳統 RAG) | Adaptive-RAG (自適應 RAG) |
| :--- | :--- | :--- |
| **檢索開銷** | 固定高開銷（對簡單問題亦執行檢索） | 最佳化（簡單問題不檢索，省時省算力） |
| **複雜問題解答能力** | 有限（單次檢索無法涵蓋多跳推論） | 極佳（自動切換為多步疊代檢索） |
| **延遲 (Latency)** | 平均延遲固定 | 簡單問題反應迅速，複雜問題精確深入 |

---

## 適用場景 (Use Cases)

1. **企業級智慧客服與知識庫**：處理大量多樣化的用戶提問，能同時兼顧即時常見問答與複雜產品故障排查。
2. **多跳問答系統 (Multi-hop Question Answering)**：如法規檢索、醫療診斷支援等需要綜合多個文件段落的領域。
3. **成本敏銳型 AI 應用**：顯著降低向量數據庫 (Vector DB) 與 API 檢索的請求次數與費用。
