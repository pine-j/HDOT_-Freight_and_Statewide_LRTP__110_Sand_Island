---
name: pptx-visual-feedback
description: Visual feedback loop for developing and debugging PowerPoint output. Use when generating presentations from markdown, fixing slide layout issues, debugging a PowerPoint converter, or when the user asks to review rendered slides for visual correctness.
---

# PowerPoint Visual Feedback Workflow

Enables a build-inspect-fix cycle for PowerPoint generation. The agent can generate a `.pptx`, render every slide to PNG, visually inspect the output, and iterate on fixes — all without the user opening PowerPoint manually.

## Prerequisites

- **Python packages**: `python-pptx`, `comtypes`, `Pillow`
- **Microsoft PowerPoint** installed (Windows — used for pixel-perfect slide rendering via COM)
- **`pptx_to_images.py`** — the rendering script (see Utility Scripts below)

## Workflow

```
1. Generate   →  Create or update the .pptx file (converter, python-pptx, manual edit, etc.)
2. Render     →  Run pptx_to_images.py on the .pptx to export slide PNGs
3. Inspect    →  Read the slide PNGs to visually check each slide
4. Fix        →  Edit the generator code or source content
5. Repeat     →  Go back to step 1 until all slides look correct
```

### Step 1: Generate the PowerPoint

Use whatever tool or script produces the `.pptx`. Examples:

```bash
# With a markdown-to-pptx converter
python md_to_pptx_converter.py INPUT.md -t template.pptx

# Or any other python-pptx script
python build_slides.py
```

### Step 2: Render Slides to Images

```bash
python pptx_to_images.py INPUT.pptx
```

- Creates folder `_temp-pptx-to-png/` (next to the input file) containing `slide_01.png`, `slide_02.png`, etc.
- Default width: 1920px (use `--width 2560` for higher resolution)
- Use `-o custom_folder` to specify a different output directory
- Use `--format jpg` for smaller files
- Takes ~1-2 seconds per slide

### Step 3: Inspect Slide Images

Read the PNGs using the Read tool to visually inspect each slide:

```
Read slide_01.png, slide_02.png, ... etc.
```

**What to check:**
- Title text is positioned correctly and not overlapping
- Bullet points are readable and properly indented
- Tables fit within the slide and columns are appropriately sized
- Section dividers use the correct layout
- Text is not cut off or overflowing the content area
- Fonts and colors match the intended branding
- Background images and template elements render correctly

### Step 4: Fix Issues

> **CRITICAL: NEVER modify the original Markdown (`.md`) source file to fix a visual issue. All fixes must be made in the Python converter script (`md_to_pptx_converter.py`).** The Markdown content is the source of truth — if something looks wrong in the rendered presentation, the converter is responsible for handling it correctly.

Based on visual inspection, edit **the generator script** (`md_to_pptx_converter.py`) — for layout, sizing, formatting, or rendering bugs.

Common fixes:
- Adjusting text box positions (`Inches` values in python-pptx code)
- Fixing font sizes for readability
- Correcting table column width calculations
- Fixing bullet indentation levels
- Adjusting content area boundaries to avoid overlap with template elements

### Step 5: Repeat

Re-run steps 1-3 until all slides look correct. Batch-read multiple slide images in parallel for efficiency.

## Quick Reference

**Full pipeline (generate + render):**

```bash
python my_converter.py INPUT.md && python pptx_to_images.py OUTPUT.pptx
```

**Render only — for reviewing any existing .pptx file:**

```bash
python pptx_to_images.py any_presentation.pptx
```

**Higher resolution:**

```bash
python pptx_to_images.py INPUT.pptx --width 2560
```

**JPG for faster iteration:**

```bash
python pptx_to_images.py INPUT.pptx --format jpg
```

## Tips for Efficient Debugging

1. **Start with problem slides** — if the user reports a specific issue, render and inspect only that slide number
2. **Batch reads** — read 3-5 slide images in parallel to speed up inspection
3. **Check edge cases first** — title slides, section dividers, slides with tables, and slides with long content are most likely to have issues
4. **Compare before/after** — after a fix, re-render and re-read only the affected slides
5. **Use `--format jpg`** for faster iteration when pixel-perfect quality isn't needed

## Utility Scripts

### pptx_to_images.py

Exports every slide in a `.pptx` to individual PNG/JPG images using PowerPoint's COM interface on Windows. Gives pixel-perfect rendering identical to PowerPoint's own display.

**Usage:**

```bash
python pptx_to_images.py presentation.pptx              # default: 1920px PNG
python pptx_to_images.py presentation.pptx -o my_slides  # custom output folder
python pptx_to_images.py presentation.pptx --width 2560  # higher resolution
python pptx_to_images.py presentation.pptx --format jpg  # JPG instead of PNG
```

**Requirements:** Windows, Microsoft PowerPoint, `comtypes`, `Pillow`

**Output:** `_temp-pptx-to-png/slide_01.png`, `slide_02.png`, etc.

**Key function** (can also be imported):

```python
from pptx_to_images import export_slides

images = export_slides("my_deck.pptx", output_dir="slides", width=1920, img_format="png")
# Returns list of exported file paths
```
