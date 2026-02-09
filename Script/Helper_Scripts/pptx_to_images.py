"""
PowerPoint to Images Converter

Exports each slide of a .pptx file to individual PNG images using
PowerPoint's COM interface (Windows only). This gives pixel-perfect
rendering identical to what you see in PowerPoint.

Usage:
    python pptx_to_images.py input.pptx
    python pptx_to_images.py input.pptx -o output_folder
    python pptx_to_images.py input.pptx --width 1920
    python pptx_to_images.py input.pptx --format jpg

Output:
    Creates a folder (default: _temp-pptx-to-png/ next to the input file) with:
        slide_01.png, slide_02.png, ...

Requirements:
    - Windows with Microsoft PowerPoint installed
    - pip install comtypes Pillow
"""

import argparse
import comtypes
import comtypes.client
import os
import sys
import time
from pathlib import Path


def export_slides(pptx_path: str, output_dir: str = None, 
                  width: int = 1920, img_format: str = "png") -> list[str]:
    """
    Export all slides from a .pptx file to individual images.
    
    Args:
        pptx_path: Path to the .pptx file
        output_dir: Output directory (default: _temp-pptx-to-png/)
        width: Width of exported images in pixels (height auto-calculated)
        img_format: Image format - 'png' or 'jpg'
    
    Returns:
        List of paths to the exported image files
    """
    pptx_path = os.path.abspath(pptx_path)
    
    if not os.path.exists(pptx_path):
        print(f"Error: File not found: {pptx_path}")
        sys.exit(1)
    
    if not pptx_path.lower().endswith(('.pptx', '.ppt', '.potx')):
        print(f"Error: Not a PowerPoint file: {pptx_path}")
        sys.exit(1)
    
    # Default output directory: _temp-pptx-to-png/ (next to input file)
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(pptx_path), "_temp-pptx-to-png")
    
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Input:  {pptx_path}")
    print(f"Output: {output_dir}")
    print(f"Size:   {width}px wide")
    print(f"Format: {img_format.upper()}")
    print()
    
    # Initialize COM
    comtypes.CoInitialize()
    powerpoint = None
    presentation = None
    
    try:
        # Launch PowerPoint (hidden)
        powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
        # PowerPoint must be visible = False doesn't always work reliably
        # but we minimize it. Setting to 0 = hidden via ppWindowMinimized
        powerpoint.WindowState = 2  # ppWindowMinimized
        
        # Open the presentation (ReadOnly, no window)
        presentation = powerpoint.Presentations.Open(
            pptx_path,
            ReadOnly=True,      # Don't modify
            Untitled=False,
            WithWindow=False    # No visible window
        )
        
        slide_count = presentation.Slides.Count
        print(f"Found {slide_count} slide(s)")
        print()
        
        # Calculate height based on slide dimensions
        slide_width = presentation.SlideMaster.Width   # in points
        slide_height = presentation.SlideMaster.Height  # in points
        height = int(width * slide_height / slide_width)
        
        exported_files = []
        
        for i in range(1, slide_count + 1):
            slide = presentation.Slides(i)
            
            # Build output filename
            filename = f"slide_{i:02d}.{img_format}"
            filepath = os.path.join(output_dir, filename)
            
            # Export the slide
            slide.Export(filepath, img_format.upper(), width, height)
            
            exported_files.append(filepath)
            print(f"  Exported slide {i}/{slide_count}: {filename}")
        
        print()
        print(f"Done! {slide_count} slides exported to: {output_dir}")
        
        return exported_files
        
    except comtypes.COMError as e:
        print(f"\nCOM Error: {e}")
        print("Make sure Microsoft PowerPoint is installed.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
    finally:
        # Clean up COM objects
        try:
            if presentation:
                presentation.Close()
        except Exception:
            pass
        try:
            if powerpoint:
                powerpoint.Quit()
        except Exception:
            pass
        comtypes.CoUninitialize()


def main():
    parser = argparse.ArgumentParser(
        description="Export PowerPoint slides to individual images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python pptx_to_images.py presentation.pptx
    python pptx_to_images.py presentation.pptx -o my_slides
    python pptx_to_images.py presentation.pptx --width 2560
    python pptx_to_images.py presentation.pptx --format jpg
        """
    )
    
    parser.add_argument("input", help="Path to .pptx file")
    parser.add_argument("-o", "--output", default=None,
                        help="Output directory (default: _temp-pptx-to-png/)")
    parser.add_argument("--width", type=int, default=1920,
                        help="Image width in pixels (default: 1920)")
    parser.add_argument("--format", choices=["png", "jpg"], default="png",
                        help="Image format (default: png)")
    
    args = parser.parse_args()
    
    export_slides(args.input, args.output, args.width, args.format)


if __name__ == "__main__":
    main()
