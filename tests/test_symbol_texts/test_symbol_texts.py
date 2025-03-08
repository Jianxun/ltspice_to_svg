"""
Tests for symbol text rendering in SVG output.
Tests:
- Instance names (SYMATTR InstName)
- Symbol values (SYMATTR Value)
- Symbol-specific texts with proper font sizes
"""
import os
from pathlib import Path
from src.parsers.asc_parser import ASCParser
from src.parsers.asy_parser import ASYParser
from src.generators.svg_generator import SVGGenerator

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

def test_symbol_text_parsing():
    """Test parsing of symbol text attributes."""
    # Parse schematic
    asc_file = PROJECT_ROOT / 'tests' / 'test_symbol_texts' / 'test_symbol_texts.asc'
    asc_parser = ASCParser(str(asc_file))
    schematic_data = asc_parser.parse()
    
    # Verify symbols are parsed
    symbols = schematic_data['symbols']
    assert len(symbols) == 4  # C1, R1, X9, GND
    
    # Group symbols by type
    capacitors = [s for s in symbols if s['symbol_name'] == 'cap']
    resistors = [s for s in symbols if s['symbol_name'] == 'Res']
    mosfets = [s for s in symbols if s['symbol_name'] == 'CS_nMOS']
    grounds = [s for s in symbols if s['symbol_name'] == 'GND']
    
    # Verify symbol counts
    assert len(capacitors) == 1  # One capacitor
    assert len(resistors) == 1  # One resistor
    assert len(mosfets) == 1  # One MOSFET
    assert len(grounds) == 1  # One ground symbol
    
    # Verify capacitor text attributes
    c1 = capacitors[0]
    assert c1['instance_name'] == 'C1'
    
    # Verify resistor text attributes
    r1 = resistors[0]
    assert r1['instance_name'] == 'R1'
    
    # Verify MOSFET text attributes
    x9 = mosfets[0]
    assert x9['instance_name'] == 'X9'
    
    # Verify ground symbol
    gnd = grounds[0]
    assert gnd['instance_name'] == 'GND'
    
    # Parse symbol files to verify text elements
    test_dir = PROJECT_ROOT / 'tests' / 'test_symbol_texts'
    
    # Parse CS_nMOS symbol
    cs_nmos_parser = ASYParser(str(test_dir / 'CS_nMOS.asy'))
    cs_nmos_data = cs_nmos_parser.parse()
    
    # Verify CS_nMOS texts
    cs_nmos_texts = cs_nmos_data['texts']
    assert len(cs_nmos_texts) == 3  # "4x", "28", "29"
    
    # Find "4x" text
    size_text = next(t for t in cs_nmos_texts if t['text'] == '4x')
    assert size_text['size_multiplier'] == 1  # Size 1 font
    assert size_text['justification'] == 'Left'
    
    # Find node number texts
    node_28 = next(t for t in cs_nmos_texts if t['text'] == '28')
    assert node_28['size_multiplier'] == 0  # Size 0 font
    assert node_28['justification'] == 'Center'
    
    node_29 = next(t for t in cs_nmos_texts if t['text'] == '29')
    assert node_29['size_multiplier'] == 0  # Size 0 font
    assert node_29['justification'] == 'Center'

def test_svg_text_rendering():
    """Test SVG generation with proper text rendering."""
    # Get test case directory
    test_dir = PROJECT_ROOT / 'tests' / 'test_symbol_texts'
    asc_file = test_dir / 'test_symbol_texts.asc'
    
    # Parse schematic
    asc_parser = ASCParser(str(asc_file))
    schematic_data = asc_parser.parse()
    
    # Save parsed data as JSON for reference
    json_file = test_dir / 'test_symbol_texts_parsed.json'
    asc_parser.export_json(str(json_file))
    print(f"Exported parsed data to {json_file}")
    
    # Generate SVG
    svg_file = test_dir / 'test_symbol_texts.svg'
    
    # Set up symbol paths
    ltspice_lib_path = os.getenv('LTSPICE_LIB_PATH')
    assert ltspice_lib_path is not None, "LTSPICE_LIB_PATH environment variable not set"
    
    # Parse symbol files
    symbol_paths = {
        'cap': str(test_dir / 'cap.asy'),
        'Res': str(test_dir / 'res.asy'),
        'CS_nMOS': str(test_dir / 'CS_nMOS.asy')
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
    
    # Verify instance names are rendered
    assert '>C1<' in svg_content  # Capacitor instance name
    assert '>R1<' in svg_content  # Resistor instance name
    assert '>X9<' in svg_content  # MOSFET instance name
    assert '>GND<' in svg_content  # Ground symbol label
    
    # Verify symbol-specific texts from CS_nMOS
    assert '>4x<' in svg_content  # Size multiplier text
    assert '>28<' in svg_content  # Node number
    assert '>29<' in svg_content  # Node number
    
    # Verify text attributes
    assert 'font-size="24.0px"' in svg_content  # Size 2 (1.5x) for instance names
    assert 'font-size="10.0px"' in svg_content  # Size 0 (0.625x) for node numbers
    assert 'font-size="16.0px"' in svg_content  # Size 1 (1.0x) for "4x" text 