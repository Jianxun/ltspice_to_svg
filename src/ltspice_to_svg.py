"""
Main script to convert LTspice schematics to SVG format.
"""
import os
import json
from pathlib import Path
from parsers.asc_parser import ASCParser
from parsers.asy_parser import ASYParser
from generators.svg_generator import SVGGenerator

def convert_schematic(asc_file: str, 
                     stroke_width: float = 3.0, dot_size_multiplier: float = 1.5,
                     scale: float = 1.0, font_size: float = 16.0, export_json: bool = False):
    """
    Convert an LTspice schematic to SVG format.
    
    Args:
        asc_file: Path to the .asc schematic file
        stroke_width: Width of lines in the SVG (default: 3.0)
        dot_size_multiplier: Size of junction dots relative to stroke width (default: 1.5)
        scale: Scale factor for coordinates (default: 1.0)
        font_size: Font size in pixels (default: 16.0)
        export_json: Whether to export intermediate JSON files for debugging (default: False)
    """
    # Get the directory and base name of the schematic file
    asc_path = Path(asc_file)
    schematic_dir = asc_path.parent
    base_name = asc_path.stem
    
    # Create output directory if exporting JSON
    if export_json:
        output_dir = schematic_dir / 'output'
        output_dir.mkdir(exist_ok=True)
    
    # Parse the schematic file
    asc_parser = ASCParser(str(asc_path))
    schematic_data = asc_parser.parse()
    
    # Export schematic data to JSON if requested
    if export_json:
        schematic_json = output_dir / f"{base_name}_schematic.json"
        asc_parser.export_json(str(schematic_json))
    
    # Parse symbol files and collect their data
    symbols_data = {}
    for symbol in schematic_data['symbols']:
        symbol_name = symbol['name']
        asy_file = schematic_dir / f"{symbol_name}.asy"
        
        if asy_file.exists():
            asy_parser = ASYParser(str(asy_file))
            symbol_data = asy_parser.parse()
            symbols_data[symbol_name] = symbol_data
            
            # Export symbol data to JSON if requested
            if export_json:
                symbol_json = output_dir / f"{symbol_name}_symbol.json"
                asy_parser.export_json(str(symbol_json))
        else:
            print(f"Warning: Symbol file not found: {asy_file}")
    
    # Generate SVG in the same directory as the schematic
    svg_file = schematic_dir / f"{base_name}.svg"
    generator = SVGGenerator(stroke_width=stroke_width, 
                           dot_size_multiplier=dot_size_multiplier,
                           scale=scale,
                           font_size=font_size)
    generator.generate(schematic_data, str(svg_file), symbols_data)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert LTspice schematic to SVG")
    parser.add_argument("asc_file", help="Path to the .asc schematic file")
    parser.add_argument("--stroke-width", type=float, default=3.0,
                      help="Width of lines in the SVG (default: 3.0)")
    parser.add_argument("--dot-size", type=float, default=1.5,
                      help="Size of junction dots relative to stroke width (default: 1.5)")
    parser.add_argument("--scale", type=float, default=1,
                      help="Scale factor for coordinates (default: 1.0)")
    parser.add_argument("--font-size", type=float, default=16.0,
                      help="Font size in pixels (default: 16.0)")
    parser.add_argument("--export-json", action="store_true",
                      help="Export intermediate JSON files for debugging")
    
    args = parser.parse_args()
    convert_schematic(args.asc_file, args.stroke_width, args.dot_size, 
                     args.scale, args.font_size, args.export_json) 