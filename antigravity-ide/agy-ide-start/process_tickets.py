import os
import re
import shutil
import datetime
import sys
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def resource_path(relative_path):
    """ 取得 PyInstaller 運行時的資源路徑 """
    try:
        # PyInstaller 建立的臨時資料夾路徑存於 sys._MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def parse_ticket(pdf_path):
    """
    解析高鐵交易紀錄 PDF 檔案，提取乘車日期、出發時間與票款。
    """
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
        
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    travel_date = None
    dep_time = None
    fare = None
    
    # 1. 區塊/行定位匹配
    for i, line in enumerate(lines):
        if "乘車日期" in line or "Travel Date" in line:
            for j in range(i+1, min(i+10, len(lines))):
                if re.match(r'^\d{4}/\d{2}/\d{2}$', lines[j]):
                    travel_date = lines[j]
                    break
                    
        if "區間" in line or "Itinerary" in line:
            for j in range(i+1, min(i+10, len(lines))):
                time_match = re.search(r'(\d{2}:\d{2})\s*-\s*.*(\d{2}:\d{2})', lines[j])
                if time_match:
                    dep_time = time_match.group(1)
                    break
                    
        if "票款" in line or "Fare" in line:
            for j in range(i+1, min(i+10, len(lines))):
                fare_match = re.search(r'NT\$\s*([0-9,]+)', lines[j])
                if fare_match:
                    fare = fare_match.group(1).replace(',', '')
                    break
                    
    # 2. 全文 Regex Fallback 匹配
    if not travel_date:
        dates = re.findall(r'(\d{4}/\d{2}/\d{2})', text)
        if len(dates) >= 2:
            travel_date = dates[1]
        elif len(dates) == 1:
            travel_date = dates[0]
            
    if not dep_time:
        time_match = re.search(r'(\d{2}:\d{2})\s*-\s*.*(\d{2}:\d{2})', text)
        if time_match:
            dep_time = time_match.group(1)
            
    if not fare:
        fare_match = re.search(r'NT\$\s*([0-9,]+)', text)
        if fare_match:
            fare = fare_match.group(1).replace(',', '')
            
    return travel_date, dep_time, fare

def main():
    base_dir = "/home/dengkai/projects/google-ai-tools/antigravity-ide/agy-ide-start"
    tickets_dir = os.path.join(base_dir, "Tickets")
    
    # 取得今天日期
    today_str = datetime.datetime.now().strftime("%Y%m%d")
    target_dir_name = f"Tickets-{today_str}"
    target_dir = os.path.join(base_dir, target_dir_name)
    
    # 建立目標資料夾
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"建立資料夾：{target_dir_name}")
        
    copied_files_info = []
    
    # 1. 處理並命名複製的檔案
    for filename in sorted(os.listdir(tickets_dir)):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(tickets_dir, filename)
            travel_date, dep_time, fare = parse_ticket(pdf_path)
            
            if not travel_date or not dep_time or not fare:
                print(f"警告：無法完整解析檔案 {filename} 的資訊。")
                continue
                
            # 格式化日期與時間為 YYYYMMDD-HHMM
            date_formatted = travel_date.replace('/', '')
            time_formatted = dep_time.replace(':', '')
            
            # 產生新檔名：[時間][票價]原檔名
            new_filename = f"[{date_formatted}-{time_formatted}][{fare}]{filename}"
            target_path = os.path.join(target_dir, new_filename)
            
            # 複製檔案到目標資料夾
            shutil.copy2(pdf_path, target_path)
            print(f"已複製並重新命名：{filename} -> {target_dir_name}/{new_filename}")
            copied_files_info.append((new_filename, int(fare)))
            
    if not copied_files_info:
        print("未找到可處理的 PDF 車票。")
        return
        
    # 2. 合併 PDF 並在最下面增加費用 [總金額]
    # 依照檔名（時間）排序以確保票券順序正確
    copied_files_info.sort(key=lambda x: x[0])
    
    total_fare = sum(info[1] for info in copied_files_info)
    print(f"車票總金額為：NT$ {total_fare}")
    
    # 合併 PDF 內容
    writer = PdfWriter()
    for filename, _ in copied_files_info:
        file_path = os.path.join(target_dir, filename)
        reader = PdfReader(file_path)
        for page in reader.pages:
            writer.add_page(page)
            
    # 使用 reportlab 建立臨時 PDF，在底部繪製「費用 [總金額]」
    # 註冊 Linux 系統內建的中文字型，防止中文亂碼
    font_path = resource_path("DroidSansFallbackFull.ttf")
    if not os.path.exists(font_path):
        font_path = "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf"
    pdfmetrics.registerFont(TTFont('DroidSans', font_path))
    
    temp_pdf_path = os.path.join(base_dir, "temp_footer.pdf")
    c = canvas.Canvas(temp_pdf_path, pagesize=A4)
    c.setFont('DroidSans', 12)
    c.setFillColorRGB(0.2, 0.2, 0.2) # 深灰字體
    
    # 依使用者需求：在最下面增加 費用 [總金額]
    # 格式：費用：總金額
    # 使用 DroidSans 繪製中文，Helvetica 繪製數字，防止 PDF 內文數字轉為 NUL (\x00) 字元
    c.setFont('DroidSans', 12)
    c.drawString(440, 35, "費用：")
    c.setFont('Helvetica', 12)
    c.drawString(480, 35, str(total_fare))
    c.save()
    
    # 將臨時繪製了費用的頁面疊加至合併 PDF 的最後一頁
    footer_reader = PdfReader(temp_pdf_path)
    footer_page = footer_reader.pages[0]
    
    last_page = writer.pages[-1]
    last_page.merge_page(footer_page)
    
    # 儲存合併後的 PDF 檔案
    merge_filename = f"Tickets{today_str}-merge.pdf"
    merge_filepath = os.path.join(base_dir, merge_filename)
    
    with open(merge_filepath, 'wb') as f_out:
        writer.write(f_out)
        
    print(f"成功合併 PDF 檔案並加上總金額，輸出至：{merge_filename}")
    
    # 清理臨時檔案
    if os.path.exists(temp_pdf_path):
        os.remove(temp_pdf_path)

if __name__ == "__main__":
    main()
