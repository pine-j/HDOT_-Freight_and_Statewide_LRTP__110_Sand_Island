"""
Word Document to Images Converter

Exports each page of a .docx file to individual PNG images using
Word's COM interface for PDF export (Windows only) and PyMuPDF for
rendering.  This gives pixel-perfect rendering identical to what you
see in Microsoft Word.

Usage:
    python docx_to_images.py input.docx
    python docx_to_images.py input.docx -o output_folder
    python docx_to_images.py input.docx --width 1920
    python docx_to_images.py input.docx --format jpg
    python docx_to_images.py input.docx --keep-pdf

Output:
    Creates a folder (default: _temp-docx-to-png/ next to the input file) with:
        page_01.png, page_02.png, ...

Requirements:
    - Windows with Microsoft Word installed
    - pip install comtypes PyMuPDF
"""

import argparse
import comtypes
import comtypes.client
import fitz  # PyMuPDF
import os
import sys
import time
from pathlib import Path


def export_pages(docx_path: str, output_dir: str = None,
                 width: int = 1920, img_format: str = "png",
                 keep_pdf: bool = False) -> list[str]:
    """
    Export all pages from a .docx file to individual images.

    The process has two stages:
      1. Word COM exports the document to a temporary PDF (pixel-perfect).
      2. PyMuPDF renders each PDF page to an image at the requested width.

    Args:
        docx_path: Path to the .docx file
        output_dir: Output directory (default: _temp-docx-to-png/)
        width: Width of exported images in pixels (height auto-calculated)
        img_format: Image format - 'png' or 'jpg'
        keep_pdf: If True, keep the intermediate PDF file

    Returns:
        List of paths to the exported image files
    """
    docx_path = os.path.abspath(docx_path)

    if not os.path.exists(docx_path):
        print(f"Error: File not found: {docx_path}")
        sys.exit(1)

    if not docx_path.lower().endswith(('.docx', '.doc', '.dotx')):
        print(f"Error: Not a Word document: {docx_path}")
        sys.exit(1)

    # Default output directory: _temp-docx-to-png/ (next to input file)
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(docx_path), "_temp-docx-to-png")

    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Temporary PDF path inside the output directory
    pdf_path = os.path.join(output_dir, "_temp_render.pdf")

    print(f"Input:  {docx_path}")
    print(f"Output: {output_dir}")
    print(f"Size:   {width}px wide")
    print(f"Format: {img_format.upper()}")
    print()

    # ------------------------------------------------------------------
    # Stage 1: Export DOCX -> PDF via Word COM
    # ------------------------------------------------------------------
    print("Stage 1: Exporting to PDF via Microsoft Word ...")

    comtypes.CoInitialize()
    word = None
    doc = None

    try:
        word = comtypes.client.CreateObject("Word.Application")
        word.Visible = False

        doc = word.Documents.Open(docx_path, ReadOnly=True)

        # wdExportFormatPDF = 17, wdExportOptimizeForPrint = 0
        doc.ExportAsFixedFormat(
            OutputFileName=pdf_path,
            ExportFormat=17,
            OptimizeFor=0,
        )

        page_count = doc.ComputeStatistics(2)  # wdStatisticPages = 2
        print(f"  Word reports {page_count} page(s)")

    except comtypes.COMError as e:
        print(f"\nCOM Error: {e}")
        print("Make sure Microsoft Word is installed.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError during Word export: {e}")
        sys.exit(1)
    finally:
        try:
            if doc:
                doc.Close(False)
        except Exception:
            pass
        try:
            if word:
                word.Quit()
        except Exception:
            pass
        comtypes.CoUninitialize()

    if not os.path.exists(pdf_path):
        print("Error: PDF was not created. Word export may have failed.")
        sys.exit(1)

    print(f"  PDF saved: {pdf_path}")
    print()

    # ------------------------------------------------------------------
    # Stage 2: Render PDF pages -> images via PyMuPDF
    # ------------------------------------------------------------------
    print("Stage 2: Rendering pages to images ...")

    exported_files = []

    try:
        pdf = fitz.open(pdf_path)
        page_count = len(pdf)

        print(f"  Found {page_count} page(s) in PDF")
        print()

        for i, page in enumerate(pdf, start=1):
            # Calculate zoom factor to reach the target width
            zoom = width / page.rect.width
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)

            filename = f"page_{i:02d}.{img_format}"
            filepath = os.path.join(output_dir, filename)

            if img_format == "jpg":
                pix.save(filepath, jpg_quality=95)
            else:
                pix.save(filepath)

            exported_files.append(filepath)
            print(f"  Exported page {i}/{page_count}: {filename}")

        pdf.close()

    except Exception as e:
        print(f"\nError during PDF rendering: {e}")
        sys.exit(1)

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------
    if keep_pdf:
        print(f"\n  PDF kept at: {pdf_path}")
    else:
        try:
            os.remove(pdf_path)
        except OSError:
            pass

    print()
    print(f"Done! {len(exported_files)} pages exported to: {output_dir}")

    return exported_files


def main():
    parser = argparse.ArgumentParser(
        description="Export Word document pages to individual images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python docx_to_images.py report.docx
    python docx_to_images.py report.docx -o my_pages
    python docx_to_images.py report.docx --width 2560
    python docx_to_images.py report.docx --format jpg
    python docx_to_images.py report.docx --keep-pdf
        """
    )

    parser.add_argument("input", help="Path to .docx file")
    parser.add_argument("-o", "--output", default=None,
                        help="Output directory (default: _temp-docx-to-png/)")
    parser.add_argument("--width", type=int, default=1920,
                        help="Image width in pixels (default: 1920)")
    parser.add_argument("--format", choices=["png", "jpg"], default="png",
                        help="Image format (default: png)")
    parser.add_argument("--keep-pdf", action="store_true", default=False,
                        help="Keep the intermediate PDF file")

    args = parser.parse_args()

    export_pages(args.input, args.output, args.width, args.format, args.keep_pdf)


if __name__ == "__main__":
    main()
