import pytest
from pathlib import Path
from src.renderers.svg_renderer import SVGRenderer
from src.parsers.asc_parser import ASCParser
import xml.etree.ElementTree as ET

class TestTextRendering:
    """Test suite for text rendering functionality.
    
    Tests various aspects of text rendering including:
    - Text alignment (Left, Right, Center, Top, Bottom)
    - Text orientation (Horizontal, Vertical)
    - Text size multipliers
    - Special text types (comments, spice directives)
    """
    
    @pytest.fixture
    def test_schematic(self):
        """Load the test schematic"""
        schematic_path = Path(__file__).parent / "test_texts.asc"
        return schematic_path

    @pytest.fixture
    def svg_renderer(self):
        """Create a new SVG renderer instance"""
        return SVGRenderer()

    @pytest.fixture
    def asc_parser(self, test_schematic):
        """Create a new ASC parser instance"""
        return ASCParser(test_schematic)
        
    @pytest.fixture
    def rendered_svg(self, test_schematic, svg_renderer, asc_parser):
        """Render the test schematic and return the SVG root element"""
        # Parse the schematic
        schematic_data = asc_parser.parse()
        
        # Save schematic data as JSON
        results_dir = Path(__file__).parent / "results"
        results_dir.mkdir(exist_ok=True)
        json_path = results_dir / "test2_texts.json"
        asc_parser.export_json(str(json_path))
        
        # Load schematic data into renderer
        svg_renderer.load_schematic(schematic_data)
        
        # Create drawing
        output_path = results_dir / "test2_texts.svg"
        svg_renderer.create_drawing(str(output_path))
        
        # Set font size and render text elements
        svg_renderer.set_base_font_size(16.0)
        svg_renderer.render_texts()
        
        # Save the SVG
        svg_renderer.save()
        
        # Parse and return the SVG root element
        tree = ET.parse(output_path)
        return tree.getroot()

    def test_text_count(self, rendered_svg):
        """Test that all text elements are rendered."""
        text_elements = rendered_svg.findall(".//{http://www.w3.org/2000/svg}text")
        assert len(text_elements) == 30, f"Expected 30 text elements, got {len(text_elements)}"

    def test_text_attributes(self, rendered_svg):
        """Test that text elements have required attributes."""
        text_elements = rendered_svg.findall(".//{http://www.w3.org/2000/svg}text")
        for i, text in enumerate(text_elements, 1):
            assert "x" in text.attrib, f"Text element {i} missing x coordinate"
            assert "y" in text.attrib, f"Text element {i} missing y coordinate"
            assert "text-anchor" in text.attrib, f"Text element {i} missing text-anchor attribute"
            assert text.text is not None, f"Text element {i} has no content"

    def test_text_alignment(self, rendered_svg):
        """Test text alignment attributes."""
        text_elements = rendered_svg.findall(".//{http://www.w3.org/2000/svg}text")
        for text in text_elements:
            text_anchor = text.attrib["text-anchor"]
            assert text_anchor in ["start", "middle", "end"], \
                f"Invalid text-anchor value: {text_anchor} for text: {text.text}"

    def test_vertical_text(self, rendered_svg):
        """Test vertical text rendering."""
        text_elements = rendered_svg.findall(".//{http://www.w3.org/2000/svg}text")
        vertical_texts = [t for t in text_elements if "transform" in t.attrib]
        
        for text in vertical_texts:
            transform = text.attrib["transform"]
            assert "rotate" in transform, \
                f"Vertical text should have rotation transform, found: {transform}"
            assert text.attrib["text-anchor"] == "middle", \
                f"Vertical text should be middle-aligned, found: {text.attrib['text-anchor']}"

    def test_spice_directives(self, rendered_svg):
        """Test spice directive text rendering."""
        text_elements = rendered_svg.findall(".//{http://www.w3.org/2000/svg}text")
        
        # Check for the .op directive
        op_text = next((t for t in text_elements if t.text == ".op"), None)
        assert op_text is not None, "Could not find .op directive text"
        assert op_text.attrib["text-anchor"] == "start", \
            "Directive text should be left-aligned"
        
        # Check for the .tran directive
        tran_text = next((t for t in text_elements if t.text == ".tran"), None)
        assert tran_text is not None, "Could not find .tran directive text"
        assert tran_text.attrib["text-anchor"] == "start", \
            "Directive text should be left-aligned"

    def test_text_bounds(self, rendered_svg):
        """Test that text elements are within schematic bounds."""
        text_elements = rendered_svg.findall(".//{http://www.w3.org/2000/svg}text")
        for text in text_elements:
            x = float(text.attrib["x"])
            y = float(text.attrib["y"])
            assert 0 <= x <= 1012, f"Text x coordinate {x} out of bounds for text: {text.text}"
            assert 0 <= y <= 728, f"Text y coordinate {y} out of bounds for text: {text.text}"

    def test_text_size_multipliers(self, rendered_svg):
        """Test text size multipliers.
        
        Tests that text elements have the correct font sizes based on the size multipliers:
        - Size 0: 0.625 * base_font_size = 10.0px
        - Size 1: 1.0 * base_font_size = 16.0px
        - Size 2: 1.5 * base_font_size = 24.0px (default)
        - Size 3: 2.0 * base_font_size = 32.0px
        - Size 4: 2.5 * base_font_size = 40.0px
        - Size 5: 3.5 * base_font_size = 56.0px
        - Size 6: 5.0 * base_font_size = 80.0px
        - Size 7: 7.0 * base_font_size = 112.0px
        """
        text_elements = rendered_svg.findall(".//{http://www.w3.org/2000/svg}text")
        comment_texts = [t for t in text_elements if t.text == "Comment"]
        
        # Base font size is set to 16.0 in the fixture
        base_font_size = 16.0
        
        # Expected font sizes based on multipliers
        expected_sizes = {
            "10.0": 0,  # size 0: 16.0 * 0.625
            "16.0": 0,  # size 1: 16.0 * 1.0
            "24.0": 0,  # size 2: 16.0 * 1.5 (default)
            "32.0": 0,  # size 3: 16.0 * 2.0
            "40.0": 0,  # size 4: 16.0 * 2.5
            "56.0": 0,  # size 5: 16.0 * 3.5
            "80.0": 0,  # size 6: 16.0 * 5.0
            "112.0": 0  # size 7: 16.0 * 7.0
        }
        
        for text in comment_texts:
            font_size = text.attrib.get("font-size", "24.0")  # Default is size 2 (1.5x)
            # Remove 'px' suffix if present and convert to string
            font_size = str(float(font_size.replace('px', '')))
            assert font_size in expected_sizes, f"Unexpected font size: {font_size}px"
            expected_sizes[font_size] += 1
            
        # Verify we have at least one text of each size
        for size, count in expected_sizes.items():
            assert count > 0, f"No text elements found with font size {size}px"
            
        # Additional assertions for specific text elements
        for text in text_elements:
            if text.text == ".op" or text.text == ".tran":
                # SPICE directives should use default size (24.0px)
                font_size = str(float(text.attrib.get("font-size", "0").replace('px', '')))
                assert font_size == "24.0", f"SPICE directive has wrong font size: {font_size}px" 