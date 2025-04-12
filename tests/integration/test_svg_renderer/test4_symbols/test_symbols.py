import os
import json
import pytest
from src.generators.svg_renderer import SVGRenderer
from src.parsers.asc_parser import ASCParser
from src.parsers.asy_parser import ASYParser

def find_symbol_file(symbol_name: str, schematic_dir: str) -> str:
    """Find the symbol file for a given symbol name.
    
    Args:
        symbol_name: Name of the symbol to find
        schematic_dir: Directory containing the schematic file
        
    Returns:
        Path to the symbol file
    """
    # First check in the schematic directory
    asy_file = os.path.join(schematic_dir, f"{symbol_name}.asy")
    if os.path.exists(asy_file):
        return asy_file
        
    # Then check in the LTspice symbol library
    lib_path = os.getenv('LTSPICE_LIB_PATH')
    if lib_path:
        asy_file = os.path.join(lib_path, f"{symbol_name}.asy")
        if os.path.exists(asy_file):
            return asy_file
            
    raise FileNotFoundError(f"Symbol file not found for {symbol_name}")

@pytest.fixture
def test_schematic():
    return os.path.join(os.path.dirname(__file__), "test4_symbols.asc")

@pytest.fixture
def output_dir():
    return os.path.join(os.path.dirname(__file__), "results")

def test_symbol_rendering(test_schematic, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Parse the schematic and save JSON
    parser = ASCParser(test_schematic)
    schematic = parser.parse()
    json_output = os.path.join(output_dir, "test4_symbols.json")
    parser.export_json(json_output)
    print(f"\nSaved parsed schematic data to: {json_output}")
    
    # Load symbol definitions
    schematic_dir = os.path.dirname(test_schematic)
    symbols_data = {}
    
    print("\nLoading symbol definitions:")
    for symbol in schematic['symbols']:
        symbol_name = symbol['symbol_name']
        if symbol_name not in symbols_data:
            try:
                asy_file = find_symbol_file(symbol_name, schematic_dir)
                print(f"Found symbol file for {symbol_name}: {asy_file}")
                asy_parser = ASYParser(asy_file)
                symbol_data = asy_parser.parse()
                symbols_data[symbol_name] = symbol_data
                print(f"Loaded symbol definition for {symbol_name}:")
                print(f"  - Lines: {len(symbol_data['lines'])}")
                print(f"  - Circles: {len(symbol_data['circles'])}")
                print(f"  - Rectangles: {len(symbol_data['rectangles'])}")
                print(f"  - Arcs: {len(symbol_data['arcs'])}")
                print(f"  - Windows: {len(symbol_data['windows'])}")
                print(f"  - Texts: {len(symbol_data['texts'])}")
            except FileNotFoundError as e:
                print(f"Warning: {str(e)}")
    
    # Create SVG renderer
    renderer = SVGRenderer()
    
    # Load schematic data with symbol definitions
    renderer.load_schematic(schematic, symbols_data)
    
    # Create SVG drawing
    svg_output = os.path.join(output_dir, "test4_symbols.svg")
    renderer.create_drawing(svg_output)
    
    # Render components
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
    assert schematic is not None
    assert 'symbols' in schematic
    assert len(schematic['symbols']) == 3  # We expect 3 symbols (2 NMOS and 1 voltage source)
    
    # Verify symbol types and orientations
    symbol_names = [symbol['symbol_name'] for symbol in schematic['symbols']]
    assert 'NMOS' in symbol_names
    assert 'Voltage' in symbol_names
    
    # Verify symbol orientations
    orientations = [symbol.get('rotation', 'R0') for symbol in schematic['symbols']]
    assert 'R0' in orientations  # Default orientation
    assert 'R270' in orientations  # Rotated NMOS 