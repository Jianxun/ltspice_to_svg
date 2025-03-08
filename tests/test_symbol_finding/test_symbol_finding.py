"""
Tests for finding and loading schematic symbols.
Tests:
- Finding symbols in LTspice library (voltage source)
- Finding symbols in local paths (resistor)
- Pin symbols with different orientations
"""
import os
from pathlib import Path
from src.parsers.asc_parser import ASCParser
from src.parsers.asy_parser import ASYParser
from src.generators.svg_generator import SVGGenerator

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

def test_symbol_finding():
    """Test finding and loading symbols from different locations."""
    # Parse schematic
    asc_file = PROJECT_ROOT / 'tests' / 'test_symbol_finding' / 'test_symbol_finding.asc'
    asc_parser = ASCParser(str(asc_file))
    schematic_data = asc_parser.parse()
    
    # Verify symbols are parsed
    symbols = schematic_data['symbols']
    assert len(symbols) == 11  # Total number of symbols (V1, R1, X1-X8, GND)
    
    # Group symbols by type
    voltage_sources = [s for s in symbols if s['symbol_name'] == 'Voltage']
    resistors = [s for s in symbols if s['symbol_name'] == 'Res']
    pins = [s for s in symbols if s['symbol_name'] == 'pin']
    grounds = [s for s in symbols if s['symbol_name'] == 'GND']
    
    # Verify symbol counts
    assert len(voltage_sources) == 1  # One voltage source
    assert len(resistors) == 1  # One resistor
    assert len(pins) == 8  # Eight pins
    assert len(grounds) == 1  # One ground symbol
    
    # Verify voltage source (from LTspice library)
    v1 = voltage_sources[0]
    assert v1['instance_name'] == 'V1'
    assert v1['rotation'] == 'R0'
    
    # Verify resistor (from local path)
    r1 = resistors[0]
    assert r1['instance_name'] == 'R1'
    assert r1['rotation'] == 'R0'
    
    # Verify ground symbol
    gnd = grounds[0]
    assert gnd['instance_name'] == 'GND'
    assert gnd['rotation'] == 'R0'
    
    # Verify pins with different orientations
    pin_configs = {
        'X1': {'rotation': 'M180'},  # Mirror + 180 degrees
        'X2': {'rotation': 'R180'},  # 180 degrees
        'X3': {'rotation': 'R270'},  # 270 degrees
        'X4': {'rotation': 'R90'},   # 90 degrees
        'X5': {'rotation': 'R0'},    # No rotation
        'X6': {'rotation': 'M270'},  # Mirror + 270 degrees
        'X7': {'rotation': 'M90'},   # Mirror + 90 degrees
        'X8': {'rotation': 'M0'}     # Mirror only
    }
    
    for pin in pins:
        inst_name = pin['instance_name']
        assert inst_name in pin_configs, f"Unexpected pin instance name: {inst_name}"
        config = pin_configs[inst_name]
        assert pin['rotation'] == config['rotation'], f"Wrong rotation for {inst_name}"

def test_svg_generation():
    """Test SVG generation with found symbols."""
    # Get test case directory
    test_dir = PROJECT_ROOT / 'tests' / 'test_symbol_finding'
    asc_file = test_dir / 'test_symbol_finding.asc'
    
    # Parse schematic
    asc_parser = ASCParser(str(asc_file))
    schematic_data = asc_parser.parse()
    
    # Save parsed data as JSON for reference
    json_file = test_dir / 'test_symbol_finding_parsed.json'
    asc_parser.export_json(str(json_file))
    print(f"Exported parsed data to {json_file}")
    
    # Generate SVG
    svg_file = test_dir / 'test_symbol_finding.svg'
    
    # Set up symbol paths
    ltspice_lib_path = os.getenv('LTSPICE_LIB_PATH')
    assert ltspice_lib_path is not None, "LTSPICE_LIB_PATH environment variable not set"
    
    # Parse symbol files
    symbol_paths = {
        'Voltage': str(Path(ltspice_lib_path) / 'voltage.asy'),
        'Res': str(test_dir / 'res.asy'),
        'pin': str(test_dir / 'pin.asy')
        # GND symbol is hard-coded in the SVG generator
    }
    
    # Verify symbol files exist
    for symbol_type, path in symbol_paths.items():
        assert Path(path).exists(), f"Symbol file not found: {path}"
    
    # Parse symbol files
    symbol_data = {}
    for symbol_type, path in symbol_paths.items():
        parser = ASYParser(path)
        symbol_data[symbol_type] = parser.parse()
    
    # Generate SVG
    generator = SVGGenerator(stroke_width=3.0, dot_size_multiplier=1.5, scale=1.0, font_size=16.0)
    generator.generate(schematic_data, str(svg_file), symbol_data)
    print(f"Generated SVG: {svg_file}")
    
    # Verify SVG file is created
    assert svg_file.exists()
    assert svg_file.stat().st_size > 0
    
    # Read SVG file to verify content
    with open(svg_file, 'r') as f:
        svg_content = f.read()
    
    # Verify basic SVG structure
    assert '<?xml version="1.0" encoding="utf-8" ?>' in svg_content
    assert '<svg' in svg_content
    assert 'viewBox' in svg_content
    
    # Verify wire connections and basic styling
    assert '<line' in svg_content  # Should have line elements for wires
    assert 'stroke="black"' in svg_content  # Lines should be black
    assert 'stroke-linecap="round"' in svg_content  # Lines should have round caps 