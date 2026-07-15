---
name: pdf-tools
description: Advanced toolset for PDF files including multi-format conversion, layout-aware text extraction, OCR, page editing, compression, encryption/decryption, metadata editing, and watermarking.
---

# Advanced PDF Tools Skill

A comprehensive toolset for programmatic PDF manipulation, conversion, analysis, and security.

## Setup
Before executing this skill, ensure that the Python virtual environment has all the required libraries:
```bash
pip install -r requirements.txt
```

If you plan to use the OCR capability (`extract-text --ocr`), you must install Tesseract OCR on the host system:
- **Debian/Ubuntu**: `sudo apt-get install tesseract-ocr`
- **macOS**: `brew install tesseract`
- **Windows**: Install the Tesseract binaries and add the installation folder to the system PATH.

All subcommands are executed using:
`python3 scripts/pdf_op.py`

---

## Subcommands & Arguments Schema

### 1. `convert` (Bidirectional Conversion)
Converts PDF to HTML, Markdown, or Plain Text, and converts Markdown/HTML into formatted PDF documents.

**Arguments:**
- `--input`, `-i` (string, required): Path to the source file (.pdf, .md, .html, .txt).
- `--output`, `-o` (string, required): Path to the target output file (.pdf, .md, .html, .txt).

**Examples:**
*Convert PDF to Markdown:*
```bash
python3 scripts/pdf_op.py convert -i document.pdf -o output.md
```
*Compile Markdown into PDF:*
```bash
python3 scripts/pdf_op.py convert -i source.md -o output.pdf
```

---

### 2. `extract-text` (Text & OCR Extraction)
Extracts text from a PDF, supporting scanned page detection, layout preservation, and OCR.

**Arguments:**
- `--input`, `-i` (string, required): Path to the input PDF file.
- `--output`, `-o` (string, optional): Path to save the extracted text file. If omitted, prints results to standard output.
- `--layout` (flag, optional): Preserves the spatial/visual block layout of the document text.
- `--ocr` (flag, optional): Triggers OCR on scanned pages (requires `tesseract-ocr` system dependency).

**Examples:**
*Extract text retaining layout:*
```bash
python3 scripts/pdf_op.py extract-text -i document.pdf --layout -o text.txt
```
*Extract text using OCR for scanned PDF files:*
```bash
python3 scripts/pdf_op.py extract-text -i scanned.pdf --ocr -o ocr_text.txt
```

---

### 3. `page-edit` (Page Editing & Restructuring)
Performs structural changes on PDF pages.

**Arguments:**
- `--op` (string, required): Operation to perform. Choices: `merge`, `split`, `rotate`, `insert`, `delete-blank`.
- `--input`, `-i` (string, optional): Path to the input PDF (required for all operations except `merge`).
- `--inputs` (array of strings, optional): Space-separated list of PDFs to merge (required for `merge`).
- `--output`, `-o` (string, required): Path to save the output PDF.
- `--pages`, `-p` (string, optional): Page range or indices (1-based, inclusive, e.g. `1-3`, `5`, `7-end`).
- `--angle` (integer, optional): Clockwise rotation angle. Choices: `90`, `180`, `270`.
- `--insert-pdf` (string, optional): Path of the PDF to insert.
- `--insert-at` (integer, optional): 0-based index position where the PDF will be inserted.

**Examples:**
*Merge multiple PDF files:*
```bash
python3 scripts/pdf_op.py page-edit --op merge --inputs doc1.pdf doc2.pdf doc3.pdf -o merged.pdf
```
*Extract pages 1 to 3 and page 5 to a new file:*
```bash
python3 scripts/pdf_op.py page-edit --op split -i doc.pdf --pages 1-3,5 -o split_doc.pdf
```
*Rotate pages 1 and 2 by 90 degrees clockwise:*
```bash
python3 scripts/pdf_op.py page-edit --op rotate -i doc.pdf --pages 1,2 --angle 90 -o rotated_doc.pdf
```
*Delete blank pages:*
```bash
python3 scripts/pdf_op.py page-edit --op delete-blank -i doc.pdf -o cleaned.pdf
```

---

### 4. `compress` (PDF Size Compression)
Compresses PDF content streams and cleans unreferenced objects to reduce size with minimal quality loss.

**Arguments:**
- `--input`, `-i` (string, required): Path to the input PDF file.
- `--output`, `-o` (string, required): Path to save the compressed PDF.

**Example:**
```bash
python3 scripts/pdf_op.py compress -i large.pdf -o compressed.pdf
```

---

### 5. `security` (Security & Protection)
Manages encryption/decryption, document metadata, and watermarks.

**Arguments:**
- `--op` (string, required): Operation to perform. Choices: `metadata`, `encrypt`, `decrypt`, `watermark`.
- `--input`, `-i` (string, required): Path to the input PDF file.
- `--output`, `-o` (string, optional): Path to save the output PDF (required for all operations except reading metadata).
- `--password` (string, optional): Password for encryption, decryption, or unlocking protected PDFs.
- `--title`, `--author`, `--subject`, `--keywords` (string, optional): Metadata fields to update.
- `--watermark-text` (string, optional): Text to place diagonally across all pages.
- `--opacity` (float, optional, default: `0.3`): Opacity value of the watermark (between `0.0` and `1.0`).

**Examples:**
*Read PDF Metadata:*
```bash
python3 scripts/pdf_op.py security --op metadata -i doc.pdf
```
*Encrypt PDF using AES-256:*
```bash
python3 scripts/pdf_op.py security --op encrypt -i doc.pdf --password "mySecurePassword" -o encrypted.pdf
```
*Add a diagonal watermark to all pages:*
```bash
python3 scripts/pdf_op.py security --op watermark -i doc.pdf --watermark-text "CONFIDENTIAL" --opacity 0.25 -o watermarked.pdf
```
