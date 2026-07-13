import os
import shutil
import io
from datetime import datetime
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from pdf_parser import extract_ticket_info

def main():
    # 定義輸入與歸檔資料夾
    input_dir = "Tickets"
    
    # 建立輸入資料夾（如果不存在）
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
        print(f"已建立 '{input_dir}' 資料夾，請將車票 PDF 放入其中後重新執行。")
        return

    # 取得輸入資料夾下的所有 PDF 檔案
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print(f"在 '{input_dir}' 資料夾下找不到任何 PDF 檔案，請放入車票後重新執行。")
        return

    # 執行時間戳記
    now = datetime.now()
    current_timestamp = now.strftime("%Y%m%d_%H%M%S")
    archive_dir = f"Tickets-{current_timestamp}"
    os.makedirs(archive_dir, exist_ok=True)
    print(f"已建立歸檔資料夾: {archive_dir}")

    total_price = 0
    copied_tickets = []

    # 遍歷處理每個 PDF 檔案
    for file_name in pdf_files:
        src_path = os.path.join(input_dir, file_name)
        print(f"\n正在解析檔案: {file_name}...")
        
        # 呼叫解析器取得資料
        date_str, time_str, price_val = extract_ticket_info(src_path)
        
        # 套用 fallback 機制
        final_date = date_str if date_str else "UNKNOWN_DATE"
        final_time = time_str if time_str else "UNKNOWN_TIME"
        
        if price_val is not None:
            final_price = str(price_val)
            total_price += price_val
        else:
            final_price = "UNKNOWN_PRICE"
            
        # 組合新檔名：[日期][時間][票價]原檔名.pdf
        new_file_name = f"[{final_date}][{final_time}][{final_price}]{file_name}"
        dest_path = os.path.join(archive_dir, new_file_name)
        
        # 複製並重新命名
        shutil.copy2(src_path, dest_path)
        print(f" -> 複製並重命名為: {new_file_name}")
        copied_tickets.append(dest_path)

    if not copied_tickets:
        print("沒有成功複製任何檔案，停止合併。")
        return

    print("\n開始進行 PDF 合併作業...")
    # 建立 PdfWriter 以便合併與疊加頁面
    writer = PdfWriter()
    for path in copied_tickets:
        writer.append(path)

    # 在最後一頁的最下方繪製總金額
    last_page_idx = len(writer.pages) - 1
    if last_page_idx >= 0:
        last_page = writer.pages[last_page_idx]
        width = float(last_page.mediabox.width)
        height = float(last_page.mediabox.height)
        
        # 建立 ReportLab 透明頁面
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(width, height))
        
        # 在最下方繪製總金額 (x=50, y=30)
        # 高鐵票底下通常有空白，y=30 是一個很安全的底部邊距
        can.setFont("Helvetica-Bold", 14)
        can.setFillColorRGB(0.8, 0.1, 0.1) # 紅色
        can.drawString(50, 30, f"Total Amount: NT$ {total_price:,}")
        can.save()
        
        # 將 Canvas 頁面轉為 pypdf page
        packet.seek(0)
        watermark_pdf = PdfReader(packet)
        watermark_page = watermark_pdf.pages[0]
        
        # 合併（疊加）到最後一頁
        last_page.merge_page(watermark_page)
        print(f" -> 已在合併 PDF 的最後一頁底部標記總金額: NT$ {total_price:,}")

    # 合併檔命名為：Tickets-[日期][時間][總金額]-merge.pdf
    merge_date = now.strftime("%Y%m%d")
    merge_time = now.strftime("%H%M")
    merged_file_name = f"Tickets-{merge_date}-{merge_time}-{total_price}-merge.pdf"
    
    with open(merged_file_name, "wb") as f:
        writer.write(f)
        
    print(f"\n合併完成！已產生最終 PDF 檔案: {merged_file_name}")
    print(f"共處理了 {len(copied_tickets)} 張車票，總金額: NT$ {total_price:,}")

if __name__ == "__main__":
    main()
