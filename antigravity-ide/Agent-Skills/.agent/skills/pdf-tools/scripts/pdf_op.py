#!/usr/bin/env python3
import os
import sys
import json
import argparse
import io
from typing import List, Optional

# Third party library imports
try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF (fitz) is not installed. Please install it using 'pip install pymupdf'.", file=sys.stderr)
    sys.exit(1)

try:
    import markdown
    from xhtml2pdf import pisa
except ImportError:
    # Optional or warnings can be printed if conversion subcommand is called.
    pass

try:
    import pytesseract
    from PIL import Image
except ImportError:
    # OCR imports
    pass


def parse_pages_arg(pages_str: str, total_pages: int) -> List[int]:
    """
    Parses page range strings like '1-3,5,7-end' and returns 0-based page indices.
    """
    indices = []
    parts = pages_str.split(',')
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            start_str, end_str = part.split('-', 1)
            start_str = start_str.strip()
            end_str = end_str.strip()
            
            start = int(start_str) if start_str else 1
            if end_str.lower() == 'end':
                end = total_pages
            else:
                end = int(end_str) if end_str else total_pages
                
            for p in range(start, end + 1):
                if 1 <= p <= total_pages:
                    indices.append(p - 1)
        else:
            if part.lower() == 'end':
                indices.append(total_pages - 1)
            else:
                p = int(part)
                if 1 <= p <= total_pages:
                    indices.append(p - 1)
    return sorted(list(set(indices)))


def cmd_convert(args):
    """
    Handles bidirectional conversion between PDF and HTML/Markdown/TXT
    """
    input_path = args.input
    output_path = args.output
    
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found.", file=sys.stderr)
        sys.exit(1)
        
    ext_in = os.path.splitext(input_path.lower())[1]
    ext_out = os.path.splitext(output_path.lower())[1]
    
    # 1. HTML/MD -> PDF
    if ext_in in ['.html', '.htm', '.md', '.markdown'] and ext_out == '.pdf':
        print(f"Converting '{input_path}' to PDF '{output_path}'...")
        
        # Read source content
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # If it's Markdown, convert to HTML first
        if ext_in in ['.md', '.markdown']:
            try:
                content = markdown.markdown(content, extensions=['tables', 'fenced_code'])
            except NameError:
                print("Error: 'markdown' package is required. Install it with pip.", file=sys.stderr)
                sys.exit(1)
                
        # Render HTML to PDF using xhtml2pdf
        try:
            with open(output_path, "wb") as pdf_file:
                pisa_status = pisa.CreatePDF(content, dest=pdf_file)
                if pisa_status.err:
                    print("Error occurred during PDF generation.", file=sys.stderr)
                    sys.exit(1)
            print(f"Successfully created PDF: '{output_path}'")
        except NameError:
            print("Error: 'xhtml2pdf' (pisa) is required. Install it with pip.", file=sys.stderr)
            sys.exit(1)
            
    # 2. PDF -> TXT/MD/HTML
    elif ext_in == '.pdf' and ext_out in ['.txt', '.md', '.html', '.markdown']:
        print(f"Converting PDF '{input_path}' to '{output_path}'...")
        doc = fitz.open(input_path)
        
        output_data = []
        for i, page in enumerate(doc):
            if ext_out == '.html':
                output_data.append(page.get_text("html"))
            elif ext_out in ['.md', '.markdown']:
                # Basic conversion to Markdown blocks
                text = page.get_text("blocks")
                # Sort blocks top-to-bottom, left-to-right
                text.sort(key=lambda b: (b[1], b[0]))
                md_blocks = []
                for b in text:
                    block_text = b[4].strip()
                    if not block_text:
                        continue
                    # Check if it looks like a heading
                    if block_text.isupper() and len(block_text) < 60:
                        md_blocks.append(f"\n## {block_text}\n")
                    else:
                        md_blocks.append(f"\n{block_text}\n")
                output_data.append(f"# Page {i + 1}\n" + "".join(md_blocks))
            else: # TXT
                output_data.append(f"--- Page {i + 1} ---\n" + page.get_text("text"))
                
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n\n".join(output_data))
        print(f"Successfully converted PDF to '{output_path}'")
    else:
        print(f"Error: Unsupported conversion from '{ext_in}' to '{ext_out}'", file=sys.stderr)
        sys.exit(1)


def cmd_extract_text(args):
    """
    Extracts text with scanning detection, layout preservation, and OCR
    """
    input_path = args.input
    output_path = args.output
    use_layout = args.layout
    use_ocr = args.ocr
    
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found.", file=sys.stderr)
        sys.exit(1)
        
    doc = fitz.open(input_path)
    total_pages = len(doc)
    extracted_text = []
    
    print(f"Extracting text from '{input_path}' (Total pages: {total_pages})...")
    
    for page_num in range(total_pages):
        page = doc[page_num]
        
        # 1. Normal Extraction
        if use_layout:
            # Sort layout text blocks
            blocks = page.get_text("blocks")
            blocks.sort(key=lambda b: (b[1], b[0]))
            page_text = "\n".join([b[4].strip() for b in blocks if b[4].strip()])
        else:
            page_text = page.get_text("text")
            
        # 2. Scanning Detection (No text, but has images)
        is_scanned = len(page_text.strip()) < 50 and len(page.get_images()) > 0
        
        if is_scanned:
            print(f"Page {page_num + 1}: Scanned page/image detected.")
            if use_ocr:
                try:
                    # Render page to high-res image for OCR
                    pix = page.get_pixmap(dpi=150)
                    img_data = pix.tobytes("png")
                    img = Image.open(io.BytesIO(img_data))
                    
                    ocr_text = pytesseract.image_to_string(img)
                    page_text = f"[OCR Extracted Text]\n{ocr_text}"
                except NameError:
                    page_text = f"[Warning: OCR requested but 'pytesseract' or 'PIL' libraries not found. Page {page_num + 1} skipped.]"
                except Exception as e:
                    page_text = f"[Error performing OCR: {e}]"
                    # Check if tesseract binary is missing
                    if "tesseract is not installed" in str(e).lower() or "no such file" in str(e).lower():
                        page_text += "\nTo use OCR, install Tesseract OCR on your system (e.g., 'sudo apt-get install tesseract-ocr')."
            else:
                page_text = f"[Scanned page detected. Use --ocr to perform optical character recognition.]"
                
        extracted_text.append(f"--- Page {page_num + 1} ---\n{page_text}")
        
    full_output = "\n\n".join(extracted_text)
    
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_output)
        print(f"Text successfully extracted and saved to '{output_path}'.")
    else:
        print(full_output)


def cmd_page_edit(args):
    """
    Page editing and restructuring: merge, split, rotate, insert, delete blank pages
    """
    op = args.op
    output_path = args.output
    
    if op == 'merge':
        if not args.inputs or len(args.inputs) < 2:
            print("Error: --inputs requires at least two PDF files to merge.", file=sys.stderr)
            sys.exit(1)
            
        writer = fitz.open()
        for path in args.inputs:
            if not os.path.exists(path):
                print(f"Error: File '{path}' not found.", file=sys.stderr)
                sys.exit(1)
            reader = fitz.open(path)
            writer.insert_pdf(reader)
            
        writer.save(output_path)
        writer.close()
        print(f"Successfully merged files into '{output_path}'")
        
    elif op in ['split', 'rotate', 'insert', 'delete-blank']:
        if not args.input:
            print("Error: --input is required.", file=sys.stderr)
            sys.exit(1)
        if not os.path.exists(args.input):
            print(f"Error: Input file '{args.input}' not found.", file=sys.stderr)
            sys.exit(1)
            
        doc = fitz.open(args.input)
        total_pages = len(doc)
        
        if op == 'split':
            # Extract specified pages to new document
            if not args.pages:
                print("Error: --pages parameter is required for splitting (e.g. --pages 1-3,5).", file=sys.stderr)
                sys.exit(1)
            try:
                indices = parse_pages_arg(args.pages, total_pages)
            except ValueError as e:
                print(f"Error parsing pages: {e}", file=sys.stderr)
                sys.exit(1)
                
            new_doc = fitz.open()
            for idx in indices:
                new_doc.insert_pdf(doc, from_page=idx, to_page=idx)
            new_doc.save(output_path)
            new_doc.close()
            print(f"Successfully split pages [{', '.join(str(i+1) for i in indices)}] to '{output_path}'")
            
        elif op == 'rotate':
            if not args.pages:
                print("Error: --pages parameter is required for rotating (e.g. --pages 1,2).", file=sys.stderr)
                sys.exit(1)
            if args.angle is None or args.angle not in [90, 180, 270]:
                print("Error: --angle must be 90, 180, or 270 degrees.", file=sys.stderr)
                sys.exit(1)
                
            indices = parse_pages_arg(args.pages, total_pages)
            for idx in indices:
                page = doc[idx]
                current_rot = page.rotation
                page.set_rotation((current_rot + args.angle) % 360)
                
            doc.save(output_path)
            print(f"Successfully rotated pages [{', '.join(str(i+1) for i in indices)}] by {args.angle} degrees and saved to '{output_path}'")
            
        elif op == 'insert':
            if not args.insert_pdf or not os.path.exists(args.insert_pdf):
                print(f"Error: --insert-pdf file not found.", file=sys.stderr)
                sys.exit(1)
                
            insert_at = args.insert_at if args.insert_at is not None else total_pages
            if insert_at < 0 or insert_at > total_pages:
                print(f"Error: Invalid insertion position index {insert_at}.", file=sys.stderr)
                sys.exit(1)
                
            insert_doc = fitz.open(args.insert_pdf)
            # Insert at position (insert_at is 0-indexed page index in destination doc)
            doc.insert_pdf(insert_doc, start_at=insert_at)
            doc.save(output_path)
            print(f"Successfully inserted '{args.insert_pdf}' into '{args.input}' at position {insert_at} and saved to '{output_path}'")
            
        elif op == 'delete-blank':
            new_doc = fitz.open()
            kept_pages = []
            for i in range(total_pages):
                page = doc[i]
                # Page is considered blank if it has no text and no images/drawings
                is_blank = len(page.get_text().strip()) == 0 and len(page.get_images()) == 0 and len(page.get_drawings()) == 0
                if not is_blank:
                    new_doc.insert_pdf(doc, from_page=i, to_page=i)
                    kept_pages.append(i + 1)
                    
            new_doc.save(output_path)
            new_doc.close()
            print(f"Removed blank pages. Kept pages: {kept_pages}. Saved to '{output_path}'")
            
        doc.close()


def cmd_compress(args):
    """
    Optimizes and compresses PDF file sizes
    """
    input_path = args.input
    output_path = args.output
    
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found.", file=sys.stderr)
        sys.exit(1)
        
    print(f"Compressing PDF '{input_path}'...")
    initial_size = os.path.getsize(input_path)
    
    doc = fitz.open(input_path)
    # PyMuPDF save options for maximum compression:
    # garbage=4 (clean up unused objects), deflate=True (compress streams), clean=True (clean contents)
    doc.save(output_path, garbage=4, deflate=True, clean=True)
    doc.close()
    
    final_size = os.path.getsize(output_path)
    reduction = ((initial_size - final_size) / initial_size) * 100
    print(f"Successfully compressed. Size reduced from {initial_size} to {final_size} bytes ({reduction:.2f}% reduction). Saved to '{output_path}'")


def cmd_security(args):
    """
    Handles security, passwords, metadata, and watermarks
    """
    op = args.op
    input_path = args.input
    output_path = args.output
    
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found.", file=sys.stderr)
        sys.exit(1)
        
    doc = fitz.open(input_path)
    
    # Decrypt if encrypted before we do any operations
    if doc.is_encrypted:
        if not args.password:
            print("Error: Input PDF is encrypted. --password is required to unlock it.", file=sys.stderr)
            sys.exit(1)
        success = doc.authenticate(args.password)
        if not success:
            print("Error: Authentication failed with the provided password.", file=sys.stderr)
            sys.exit(1)
            
    if op == 'metadata':
        # Read or update metadata
        metadata = doc.metadata
        
        # If no updates are specified, print current metadata
        if not any([args.title, args.author, args.subject, args.keywords]):
            print(json.dumps(metadata, indent=2, ensure_ascii=False))
            doc.close()
            return
            
        if not output_path:
            print("Error: --output is required when updating metadata.", file=sys.stderr)
            sys.exit(1)
            
        new_metadata = {}
        for key, val in metadata.items():
            new_metadata[key] = val
            
        if args.title is not None:
            new_metadata['title'] = args.title
        if args.author is not None:
            new_metadata['author'] = args.author
        if args.subject is not None:
            new_metadata['subject'] = args.subject
        if args.keywords is not None:
            new_metadata['keywords'] = args.keywords
            
        doc.set_metadata(new_metadata)
        doc.save(output_path)
        print(f"Successfully updated metadata and saved to '{output_path}'")
        
    elif op == 'encrypt':
        if not args.password:
            print("Error: --password is required for encryption.", file=sys.stderr)
            sys.exit(1)
        if not output_path:
            print("Error: --output is required for saving the encrypted PDF.", file=sys.stderr)
            sys.exit(1)
            
        # Encrypt and save
        doc.save(output_path, 
                 user_pw=args.password, 
                 owner_pw=args.password, 
                 encryption=fitz.PDF_ENCRYPT_AES_256)
        print(f"Successfully encrypted PDF with AES-256 and saved to '{output_path}'")
        
    elif op == 'decrypt':
        if not output_path:
            print("Error: --output is required for saving the decrypted PDF.", file=sys.stderr)
            sys.exit(1)
        # We already decrypted/authenticated above; saving to output_path removes password
        doc.save(output_path)
        print(f"Successfully decrypted PDF and saved unencrypted version to '{output_path}'")
        
    elif op == 'watermark':
        if not args.watermark_text:
            print("Error: --watermark-text is required.", file=sys.stderr)
            sys.exit(1)
        if not output_path:
            print("Error: --output is required.", file=sys.stderr)
            sys.exit(1)
            
        opacity = args.opacity if args.opacity is not None else 0.3
        
        # Add text watermark to all pages
        for page in doc:
            rect = page.rect
            # Place watermarks diagonally or in the center
            # Insert rotated text in the center
            p1 = fitz.Point(rect.width / 5, rect.height / 2)
            page.insert_text(p1, args.watermark_text, 
                             fontsize=40, 
                             color=(0.7, 0.7, 0.7), # Light grey
                             rotate=0, 
                             fill_opacity=opacity)
                             
        doc.save(output_path)
        print(f"Successfully applied watermark '{args.watermark_text}' and saved to '{output_path}'")
        
    doc.close()


def main():
    parser = argparse.ArgumentParser(description="Advanced PDF Tools CLI for Antigravity Skill")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Subcommands")
    
    # convert
    parser_conv = subparsers.add_parser("convert", help="Bidirectional conversion between PDF and markdown/text/HTML")
    parser_conv.add_argument("--input", "-i", required=True, help="Input file path (.pdf, .md, .html, .txt)")
    parser_conv.add_argument("--output", "-o", required=True, help="Output file path (.pdf, .md, .html, .txt)")
    
    # extract-text
    parser_ext = subparsers.add_parser("extract-text", help="Extract text with scan detection and OCR options")
    parser_ext.add_argument("--input", "-i", required=True, help="Path to input PDF file")
    parser_ext.add_argument("--output", "-o", help="Path to save the output text file (prints to stdout if omitted)")
    parser_ext.add_argument("--layout", action="store_true", help="Preserve spatial text layout")
    parser_ext.add_argument("--ocr", action="store_true", help="Perform OCR on scanned pages (requires Tesseract)")
    
    # page-edit
    parser_edit = subparsers.add_parser("page-edit", help="Merge, split, rotate, insert, or delete blank pages")
    parser_edit.add_argument("--op", required=True, choices=['merge', 'split', 'rotate', 'insert', 'delete-blank'], help="Editing operation")
    parser_edit.add_argument("--input", "-i", help="Path to input PDF (required for split, rotate, insert, delete-blank)")
    parser_edit.add_argument("--inputs", nargs="+", help="Paths to input PDFs to merge (required for merge)")
    parser_edit.add_argument("--output", "-o", required=True, help="Output PDF file path")
    parser_edit.add_argument("--pages", "-p", help="Pages/ranges to process (e.g. '1-3,5')")
    parser_edit.add_argument("--angle", type=int, choices=[90, 180, 270], help="Rotation angle clockwise (required for rotate)")
    parser_edit.add_argument("--insert-pdf", help="Path of PDF to insert (required for insert)")
    parser_edit.add_argument("--insert-at", type=int, help="Page index to insert at (0-based, defaults to end)")
    
    # compress
    parser_comp = subparsers.add_parser("compress", help="Compress PDF size without resolution loss")
    parser_comp.add_argument("--input", "-i", required=True, help="Path to input PDF file")
    parser_comp.add_argument("--output", "-o", required=True, help="Path to save compressed PDF file")
    
    # security
    parser_sec = subparsers.add_parser("security", help="Passwords, Metadata and Watermarks")
    parser_sec.add_argument("--op", required=True, choices=['metadata', 'encrypt', 'decrypt', 'watermark'], help="Security operation")
    parser_sec.add_argument("--input", "-i", required=True, help="Path to input PDF file")
    parser_sec.add_argument("--output", "-o", help="Path to save the output PDF file")
    parser_sec.add_argument("--password", help="Password for encryption, decryption, or unlocking protected PDFs")
    parser_sec.add_argument("--title", help="Set PDF Title metadata")
    parser_sec.add_argument("--author", help="Set PDF Author metadata")
    parser_sec.add_argument("--subject", help="Set PDF Subject metadata")
    parser_sec.add_argument("--keywords", help="Set PDF Keywords metadata")
    parser_sec.add_argument("--watermark-text", help="Text to overlay as a watermark")
    parser_sec.add_argument("--opacity", type=float, help="Watermark text opacity (0.0 to 1.0, default 0.3)")
    
    args = parser.parse_args()
    
    if args.command == "convert":
        cmd_convert(args)
    elif args.command == "extract-text":
        cmd_extract_text(args)
    elif args.command == "page-edit":
        cmd_page_edit(args)
    elif args.command == "compress":
        cmd_compress(args)
    elif args.command == "security":
        cmd_security(args)


if __name__ == "__main__":
    main()
