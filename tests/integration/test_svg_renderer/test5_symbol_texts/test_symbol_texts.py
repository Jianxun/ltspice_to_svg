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
    return os.path.join(os.path.dirname(__file__), "test5_symbol_texts.asc")

@pytest.fixture
def output_dir():
    return os.path.join(os.path.dirname(__file__), "results")

def test_symbol_texts(test_schematic, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Parse the schematic and symbols
    parser = SchematicParser(test_schematic)
    data = parser.parse()
    
    # Save JSON output
    json_output = os.path.join(output_dir, "test5_symbol_texts.json")
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
    
    # Create SVG renderer
    renderer = SVGRenderer()
    
    # Load schematic data with symbol definitions
    renderer.load_schematic(data['schematic'], data['symbols'])
    
    # Create SVG drawing
    svg_output = os.path.join(output_dir, "test5_symbol_texts.svg")
    renderer.create_drawing(svg_output)
    
    # Render components with increased stroke width
    renderer.render_wires(stroke_width=2.0)
    renderer.render_symbols(stroke_width=2.0)
    renderer.render_texts()
    renderer.render_shapes(stroke_width=2.0)
    
    # Save the SVG
    renderer.save()
    
    # Verify the output files exist
    assert os.path.exists(svg_output)
    assert os.path.exists(json_output)
    
    # Verify the schematic data
    schematic = data['schematic']
    assert schematic is not None
    assert 'symbols' in schematic
    assert len(schematic['symbols']) == 5  # We expect 5 symbols (3 NMOS and 2 voltage sources)
    
    # Verify symbol types and orientations
    symbol_names = [symbol['symbol_name'] for symbol in schematic['symbols']]
    assert 'NMOS' in symbol_names
    assert 'Voltage' in symbol_names
    assert symbol_names.count('NMOS') == 3  # Should have 3 NMOS symbols
    assert symbol_names.count('Voltage') == 2  # Should have 2 Voltage symbols
    
    # Verify symbol orientations
    orientations = [symbol.get('rotation', 'R0') for symbol in schematic['symbols']]
    assert 'R0' in orientations  # Default orientation
    assert 'R270' in orientations  # Rotated NMOS
    assert 'M0' in orientations  # Mirrored NMOS
    
    # Verify symbol texts
    nmos_symbol = data['symbols']['NMOS']
    assert len(nmos_symbol['texts']) >= 3, "NMOS should have at least 3 text elements (G, S, D)"
    
    # Verify text content
    text_contents = [text['text'] for text in nmos_symbol['texts']]
    assert 'G' in text_contents, "NMOS should have gate pin label"
    assert 'S' in text_contents, "NMOS should have source pin label"
    assert 'D' in text_contents, "NMOS should have drain pin label"
    
    # Verify text positions and properties
    for text in nmos_symbol['texts']:
        assert 'x' in text, "Text should have x coordinate"
        assert 'y' in text, "Text should have y coordinate"
        assert 'justification' in text, "Text should have justification"
        assert 'size_multiplier' in text, "Text should have size multiplier"
        assert 'text' in text, "Text should have content"
    
    # Read the SVG output to verify text rendering
    with open(svg_output, 'r') as f:
        svg_content = f.read()
    
    # Verify text elements are present in the SVG
    assert '<text' in svg_content, "SVG should contain text elements"
    
    # Verify text content is present
    for text in nmos_symbol['texts']:
        assert text['text'] in svg_content, f"SVG should contain text '{text['text']}'"
    
    # Verify text transformations for mirrored symbol
    mirrored_symbol = next(symbol for symbol in schematic['symbols'] if symbol.get('rotation', 'R0') == 'M0')
    assert mirrored_symbol is not None, "Should find mirrored NMOS symbol"
    
    # The text elements should be rendered with the correct transformations
    # We can't easily parse the SVG to verify exact positions, but we can check
    # that the text elements are present and the transformations are applied
    assert 'scale(-1,1)' in svg_content, "SVG should contain mirroring transformation" 