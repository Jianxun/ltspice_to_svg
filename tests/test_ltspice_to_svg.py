"""
Tests for the LTspice to SVG converter.
"""
import os
import json
from pathlib import Path
from src.parsers.asc_parser import ASCParser
from src.parsers.asy_parser import ASYParser
from src.generators.svg_generator import SVGGenerator

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent

def test_asc_parser():
    """Test ASC parser with miller_ota.asc file."""
    asc_file = PROJECT_ROOT / 'schematics' / 'miller_ota.asc'
    parser = ASCParser(str(asc_file))
    data = parser.parse()
    
    # Verify wires are parsed
    assert len(data['wires']) > 0
    wire = data['wires'][0]
    assert all(k in wire for k in ['x1', 'y1', 'x2', 'y2'])
    
    # Verify symbols are parsed
    assert len(data['symbols']) > 0
    symbol = data['symbols'][0]
    assert all(k in symbol for k in ['symbol_name', 'instance_name', 'x', 'y', 'rotation'])
    
    # Verify texts are parsed
    assert 'texts' in data
    if len(data['texts']) > 0:  # Only test if text elements exist
        text = data['texts'][0]
        assert all(k in text for k in ['x', 'y', 'justification', 'text'])
        
    # Verify flags are parsed
    assert 'flags' in data
    if len(data['flags']) > 0:  # Only test if flag elements exist
        flag = data['flags'][0]
        assert all(k in flag for k in ['x', 'y', 'net_name'])

def test_flag_parsing():
    """Test FLAG line parsing with a test schematic."""
    # Create a temporary test file
    test_file = PROJECT_ROOT / 'tests' / 'test_flags.asc'
    test_file.parent.mkdir(exist_ok=True)
    
    try:
        # Write test content
        with open(test_file, 'w') as f:
            f.write("Version 4\n")
            f.write("SHEET 1 1208 692\n")
            f.write("FLAG 100 200 Vout\n")
            f.write("FLAG 300 400 GND\n")
            f.write("FLAG 500 600 Vin with spaces\n")
        
        # Parse the test file
        parser = ASCParser(str(test_file))
        data = parser.parse()
        
        # Verify flags are parsed correctly
        assert 'flags' in data
        assert len(data['flags']) == 3
        
        # Check first flag
        flag1 = data['flags'][0]
        assert flag1['x'] == 100
        assert flag1['y'] == 200
        assert flag1['net_name'] == 'Vout'
        
        # Check second flag
        flag2 = data['flags'][1]
        assert flag2['x'] == 300
        assert flag2['y'] == 400
        assert flag2['net_name'] == 'GND'
        
        # Check third flag (with spaces in net name)
        flag3 = data['flags'][2]
        assert flag3['x'] == 500
        assert flag3['y'] == 600
        assert flag3['net_name'] == 'Vin with spaces'
        
    finally:
        # Clean up test file
        if test_file.exists():
            test_file.unlink()

def test_asy_parser():
    """Test ASY parser with pin.asy file."""
    asy_file = PROJECT_ROOT / 'schematics' / 'pin.asy'
    parser = ASYParser(str(asy_file))
    data = parser.parse()
    
    # Verify lines are parsed
    assert len(data['lines']) > 0
    line = data['lines'][0]
    assert all(k in line for k in ['x1', 'y1', 'x2', 'y2'])
    
    # Verify circles are parsed if they exist
    if len(data.get('circles', [])) > 0:
        circle = data['circles'][0]
        assert all(k in circle for k in ['x1', 'y1', 'x2', 'y2'])

def test_svg_generator():
    """Test SVG generation with parsed data."""
    # Parse schematic
    asc_file = PROJECT_ROOT / 'schematics' / 'miller_ota.asc'
    asc_parser = ASCParser(str(asc_file))
    schematic_data = asc_parser.parse()
    
    # Parse symbols
    symbols_data = {}
    for symbol in schematic_data['symbols']:
        symbol_name = symbol['symbol_name']
        asy_file = PROJECT_ROOT / 'schematics' / f'{symbol_name}.asy'
        if asy_file.exists():
            asy_parser = ASYParser(str(asy_file))
            symbols_data[symbol_name] = asy_parser.parse()
    
    # Generate SVG in the same directory as the schematic
    svg_file = asc_file.with_suffix('.svg')
    
    stroke_width = 3.0
    dot_size_multiplier = 1.5
    scale = 1.0
    font_size = 16.0

    generator = SVGGenerator(stroke_width=stroke_width, 
                           dot_size_multiplier=dot_size_multiplier, 
                           scale=scale, 
                           font_size=font_size)
    generator.generate(schematic_data, str(svg_file), symbols_data)
    
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
    
    # Verify text elements if they exist
    if schematic_data.get('texts'):
        text = schematic_data['texts'][0]
        # Check text attributes
        assert all(k in text for k in ['x', 'y', 'justification', 'text'])
        
        # Check horizontal alignment
        if text['justification'] in ['Left', 'Center', 'Right']:
            text_anchor = {
                'Left': 'start',
                'Center': 'middle',
                'Right': 'end'
            }[text['justification']]
            assert f'text-anchor="{text_anchor}"' in svg_content
            
        # Check font size
        font_size = text.get('size', font_size)  # Use text size if provided
        scaled_font_size = font_size * scale
        assert f'font-size="{scaled_font_size}px"' in svg_content 