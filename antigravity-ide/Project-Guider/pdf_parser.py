import pdfplumber
import re

def extract_ticket_info(pdf_path):
    """
    從 PDF 中擷取乘車日期、出發時間與票價。
    支援高鐵、台鐵等電子車票 PDF 格式的解析。
    
    回傳值：
        (date_str, time_str, price_val)
        - date_str: YYYYMMDD 格式 (例如 "20260713")，若無則為 None
        - time_str: HHMM 格式 (例如 "1430")，若無則為 None
        - price_val: 整數格式的票價 (例如 1200)，若無則為 None
    """
    date_str = None
    time_str = None
    price_val = None

    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
            
            if not full_text.strip():
                return None, None, None
            
            # 為了方便正規表達式比對，將所有半形與全形空白統一，並轉為半形字元
            cleaned_text = re.sub(r'\s+', ' ', full_text)
            
            # --- 1. 解析日期 (Date) ---
            # 支援格式：YYYY/MM/DD, YYYY-MM-DD
            date_match = re.search(r'(\d{4})[/\-–](\d{2})[/\-–](\d{2})', cleaned_text)
            if date_match:
                date_str = f"{date_match.group(1)}{date_match.group(2)}{date_match.group(3)}"
            else:
                # 支援民國年格式：YYY/MM/DD, YYY-MM-DD
                roc_date_match = re.search(r'\b(\d{2,3})[/\-–](\d{2})[/\-–](\d{2})\b', cleaned_text)
                if roc_date_match:
                    roc_year = int(roc_date_match.group(1))
                    year = roc_year + 1911
                    date_str = f"{year}{roc_date_match.group(2)}{roc_date_match.group(3)}"

            # --- 2. 解析時間 (Time) ---
            # 匹配 HH:MM 格式
            time_matches = re.findall(r'(\d{2}):(\d{2})', cleaned_text)
            if time_matches:
                # 通常車票第一個出發時間即為乘車時間，並排除不合理的時分
                for hour, minute in time_matches:
                    h, m = int(hour), int(minute)
                    if 0 <= h < 24 and 0 <= m < 60:
                        time_str = f"{hour}{minute}"
                        break

            # --- 3. 解析票價 (Price) ---
            # 正規表達式比對多種票價字樣，例如 "票價 1,200", "總價 NT$970", "$1,490 元", "費用 600"
            price_patterns = [
                r'(?:票價|總價|實收|金額|實付金額|票價合計|總金額)\s*(?:NT\$|\$)?\s*(\d+(?:,\d{3})*)',
                r'(?:NT\$|\$)\s*(\d+(?:,\d{3})*)',
                r'(\d+(?:,\d{3})*)\s*元'
            ]
            for pattern in price_patterns:
                price_match = re.search(pattern, cleaned_text, re.IGNORECASE)
                if price_match:
                    raw_price = price_match.group(1).replace(",", "")
                    price_val = int(raw_price)
                    break
            
            # 若無上述關鍵字，尋找 100~9999 之間的數字，且非日期與時間的資訊
            if price_val is None:
                potential_prices = re.findall(r'\b\d{3,4}\b', cleaned_text)
                exclude_vals = []
                if date_match:
                    exclude_vals.extend(date_match.groups())
                if time_matches:
                    for h, m in time_matches:
                        exclude_vals.extend([h, m])
                
                for val in potential_prices:
                    if val not in exclude_vals:
                        price_val = int(val)
                        break

    except Exception as e:
        print(f"[ERROR] 解析檔案 {pdf_path} 時發生錯誤: {e}")
        
    return date_str, time_str, price_val
