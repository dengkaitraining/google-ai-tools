#!/usr/bin/env python3
import sys
import os
import argparse
import markdown

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@page {
    size: a4;
    margin: 2cm;
}
body {
    font-family: sans-serif;
    line-height: 1.5;
    color: #24292e;
    font-size: 11pt;
}

h1 {
    font-size: 20pt;
    border-bottom: 2px solid #eaecef;
    padding-bottom: 5px;
    color: #1a202c;
    margin-top: 0;
}

h2 {
    font-size: 15pt;
    border-bottom: 1px solid #eaecef;
    padding-bottom: 4px;
    color: #2d3748;
    margin-top: 15px;
}

h3 {
    font-size: 12pt;
    color: #4a5568;
    margin-top: 12px;
}

code {
    font-family: monospace;
    background-color: #f6f8fa;
    padding: 2px 4px;
    font-size: 10pt;
}

pre {
    background-color: #f6f8fa;
    padding: 10px;
    border: 1px solid #e1e4e8;
    font-size: 9pt;
}

blockquote {
    margin: 0;
    padding: 0 10px;
    color: #6a737d;
    border-left: 4px solid #dfe2e5;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
    margin-bottom: 10px;
}

table th, table td {
    padding: 6px 10px;
    border: 1px solid #dfe2e5;
    text-align: left;
}

table th {
    background-color: #f6f8fa;
    font-weight: bold;
}

hr {
    height: 1px;
    background-color: #e1e4e8;
    border: none;
    margin: 20px 0;
}

ul, ol {
    padding-left: 20px;
}
</style>
</head>
<body>
<!--CONTENT-->
</body>
</html>
"""

def convert_md_to_pdf(input_md_path, output_pdf_path):
    if not os.path.exists(input_md_path):
        print(f"Error: Input file {input_md_path} does not exist.")
        sys.exit(1)

    with open(input_md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # Convert markdown to html
    html_body = markdown.markdown(
        md_text,
        extensions=['fenced_code', 'tables', 'toc', 'nl2br', 'sane_lists']
    )

    full_html = HTML_TEMPLATE.replace("<!--CONTENT-->", html_body)

    output_dir = os.path.dirname(os.path.abspath(output_pdf_path))
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Try playwright first
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.set_content(full_html, wait_until='networkidle')
            page.pdf(
                path=output_pdf_path,
                format='A4',
                margin={'top': '20mm', 'bottom': '20mm', 'left': '20mm', 'right': '20mm'},
                print_background=True
            )
            browser.close()
            print(f"Successfully converted (via Playwright) {input_md_path} -> {output_pdf_path}")
            return
    except Exception as e:
        print(f"Playwright conversion failed ({e}), using xhtml2pdf fallback...")

    # Fallback to xhtml2pdf
    try:
        from xhtml2pdf import pisa
        with open(output_pdf_path, "wb") as output_file:
            pisa_status = pisa.CreatePDF(full_html, dest=output_file, encoding='utf-8')
            if pisa_status.err:
                print(f"xhtml2pdf error: {pisa_status.err}")
                sys.exit(1)
        print(f"Successfully converted (via xhtml2pdf) {input_md_path} -> {output_pdf_path}")
    except Exception as e:
        print(f"Error converting MD to PDF: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Markdown file to PDF")
    parser.add_argument("input", help="Input Markdown file path")
    parser.add_argument("output", help="Output PDF file path")
    args = parser.parse_args()

    convert_md_to_pdf(args.input, args.output)
