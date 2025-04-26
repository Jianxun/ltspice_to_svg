import os
import pytest
import xml.etree.ElementTree as ET
import logging
from src.renderers.svg_renderer import SVGRenderer
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
    
    # Find all text elements with the net label text
    text_elements = root.findall(".//{http://www.w3.org/2000/svg}text")
    net_label_texts = [text for text in text_elements if text.text == 'net1']
    
    # Should find 6 net labels based on the test file
    assert len(net_label_texts) == 6, f"Expected 6 net labels, found {len(net_label_texts)}"
    
    # Verify each net label text element has proper attributes
    for text in net_label_texts:
        # Check text properties
        assert text.text == 'net1', "Incorrect net label text"
        # Skip text-anchor check as it varies based on justification
        assert text.attrib['font-family'] == 'Arial', "Incorrect font family"
        assert 'px' in text.attrib['font-size'], "Font size should be specified in pixels"
        # Check position attributes
        assert 'x' in text.attrib, "Text element missing x coordinate"
        assert 'y' in text.attrib, "Text element missing y coordinate"
    
    # Log wire and flag counts for visual inspection reference
    print(f"\nRendered {len(schematic_data['wires'])} wires and {len(net_label_texts)} net labels") 