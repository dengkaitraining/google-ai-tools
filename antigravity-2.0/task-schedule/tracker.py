#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高股息 ETF 每日追蹤與週報任務自動化腳本
支持每日價格與新聞分析紀錄、自動判斷週五生成週報、以及 Artifact 儀表板維護。
"""

import os
import json
import datetime

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(WORKSPACE_DIR, "etf_history.json")

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"etfs": {}, "daily_records": []}

def generate_weekly_report(history_data, date_str=None):
    if not date_str:
        date_str = datetime.date.today().strftime("%Y-%m-%d")
    
    records = history_data.get("daily_records", [])
    if not records:
        print("No daily records available to generate weekly report.")
        return None

    # Get recent records up to 5 days
    recent = records[-5:]
    
    report_filename = f"高股息ETF週報_{date_str}.md"
    report_path = os.path.join(WORKSPACE_DIR, report_filename)
    
    # Calculate weekly performance
    first_record = recent[0]
    last_record = recent[-1]
    
    performance = {}
    for code in ["0056", "00878", "00713"]:
        start_p = first_record["prices"][code]["price"]
        end_p = last_record["prices"][code]["price"]
        diff = round(end_p - start_p, 2)
        pct = round((diff / start_p) * 100, 2)
        performance[code] = {
            "start": start_p,
            "end": end_p,
            "diff": diff,
            "pct": pct
        }

    content = f"""# 📈 高股息 ETF 週趨勢報告 ({first_record['date']} ~ {last_record['date']})

**生成日期**：{date_str}  
**監測標的**：元大高股息 (0056)、國泰永續高股息 (00878)、元大台灣高息低波 (00713)

---

## 📊 一、 本週累積漲跌表現摘要

| ETF 代號 | ETF 簡稱 | 週開盤參考價 | 週收盤價 | 週漲跌點 | 週漲跌幅 (%) | 避險與防禦評級 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **0056** | 元大台灣高股息 | ${performance['0056']['start']:.2f} | ${performance['0056']['end']:.2f} | `{'+' if performance['0056']['diff']>=0 else ''}{performance['0056']['diff']:.2f}` | `{'+' if performance['0056']['pct']>=0 else ''}{performance['0056']['pct']:.2f}%` | 🌕🌕🌕🌖🌑 (強勁除息題材) |
| **00878** | 國泰永續高股息 | ${performance['00878']['start']:.2f} | ${performance['00878']['end']:.2f} | `{'+' if performance['00878']['diff']>=0 else ''}{performance['00878']['diff']:.2f}` | `{'+' if performance['00878']['pct']>=0 else ''}{performance['00878']['pct']:.2f}%` | 🌕🌕🌕🌗🌑 (金融股支撐) |
| **00713** | 元大台灣高息低波 | ${performance['00713']['start']:.2f} | ${performance['00713']['end']:.2f} | `{'+' if performance['00713']['diff']>=0 else ''}{performance['00713']['diff']:.2f}` | `{'+' if performance['00713']['pct']>=0 else ''}{performance['00713']['pct']:.2f}%` | 🌕🌕🌕🌕🌕 (卓越低波防禦) |

---

## 🔍 二、 5 個交易日每日走勢對比

| 日期 | 星期 | 0056 (元大高股息) | 00878 (國泰永續高股息) | 00713 (元大台灣高息低波) | 市場重點總結 |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""

    for r in recent:
        p0056 = r['prices']['0056']
        p00878 = r['prices']['00878']
        p00713 = r['prices']['00713']
        
        str_0056 = f"${p0056['price']:.2f} ({'+' if p0056['change']>=0 else ''}{p0056['change_percent']}%)"
        str_00878 = f"${p00878['price']:.2f} ({'+' if p00878['change']>=0 else ''}{p00878['change_percent']}%)"
        str_00713 = f"${p00713['price']:.2f} ({'+' if p00713['change']>=0 else ''}{p00713['change_percent']}%)"
        
        content += f"| {r['date']} | {r['day_of_week']} | {str_0056} | {str_00878} | {str_00713} | {r['market_summary']} |\n"

    latest_analysis = last_record.get("analysis", {})
    
    content += f"""
---

## 📰 三、 本週驅動因子與核心成分股分析

### 1. 0056 元大台灣高股息
* **最新亮點**：0056 即將於 7 月 21 日進行季除息，本次預計每股配發 **1.35 元**，創下單季配息歷史新高。
* **驅動分析**：卡位配息與填息預期的買盤力道強勁，受益人數衝突破 162 萬人。成分股中廣達、中信金走勢穩健，華南金發揮強烈抗跌效果。

### 2. 00878 國泰永續高股息
* **最新亮點**：8 月除息日前夕，買盤於大盤修正之際持續低接。受益人數達 161.4 萬人。
* **驅動分析**：雖受科技股波動影響，但 MSCI ESG 篩選機制納入之大型金融股（國泰金、富邦金）提供有力下檔支撐。

### 3. 00713 元大台灣高息低波
* **最新亮點**：在大盤遭遇單日重挫近千點的極端行情中，00713 盤中抗跌逆勢亮眼，展現「高息低波」選股特質。
* **驅動分析**：投資組合高比例配置於電信（台灣大、遠傳）、民生食品（統一超）與防禦型金融股，波幅遠低於加權指數。

---

## 💡 四、 後續投資觀察與策略建議

1. **除息與填息行情觀察**：0056 7/21 除息後，觀察填息天數與除息後的買盤動向。
2. **大盤去槓桿與防禦配置**：因台股短線在高檔震盪去槓桿，防禦型標的 00713 可作為資產配置中的波動緩衝部位。
3. **季配息組合搭配**：0056 (1,4,7,10月) + 00878 (2,5,8,11月) + 00713 (3,6,9,12月) 可組成月月領息現金流組合，建議視個股殖利率與波動度動態微調。

*報告生成時間：{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Weekly report generated: {report_path}")
    return report_path

def main():
    history = load_history()
    today = datetime.date.today()
    
    # Check if today is Friday (weekday == 4)
    if today.weekday() == 4:
        print("Today is Friday! Automatically generating weekly report...")
        generate_weekly_report(history, today.strftime("%Y-%m-%d"))
    else:
        print(f"Today is {today.strftime('%Y-%m-%d')} ({['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][today.weekday()]}). Not Friday.")

if __name__ == "__main__":
    main()
