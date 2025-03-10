"""
Main script to convert LTspice schematics to SVG format.
"""
import os
import json
from pathlib import Path
from parsers.asc_parser import ASCParser
from parsers.asy_parser import ASYParser
from generators.svg_generator import SVGGenerator

def find_symbol_file(symbol_name: str, schematic_dir: Path) -> Path:
    """
    Find a symbol file by searching in the following order:
    1. Local directory (same as schematic)
    2. LTspice library directory (from LTSPICE_LIB_PATH environment variable)
    
    Args:
        symbol_name: Name of the symbol to find
        schematic_dir: Directory containing the schematic file
        
    Returns:
        Path to the symbol file if found, None otherwise
    """
    # Skip built-in symbols
    if symbol_name in SVGGenerator.BUILTIN_SYMBOLS:
        return None
        
    # First try local directory
    local_symbol = schematic_dir / f"{symbol_name}.asy"
    if local_symbol.exists():
        return local_symbol
        
    # Then try LTspice library directory
    ltspice_lib = os.environ.get('LTSPICE_LIB_PATH')
    if ltspice_lib:
        lib_symbol = Path(ltspice_lib) / f"{symbol_name}.asy"
        if lib_symbol.exists():
            return lib_symbol
            
    return None

def convert_schematic(asc_file: str, 
                     stroke_width: float = 3.0, dot_size_multiplier: float = 1.5,
                     scale: float = 1.0, font_size: float = 16.0, export_json: bool = False,
                     no_text: bool = False, no_symbol_text: bool = False):
    """
    Convert an LTspice schematic to SVG format.
    
    Args:
        asc_file: Path to the .asc schematic file
        stroke_width: Width of lines in the SVG (default: 3.0)
        dot_size_multiplier: Size of junction dots relative to stroke width (default: 1.5)
        scale: Scale factor for coordinates (default: 1.0)
        font_size: Font size in pixels (default: 16.0)
        export_json: Whether to export intermediate JSON files for debugging (default: False)
        no_text: Whether to skip rendering text elements (default: False)
        no_symbol_text: Whether to skip rendering symbol text elements (default: False)
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
        print(f"Exported schematic data to {schematic_json}")
    
    # Parse symbol files and collect their data
    symbols_data = {}
    missing_symbols = []
    symbol_cache = {}
    
    for symbol in schematic_data['symbols']:
        symbol_name = symbol['symbol_name']
        
        # Skip if we've already parsed this symbol
        if symbol_name in symbols_data:
            continue
            
        # Try to find the symbol file
        asy_file = find_symbol_file(symbol_name, schematic_dir)
        
        if asy_file:
            # Use cached data if available
            cache_key = str(asy_file)
            if cache_key in symbol_cache:
                symbol_data = symbol_cache[cache_key]
            else:
                asy_parser = ASYParser(str(asy_file))
                symbol_data = asy_parser.parse()
                symbol_cache[cache_key] = symbol_data
                
                # Export symbol data to JSON if requested
                if export_json:
                    symbol_json = output_dir / f"{symbol_name}_symbol.json"
                    asy_parser.export_json(str(symbol_json))
                    print(f"Exported symbol data for {symbol_name} to {symbol_json}")
            
            symbols_data[symbol_name] = symbol_data
        elif symbol_name not in SVGGenerator.BUILTIN_SYMBOLS:  # Only add to missing if not built-in
            missing_symbols.append(symbol_name)
    
    # Report missing symbols
    if missing_symbols:
        print("Warning: The following symbols were not found:")
        print("  Local directory:", schematic_dir)
        if os.environ.get('LTSPICE_LIB_PATH'):
            print("  LTspice library:", os.environ.get('LTSPICE_LIB_PATH'))
        else:
            print("  Note: Set LTSPICE_LIB_PATH environment variable to use LTspice standard library")
        for symbol in missing_symbols:
            print(f"  - {symbol}")
    
    # Generate SVG in the same directory as the schematic
    svg_file = schematic_dir / f"{base_name}.svg"
    
    generator = SVGGenerator(stroke_width=stroke_width, 
                           dot_size_multiplier=dot_size_multiplier, 
                           scale=scale, 
                           font_size=font_size,
                           export_json=export_json,
                           no_text=no_text,
                           no_symbol_text=no_symbol_text)
    generator.generate(schematic_data, str(svg_file), symbols_data)
    
    print(f"Generated SVG: {svg_file}")
    if no_text:
        print("Text rendering disabled")
    if no_symbol_text:
        print("Symbol text rendering disabled")

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
    parser.add_argument("--ltspice-lib", type=str,
                      help="Path to LTspice symbol library (overrides LTSPICE_LIB_PATH)")
    parser.add_argument("--no-text", action="store_true",
                      help="Skip rendering text elements")
    parser.add_argument("--no-symbol-text", action="store_true",
                      help="Skip rendering symbol text elements")
    
    args = parser.parse_args()
    
    # Set LTspice library path from argument or environment variable
    if args.ltspice_lib:
        os.environ['LTSPICE_LIB_PATH'] = args.ltspice_lib
        
    convert_schematic(args.asc_file, args.stroke_width, args.dot_size, 
                     args.scale, args.font_size, args.export_json,
                     args.no_text, args.no_symbol_text) 