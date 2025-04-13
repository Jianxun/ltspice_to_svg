import os
import pytest
import xml.etree.ElementTree as ET
import logging
from src.generators.svg_renderer import SVGRenderer
from src.parsers.asc_parser import ASCParser
from src.parsers.schematic_parser import SchematicParser

@pytest.fixture(autouse=True)
def setup_ltspice_lib():
    """Set up the LTspice library path environment variable."""
    os.environ['LTSPICE_LIB_PATH'] = f"/Users/{os.getenv('USER')}/Library/Application Support/LTspice/lib/sym"

def test_wires_and_tjunctions():
    # Setup paths
    test_dir = os.path.dirname(os.path.abspath(__file__))
    schematic_path = os.path.join(test_dir, 'test1_wires_and_tjunctions.asc')
    output_path = os.path.join(test_dir, 'results', 'test1_wires_and_tjunctions.svg')
    json_path = os.path.join(test_dir, 'results', 'test1_wires_and_tjunctions.json')
    
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
    
    # Render wires with T-junctions
    renderer.render_wires(stroke_width=2.0, dot_size_multiplier=2.0)
    
    # Save the SVG
    renderer.save()
    
    # Print found T-junctions for visual inspection
    t_junctions = renderer._find_t_junctions(schematic_data['wires'])
    print("\nFound T-junctions:")
    for x, y in t_junctions:
        print(f"({x}, {y})")
        
    # Verify the total number of T-junctions
    assert len(t_junctions) == 9, f"Expected 9 T-junctions, found {len(t_junctions)}" 