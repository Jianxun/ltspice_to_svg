"""
Main script to convert LTspice schematics to SVG format.
"""
import os
from pathlib import Path
from .parsers.schematic_parser import SchematicParser
from .renderers.svg_renderer import SVGRenderer

def convert_schematic(asc_file: str, 
                     stroke_width: float = 3.0, dot_size_multiplier: float = 1.5,
                     scale: float = 1.0, font_size: float = 16.0, export_json: bool = False,
                     no_text: bool = False):
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
    """
    # Get the directory and base name of the schematic file
    asc_path = Path(asc_file)
    schematic_dir = asc_path.parent
    base_name = asc_path.stem
    
    # Create output directory if exporting JSON
    if export_json:
        output_dir = schematic_dir / 'output'
        output_dir.mkdir(exist_ok=True)
    
    # Parse the schematic and symbols
    parser = SchematicParser(str(asc_path))
    data = parser.parse()
    
    # Export schematic data to JSON if requested
    if export_json:
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
    renderer.set_stroke_width(stroke_width)
    renderer.set_base_font_size(font_size)
    
    # Render components
    renderer.render_wires(dot_size_multiplier)
    renderer.render_symbols()
    if not no_text:
        renderer.render_texts()
    renderer.render_shapes()
    renderer.render_flags()
    
    # Save the SVG
    renderer.save()
    
    if no_text:
        print("Text rendering disabled")

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
    
    args = parser.parse_args()
    
    # Set LTspice library path from argument or environment variable
    if args.ltspice_lib:
        os.environ['LTSPICE_LIB_PATH'] = args.ltspice_lib
        
    convert_schematic(args.asc_file, args.stroke_width, args.dot_size, 
                     args.scale, args.font_size, args.export_json,
                     args.no_text) 