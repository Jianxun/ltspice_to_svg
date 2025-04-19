"""
Test text rendering switches for SPICE directives and schematic comments.
"""
import os
import pytest
import xml.etree.ElementTree as ET
from pathlib import Path
from src.parsers.schematic_parser import SchematicParser
from src.renderers.svg_renderer import SVGRenderer

# Create results directory if it doesn't exist
os.makedirs('tests/integration/test_svg_renderer/test2_text/results', exist_ok=True)

def test_text_rendering_switches():
    """Test text rendering switches for SPICE directives and schematic comments."""
    # Paths
    schematic_path = 'tests/integration/test_svg_renderer/test2_text/test_texts_rendering_switches.asc'
    output_path = 'tests/integration/test_svg_renderer/test2_text/results/test_texts_rendering_switches.svg'
    
    # Parse schematic
    parser = SchematicParser(schematic_path)
    data = parser.parse()
    
    # Test case 1: All text enabled
    renderer = SVGRenderer()
    renderer.load_schematic(data['schematic'], data['symbols'])
    renderer.create_drawing(output_path)
    renderer.render_texts()
    renderer.save()
    
    # Verify all text is rendered
    tree = ET.parse(output_path)
    root = tree.getroot()
    text_elements = root.findall(".//{http://www.w3.org/2000/svg}text")
    assert len(text_elements) == 2, "Expected 2 text elements when all enabled"
    assert any(t.text == ".tran" for t in text_elements), "SPICE directive not found"
    assert any(t.text == "Comment" for t in text_elements), "Comment not found"
    
    # Test case 2: SPICE directives disabled
    renderer = SVGRenderer()
    renderer.load_schematic(data['schematic'], data['symbols'])
    renderer.create_drawing(output_path)
    renderer.config.set_option('no_spice_directive', True)
    renderer.render_texts()
    renderer.save()
    
    # Verify only comment is rendered
    tree = ET.parse(output_path)
    root = tree.getroot()
    text_elements = root.findall(".//{http://www.w3.org/2000/svg}text")
    assert len(text_elements) == 1, "Expected 1 text element when SPICE disabled"
    assert text_elements[0].text == "Comment", "Comment not found when SPICE disabled"
    
    # Test case 3: Comments disabled
    renderer = SVGRenderer()
    renderer.load_schematic(data['schematic'], data['symbols'])
    renderer.create_drawing(output_path)
    renderer.config.set_option('no_schematic_comment', True)
    renderer.render_texts()
    renderer.save()
    
    # Verify only SPICE directive is rendered
    tree = ET.parse(output_path)
    root = tree.getroot()
    text_elements = root.findall(".//{http://www.w3.org/2000/svg}text")
    assert len(text_elements) == 1, "Expected 1 text element when comments disabled"
    assert text_elements[0].text == ".tran", "SPICE directive not found when comments disabled"
    
    # Test case 4: All text disabled
    renderer = SVGRenderer()
    renderer.load_schematic(data['schematic'], data['symbols'])
    renderer.create_drawing(output_path)
    renderer.config.set_option('no_schematic_comment', True)
    renderer.config.set_option('no_spice_directive', True)
    renderer.render_texts()
    renderer.save()
    
    # Verify no text is rendered
    tree = ET.parse(output_path)
    root = tree.getroot()
    text_elements = root.findall(".//{http://www.w3.org/2000/svg}text")
    assert len(text_elements) == 0, "Expected no text elements when all disabled" 