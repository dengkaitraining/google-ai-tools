#!/usr/bin/env python3
import argparse
import os
import sys
from pypdf import PdfWriter

def merge_pdfs(input_files, output_file):
    """
    合併指定的 PDF 檔案列表並輸出到指定檔案。
    """
    merger = PdfWriter()
    try:
        for pdf_file in input_files:
            if not os.path.exists(pdf_file):
                print(f"錯誤：找不到檔案 '{pdf_file}'", file=sys.stderr)
                sys.exit(1)
            print(f"正在加入檔案：{pdf_file}")
            merger.append(pdf_file)
        
        # 確保輸出的父目錄存在
        output_dir = os.path.dirname(os.path.abspath(output_file))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        print(f"正在將合併後的 PDF 寫入：{output_file}")
        with open(output_file, "wb") as f:
            merger.write(f)
        print("合併成功！")
    except Exception as e:
        print(f"合併過程中發生錯誤：{e}", file=sys.stderr)
        sys.exit(1)
    finally:
        merger.close()

def main():
    parser = argparse.ArgumentParser(description="PDF 合併工具")
    parser.add_argument(
        "inputs", 
        nargs="*", 
        help="要合併的 PDF 檔案路徑列表。若未指定，將預設合併工作區的 ticket_A.pdf 與 ticket_B.pdf"
    )
    parser.add_argument(
        "-o", "--output", 
        default="merged.pdf", 
        help="合併後的輸出 PDF 檔案名稱，預設為 merged.pdf"
    )

    args = parser.parse_args()

    # 如果使用者沒有輸入任何檔案，使用預設規則
    if not args.inputs:
        default_inputs = ["ticket_A.pdf", "ticket_B.pdf"]
        print("未指定輸入檔案。將依預設規則合併工作區內的 ticket_A.pdf 與 ticket_B.pdf。")
        merge_pdfs(default_inputs, args.output)
    else:
        merge_pdfs(args.inputs, args.output)

if __name__ == "__main__":
    main()
