"""
Tests for schematic shape parsing and rendering.
"""
import os
import shutil
from pathlib import Path
from src.parsers.asc_parser import ASCParser
from src.generators.svg_generator import SVGGenerator

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

def test_schematic_shapes():
    """Test shape parsing and rendering with test_sch_shapes.asc file."""
    # Parse schematic
    asc_file = PROJECT_ROOT / 'tests' / 'test_schematic_shapes' / 'test_sch_shapes.asc'
    asc_parser = ASCParser(str(asc_file))
    schematic_data = asc_parser.parse()
    
    # Verify wires are parsed
    assert len(schematic_data['wires']) == 4  # Updated to match actual wire count
    wire = schematic_data['wires'][0]
    assert all(k in wire for k in ['x1', 'y1', 'x2', 'y2'])
    assert wire['x1'] == 0 and wire['y1'] == -160  # First wire coordinates
    
    # Verify ground flag is parsed
    assert len(schematic_data['flags']) == 1
    flag = schematic_data['flags'][0]
    assert flag['net_name'] == '0'  # Ground flag
    assert flag['x'] == 0 and flag['y'] == 96

def test_line_parsing():
    """Test parsing of LINE elements with different styles."""
    asc_file = PROJECT_ROOT / 'tests' / 'test_schematic_shapes' / 'test_sch_shapes.asc'
    asc_parser = ASCParser(str(asc_file))
    schematic_data = asc_parser.parse()
    
    # Verify lines are parsed
    lines = schematic_data['shapes']['lines']
    assert len(lines) == 5
    for i, line in enumerate(lines):
        assert all(k in line for k in ['x1', 'y1', 'x2', 'y2'])
        # All lines should have style, but style=None means solid line (style code 0)
        if i < 4:
            assert 'style' in line and line['style'] is not None
        else:
            # Last line has no style attribute or style=None, both mean solid line
            assert 'style' not in line or line.get('style') is None
        
    # Verify line coordinates and styles
    first_line = lines[0]
    assert first_line['x1'] == -796 and first_line['y1'] == -164
    assert first_line['x2'] == -608 and first_line['y2'] == -168
    assert first_line['style'] == '4,2,0.001,2,0.001,2'  # Style 4 (dash dot dot)
    
    # Verify other line styles
    assert lines[1]['style'] == '4,2,0.001,2'  # Style 3 (dash dot)
    assert lines[2]['style'] == '0.001,2'  # Style 2 (dot)
    assert lines[3]['style'] == '4,2'  # Style 1 (dash)
    # Last line is solid (style code 0), so either no style attribute or style=None

def test_rectangle_parsing():
    """Test parsing of RECTANGLE elements."""
    asc_file = PROJECT_ROOT / 'tests' / 'test_schematic_shapes' / 'test_sch_shapes.asc'
    asc_parser = ASCParser(str(asc_file))
    schematic_data = asc_parser.parse()
    
    # Verify rectangle is parsed
    rectangles = schematic_data['shapes']['rectangles']
    assert len(rectangles) == 1
    rect = rectangles[0]
    assert all(k in rect for k in ['x1', 'y1', 'x2', 'y2', 'style'])
    assert rect['style'] == '4,2'  # Style 1 (dash)
    
    # Verify rectangle coordinates
    assert rect['x1'] == -792 and rect['y1'] == -60
    assert rect['x2'] == -580 and rect['y2'] == 92

def test_circle_parsing():
    """Test parsing of CIRCLE elements."""
    asc_file = PROJECT_ROOT / 'tests' / 'test_schematic_shapes' / 'test_sch_shapes.asc'
    asc_parser = ASCParser(str(asc_file))
    schematic_data = asc_parser.parse()
    
    # Verify circle is parsed
    circles = schematic_data['shapes']['circles']
    assert len(circles) == 1
    circle = circles[0]
    assert all(k in circle for k in ['x1', 'y1', 'x2', 'y2'])
    
    # Verify circle coordinates
    assert circle['x1'] == -1076 and circle['y1'] == -56
    assert circle['x2'] == -880 and circle['y2'] == 40

def test_arc_parsing():
    """Test parsing of ARC elements."""
    asc_file = PROJECT_ROOT / 'tests' / 'test_schematic_shapes' / 'test_sch_shapes.asc'
    asc_parser = ASCParser(str(asc_file))
    schematic_data = asc_parser.parse()
    
    # Verify arc is parsed
    arcs = schematic_data['shapes']['arcs']
    assert len(arcs) == 1
    arc = arcs[0]
    assert all(k in arc for k in ['x1', 'y1', 'x2', 'y2', 'start_angle', 'end_angle', 'style'])
    assert arc['style'] == '4,2'  # Style 1 (dash)
    
    # Verify arc coordinates and angles
    assert arc['x1'] == -1000 and arc['y1'] == 208
    assert arc['x2'] == -904 and arc['y2'] == 136
    assert 250 < arc['start_angle'] < 260  # Approximate angle check
    assert 320 < arc['end_angle'] < 330  # Approximate angle check

def test_svg_generation():
    """Test SVG generation with shapes."""
    # Get test case directory
    test_dir = PROJECT_ROOT / 'tests' / 'test_schematic_shapes'
    asc_file = test_dir / 'test_sch_shapes.asc'
    
    # Parse schematic
    asc_parser = ASCParser(str(asc_file))
    schematic_data = asc_parser.parse()
    
    # Save parsed data as JSON for reference
    json_file = test_dir / 'test_sch_shapes_parsed.json'
    asc_parser.export_json(str(json_file))
    print(f"Exported parsed data to {json_file}")
    
    # Generate SVG
    svg_file = test_dir / 'test_sch_shapes.svg'
    generator = SVGGenerator(stroke_width=3.0, dot_size_multiplier=1.5, scale=1.0, font_size=16.0)
    generator.generate(schematic_data, str(svg_file), {})
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
    
    # Verify shape elements in SVG
    # Lines (4 wires + 5 styled lines + 3 lines for GND symbol = 12 lines)
    assert svg_content.count('<line') == 12
    assert 'stroke-dasharray' in svg_content  # At least one styled line
    
    # Rectangle (converted to path for styling)
    assert '<path' in svg_content and 'Z' in svg_content  # Closed path for rectangle
    assert 'stroke-dasharray' in svg_content  # Styled rectangle
    
    # Circle
    assert '<ellipse' in svg_content  # Circle is rendered as ellipse
    
    # Arc (path)
    assert '<path' in svg_content
    assert 'A' in svg_content  # Arc command in path 