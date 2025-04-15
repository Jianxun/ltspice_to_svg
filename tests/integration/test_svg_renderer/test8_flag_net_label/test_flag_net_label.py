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

def test_net_label_rendering():
    """Test the rendering of net labels in an LTspice schematic.
    
    The test schematic contains:
    - 6 net labels all named "net1"
    - Connected to a wire network at different positions and orientations
    """
    # Setup paths
    test_dir = os.path.dirname(os.path.abspath(__file__))
    schematic_path = os.path.join(test_dir, 'test_flag_net_label.asc')
    output_path = os.path.join(test_dir, 'results', 'test_flag_net_label.svg')
    json_path = os.path.join(test_dir, 'results', 'test_flag_net_label.json')
    
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
    
    # Then render net labels
    renderer.render_flags()
    
    # Save the SVG
    renderer.save()
    
    # Verify the SVG file was created
    assert os.path.exists(output_path), "SVG output file was not created"
    assert os.path.getsize(output_path) > 0, "SVG output file is empty"
    
    # Parse and verify SVG content
    tree = ET.parse(output_path)
    root = tree.getroot()
    
    # Register SVG namespace
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    
    # Count net labels (should be 6 based on the test file)
    net_label_groups = root.findall(".//{http://www.w3.org/2000/svg}g[@class='net-label']")
    assert len(net_label_groups) == 6, f"Expected 6 net labels, found {len(net_label_groups)}"
    
    # Verify each net label has proper structure and content
    for group in net_label_groups:
        # Check group has transform attribute
        assert 'transform' in group.attrib, "Net label group missing transform attribute"
        
        # Find text group
        text_groups = group.findall(".//{http://www.w3.org/2000/svg}g[@class='text-group']")
        assert len(text_groups) == 1, "Expected exactly one text group per net label"
        
        # Find text element
        text_elements = text_groups[0].findall(".//{http://www.w3.org/2000/svg}text")
        assert len(text_elements) == 1, "Expected exactly one text element per net label"
        
        # Check text content and properties
        text = text_elements[0]
        assert text.text == 'net1', "Incorrect net label text"
        assert text.attrib['text-anchor'] == 'middle', "Text should be center-justified"
        assert text.attrib['font-family'] == 'Arial', "Incorrect font family"
        assert 'px' in text.attrib['font-size'], "Font size should be specified in pixels"
    
    # Log wire and flag counts for visual inspection reference
    print(f"\nRendered {len(schematic_data['wires'])} wires and {len(net_label_groups)} net labels") 