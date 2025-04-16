import os
import pytest
import xml.etree.ElementTree as ET
import logging
from src.renderers.svg_renderer import SVGRenderer
from src.parsers.asc_parser import ASCParser
from src.parsers.schematic_parser import SchematicParser

@pytest.fixture(autouse=True)
def setup_ltspice_lib():
    """Set up the LTspice library path environment variable."""
    os.environ['LTSPICE_LIB_PATH'] = f"/Users/{os.getenv('USER')}/Library/Application Support/LTspice/lib/sym"

def test_wires_and_tjunctions():
    """Test rendering of wires and T-junctions.
    
    This test verifies that:
    1. All wires are rendered correctly
    2. T-junctions are properly identified and rendered
    3. The output SVG file is created with the expected elements
    4. The JSON output file is created for debugging
    """
    # Setup paths
    test_dir = os.path.dirname(os.path.abspath(__file__))
    schematic_path = os.path.join(test_dir, 'test_wires_and_tjunctions.asc')
    output_path = os.path.join(test_dir, 'results', 'test_wires_and_tjunctions.svg')
    json_path = os.path.join(test_dir, 'results', 'test_wires_and_tjunctions.json')
    
    # Create results directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Parse the schematic and save to JSON
    parser = ASCParser(schematic_path)
    schematic_data = parser.parse()
    parser.export_json(json_path)
    
    # Create SVG renderer
    renderer = SVGRenderer()
    renderer.load_schematic(schematic_data)
    renderer.create_drawing(output_path)
    
    # Set stroke width and render wires with T-junctions
    renderer.set_stroke_width(2.0)
    renderer.render_wires(dot_size_multiplier=2.0)
    
    # Save the SVG
    renderer.save()
    
    # Print found T-junctions for visual inspection
    t_junctions = renderer._find_t_junctions(schematic_data['wires'])
    print("\nFound T-junctions:")
    for x, y in t_junctions:
        print(f"({x}, {y})")
        
    # Verify the total number of T-junctions
    assert len(t_junctions) == 9, f"Expected 9 T-junctions, found {len(t_junctions)}"
    
    # Verify output files exist
    assert os.path.exists(output_path), f"SVG file not created at {output_path}"
    assert os.path.exists(json_path), f"JSON file not created at {json_path}"
    
    # Parse the SVG file to verify its contents
    tree = ET.parse(output_path)
    root = tree.getroot()
    
    # Verify wire elements
    wire_elements = root.findall(".//{http://www.w3.org/2000/svg}line")
    assert len(wire_elements) == len(schematic_data['wires']), \
        f"Expected {len(schematic_data['wires'])} wire elements, found {len(wire_elements)}"
    
    # Verify T-junction dots
    dot_elements = root.findall(".//{http://www.w3.org/2000/svg}circle")
    assert len(dot_elements) == len(t_junctions), \
        f"Expected {len(t_junctions)} T-junction dots, found {len(dot_elements)}"
    
    # Verify wire properties
    for wire_element in wire_elements:
        assert float(wire_element.attrib['stroke-width']) == 2.0, \
            f"Wire stroke width should be 2.0, found {wire_element.attrib['stroke-width']}"
        assert wire_element.attrib['stroke'] == 'black', \
            f"Wire color should be black, found {wire_element.attrib['stroke']}"
    
    # Verify T-junction dot properties
    for dot_element in dot_elements:
        assert float(dot_element.attrib['r']) == 4.0, \
            f"T-junction dot radius should be 4.0, found {dot_element.attrib['r']}"
        assert dot_element.attrib['fill'] == 'black', \
            f"T-junction dot fill should be black, found {dot_element.attrib['fill']}" 