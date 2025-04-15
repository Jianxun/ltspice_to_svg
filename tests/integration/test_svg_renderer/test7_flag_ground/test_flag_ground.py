import os
import pytest
import xml.etree.ElementTree as ET
import logging
from src.generators.svg_renderer import SVGRenderer
from src.parsers.asc_parser import ASCParser

@pytest.fixture(autouse=True)
def setup_ltspice_lib():
    """Set up the LTspice library path environment variable."""
    os.environ['LTSPICE_LIB_PATH'] = f"/Users/{os.getenv('USER')}/Library/Application Support/LTspice/lib/sym"

def test_ground_flag_rendering():
    """Test the rendering of ground flags in an LTspice schematic."""
    # Setup paths
    test_dir = os.path.dirname(os.path.abspath(__file__))
    schematic_path = os.path.join(test_dir, 'test_flag_ground.asc')
    output_path = os.path.join(test_dir, 'results', 'test_flag_ground.svg')
    json_path = os.path.join(test_dir, 'results', 'test_flag_ground.json')
    
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
    
    # Set stroke width
    renderer.set_stroke_width(2.0)
    
    # Render wires first (for visual inspection)
    renderer.render_wires(dot_size_multiplier=2.0)
    
    # Then render ground flags
    renderer.render_flags()
    
    # Save the SVG
    renderer.save()
    
    # Verify the SVG file was created
    assert os.path.exists(output_path), "SVG output file was not created"
    assert os.path.getsize(output_path) > 0, "SVG output file is empty"
    
    # Parse and verify SVG content
    tree = ET.parse(output_path)
    root = tree.getroot()
    
    # Count ground flags (should be 4 based on the test file)
    ground_flags = root.findall(".//*[@class='ground-flag']")
    assert len(ground_flags) == 4, f"Expected 4 ground flags, found {len(ground_flags)}"
    
    # Log wire and flag counts for visual inspection reference
    print(f"\nRendered {len(schematic_data['wires'])} wires and {len(ground_flags)} ground flags") 