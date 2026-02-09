---
name: docx-visual-feedback
description: Visual feedback loop for developing and debugging Word document output. Use when generating documents from markdown, fixing page layout issues, debugging a DOCX converter, or when the user asks to review rendered pages for visual correctness.
---

# Word Document Visual Feedback Workflow

Enables a build-inspect-fix cycle for Word document generation. The agent can generate a `.docx`, render every page to PNG, visually inspect the output, and iterate on fixes — all without the user opening Word manually.

## Prerequisites

- **Python packages**: `python-docx`, `comtypes`, `PyMuPDF`
- **Microsoft Word** installed (Windows — used for pixel-perfect PDF export via COM)
- **`docx_to_images.py`** — the rendering script (see Utility Scripts below)

## Workflow

```
1. Generate   →  Create or update the .docx file (md_to_docx.py, python-docx, etc.)
2. Render     →  Run docx_to_images.py on the .docx to export page PNGs
3. Inspect    →  Read the page PNGs to visually check each page
4. Fix        →  Edit the generator code or source content
5. Repeat     →  Go back to step 1 until all pages look correct
```

### Step 1: Generate the Word Document

Use whatever tool or script produces the `.docx`. Examples:

```bash
# With the markdown-to-docx converter
python md_to_docx.py INPUT.md OUTPUT.docx

# Or any other python-docx script
python build_report.py
```

### Step 2: Render Pages to Images

```bash
python docx_to_images.py INPUT.docx
```

- Creates folder `_temp-docx-to-png/` (next to the input file) containing `page_01.png`, `page_02.png`, etc.
- Default width: 1920px (use `--width 2560` for higher resolution)
- Use `-o custom_folder` to specify a different output directory
- Use `--format jpg` for smaller files
- Use `--keep-pdf` to retain the intermediate PDF
- Takes ~1-3 seconds per page (Word COM export + PDF rendering)

### Step 3: Inspect Page Images

Read the PNGs using the Read tool to visually inspect each page:

```
Read page_01.png, page_02.png, ... etc.
```

**What to check:**
- Headings are styled correctly and at the right level
- Tables fit within page margins and columns are appropriately sized
- Bullet and numbered lists are properly indented and formatted
- Bold, italic, and inline code render correctly
- Images are positioned and sized appropriately
- Page breaks fall at reasonable points
- Blockquotes have the left border and italic styling
- Code blocks have the gray background shading
- Text is not cut off at page boundaries
- Hyperlinks are styled and underlined

### Step 4: Fix Issues

> **CRITICAL: NEVER modify the original Markdown (`.md`) source file to fix a visual issue. All fixes must be made in the Python converter script (`md_to_docx.py`).** The Markdown content is the source of truth — if something looks wrong in the rendered document, the converter is responsible for handling it correctly.

Based on visual inspection, edit **the generator script** (`md_to_docx.py`) — for layout, sizing, formatting, or rendering bugs.

Common fixes:
- Adjusting table autofit logic (content vs. window mode)
- Fixing font sizes for readability
- Correcting list indentation levels
- Adjusting image widths (`Inches` values in python-docx code)
- Fixing cell padding or margin values
- Adjusting paragraph spacing or indent values

### Step 5: Repeat

Re-run steps 1-3 until all pages look correct. Batch-read multiple page images in parallel for efficiency.

## Quick Reference

**Full pipeline (generate + render):**

```bash
python md_to_docx.py INPUT.md OUTPUT.docx && python docx_to_images.py OUTPUT.docx
```

**Render only — for reviewing any existing .docx file:**

```bash
python docx_to_images.py any_document.docx
```

**Higher resolution:**

```bash
python docx_to_images.py INPUT.docx --width 2560
```

**JPG for faster iteration:**

```bash
python docx_to_images.py INPUT.docx --format jpg
```

**Keep the intermediate PDF:**

```bash
python docx_to_images.py INPUT.docx --keep-pdf
```

## Tips for Efficient Debugging

1. **Start with problem pages** — if the user reports a specific issue, render and inspect only that page number
2. **Batch reads** — read 3-5 page images in parallel to speed up inspection
3. **Check edge cases first** — pages with tables, pages with images, long lists, and code blocks are most likely to have issues
4. **Compare before/after** — after a fix, re-render and re-read only the affected pages
5. **Use `--format jpg`** for faster iteration when pixel-perfect quality isn't needed
6. **Use `--keep-pdf`** to inspect the intermediate PDF in a viewer for additional debugging

## Utility Scripts

### docx_to_images.py

Exports every page in a `.docx` to individual PNG/JPG images. Uses Word's COM interface to export a pixel-perfect PDF, then PyMuPDF to render each page as an image.

**Usage:**

```bash
python docx_to_images.py report.docx                # default: 1920px PNG
python docx_to_images.py report.docx -o my_pages     # custom output folder
python docx_to_images.py report.docx --width 2560    # higher resolution
python docx_to_images.py report.docx --format jpg    # JPG instead of PNG
python docx_to_images.py report.docx --keep-pdf      # keep intermediate PDF
```

**Requirements:** Windows, Microsoft Word, `comtypes`, `PyMuPDF`

**Output:** `_temp-docx-to-png/page_01.png`, `page_02.png`, etc.

**Key function** (can also be imported):

```python
from docx_to_images import export_pages

images = export_pages("my_report.docx", output_dir="pages", width=1920, img_format="png")
# Returns list of exported file paths
```
