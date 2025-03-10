"""
Tests for flag parsing in ASC files.
Tests:
- IO pins (FLAG + IOPIN)
- Net labels (FLAG without IOPIN)
- Ground flags (FLAG with net_name '0')
"""
import os
from pathlib import Path
from src.parsers.asc_parser import ASCParser
from src.generators.svg_generator import SVGGenerator
import tempfile

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

def test_flag_parsing():
    """Test parsing of different flag types."""
    # Parse schematic
    asc_file = PROJECT_ROOT / 'tests' / 'test_flags' / 'test_flags.asc'
    asc_parser = ASCParser(str(asc_file))
    schematic_data = asc_parser.parse()
    
    # Get flags and io_pins
    flags = schematic_data['flags']
    io_pins = schematic_data['io_pins']
    
    # Group flags by type
    net_labels = [f for f in flags if f['type'] == 'net_label']
    gnd_flags = [f for f in flags if f['type'] == 'gnd']
    
    # Verify counts
    assert len(io_pins) == 10  # BUS01-BUS10
    assert len(net_labels) == 2  # net1, net2
    assert len(gnd_flags) == 4  # Four ground flags
    
    # Verify IO pins
    expected_directions = {
        'BUS01': 'BiDir',
        'BUS02': 'In',
        'BUS03': 'BiDir',
        'BUS04': 'Out',
        'BUS05': 'BiDir',
        'BUS06': 'BiDir',
        'BUS07': 'BiDir',
        'BUS08': 'BiDir',
        'BUS09': 'BiDir',
        'BUS10': 'BiDir'
    }
    for i in range(10):
        bus_name = f'BUS{i+1:02d}'
        pin = next(p for p in io_pins if p['net_name'] == bus_name)
        assert pin['direction'] == expected_directions[bus_name], f"Wrong direction for {bus_name}"
    
    # Verify net labels
    net1 = next(f for f in net_labels if f['net_name'] == 'net1')
    assert net1['x'] == -128
    assert net1['y'] == 576
    
    net2 = next(f for f in net_labels if f['net_name'] == 'net2')
    assert net2['x'] == 144
    assert net2['y'] == 576
    
    # Verify ground flags
    gnd_positions = {(320, 592), (256, 528), (320, 464), (384, 528)}
    for flag in gnd_flags:
        assert (flag['x'], flag['y']) in gnd_positions
        assert flag['net_name'] == '0'
    
    # Generate SVG to see debug output
    with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as tmp:
        svg_gen = SVGGenerator()
        svg_gen.generate(schematic_data, tmp.name)
        print(f"\nGenerated SVG file: {tmp.name}")
        
        # Print SVG content
        with open(tmp.name, 'r') as f:
            svg_content = f.read()
            print("\nSVG Content:")
            print(svg_content) 