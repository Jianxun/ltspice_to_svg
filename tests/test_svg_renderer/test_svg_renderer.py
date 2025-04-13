import pytest
import os
import tempfile
from src.generators.svg_renderer import SVGRenderer
from src.utils.logger import setup_logging

# Setup logging for tests
setup_logging('tests/test_svg_renderer/results/test.log')

class TestSVGRenderer:
    @pytest.fixture
    def renderer(self):
        return SVGRenderer()
    
    @pytest.fixture
    def sample_schematic(self):
        return {
            'wires': [
                {'x1': 0, 'y1': 0, 'x2': 100, 'y2': 0},
                {'x1': 50, 'y1': 0, 'x2': 50, 'y2': 100}
            ],
            'symbols': [
                {'symbol_name': 'resistor', 'x': 50, 'y': 50, 'rotation': 'R0', 'instance_name': 'R1'}
            ],
            'texts': [
                {'text': 'R1', 'x': 60, 'y': 50, 'rotation': 0}
            ],
            'shapes': {
                'lines': [
                    {'x1': 10, 'y1': 10, 'x2': 90, 'y2': 90}
                ],
                'rectangles': [
                    {'x1': 25, 'y1': 25, 'x2': 75, 'y2': 75}
                ],
                'circles': [
                    {'x1': 50, 'y1': 50, 'x2': 60, 'y2': 60}
                ],
                'arcs': []
            }
        }
    
    def test_initialization(self, renderer):
        """Test that the renderer initializes correctly."""
        assert renderer.dwg is None
        assert renderer.schematic_data is None
        assert renderer.view_box is None
        assert renderer._renderers == {}
    
    def test_load_schematic(self, renderer, sample_schematic):
        """Test loading schematic data."""
        renderer.load_schematic(sample_schematic)
        assert renderer.schematic_data == sample_schematic
        assert renderer.view_box is not None
    
    def test_create_drawing(self, renderer, sample_schematic):
        """Test creating a new SVG drawing."""
        with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as tmp:
            renderer.load_schematic(sample_schematic)
            renderer.create_drawing(tmp.name)
            assert renderer.dwg is not None
            assert os.path.exists(tmp.name)
            os.unlink(tmp.name)
    
    def test_render_wires(self, renderer, sample_schematic):
        """Test wire rendering."""
        with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as tmp:
            renderer.load_schematic(sample_schematic)
            renderer.create_drawing(tmp.name)
            renderer.render_wires()
            renderer.save()
            assert os.path.exists(tmp.name)
            os.unlink(tmp.name)
    
    def test_render_symbols(self, renderer, sample_schematic):
        """Test symbol rendering."""
        with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as tmp:
            renderer.load_schematic(sample_schematic)
            renderer.create_drawing(tmp.name)
            renderer.render_symbols()
            renderer.save()
            assert os.path.exists(tmp.name)
            os.unlink(tmp.name)
    
    def test_render_texts(self, renderer, sample_schematic):
        """Test text rendering."""
        with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as tmp:
            renderer.load_schematic(sample_schematic)
            renderer.create_drawing(tmp.name)
            renderer.render_texts()
            renderer.save()
            assert os.path.exists(tmp.name)
            os.unlink(tmp.name)
    
    def test_render_shapes(self, renderer, sample_schematic):
        """Test shape rendering."""
        with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as tmp:
            renderer.load_schematic(sample_schematic)
            renderer.create_drawing(tmp.name)
            renderer.render_shapes()
            renderer.save()
            assert os.path.exists(tmp.name)
            os.unlink(tmp.name)
    
    def test_error_handling(self, renderer):
        """Test error handling for invalid operations."""
        # Test rendering without loading schematic
        with pytest.raises(ValueError):
            renderer.render_wires()
        
        # Test rendering without creating drawing
        renderer.load_schematic({})
        with pytest.raises(ValueError):
            renderer.render_wires()
        
        # Test saving without creating drawing
        with pytest.raises(ValueError):
            renderer.save()
    
    def test_custom_parameters(self, renderer, sample_schematic):
        """Test rendering with custom parameters."""
        with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as tmp:
            renderer.load_schematic(sample_schematic)
            renderer.create_drawing(tmp.name)
            
            # Test custom stroke width
            renderer.set_stroke_width(2.0)
            renderer.render_wires()
            
            # Test custom font size
            renderer.set_base_font_size(24.0)
            renderer.render_texts()
            
            # Test custom dot size multiplier
            renderer.render_wires(dot_size_multiplier=1.0)
            
            renderer.save()
            assert os.path.exists(tmp.name)
            os.unlink(tmp.name) 