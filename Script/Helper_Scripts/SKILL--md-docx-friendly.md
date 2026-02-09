---
name: markdown-to-docx-authoring
description: Structure markdown files for optimal Word document conversion using md_to_docx.py. Use when creating markdown documents intended for Word reports or when the user asks about formatting markdown for DOCX.
---

# Markdown to Word Document Authoring Guide

This guide teaches how to structure markdown files for conversion to professional Word documents using the `md_to_docx.py` script.

## Heading Hierarchy Rules

The converter maps markdown headings to Word heading styles:

| Markdown | Word Style | Visual Behavior |
|----------|------------|-----------------|
| `# H1` | Heading 1 | Centered, used for document title |
| `## H2` | Heading 2 | Major section heading |
| `### H3` | Heading 3 | Subsection heading |
| `#### H4` | Heading 4 | Sub-subsection heading |
| `##### H5` | Heading 5 | Minor heading |
| `###### H6` | Heading 6 | Lowest-level heading |

### Best Practices

- **Use ONE H1** at the start for the document title (it is centered automatically)
- **Use H2** for major sections (Executive Summary, Methodology, Findings, etc.)
- **Use H3** for subsections within each major section
- **Use H4–H6** sparingly for deeply nested content
- **Trailing `#` characters** are automatically stripped from headings

## Content Guidelines

### Bullet Lists

Supports three levels of nesting via indentation:

```markdown
- Top-level bullet (no indent)
  - Second-level bullet (2+ spaces)
    - Third-level bullet (4+ spaces)
```

Use `-`, `*`, or `+` as bullet markers — all are equivalent.

**Optimal:** 3–7 bullets per group, 1–2 nesting levels

**Avoid:**
- More than 3 levels of nesting (only 3 styles available)
- Very long bullet text without breaking into sub-bullets
- Mixing bullet markers within the same list (pick one)

### Numbered Lists

Supports three levels of nesting, same indentation rules:

```markdown
1. First item
2. Second item
  1. Sub-item A
  2. Sub-item B
    1. Deep sub-item
3. Third item
```

Use `1.` or `1)` format — both are supported.

### Tables

Tables are automatically formatted with the "Table Grid" style. The converter intelligently selects an autofit mode:

- **AutoFit to Contents** — when the table fits within page margins (columns sized to content)
- **AutoFit to Window** — when content would overflow; table stretches to full page width and font size is reduced proportionally (minimum 8 pt)

**Optimal:** 3–5 columns, 5–15 rows

```markdown
| Feature | Option A | Option B | Recommendation |
|---------|----------|----------|----------------|
| Cost | $10K | $15K | Option A |
| Timeline | 6 months | 4 months | Option B |
| Quality | Good | Excellent | Option B |
```

**Column alignment** is supported via the separator row:

```markdown
| Left-aligned | Center-aligned | Right-aligned |
|:-------------|:--------------:|--------------:|
| data         | data           | data          |
```

**Table features:**
- Header row is automatically bolded
- Cells are vertically centered
- Cell padding is added for comfortable spacing
- Inline formatting (**bold**, *italic*, `code`, [links](url)) works inside cells

**Avoid:**
- More than 6 columns (text becomes cramped even with auto-scaling)
- Very long cell content (use abbreviations or split into multiple rows)
- Tables without a separator row (required for proper parsing)

### Text Formatting

Use standard markdown inline formatting:

- `**bold**` for key terms and emphasis
- `*italic*` for subtle emphasis or definitions
- `` `code` `` for inline code (rendered in Consolas, 9 pt, pink/magenta)
- `[link text](url)` for hyperlinks (rendered as blue underlined clickable links)

### Images

Block-level images are supported:

```markdown
![Alt text](path/to/image.png)
```

- Images are rendered at **5.5 inches wide**, centered on the page
- Relative paths are resolved against the markdown file's directory
- If an image cannot be loaded, alt text is shown as a gray italic fallback

### Code Blocks

Fenced code blocks are rendered with monospace formatting:

````markdown
```python
def example():
    return "Hello, world!"
```
````

**Rendering:**
- Font: Consolas, 9 pt
- Light gray background shading (`#F2F2F2`)
- Indented 0.3 inches on left and right for visual separation

**Best practice:** Keep code blocks short (under 20 lines). For longer code, consider placing it in an appendix section or referencing an external file.

### Blockquotes

```markdown
> This is a blockquote that will be rendered with a left border,
> italic text, and gray color for visual distinction.
```

**Rendering:**
- Italic gray text (`#555555`)
- Left border (gray vertical line)
- Indented 0.5 inches from left margin
- Consecutive `>` lines are merged into a single paragraph

### Horizontal Rules

```markdown
---
```

By default, horizontal rules (`---`, `***`, `___`) are **silently skipped**. The script has a configuration flag `ENABLE_HORIZONTAL_RULES` that can be set to `True` to render them as a centered line of `─` characters.

### Paragraphs

Consecutive lines of plain text (not headings, lists, tables, etc.) are **automatically merged** into a single paragraph. Separate paragraphs with a blank line.

```markdown
This is the first sentence of a paragraph.
This line will be merged into the same paragraph.

This starts a new paragraph because of the blank line above.
```

## Complete Template

Use this structure for new documents:

```markdown
# Document Title

## Executive Summary

Brief overview of the document's purpose and key findings.
This can span multiple lines and will be merged into one paragraph.

- Key finding 1
- Key finding 2
- Key finding 3

## Introduction

### Background

Context and motivation for the analysis. Describe the problem
space and why this work matters.

### Objectives

1. Primary objective
2. Secondary objective
3. Tertiary objective

## Methodology

### Data Sources

| Source | Description | Time Period | Coverage |
|--------|-------------|-------------|----------|
| Source A | Description | 2020–2025 | Statewide |
| Source B | Description | 2023–2025 | Regional |

### Analytical Approach

- Step 1: Data collection and cleaning
- Step 2: Statistical analysis
  - Sub-step 2a: Descriptive statistics
  - Sub-step 2b: Regression modeling
- Step 3: Validation and review

## Findings

### Finding Category 1

Key insight supported by data and analysis.

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Value 1 | 100 | 150 | +50% |
| Value 2 | 200 | 180 | -10% |

### Finding Category 2

![Analysis Chart](figures/chart_01.png)

Additional narrative discussing the chart above.

> "Notable quote or callout that deserves emphasis."

## Recommendations

### Short-term Actions

1. Immediate priority with rationale
2. Quick win with expected impact
3. Process improvement

### Long-term Strategy

- Strategic initiative 1 with timeline
- Strategic initiative 2 with dependencies
- Future considerations and monitoring plan

## Conclusion

Summary of key takeaways and next steps. Restate the most
important findings and their implications for decision-making.

## Appendix

### Appendix A: Data Dictionary

| Field | Type | Description |
|-------|------|-------------|
| field_a | String | Description of field A |
| field_b | Integer | Description of field B |
```

## Anti-Patterns to Avoid

### 1. Skipping Heading Levels

```markdown
# Title

### Subsection  ❌ Missing H2 — breaks document outline

Use this instead:

# Title

## Section Name

### Subsection  ✓
```

### 2. Missing Table Separator Row

```markdown
| Header 1 | Header 2 |
| Data 1 | Data 2 |  ❌ No separator — parsed as two data rows

Use this instead:

| Header 1 | Header 2 |
|----------|----------|
| Data 1 | Data 2 |  ✓
```

### 3. Mixing List Types in a Group

```markdown
- Bullet item
1. Numbered item  ❌ Inconsistent list type
- Another bullet

Use separate groups:

- Bullet item
- Another bullet

1. Numbered item
2. Another numbered item  ✓
```

### 4. Missing Blank Lines Between Elements

```markdown
Some paragraph text.
| Col 1 | Col 2 |  ❌ Table immediately after text — may not parse correctly
|-------|-------|

Use this instead:

Some paragraph text.

| Col 1 | Col 2 |  ✓
|-------|-------|
```

### 5. HTML/CSS Blocks

```markdown
<div style="color: red;">Important</div>  ❌ HTML is not processed

Use markdown formatting instead:

**Important**  ✓
```

### 6. Overly Wide Tables

```markdown
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 |  ❌ Too many columns

The converter will scale down the font (min 8 pt), but readability suffers.
Split into multiple tables or reduce columns:

| Category | Metric | Value | Status |  ✓
|----------|--------|-------|--------|
```

## Usage

### Basic Conversion

```bash
python md_to_docx.py input.md
```

Output: `input.docx` in the same directory.

### Custom Output Path

```bash
python md_to_docx.py input.md "reports/final_report.docx"
```

## Differences from PowerPoint Authoring

If you are also producing a PPTX version, be aware of these key differences:

| Aspect | DOCX (this guide) | PPTX |
|--------|-------------------|------|
| **Heading depth** | H1–H6 all render as Word headings | Only H1–H3 create slides |
| **Content length** | No per-page limits — text flows naturally | Must fit on slides (5–7 bullets max) |
| **Horizontal rules** | Skipped by default | Create slide breaks (`---`) |
| **Code blocks** | Fully supported with syntax shading | Minimal support |
| **Blockquotes** | Rendered with left border and italic style | Not supported |
| **Images** | Centered at 5.5" width | Placed on slides |
| **Paragraphs** | Consecutive lines merge into one paragraph | Each line becomes a bullet |
| **Tables** | Smart autofit with font scaling | Fixed slide dimensions |

## Tips for Professional Results

1. **Use a clear heading hierarchy** — H1 > H2 > H3 gives a clean Table of Contents
2. **Keep paragraphs focused** — one idea per paragraph aids readability
3. **Use tables for structured data** — easier to scan than inline lists
4. **Add images for visual evidence** — charts, maps, and diagrams enhance reports
5. **Use blockquotes for callouts** — highlight important quotes or notes
6. **Separate content with blank lines** — ensures proper element parsing
7. **Keep code blocks short** — move lengthy code to appendices
8. **Use numbered lists for sequences** — bullets for unordered items, numbers for ordered steps
9. **Test with a small section first** — verify formatting before converting the full document
10. **Review the Word doc's heading navigation** — check the Navigation Pane to ensure proper document structure
