import pytest
from pathlib import Path
from src.generators.svg_renderer import SVGRenderer
from src.parsers.asc_parser import ASCParser
import xml.etree.ElementTree as ET

class TestTextRendering:
    @pytest.fixture
    def test_schematic(self):
        """Load the test schematic"""
        schematic_path = Path(__file__).parent / "test2_texts.asc"
        return schematic_path

    @pytest.fixture
    def svg_renderer(self):
        return SVGRenderer()

    @pytest.fixture
    def asc_parser(self, test_schematic):
        return ASCParser(test_schematic)

    def test_text_rendering(self, test_schematic, svg_renderer, asc_parser):
        """Test text rendering with various alignments and orientations"""
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
        results_dir = Path(__file__).parent / "results"
        results_dir.mkdir(exist_ok=True)
        output_path = results_dir / "test2_texts.svg"
        svg_renderer.create_drawing(str(output_path))
        
        # Set font size and render text elements
        svg_renderer.set_base_font_size(16.0)
        svg_renderer.render_texts()
        
        # Save the SVG
        svg_renderer.save()
        
        # Parse the SVG for verification
        with open(output_path, "r") as f:
            svg_output = f.read()
        root = ET.fromstring(svg_output)
        
        # Verify text elements
        text_elements = root.findall(".//{http://www.w3.org/2000/svg}text")
        
        # Verify text count
        assert len(text_elements) == 30, f"Expected 30 text elements, got {len(text_elements)}"
        
        # Verify text content and attributes
        for text in text_elements:
            # Check required attributes
            assert "x" in text.attrib, "Text element missing x coordinate"
            assert "y" in text.attrib, "Text element missing y coordinate"
            assert "text-anchor" in text.attrib, "Text element missing text-anchor attribute"
            
            # Verify text content
            assert text.text is not None, "Text element has no content"
            
            # Verify text-anchor values
            text_anchor = text.attrib["text-anchor"]
            assert text_anchor in ["start", "middle", "end"], f"Invalid text-anchor value: {text_anchor}"
            
            # Verify transform attribute for rotated text
            if "transform" in text.attrib:
                transform = text.attrib["transform"]
                assert "rotate" in transform, "Transform should contain rotation"
                
        # Verify specific text elements
        # Check for the .op directive
        op_text = next((t for t in text_elements if t.text == ".op"), None)
        assert op_text is not None, "Could not find .op directive text"
        
        # Check for the .tran directive
        tran_text = next((t for t in text_elements if t.text == ".tran"), None)
        assert tran_text is not None, "Could not find .tran directive text"
        
        # Check for comment texts
        comment_texts = [t for t in text_elements if t.text == "Comment"]
        assert len(comment_texts) == 28, f"Expected 28 comment texts, got {len(comment_texts)}"
        
        # Check for spice directive texts
        spice_texts = [t for t in text_elements if t.text in [".op", ".tran"]]
        assert len(spice_texts) == 2, f"Expected 2 spice directive texts, got {len(spice_texts)}"
        
        # Verify text positions and alignments
        for text in text_elements:
            x = float(text.attrib["x"])
            y = float(text.attrib["y"])
            text_anchor = text.attrib["text-anchor"]
            
            # Verify text is within schematic bounds
            assert 0 <= x <= 1012, f"Text x coordinate {x} out of bounds"
            assert 0 <= y <= 728, f"Text y coordinate {y} out of bounds"
            
            # Verify text-anchor matches expected alignment
            if text.text == ".op":
                assert text_anchor == "start", "Directive text should be left-aligned"
            elif "V" in text.attrib.get("transform", ""):
                # Vertical text should be middle-aligned
                assert text_anchor == "middle", "Vertical text should be middle-aligned" 