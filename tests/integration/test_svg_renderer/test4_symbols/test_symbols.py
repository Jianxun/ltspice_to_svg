import os
import pytest
import logging
from src.renderers.svg_renderer import SVGRenderer
from src.parsers.schematic_parser import SchematicParser

@pytest.fixture(autouse=True)
def setup_ltspice_lib():
    """Set up the LTspice library path environment variable."""
    os.environ['LTSPICE_LIB_PATH'] = f"/Users/{os.getenv('USER')}/Library/Application Support/LTspice/lib/sym"

@pytest.fixture
def test_schematic():
    return os.path.join(os.path.dirname(__file__), "test_symbols.asc")

@pytest.fixture
def output_dir():
    return os.path.join(os.path.dirname(__file__), "results")

def test_symbol_rendering(test_schematic, output_dir):
    """Test comprehensive symbol rendering with all 8 possible orientations.
    
    This test verifies that symbols render correctly with:
    - Regular orientations: R0, R90, R180, R270
    - Mirrored orientations: M0, M90, M180, M270
    
    Contains 10 symbols total: 8 NMOS (one for each orientation) + 2 Voltage sources.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Parse the schematic and symbols
    parser = SchematicParser(test_schematic)
    data = parser.parse()
    
    # Save JSON output
    json_output = os.path.join(output_dir, "test4_symbols.json")
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
    svg_output = os.path.join(output_dir, "test4_symbols.svg")
    renderer.create_drawing(svg_output)
    
    # Set stroke width and render components
    renderer.set_stroke_width(2.0)
    renderer.render_wires()
    renderer.render_symbols()
    renderer.render_texts()
    renderer.render_shapes()
    
    # Save the SVG
    renderer.save()
    
    # Verify the output files exist
    assert os.path.exists(svg_output)
    assert os.path.exists(json_output)
    
    # Verify the schematic data
    schematic = data['schematic']
    assert schematic is not None
    assert 'symbols' in schematic
    assert len(schematic['symbols']) == 10  # We expect 10 symbols (8 NMOS and 2 voltage sources)
    
    # Verify symbol types and orientations
    symbol_names = [symbol['symbol_name'] for symbol in schematic['symbols']]
    assert 'NMOS' in symbol_names
    assert 'Voltage' in symbol_names
    
    # Count symbol types
    nmos_count = sum(1 for name in symbol_names if name == 'NMOS')
    voltage_count = sum(1 for name in symbol_names if name == 'Voltage')
    assert nmos_count == 8, f"Expected 8 NMOS symbols, found {nmos_count}"
    assert voltage_count == 2, f"Expected 2 Voltage symbols, found {voltage_count}"
    
    # Verify all 8 orientations are present (comprehensive orientation test)
    orientations = [symbol.get('rotation', 'R0') for symbol in schematic['symbols']]
    expected_orientations = ['R0', 'R90', 'R180', 'R270', 'M0', 'M90', 'M180', 'M270']
    for expected_orientation in expected_orientations:
        assert expected_orientation in orientations, f"Missing orientation: {expected_orientation}"
    
    # Verify symbol elements
    voltage_symbol = data['symbols']['Voltage']
    assert len(voltage_symbol['lines']) == 5, "Voltage source should have 5 lines"
    assert len(voltage_symbol['circles']) == 1, "Voltage source should have 1 circle"
    assert len(voltage_symbol['rectangles']) == 0, "Voltage source should have no rectangles"
    assert len(voltage_symbol['arcs']) == 0, "Voltage source should have no arcs"
    
    nmos_symbol = data['symbols']['NMOS']
    assert len(nmos_symbol['lines']) == 14, "NMOS should have 14 lines"
    assert len(nmos_symbol['circles']) == 0, "NMOS should have no circles"
    assert len(nmos_symbol['rectangles']) == 0, "NMOS should have no rectangles"
    assert len(nmos_symbol['arcs']) == 0, "NMOS should have no arcs" 