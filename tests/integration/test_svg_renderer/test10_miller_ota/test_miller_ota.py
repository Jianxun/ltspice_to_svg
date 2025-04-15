import os
import pytest
import logging
from src.generators.svg_renderer import SVGRenderer
from src.parsers.schematic_parser import SchematicParser

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture(autouse=True)
def setup_ltspice_lib():
    """Set up the LTspice library path environment variable."""
    os.environ['LTSPICE_LIB_PATH'] = f"/Users/{os.getenv('USER')}/Library/Application Support/LTspice/lib/sym"

@pytest.fixture
def test_schematic():
    """Get the path to the test schematic file."""
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))), "schematics", "miller_ota.asc")

@pytest.fixture
def output_dir():
    return os.path.join(os.path.dirname(__file__), "results")

def test_miller_ota(test_schematic, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Parse the schematic and symbols
    parser = SchematicParser(test_schematic)
    data = parser.parse()
    
    # Save JSON output
    json_output = os.path.join(output_dir, "test10_miller_ota.json")
    parser.export_json(json_output)
    print(f"\nSaved parsed schematic data to: {json_output}")
    
    # Print symbol information
    print("\nLoaded symbol definitions:")
    for symbol_name, symbol_data in data['symbols'].items():
        print(f"Symbol: {symbol_name}")
        print(f"  - Lines: {len(symbol_data['lines'])}")
        print(f"  - Circles: {len(symbol_data['circles'])}")
        print(f"  - Rectangles: {len(symbol_data['rectangles'])}")
        print(f"  - Arcs: {len(symbol_data['arcs'])}")
        print(f"  - Windows: {len(symbol_data['windows'])}")
        print(f"  - Texts: {len(symbol_data['texts'])}")
    
    # Create SVG renderer with custom parameters
    renderer = SVGRenderer()
    
    # Load schematic data with symbol definitions
    renderer.load_schematic(data['schematic'], data['symbols'])
    
    # Experiment with different stroke widths and font sizes
    # Try different combinations to find the optimal values
    stroke_widths = [1.0, 2.0, 3.0]
    font_sizes = [16.0, 20.0, 24.0]
    
    for stroke_width in stroke_widths:
        for font_size in font_sizes:
            # Create a new SVG file for each combination
            variant_svg = os.path.join(output_dir, f"test10_miller_ota_sw{stroke_width}_fs{font_size}.svg")
            
            # Create and save SVG with current parameters
            renderer.create_drawing(variant_svg)
            renderer.set_stroke_width(stroke_width)
            renderer.set_base_font_size(font_size)
            renderer.render_wires()
            renderer.render_symbols()
            renderer.render_texts()
            renderer.render_shapes()
            renderer.render_flags()  # Add flag rendering
            renderer.save()
            
            print(f"\nGenerated SVG with stroke_width={stroke_width}, font_size={font_size}")
            print(f"Saved to: {variant_svg}")
    
    # Create default SVG
    svg_output = os.path.join(output_dir, "test10_miller_ota.svg")
    renderer.create_drawing(svg_output)
    renderer.set_stroke_width(1.0)  # Default stroke width
    renderer.set_base_font_size(16.0)  # Default font size
    renderer.render_wires()
    renderer.render_symbols()
    renderer.render_texts()
    renderer.render_shapes()
    renderer.render_flags()  # Add flag rendering
    renderer.save()
    
    # Print debug information about window overrides
    for symbol in data['schematic']['symbols']:
        if 'window_overrides' in symbol:
            print(f"\nSymbol {symbol['instance_name']} has window overrides:")
            for window_id, override in symbol['window_overrides'].items():
                print(f"  Window {window_id}:")
                print(f"    x: {override['x']}")
                print(f"    y: {override['y']}")
                print(f"    justification: {override['justification']}")
                print(f"    size_multiplier: {override['size_multiplier']}") 