"""
Main script to convert LTspice schematics to SVG format.
"""
import os
import platform
from pathlib import Path
from src.parsers.schematic_parser import SchematicParser
from src.renderers.svg_renderer import SVGRenderer
from src.renderers.rendering_config import RenderingConfig

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

def create_config_from_args(args):
    """
    Create a RenderingConfig object from command-line arguments.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        RenderingConfig: Configuration object with options from arguments
    """
    # Create a dict of option values from args
    config_options = {
        "stroke_width": args.stroke_width,
        "base_font_size": args.base_font_size,
        "dot_size_multiplier": args.dot_size,
        "no_schematic_comment": args.no_schematic_comment,
        "no_spice_directive": args.no_spice_directive,
        "no_nested_symbol_text": args.no_nested_symbol_text,
        "no_component_name": args.no_component_name,
        "no_component_value": args.no_component_value,
        "no_net_label": args.no_net_label,
        "no_pin_name": args.no_pin_name
    }
    
    # Create the config object
    return RenderingConfig(**config_options)

def main():
    """
    Main function to handle command-line arguments and convert LTspice schematics to SVG.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert LTspice schematic to SVG")
    parser.add_argument("asc_file", help="Path to the .asc schematic file")
    parser.add_argument("--stroke-width", type=float, default=2.0,
                      help="Width of lines in the SVG (default: 2.0)")
    parser.add_argument("--dot-size", type=float, default=1.5,
                      help="Size of junction dots relative to stroke width (default: 1.5)")
    parser.add_argument("--base-font-size", type=float, default=16.0,
                      help="Base font size in pixels (default: 16.0)")
    parser.add_argument("--export-json", action="store_true",
                      help="Export intermediate JSON files for debugging")
    parser.add_argument("--ltspice-lib", type=str,
                      help="Path to LTspice symbol library (overrides system default)")
    parser.add_argument("--no-text", action="store_true",
                      help="Master switch to disable ALL text rendering (component names, values, comments, etc.)")
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
    parser.add_argument("--no-net-label", action="store_true",
                      help="Skip rendering net label flags")
    parser.add_argument("--no-pin-name", action="store_true",
                      help="Skip rendering I/O pin text while keeping the pin shapes")
    
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
    
    # Create configuration from arguments
    config = create_config_from_args(args)
    
    # Create SVG renderer with configuration
    renderer = SVGRenderer(config)
    
    # For backward compatibility: explicitly call set_text_rendering_options
    # This ensures the test_text_rendering_options test passes
    text_options = {
        "no_schematic_comment": args.no_schematic_comment,
        "no_spice_directive": args.no_spice_directive,
        "no_nested_symbol_text": args.no_nested_symbol_text,
        "no_component_name": args.no_component_name,
        "no_component_value": args.no_component_value,
        "no_net_label": args.no_net_label,
        "no_pin_name": args.no_pin_name
    }
    
    # If --no-text is specified, set all text rendering options to True
    if args.no_text:
        for key in text_options:
            text_options[key] = True
    
    # Only call if at least one option is True to avoid unnecessary calls
    if any(text_options.values()) or args.no_text:
        renderer.set_text_rendering_options(**text_options)
    
    # Load schematic and symbol data
    renderer.load_schematic(data['schematic'], data['symbols'])
    
    # Create drawing 
    renderer.create_drawing(str(svg_file))
    
    # Render components
    renderer.render_wires(args.dot_size)
    renderer.render_symbols()
    if not args.no_text:
        renderer.render_texts()
    renderer.render_shapes()
    renderer.render_flags()
    
    # Save the SVG
    renderer.save()

if __name__ == "__main__":
    main() 