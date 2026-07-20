---
name: md-to-pdf
description: Convert Markdown (.md) documents into visually appealing PDF (.pdf) files using Python and Playwright within a clean uv virtual environment.
---

# Markdown to PDF Conversion Skill

This skill allows converting any Markdown file into a styled PDF document.

## Prerequisites
- Requires Python virtual environment managed via `uv`.
- Dependencies: `markdown`, `playwright`.

## Usage Instructions

To convert a Markdown file to PDF, run the following command:

```bash
uv run python .agents/skills/md-to-pdf/scripts/convert.py <input_markdown_file> <output_pdf_file>
```

### Example

```bash
uv run python .agents/skills/md-to-pdf/scripts/convert.py crawl_results/techs/Adaptive-RAG.md crawl_results/techs/Adaptive-RAG.pdf
```
