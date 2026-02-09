# Markdown to PowerPoint Converter - Usage Guide

## Overview

The `md_to_pptx_converter.py` script converts structured markdown files into professional PowerPoint presentations using the Sand Island PPT Template with HDOT branding.

## Template Layouts

The Sand Island template includes 4 layouts that are automatically mapped:

1. **Title Slide** - Used for the main presentation title
2. **Agenda or Table of Contents** - Can be used for agenda/TOC slides
3. **Transition Slide** - Used for section dividers (H2 headings)
4. **Content Slide** - Used for regular content with bullets and tables

## HDOT Brand Colors

The converter uses the official HDOT Makai (Ocean) theme colors:

- **Primary Blue**: `#26486E` (38, 72, 110) - Headers, title bars
- **Medium Blue**: `#4D76A4` (77, 118, 164) - Section dividers, accents
- **Dark Gray**: `#555555` (85, 85, 85) - Body text

**Font**: Open Sans (HDOT standard typeface)

## Usage

### Basic Command

```bash
python Templates\md_to_pptx_converter.py METHODOLOGY_PPT.md -t "Templates\Sand-Island-PPT-Template.pptx"
```

### With Custom Output Name

```bash
python Templates\md_to_pptx_converter.py METHODOLOGY_PPT.md -o MyPresentation.pptx -t "Templates\Sand-Island-PPT-Template.pptx"
```

### Without Template (Uses HDOT Default Styling)

```bash
python Templates\md_to_pptx_converter.py METHODOLOGY_PPT.md
```

## Markdown Structure

The converter recognizes the following markdown elements:

### Slide Types

- `# Title` - Creates a title slide (first H1 only)
- `## Section` - Creates a transition/section divider slide
- `### Content Title` - Creates a content slide
- `---` - Forces a slide break (continues with same H3 title)

### Content Elements

- **Bullets**: Use `- ` or `* ` for bullet points
  - Nested bullets: Indent with 2 spaces per level
- **Bold**: `**bold text**`
- **Italic**: `*italic text*`
- **Links**: `[link text](url)`
- **Tables**: Standard markdown tables with `|` separators

### Example Markdown

```markdown
# My Presentation Title
Subtitle text goes here

## Introduction

### Key Points
- First bullet point
- Second bullet point
  - Nested bullet
- **Bold text** and *italic text*

---

### Data Table

| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
| Data 4   | Data 5   | Data 6   |

## Conclusion

### Summary
- Final thoughts
- Next steps
```

## Layout Mapping

The converter automatically maps markdown structure to template layouts:

| Markdown Element | Template Layout Used |
|------------------|---------------------|
| `# Title` (H1) | Title Slide (Layout 0) |
| `## Section` (H2) | Transition Slide (Layout 2) |
| `### Content` (H3) | Content Slide (Layout 3) |

## Requirements

Install required packages:

```bash
pip install python-pptx mistune
```

## Troubleshooting

### Issue: Template not found
**Solution**: Use the full path to the template file in quotes:
```bash
python Templates\md_to_pptx_converter.py input.md -t "C:\Full\Path\To\Template.pptx"
```

### Issue: Font not displaying correctly
**Solution**: Ensure Open Sans font is installed on your system. The converter will fall back to system defaults if unavailable.

### Issue: Tables not fitting on slide
**Solution**: The converter automatically sizes tables to fit. If content is too large, consider:
- Splitting into multiple slides using `---`
- Reducing the number of columns
- Shortening text in cells

## Advanced Features

### Creating a Clean Template

If you have a template with existing slides and want to create a clean version:

```bash
python Templates\md_to_pptx_converter.py --clean-template source.pptx -o clean_template.pptx
```

### Customizing Colors

Edit the `CONFIG` section in `md_to_pptx_converter.py` to use different HDOT themes:

- **Makai (Ocean)**: Default - General HDOT branding
- **Mauka (Mountain)**: Inland highways, environmental projects
- **Aina (Land/Earth)**: Sustainability, infrastructure
- **Sandy (Soil/Sand)**: Construction, earthworks

## Output

The converter creates a PowerPoint file (`.pptx`) with:
- Properly formatted slides using the template layouts
- HDOT brand colors and fonts
- Automatic table sizing and formatting
- Bullet point hierarchy
- Section dividers

## Example Output

Running the converter on `METHODOLOGY_PPT.md`:

```bash
python Templates\md_to_pptx_converter.py METHODOLOGY_PPT.md -t "Templates\Sand-Island-PPT-Template.pptx"
```

Creates `METHODOLOGY_PPT.pptx` with:
- 26 slides
- Title slide with project name
- Section dividers for major topics
- Content slides with bullets and tables
- Consistent HDOT branding throughout

---

*For questions or issues, refer to the HDOT Brand Guidelines or contact the project team.*
