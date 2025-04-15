import pytest
import svgwrite
import xml.etree.ElementTree as ET
import logging
import re
from src.renderers.flag_renderer import FlagRenderer, FlagType
from src.renderers.text_renderer import TextRenderer

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def assert_font_size(text_element, expected_size):
    """Helper function to assert font size, handling both '18px' and '18.0px' formats."""
    actual_size = text_element.attrib['font-size']
    # Extract numeric part and compare
    actual_num = float(re.search(r'(\d+(?:\.\d+)?)', actual_size).group(1))
    expected_num = float(re.search(r'(\d+(?:\.\d+)?)', expected_size).group(1))
    assert actual_num == expected_num, f"Expected font size {expected_size}, got {actual_size}"

@pytest.fixture
def dwg():
    """Create a new SVG drawing for each test."""
    return svgwrite.Drawing(profile='tiny')

@pytest.fixture
def flag_renderer(dwg):
    """Create a new FlagRenderer instance for each test."""
    renderer = FlagRenderer(dwg)
    renderer.base_font_size = 12.0
    return renderer

def test_net_label_rendering(flag_renderer):
    """Test rendering of a net label."""
    # Create a net label flag
    flag = {
        'x': 100,
        'y': 200,
        'net_name': 'VCC',
        'orientation': 0
    }
    
    # Render the net label
    flag_renderer.render_net_label(flag)
    
    # Get the SVG content
    svg_content = flag_renderer.dwg.tostring()
    logger.debug(f"Generated SVG:\n{svg_content}")
    
    # Parse the SVG content
    root = ET.fromstring(svg_content)
    
    # Register SVG namespace
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    
    # Find the net label group
    net_label_groups = root.findall(".//{http://www.w3.org/2000/svg}g[@class='net-label']")
    logger.debug(f"Found {len(net_label_groups)} net label groups")
    assert len(net_label_groups) == 1, "Expected exactly one net label group"
    
    # Check the group's transform
    group = net_label_groups[0]
    assert group.attrib['transform'] == 'translate(100,200) rotate(0)', \
        "Incorrect transform for net label group"
    
    # Find the text group
    text_groups = group.findall(".//{http://www.w3.org/2000/svg}g[@class='text-group']")
    logger.debug(f"Found {len(text_groups)} text groups")
    assert len(text_groups) == 1, "Expected exactly one text group"
    
    # Find the text element
    text_elements = text_groups[0].findall(".//{http://www.w3.org/2000/svg}text")
    logger.debug(f"Found {len(text_elements)} text elements")
    assert len(text_elements) == 1, "Expected exactly one text element"
    
    # Check text content and properties
    text = text_elements[0]
    assert text.text == 'VCC', "Incorrect text content"
    assert text.attrib['text-anchor'] == 'middle', "Text should be center-justified"
    assert text.attrib['font-family'] == 'Arial', "Incorrect font family"
    assert_font_size(text, '18px')

def test_net_label_180_degree_rotation(flag_renderer):
    """Test rendering of a net label with 180-degree rotation."""
    # Create a net label flag with 180-degree rotation
    flag = {
        'x': 100,
        'y': 200,
        'net_name': 'GND',
        'orientation': 180
    }
    
    # Render the net label
    flag_renderer.render_net_label(flag)
    
    # Get the SVG content
    svg_content = flag_renderer.dwg.tostring()
    logger.debug(f"Generated SVG:\n{svg_content}")
    
    # Parse the SVG content
    root = ET.fromstring(svg_content)
    
    # Register SVG namespace
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    
    # Find the net label group
    net_label_groups = root.findall(".//{http://www.w3.org/2000/svg}g[@class='net-label']")
    logger.debug(f"Found {len(net_label_groups)} net label groups")
    assert len(net_label_groups) == 1, "Expected exactly one net label group"
    
    # Check the group's transform
    group = net_label_groups[0]
    assert group.attrib['transform'] == 'translate(100,200) rotate(180)', \
        "Incorrect transform for net label group"
    
    # Find the text group
    text_groups = group.findall(".//{http://www.w3.org/2000/svg}g[@class='text-group']")
    logger.debug(f"Found {len(text_groups)} text groups")
    assert len(text_groups) == 1, "Expected exactly one text group"
    
    # Check text group's transform
    text_group = text_groups[0]
    if 'transform' in text_group.attrib:
        assert text_group.attrib['transform'] == 'rotate(-180)', \
            "Text group should be counter-rotated for 180-degree orientation"
    
    # Find the text element
    text_elements = text_groups[0].findall(".//{http://www.w3.org/2000/svg}text")
    logger.debug(f"Found {len(text_elements)} text elements")
    assert len(text_elements) == 1, "Expected exactly one text element"
    
    # Check text content and properties
    text = text_elements[0]
    assert text.text == 'GND', "Incorrect text content"
    assert text.attrib['text-anchor'] == 'middle', "Text should be center-justified"
    assert text.attrib['font-family'] == 'Arial', "Incorrect font family"
    assert_font_size(text, '18px')

def test_net_label_with_target_group(flag_renderer):
    """Test rendering of a net label with a target group."""
    # Create a target group
    target_group = flag_renderer.dwg.g()
    
    # Create a net label flag
    flag = {
        'x': 100,
        'y': 200,
        'net_name': 'CLK',
        'orientation': 0
    }
    
    # Render the net label into the target group
    flag_renderer.render_net_label(flag, target_group)
    
    # Add the target group to the drawing
    flag_renderer.dwg.add(target_group)
    
    # Get the SVG content
    svg_content = flag_renderer.dwg.tostring()
    logger.debug(f"Generated SVG:\n{svg_content}")
    
    # Parse the SVG content
    root = ET.fromstring(svg_content)
    
    # Register SVG namespace
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    
    # Find the net label group within the target group
    net_label_groups = root.findall(".//{http://www.w3.org/2000/svg}g[@class='net-label']")
    logger.debug(f"Found {len(net_label_groups)} net label groups")
    assert len(net_label_groups) == 1, "Expected exactly one net label group in target group"
    
    # Check the group's transform
    group = net_label_groups[0]
    assert group.attrib['transform'] == 'translate(100,200) rotate(0)', \
        "Incorrect transform for net label group"
    
    # Find the text group
    text_groups = group.findall(".//{http://www.w3.org/2000/svg}g[@class='text-group']")
    logger.debug(f"Found {len(text_groups)} text groups")
    assert len(text_groups) == 1, "Expected exactly one text group"
    
    # Find the text element
    text_elements = text_groups[0].findall(".//{http://www.w3.org/2000/svg}text")
    logger.debug(f"Found {len(text_elements)} text elements")
    assert len(text_elements) == 1, "Expected exactly one text element"
    
    # Check text content and properties
    text = text_elements[0]
    assert text.text == 'CLK', "Incorrect text content"
    assert text.attrib['text-anchor'] == 'middle', "Text should be center-justified"
    assert text.attrib['font-family'] == 'Arial', "Incorrect font family"
    assert_font_size(text, '18px') 