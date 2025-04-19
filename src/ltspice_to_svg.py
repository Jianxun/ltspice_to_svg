"""
Main script to convert LTspice schematics to SVG format.
"""
import os
import platform
import warnings
from pathlib import Path
from .parsers.schematic_parser import SchematicParser
from .renderers.svg_renderer import SVGRenderer

def get_ltspice_lib_path() -> str:
    """
    Find the LTspice library path based on the operating system.
    
    Returns:
        str: Path to the LTspice symbol library
    """
    system = platform.system()
    username = os.getenv('USERNAME') or os.getenv('USER')
    
    if system == 'Darwin':  # macOS
        return f"/Users/{username}/Library/Application Support/LTspice/lib/sym"
    elif system == 'Windows':
        return f"C:\\Users\\{username}\\AppData\\Local\\LTspice\\lib\\sym"
    else:
        raise OSError(f"Unsupported operating system: {system}")

def main():
    """
    Main function to handle command-line arguments and convert LTspice schematics to SVG.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert LTspice schematic to SVG")
    parser.add_argument("asc_file", help="Path to the .asc schematic file")
    parser.add_argument("--stroke-width", type=float, default=3.0,
                      help="Width of lines in the SVG (default: 3.0)")
    parser.add_argument("--dot-size", type=float, default=1.5,
                      help="Size of junction dots relative to stroke width (default: 1.5)")
    parser.add_argument("--scale", type=float, default=1.0,
                      help="Scale factor for coordinates (default: 1.0) - DEPRECATED")
    parser.add_argument("--base-font-size", type=float, default=16.0,
                      help="Base font size in pixels (default: 16.0)")
    parser.add_argument("--export-json", action="store_true",
                      help="Export intermediate JSON files for debugging")
    parser.add_argument("--ltspice-lib", type=str,
                      help="Path to LTspice symbol library (overrides system default)")
    parser.add_argument("--no-text", action="store_true",
                      help="Skip rendering all text elements")
    parser.add_argument("--no-schematic-comment", action="store_true",
                      help="Skip rendering schematic comments")
    parser.add_argument("--no-spice-directive", action="store_true",
                      help="Skip rendering SPICE directives")
    parser.add_argument("--no-nested-symbol-text", action="store_true",
                      help="Skip rendering nested symbol text")
    parser.add_argument("--no-component-name", action="store_true",
                      help="Skip rendering component names")
    parser.add_argument("--no-component-value", action="store_true",
                      help="Skip rendering component values")
    
    args = parser.parse_args()
    
    # Get the directory and base name of the schematic file
    asc_path = Path(args.asc_file)
    schematic_dir = asc_path.parent
    base_name = asc_path.stem
    
    # Create output directory if exporting JSON
    if args.export_json:
        output_dir = schematic_dir / 'output'
        output_dir.mkdir(exist_ok=True)
    
    # Set LTspice library path
    if args.ltspice_lib:
        os.environ['LTSPICE_LIB_PATH'] = args.ltspice_lib
    elif 'LTSPICE_LIB_PATH' not in os.environ:
        os.environ['LTSPICE_LIB_PATH'] = get_ltspice_lib_path()
    
    # Parse the schematic and symbols
    parser = SchematicParser(str(asc_path))
    data = parser.parse()
    
    # Export schematic data to JSON if requested
    if args.export_json:
        json_output = output_dir / f"{base_name}_schematic.json"
        parser.export_json(str(json_output))
        print(f"Exported schematic data to {json_output}")
    
    # Generate SVG in the same directory as the schematic
    svg_file = schematic_dir / f"{base_name}.svg"
    
    # Create SVG renderer with custom parameters
    renderer = SVGRenderer()
    
    # Load schematic and symbol data
    renderer.load_schematic(data['schematic'], data['symbols'])
    
    # Create drawing and set parameters
    renderer.create_drawing(str(svg_file))
    renderer.set_stroke_width(args.stroke_width)
    renderer.set_base_font_size(args.base_font_size)
    
    # Set text rendering options
    renderer.no_schematic_comment = args.no_schematic_comment
    renderer.no_spice_directive = args.no_spice_directive
    renderer.no_nested_symbol_text = args.no_nested_symbol_text
    renderer.no_component_name = args.no_component_name
    renderer.no_component_value = args.no_component_value
    
    # Render components
    renderer.render_wires(args.dot_size)
    renderer.render_symbols()
    if not args.no_text:
        renderer.render_texts()
    renderer.render_shapes()
    renderer.render_flags()
    
    # Save the SVG
    renderer.save()
    
    # Print warnings for deprecated parameters
    if args.scale != 1.0:
        warnings.warn(
            "The 'scale' parameter is deprecated and will be removed in a future version. "
            "Use SVG viewBox or CSS transforms for scaling instead.",
            DeprecationWarning
        )

if __name__ == "__main__":
    main() 