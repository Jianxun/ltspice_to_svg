import os
import pytest
import logging
from src.renderers.svg_renderer import SVGRenderer
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
    return os.path.join(os.path.dirname(__file__), "test_symbol_window_texts.asc")

@pytest.fixture
def output_dir():
    return os.path.join(os.path.dirname(__file__), "results")

def test_symbol_window_texts(test_schematic, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Parse the schematic and symbols
    parser = SchematicParser(test_schematic)
    data = parser.parse()
    
    # Save JSON output
    json_output = os.path.join(output_dir, "test6_symbol_window_texts.json")
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
    
    # Create SVG with custom parameters
    svg_output = os.path.join(output_dir, "test6_symbol_window_texts.svg")
    renderer.create_drawing(svg_output)
    renderer.set_stroke_width(2.0)  # Custom stroke width
    renderer.set_base_font_size(20.0)  # Custom font size
    renderer.render_wires()
    renderer.render_symbols()
    renderer.render_texts()
    renderer.render_shapes()
    renderer.save()
    
    # Verify the output files exist
    assert os.path.exists(svg_output)
    assert os.path.exists(json_output)
    
    # Read the SVG output to verify window text overrides
    with open(svg_output, 'r') as f:
        svg_content = f.read()
    
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
    
    # ASSERTIONS
    # Verify the SVG content for window text overrides
    
    # 1. Find the V2 symbol with rotated text
    assert 'transform="translate(240,320) rotate(90)"' in svg_content, "V2 symbol should be rotated 90 degrees"
    
    # 2. Verify the V2 text has correct transform (rotation and position)
    assert 'transform="rotate(-90, -32, 56)"' in svg_content, "V2 text should have counter-rotation transform"
    
    # 3. Verify the V2 text is positioned and formatted correctly
    assert 'text-anchor="middle"' in svg_content, "V2 text should have 'middle' anchor for VBottom justification"
    
    # 4. Verify the V1 text (without override) is positioned correctly
    assert 'text-anchor="start"' in svg_content, "V1 text should have 'start' anchor for Left justification"
    
    # 5. Verify the 12mV text is positioned and formatted correctly
    assert 'transform="rotate(-90, 32, 56)"' in svg_content, "12mV text should have counter-rotation transform"
    assert 'text-anchor="middle"' in svg_content, "12mV text should have 'middle' anchor for VTop justification" 