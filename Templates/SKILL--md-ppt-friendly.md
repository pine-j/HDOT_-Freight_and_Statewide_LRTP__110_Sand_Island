---
name: markdown-to-pptx-authoring
description: Structure markdown files for optimal PowerPoint conversion using md_to_pptx_converter.py. Use when creating markdown documents intended for presentation slides or when the user asks about formatting markdown for PowerPoint.
---

# Markdown to PowerPoint Authoring Guide

This guide teaches how to structure markdown files for conversion to professional PowerPoint presentations using the `md_to_pptx_converter.py` script.

## Heading Hierarchy Rules

The converter maps markdown headings to specific slide types:

| Markdown | Slide Type | Visual Style |
|----------|------------|--------------|
| `# H1` | Title slide | Full-screen blue background, centered text |
| `## H2` | Section divider | Blue accent bar with centered title |
| `### H3` | Content slide | Blue title bar with content area below |
| `---` | Slide break | Creates new slide with same H3 title (adds "cont.") |

### Best Practices

- **Use ONE H1** at the start for the presentation title
- **Use H2** to divide major sections (3-5 sections typical)
- **Use H3** for each content slide within a section
- **Use `---`** only when content exceeds one slide

## Content Guidelines

### Bullet Points

**Optimal:** 5-7 bullets per slide

```markdown
### Key Findings

- First major point with brief explanation
- Second major point
- Third major point
  - Sub-point with additional detail
  - Another sub-point
- Fourth major point
```

**Avoid:**
- More than 7 top-level bullets (split into multiple slides)
- More than 2 levels of nesting (hard to read)
- Long paragraphs as bullets (keep concise)

### Tables

**Optimal:** 3-5 columns, 5-10 rows

```markdown
### Comparison Analysis

| Feature | Option A | Option B | Recommendation |
|---------|----------|----------|----------------|
| Cost | $10K | $15K | Option A |
| Timeline | 6 months | 4 months | Option B |
| Quality | Good | Excellent | Option B |
```

**Avoid:**
- More than 6 columns (text becomes unreadable)
- More than 15 rows (split into multiple slides)
- Long cell content (use abbreviations)

### Labels / Non-Bulleted Paragraphs

Use plain text lines (without `- `) for **section labels** and **subheadings** within a slide. These render as bold text without a bullet character, visually separating sections.

**Preferred — plain text label:**

```markdown
### Step 4: Data Processing

- FAF data is filtered for inbound freight

**Filtering Logic:**

| Flow Type | Origin | Destination |
|-----------|--------|-------------|
| Domestic  | Other  | Honolulu    |

**Processing Pipeline:**

1. Filter FAF data
2. Aggregate by commodity
3. Distribute to piers
```

**Also works — auto-detected label (fallback):**

Bullet lines that consist ONLY of bold text (optionally with colon) are automatically detected as labels and rendered without a bullet:

```markdown
- **Filtering Logic:**    ← auto-detected as label (no bullet rendered)
- **Note:** Some text     ← NOT a label (has text after bold, bullet rendered)
```

**When to use labels vs bullets:**
- Use **labels** (`**Label:**`) for section subheadings that introduce a table, list, or group of bullets
- Use **bullets** (`- text`) for actual list items and content points
- Labels get extra vertical spacing above them for visual separation

### Text Formatting

Use markdown formatting for emphasis:

- `**bold**` for key terms and emphasis
- `*italic*` for subtle emphasis or definitions
- `[link text](url)` for references (rendered as blue underlined text)

### Mixed Content

You can combine labels, bullets, and tables on the same slide:

```markdown
### Project Overview

- Budget: $2.5M
- Duration: 18 months
- Team size: 12 people

**Project Timeline:**

| Phase | Duration | Status |
|-------|----------|--------|
| Planning | 3 months | Complete |
| Development | 12 months | In Progress |
| Testing | 3 months | Pending |
```

Note how `**Project Timeline:**` renders as a bold label (no bullet) that introduces the table.

## Complete Template

Use this structure for new presentations:

```markdown
# Presentation Title

Subtitle or tagline (optional)

## Introduction

### Project Background

- Context and motivation
- Problem statement
- Objectives

### Methodology

- Approach overview
- Data sources
- Analysis techniques

## Key Findings

### Finding Category 1

- Major insight with supporting detail
- Related observation
- Impact assessment

### Finding Category 2

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Value 1 | 100 | 150 | +50% |
| Value 2 | 200 | 180 | -10% |

---

### Finding Category 2 (cont.)

- Additional analysis
- Implications
- Next steps

## Recommendations

### Short-term Actions

- Immediate priority 1
- Immediate priority 2
- Quick wins

### Long-term Strategy

- Strategic initiative 1
- Strategic initiative 2
- Future considerations

## Conclusion

### Summary

- Key takeaway 1
- Key takeaway 2
- Call to action
```

## Anti-Patterns to Avoid

### 1. Skipping Heading Levels

```markdown
# Title

### Content Slide  ❌ Missing H2 section divider

Use this instead:

# Title

## Section Name

### Content Slide  ✓
```

### 2. Too Much Nested Content

```markdown
### Bad Example  ❌

- Level 1
  - Level 2
    - Level 3
      - Level 4  (too deep!)

### Good Example  ✓

- Level 1
  - Level 2 with detail
- Level 1 continued
```

### 3. HTML/CSS Blocks

```markdown
<style>
body { color: red; }
</style>  ❌ Will be ignored

Use markdown formatting instead:

**Important text**  ✓
```

### 4. Code Blocks

````markdown
```python
def example():
    pass
```  ❌ Not well-supported
````

If you must include code, use it sparingly and keep it short (< 10 lines).

### 5. Wide Tables

```markdown
| Col1 | Col2 | Col3 | Col4 | Col5 | Col6 | Col7 |  ❌ Too many columns
|------|------|------|------|------|------|------|

Split into multiple slides or reduce columns:

| Category | Metric | Value | Status |  ✓
|----------|--------|-------|--------|
```

## Usage

### Basic Conversion

```bash
python md_to_pptx_converter.py your_document.md
```

Output: `your_document.pptx` in the same directory

### With TxDOT Template

```bash
python md_to_pptx_converter.py your_document.md --template "TxDOT-PPT-template -- IBM Plex.potx"
```

Uses template's colors and layouts instead of default TxDOT brand colors.

### Custom Output Path

```bash
python md_to_pptx_converter.py input.md -o "presentations/final.pptx"
```

## Slide Count Estimation

Estimate slides before conversion:

- 1 H1 → 1 title slide
- Each H2 → 1 section divider slide
- Each H3 → 1 content slide
- Each `---` → +1 continuation slide

**Example:**
```
# Title                    → 1 slide
## Section 1               → 1 slide
### Content A              → 1 slide
### Content B              → 1 slide
---                        → 1 slide (Content B cont.)
## Section 2               → 1 slide
### Content C              → 1 slide
                           --------
Total: 7 slides
```

## Tips for Professional Results

1. **Keep titles short** (5-8 words max)
2. **Use parallel structure** in bullet lists
3. **Start bullets with action verbs** when describing tasks
4. **Use consistent terminology** throughout
5. **Add white space** - don't overcrowd slides
6. **Test table width** - if > 5 columns, consider splitting
7. **Use section dividers** to give audience mental breaks
8. **End with clear next steps** or call to action
