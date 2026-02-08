"""
Generate monochromatic SVG icons for commodity types.
Uses HDOT Makai Dark Blue (#26486E) on transparent background.
Icons are 500x500px, simple geometric designs.
"""

import os
from pathlib import Path

# HDOT Makai Dark Blue
COLOR = "#26486E"
SIZE = 500
STROKE_WIDTH = 20

# Icon definitions: commodity name -> SVG path/shape data
ICONS = {
    "Alcoholic beverages": '''
        <path d="M200 100 L200 150 Q200 180 220 200 L220 400 Q220 430 250 430 L250 430 Q280 430 280 400 L280 200 Q300 180 300 150 L300 100 Z" fill="{color}"/>
        <rect x="190" y="80" width="120" height="30" rx="5" fill="{color}"/>
        <circle cx="250" cy="95" r="8" fill="white"/>
    ''',
    
    "Tobacco prods.": '''
        <rect x="150" y="200" width="200" height="40" rx="20" fill="{color}"/>
        <rect x="320" y="210" width="30" height="20" fill="{color}"/>
        <circle cx="170" cy="220" r="15" fill="none" stroke="{color}" stroke-width="{stroke}"/>
        <line x1="180" y1="200" x2="200" y2="180" stroke="{color}" stroke-width="3"/>
        <line x1="185" y1="195" x2="205" y2="175" stroke="{color}" stroke-width="3"/>
        <line x1="190" y1="190" x2="210" y2="170" stroke="{color}" stroke-width="3"/>
    ''',
    
    "Pharmaceuticals": '''
        <rect x="200" y="150" width="100" height="200" rx="10" fill="{color}"/>
        <rect x="150" y="250" width="200" height="100" rx="10" fill="{color}"/>
        <circle cx="250" cy="120" r="30" fill="{color}"/>
        <rect x="230" y="100" width="40" height="10" fill="white"/>
    ''',
    
    "Textiles/leather": '''
        <path d="M100 150 Q150 100 200 150 Q250 100 300 150 Q350 100 400 150 L400 350 Q350 300 300 350 Q250 300 200 350 Q150 300 100 350 Z" fill="{color}"/>
        <path d="M120 200 Q170 160 220 200" fill="none" stroke="white" stroke-width="8"/>
        <path d="M220 250 Q270 210 320 250" fill="none" stroke="white" stroke-width="8"/>
    ''',
    
    "Electronics": '''
        <rect x="150" y="150" width="200" height="200" rx="15" fill="{color}"/>
        <circle cx="200" cy="200" r="20" fill="white"/>
        <circle cx="300" cy="200" r="20" fill="white"/>
        <circle cx="200" cy="300" r="20" fill="white"/>
        <circle cx="300" cy="300" r="20" fill="white"/>
        <line x1="220" y1="200" x2="280" y2="200" stroke="white" stroke-width="8"/>
        <line x1="220" y1="300" x2="280" y2="300" stroke="white" stroke-width="8"/>
        <line x1="200" y1="220" x2="200" y2="280" stroke="white" stroke-width="8"/>
        <line x1="300" y1="220" x2="300" y2="280" stroke="white" stroke-width="8"/>
    ''',
    
    "Precision instruments": '''
        <circle cx="250" cy="250" r="120" fill="none" stroke="{color}" stroke-width="{stroke}"/>
        <line x1="250" y1="250" x2="250" y2="150" stroke="{color}" stroke-width="12"/>
        <line x1="250" y1="250" x2="320" y2="280" stroke="{color}" stroke-width="8"/>
        <circle cx="250" cy="250" r="15" fill="{color}"/>
        <line x1="250" y1="130" x2="250" y2="150" stroke="{color}" stroke-width="15"/>
        <line x1="370" y1="250" x2="350" y2="250" stroke="{color}" stroke-width="15"/>
        <line x1="250" y1="370" x2="250" y2="350" stroke="{color}" stroke-width="15"/>
        <line x1="130" y1="250" x2="150" y2="250" stroke="{color}" stroke-width="15"/>
    ''',
    
    "Furniture": '''
        <rect x="150" y="150" width="200" height="20" fill="{color}"/>
        <rect x="160" y="170" width="180" height="100" rx="5" fill="{color}"/>
        <rect x="170" y="270" width="20" height="100" fill="{color}"/>
        <rect x="310" y="270" width="20" height="100" fill="{color}"/>
    ''',
    
    "Mixed freight": '''
        <rect x="120" y="150" width="100" height="100" fill="{color}"/>
        <rect x="240" y="150" width="140" height="100" rx="70" fill="{color}"/>
        <polygon points="170,270 120,350 220,350" fill="{color}"/>
        <circle cx="330" cy="300" r="50" fill="{color}"/>
    ''',
    
    "Meat/seafood": '''
        <path d="M250 150 Q200 180 180 230 Q170 270 200 300 Q230 320 250 310 Q270 320 300 300 Q330 270 320 230 Q300 180 250 150 Z" fill="{color}"/>
        <ellipse cx="230" cy="240" rx="15" ry="25" fill="white"/>
        <ellipse cx="270" cy="240" rx="15" ry="25" fill="white"/>
        <path d="M220 280 Q250 295 280 280" fill="none" stroke="white" stroke-width="8"/>
    ''',
    
    "Other foodstuffs": '''
        <circle cx="250" cy="200" r="80" fill="{color}"/>
        <rect x="200" y="260" width="100" height="120" fill="{color}"/>
        <rect x="180" y="370" width="140" height="20" fill="{color}"/>
        <circle cx="230" cy="180" r="12" fill="white"/>
        <circle cx="270" cy="180" r="12" fill="white"/>
    ''',
    
    "Paper articles": '''
        <rect x="150" y="120" width="200" height="260" rx="5" fill="{color}"/>
        <line x1="180" y1="160" x2="320" y2="160" stroke="white" stroke-width="8"/>
        <line x1="180" y1="200" x2="320" y2="200" stroke="white" stroke-width="8"/>
        <line x1="180" y1="240" x2="320" y2="240" stroke="white" stroke-width="8"/>
        <line x1="180" y1="280" x2="280" y2="280" stroke="white" stroke-width="8"/>
    ''',
    
    "Printed prods.": '''
        <rect x="130" y="100" width="240" height="300" rx="8" fill="{color}"/>
        <rect x="160" y="140" width="80" height="100" fill="white"/>
        <line x1="260" y1="150" x2="340" y2="150" stroke="white" stroke-width="10"/>
        <line x1="260" y1="180" x2="340" y2="180" stroke="white" stroke-width="10"/>
        <line x1="260" y1="210" x2="340" y2="210" stroke="white" stroke-width="10"/>
        <line x1="160" y1="270" x2="340" y2="270" stroke="white" stroke-width="10"/>
        <line x1="160" y1="300" x2="340" y2="300" stroke="white" stroke-width="10"/>
        <line x1="160" y1="330" x2="280" y2="330" stroke="white" stroke-width="10"/>
    ''',
    
    "Misc. mfg. prods.": '''
        <circle cx="200" cy="200" r="60" fill="{color}"/>
        <rect x="280" y="160" width="80" height="80" fill="{color}"/>
        <polygon points="250,300 200,380 300,380" fill="{color}"/>
        <path d="M340 280 L380 300 L360 340 L320 320 Z" fill="{color}"/>
    ''',
    
    "Milled grain prods.": '''
        <rect x="180" y="280" width="140" height="120" fill="{color}"/>
        <path d="M250 120 L200 280 L300 280 Z" fill="{color}"/>
        <circle cx="250" cy="200" r="25" fill="white"/>
        <circle cx="220" cy="240" r="15" fill="white"/>
        <circle cx="280" cy="240" r="15" fill="white"/>
    ''',
    
    "Other ag prods.": '''
        <ellipse cx="250" cy="250" rx="100" ry="120" fill="{color}"/>
        <path d="M250 130 Q230 100 220 80 Q230 70 250 90 Q270 70 280 80 Q270 100 250 130" fill="{color}"/>
        <ellipse cx="230" cy="230" rx="20" ry="30" fill="white"/>
        <ellipse cx="270" cy="230" rx="20" ry="30" fill="white"/>
        <path d="M220 290 Q250 310 280 290" fill="none" stroke="white" stroke-width="10"/>
    ''',
    
    "Plastics/rubber": '''
        <path d="M150 200 Q150 150 200 150 L300 150 Q350 150 350 200 L350 300 Q350 350 300 350 L200 350 Q150 350 150 300 Z" fill="{color}"/>
        <circle cx="220" cy="220" r="25" fill="white"/>
        <circle cx="280" cy="220" r="25" fill="white"/>
        <circle cx="250" cy="290" r="30" fill="white"/>
    ''',
    
    "Articles-base metal": '''
        <rect x="180" y="150" width="140" height="200" fill="{color}"/>
        <polygon points="250,100 200,150 300,150" fill="{color}"/>
        <rect x="230" y="200" width="40" height="80" fill="white"/>
        <circle cx="250" cy="310" r="20" fill="white"/>
    ''',
    
    "Live animals/fish": '''
        <ellipse cx="250" cy="250" rx="120" ry="80" fill="{color}"/>
        <circle cx="210" cy="230" r="15" fill="white"/>
        <circle cx="205" cy="230" r="8" fill="{color}"/>
        <path d="M350 250 L420 220 L420 280 Z" fill="{color}"/>
        <path d="M180 200 L150 180 L160 210 Z" fill="{color}"/>
        <path d="M180 300 L150 320 L160 290 Z" fill="{color}"/>
    ''',
    
    "Chemical prods.": '''
        <path d="M250 120 L200 250 L150 250 L150 320 Q150 360 190 360 L310 360 Q350 360 350 320 L350 250 L300 250 Z" fill="{color}"/>
        <circle cx="250" cy="100" r="30" fill="{color}"/>
        <rect x="240" y="80" width="20" height="30" fill="white"/>
        <circle cx="200" cy="300" r="20" fill="white"/>
        <circle cx="300" cy="300" r="20" fill="white"/>
    ''',
    
    "Newsprint/paper": '''
        <rect x="140" y="100" width="220" height="300" fill="{color}"/>
        <rect x="160" y="130" width="80" height="100" fill="white"/>
        <line x1="260" y1="140" x2="340" y2="140" stroke="white" stroke-width="8"/>
        <line x1="260" y1="170" x2="340" y2="170" stroke="white" stroke-width="8"/>
        <line x1="260" y1="200" x2="340" y2="200" stroke="white" stroke-width="8"/>
        <line x1="160" y1="250" x2="340" y2="250" stroke="white" stroke-width="8"/>
        <line x1="160" y1="280" x2="340" y2="280" stroke="white" stroke-width="8"/>
        <line x1="160" y1="310" x2="340" y2="310" stroke="white" stroke-width="8"/>
        <line x1="160" y1="340" x2="340" y2="340" stroke="white" stroke-width="8"/>
    ''',
    
    "Machinery": '''
        <circle cx="250" cy="250" r="100" fill="{color}"/>
        <circle cx="250" cy="250" r="50" fill="white"/>
        <rect x="245" y="150" width="10" height="100" fill="{color}"/>
        <rect x="245" y="250" width="10" height="100" fill="{color}"/>
        <rect x="150" y="245" width="100" height="10" fill="{color}"/>
        <rect x="250" y="245" width="100" height="10" fill="{color}"/>
        <circle cx="250" cy="250" r="20" fill="{color}"/>
    ''',
    
    "Basic chemicals": '''
        <circle cx="200" cy="200" r="60" fill="{color}"/>
        <circle cx="300" cy="200" r="60" fill="{color}"/>
        <circle cx="250" cy="290" r="60" fill="{color}"/>
        <line x1="240" y1="220" x2="260" y2="260" stroke="white" stroke-width="15"/>
        <line x1="260" y1="220" x2="240" y2="260" stroke="white" stroke-width="15"/>
    ''',
    
    "Waste/scrap": '''
        <rect x="150" y="200" width="200" height="150" fill="{color}"/>
        <polygon points="180,200 200,150 220,200" fill="{color}"/>
        <polygon points="240,200 260,160 280,200" fill="{color}"/>
        <polygon points="300,200 320,140 340,200" fill="{color}"/>
        <rect x="180" y="230" width="30" height="40" fill="white"/>
        <rect x="235" y="250" width="30" height="50" fill="white"/>
        <rect x="290" y="240" width="30" height="45" fill="white"/>
    ''',
    
    "Animal feed": '''
        <rect x="170" y="250" width="160" height="130" fill="{color}"/>
        <path d="M250 120 L180 250 L320 250 Z" fill="{color}"/>
        <circle cx="220" cy="300" r="15" fill="white"/>
        <circle cx="250" cy="320" r="15" fill="white"/>
        <circle cx="280" cy="300" r="15" fill="white"/>
        <circle cx="235" cy="340" r="12" fill="white"/>
        <circle cx="265" cy="340" r="12" fill="white"/>
    ''',
    
    "Wood prods.": '''
        <rect x="160" y="150" width="40" height="220" fill="{color}"/>
        <rect x="220" y="150" width="40" height="220" fill="{color}"/>
        <rect x="280" y="150" width="40" height="220" fill="{color}"/>
        <line x1="160" y1="200" x2="320" y2="200" stroke="white" stroke-width="6"/>
        <line x1="160" y1="260" x2="320" y2="260" stroke="white" stroke-width="6"/>
        <line x1="160" y1="320" x2="320" y2="320" stroke="white" stroke-width="6"/>
    ''',
    
    "Fertilizers": '''
        <rect x="180" y="280" width="140" height="100" fill="{color}"/>
        <path d="M250 120 L200 280 L300 280 Z" fill="{color}"/>
        <circle cx="250" cy="200" r="20" fill="white"/>
        <line x1="250" y1="180" x2="250" y2="140" stroke="white" stroke-width="10"/>
        <line x1="230" y1="200" x2="200" y2="200" stroke="white" stroke-width="10"/>
        <line x1="270" y1="200" x2="300" y2="200" stroke="white" stroke-width="10"/>
        <line x1="265" y1="215" x2="285" y2="235" stroke="white" stroke-width="10"/>
    ''',
    
    "Base metals": '''
        <rect x="150" y="180" width="200" height="140" fill="{color}"/>
        <polygon points="250,100 180,180 320,180" fill="{color}"/>
        <rect x="180" y="210" width="50" height="80" fill="white"/>
        <rect x="270" y="210" width="50" height="80" fill="white"/>
    ''',
    
    "Transport equip.": '''
        <rect x="150" y="180" width="200" height="100" rx="10" fill="{color}"/>
        <rect x="170" y="150" width="160" height="40" rx="20" fill="{color}"/>
        <circle cx="200" cy="280" r="35" fill="{color}"/>
        <circle cx="300" cy="280" r="35" fill="{color}"/>
        <circle cx="200" cy="280" r="18" fill="white"/>
        <circle cx="300" cy="280" r="18" fill="white"/>
        <rect x="320" y="200" width="40" height="60" fill="{color}"/>
    ''',
    
    "Cereal grains": '''
        <ellipse cx="250" cy="280" rx="90" ry="100" fill="{color}"/>
        <path d="M250 180 Q240 150 230 130 L235 120 Q245 140 250 180" fill="{color}"/>
        <path d="M250 180 Q260 150 270 130 L265 120 Q255 140 250 180" fill="{color}"/>
        <line x1="200" y1="250" x2="300" y2="250" stroke="white" stroke-width="8"/>
        <line x1="210" y1="290" x2="290" y2="290" stroke="white" stroke-width="8"/>
        <line x1="220" y1="330" x2="280" y2="330" stroke="white" stroke-width="8"/>
    ''',
    
    "Logs": '''
        <ellipse cx="250" cy="250" rx="120" ry="80" fill="{color}"/>
        <ellipse cx="250" cy="250" rx="90" ry="60" fill="none" stroke="white" stroke-width="8"/>
        <ellipse cx="250" cy="250" rx="60" ry="40" fill="none" stroke="white" stroke-width="8"/>
        <ellipse cx="250" cy="250" rx="30" ry="20" fill="none" stroke="white" stroke-width="8"/>
        <line x1="130" y1="250" x2="370" y2="250" stroke="white" stroke-width="4"/>
    ''',
    
    "Nonmetal min. prods.": '''
        <rect x="160" y="200" width="180" height="150" fill="{color}"/>
        <polygon points="250,120 180,200 320,200" fill="{color}"/>
        <rect x="200" y="240" width="100" height="80" fill="white"/>
        <rect x="230" y="270" width="40" height="50" fill="{color}"/>
    ''',
    
    "Motorized vehicles": '''
        <rect x="140" y="200" width="220" height="90" rx="15" fill="{color}"/>
        <path d="M160 200 Q180 160 220 160 L280 160 Q320 160 340 200" fill="{color}"/>
        <circle cx="190" cy="290" r="40" fill="{color}"/>
        <circle cx="310" cy="290" r="40" fill="{color}"/>
        <circle cx="190" cy="290" r="22" fill="white"/>
        <circle cx="310" cy="290" r="22" fill="white"/>
        <rect x="200" y="175" width="40" height="35" fill="white"/>
        <rect x="260" y="175" width="40" height="35" fill="white"/>
    ''',
    
    "Building stone": '''
        <rect x="150" y="220" width="90" height="130" fill="{color}"/>
        <rect x="260" y="180" width="90" height="170" fill="{color}"/>
        <rect x="200" y="260" width="90" height="90" fill="{color}"/>
        <line x1="150" y1="220" x2="240" y2="220" stroke="white" stroke-width="6"/>
        <line x1="260" y1="250" x2="350" y2="250" stroke="white" stroke-width="6"/>
        <line x1="200" y1="305" x2="290" y2="305" stroke="white" stroke-width="6"/>
    ''',
    
    "Natural sands": '''
        <circle cx="200" cy="200" r="25" fill="{color}"/>
        <circle cx="270" cy="190" r="30" fill="{color}"/>
        <circle cx="310" cy="240" r="28" fill="{color}"/>
        <circle cx="180" cy="260" r="32" fill="{color}"/>
        <circle cx="250" cy="270" r="26" fill="{color}"/>
        <circle cx="230" cy="230" r="24" fill="{color}"/>
        <circle cx="300" cy="300" r="22" fill="{color}"/>
        <circle cx="210" cy="310" r="27" fill="{color}"/>
        <circle cx="330" cy="190" r="20" fill="{color}"/>
    ''',
    
    "Gravel": '''
        <polygon points="200,180 180,220 220,220" fill="{color}"/>
        <polygon points="280,160 255,210 305,210" fill="{color}"/>
        <polygon points="240,230 215,280 265,280" fill="{color}"/>
        <polygon points="320,240 300,280 340,280" fill="{color}"/>
        <polygon points="180,280 160,320 200,320" fill="{color}"/>
        <polygon points="290,300 270,340 310,340" fill="{color}"/>
        <polygon points="220,320 200,360 240,360" fill="{color}"/>
    ''',
    
    "Nonmetallic minerals": '''
        <path d="M250 120 L200 200 L220 280 L280 280 L300 200 Z" fill="{color}"/>
        <path d="M180 240 L150 300 L170 360 L210 360 L230 300 Z" fill="{color}"/>
        <path d="M320 240 L290 300 L310 360 L350 360 L370 300 Z" fill="{color}"/>
        <circle cx="250" cy="200" r="15" fill="white"/>
        <circle cx="190" cy="300" r="12" fill="white"/>
        <circle cx="330" cy="300" r="12" fill="white"/>
    ''',
    
    "Metallic ores": '''
        <path d="M250 100 L180 200 L200 320 L300 320 L320 200 Z" fill="{color}"/>
        <polygon points="220,180 200,220 240,220" fill="white"/>
        <polygon points="280,200 260,240 300,240" fill="white"/>
        <polygon points="240,260 220,300 260,300" fill="white"/>
    ''',
    
    "Coal": '''
        <path d="M250 140 L200 200 L180 280 L200 340 L300 340 L320 280 L300 200 Z" fill="{color}"/>
        <path d="M230 190 L210 230 L230 270 L270 270 L290 230 L270 190 Z" fill="white"/>
        <circle cx="220" cy="310" r="12" fill="white"/>
        <circle cx="280" cy="310" r="12" fill="white"/>
    ''',
    
    "Crude petroleum": '''
        <path d="M250 120 L200 200 L180 350 Q180 380 210 380 L290 380 Q320 380 320 350 L300 200 Z" fill="{color}"/>
        <ellipse cx="250" cy="100" rx="40" ry="30" fill="{color}"/>
        <rect x="240" y="90" width="20" height="20" fill="white"/>
        <path d="M200 280 Q250 300 300 280" fill="none" stroke="white" stroke-width="10"/>
    ''',
    
    "Gasoline": '''
        <rect x="180" y="200" width="140" height="180" fill="{color}"/>
        <path d="M250 120 L200 200 L300 200 Z" fill="{color}"/>
        <circle cx="250" cy="160" r="25" fill="white"/>
        <rect x="240" y="145" width="20" height="30" fill="{color}"/>
        <rect x="210" y="250" width="80" height="100" fill="white"/>
        <circle cx="250" cy="300" r="30" fill="{color}"/>
    ''',
    
    "Fuel oils": '''
        <path d="M250 100 L180 220 L180 350 Q180 380 210 380 L290 380 Q320 380 320 350 L320 220 Z" fill="{color}"/>
        <path d="M220 240 Q250 260 280 240" fill="none" stroke="white" stroke-width="12"/>
        <path d="M220 290 Q250 310 280 290" fill="none" stroke="white" stroke-width="12"/>
        <path d="M220 340 Q250 360 280 340" fill="none" stroke="white" stroke-width="12"/>
    ''',
    
    "Natural gas and other fossil products": '''
        <path d="M250 120 L200 200 L180 320 Q180 360 220 360 L280 360 Q320 360 320 320 L300 200 Z" fill="{color}"/>
        <circle cx="250" cy="100" r="30" fill="{color}"/>
        <rect x="240" y="80" width="20" height="30" fill="white"/>
        <path d="M210 250 Q230 230 250 250 Q270 230 290 250" fill="none" stroke="white" stroke-width="10"/>
        <path d="M210 300 Q230 280 250 300 Q270 280 290 300" fill="none" stroke="white" stroke-width="10"/>
    ''',
}

def sanitize_filename(name):
    """Convert commodity name to valid filename."""
    return name.replace("/", "_").replace(" ", "_").replace(".", "")

def create_svg(name, content):
    """Create SVG file with proper structure."""
    svg_content = content.format(color=COLOR, stroke=STROKE_WIDTH)
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{SIZE}" height="{SIZE}" viewBox="0 0 {SIZE} {SIZE}" xmlns="http://www.w3.org/2000/svg">
{svg_content}
</svg>'''
    
    return svg

def main():
    # Get the script directory and navigate to Commodity_icons folder
    script_dir = Path(__file__).parent
    output_dir = script_dir.parent / "Commodity_icons"
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    print(f"Generating {len(ICONS)} commodity icons...")
    print(f"Output directory: {output_dir}")
    print(f"Color: {COLOR}")
    print(f"Size: {SIZE}x{SIZE}px\n")
    
    # Generate each icon
    for commodity_name, icon_content in ICONS.items():
        filename = sanitize_filename(commodity_name) + ".svg"
        filepath = output_dir / filename
        
        svg_content = create_svg(commodity_name, icon_content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        print(f"[OK] Created: {filename}")
    
    print(f"\n[SUCCESS] Generated {len(ICONS)} icons!")

if __name__ == "__main__":
    main()
