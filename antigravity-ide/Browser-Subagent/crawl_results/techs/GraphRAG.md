# GraphRAG (Microsoft) 技術重點整理與架構分析

## 概述 (Overview)

**GraphRAG** 是由 Microsoft 團隊提出的基於知識圖譜 (Knowledge Graph) 的檢索增強生成技術，論文標題為 *"From Local to Global: A Graph RAG Approach to Query-Focused Summarization"* (arXiv:2404.16130)。

傳統基於向量相似度的 Baseline RAG 擅長處理「局部問題」(Local Queries，如「X 的電話號碼是多少？」)，但在面對「全域問題」(Global Queries，如「這份檔案集的主題與主要爭議為何？」) 時表現極差。GraphRAG 透過構建圖譜與社群摘要 (Community Summaries)，徹底解決了全域資料理解與連點成線 (Connecting the Dots) 的挑戰。

---

## 核心架構與階段 (Core Architecture & Pipeline)

GraphRAG 的運作流程分為**兩大核心階段**：

### 第一階段：圖譜建立與分群摘要 (Graph Indexing & Community Detection)

1. **實體與關係擷取 (Entity & Relationship Extraction)**
   * 利用 LLM 掃描原始文本段落 (Text Chunks)，自動提取關鍵實體 (Entities / 節點) 以及實體間的關聯 (Relationships / 邊)。
2. **社群偵測 (Community Detection)**
   * 採用圖群聚演算法（如 Leiden 或 Louvain 演算法），將緊密相連的實體劃分成階層式的「社群 (Communities)」。
3. **社群摘要生成 (Community Summarization)**
   * 由 LLM 為每一個社群預先生成階層式的摘要報告 (Hierarchical Summaries)，捕捉該社群內的全域脈絡與主題。

### 第二階段：全域與局部檢索 (Query-Focused Summarization & Retrieval)

1. **社群層級檢索 (Community-Level Retrieval)**
   * 面對全域問題時，系統不再進行單純的語義向量匹配，而是直接檢索相關社群的預生成摘要。
2. **階層式答案生成 (Hierarchical Generation & Synthesis)**
   * LLM 利用各個社群摘要生成中間回答 (Map 階段)，最後將所有中間回答融合成最終完整報告 (Reduce 階段)。

---

## 策略對比與優劣勢 (Pros & Cons)

| 評估維度 | Baseline Vector RAG (向量 RAG) | GraphRAG (圖譜 RAG) |
| :--- | :--- | :--- |
| **檢索維度** | 語義片段 (Text Chunks) 相似度匹配 | 結構化知識圖譜 + 階層式社群摘要 |
| **全域總結能力** | 差（無法涵蓋全卷檔案脈絡） | 極佳（能進行跨文件之全域摘要與主題分析） |
| **連點成線 (Reasoning)** | 容易遺漏無直接語義關聯的隱含關係 | 能沿著圖譜邊緣 (Edges) 進行跨實體推論 |
| **索引成本 (Indexing Cost)** | 低 | 較高（需調用 LLM 構建圖譜與社群摘要） |

---

## 適用場景 (Use Cases)

1. **海量文檔總結與趨勢分析**：調查報告、商業情報分析、法律訴訟案卷全域研判。
2. **跨領域關係推理**：生醫文檔關聯分析、金融反洗錢與關係網絡調查。
3. **複雜領域知識庫建設**：需要高準確度、結構化且具備追溯性之企業級 Knowledge Hub。
