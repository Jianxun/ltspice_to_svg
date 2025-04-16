import pytest
from pathlib import Path
from src.renderers.svg_renderer import SVGRenderer
from src.parsers.asc_parser import ASCParser

class TestTextCalibration:
    @pytest.fixture
    def test_schematic(self):
        """Load the text calibration schematic"""
        schematic_path = Path(__file__).parent / "test_text_calibration.asc"
        return schematic_path

    @pytest.fixture
    def svg_renderer(self):
        return SVGRenderer()

    @pytest.fixture
    def asc_parser(self, test_schematic):
        return ASCParser(test_schematic)

    def test_text_calibration(self, test_schematic, svg_renderer, asc_parser):
        """Generate SVG output for manual text calibration inspection"""
        # Parse the schematic
        schematic_data = asc_parser.parse()
        
        # Save schematic data as JSON for reference
        results_dir = Path(__file__).parent / "results"
        results_dir.mkdir(exist_ok=True)
        json_path = results_dir / "test_text_calibration.json"
        asc_parser.export_json(str(json_path))
        
        # Load schematic data into renderer
        svg_renderer.load_schematic(schematic_data)
        
        # Create drawing
        output_path = results_dir / "test_text_calibration.svg"
        svg_renderer.create_drawing(str(output_path))
        
        # Set font size and render text elements
        svg_renderer.set_base_font_size(16.0)
        svg_renderer.render_texts()
        svg_renderer.render_shapes()
        
        # Save the SVG
        svg_renderer.save()
        
        print(f"\nText calibration files generated:")
        print(f"1. Schematic JSON: {json_path}")
        print(f"2. SVG output: {output_path}")
        print("\nPlease inspect the SVG output to verify:")
        print("- Text alignments (Left, Center, Right)")
        print("- Vertical text orientations")
        print("- Text positioning relative to reference lines")
        print("- Overall text rendering quality") 