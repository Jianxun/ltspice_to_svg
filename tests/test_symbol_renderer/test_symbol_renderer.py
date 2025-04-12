import pytest
import svgwrite
import os
import json
from src.renderers.symbol_renderer import SymbolRenderer

@pytest.fixture
def dwg():
    """Create a new SVG drawing for each test."""
    return svgwrite.Drawing()

@pytest.fixture
def renderer(dwg):
    """Create a new SymbolRenderer for each test."""
    return SymbolRenderer(dwg)

@pytest.fixture
def sample_shapes():
    """Sample shapes for testing."""
    return {
        'lines': [
            {'x1': 0, 'y1': 0, 'x2': 10, 'y2': 10},
            {'x1': 10, 'y1': 0, 'x2': 0, 'y2': 10}
        ],
        'circles': [
            {'cx': 5, 'cy': 5, 'r': 2}
        ]
    }

@pytest.fixture
def sample_texts():
    """Sample texts for testing."""
    return [
        {'x': 5, 'y': 5, 'text': 'Test', 'justification': 'Center'},
        {'x': 10, 'y': 10, 'text': 'Value', 'justification': 'Right'}
    ]

def save_test_result(dwg, test_name):
    """Save the test result as an SVG file."""
    os.makedirs('tests/test_symbol_renderer/results', exist_ok=True)
    dwg.saveas(f'tests/test_symbol_renderer/results/{test_name}.svg')

def test_create_group(renderer, dwg):
    """Test creating a new group."""
    group = renderer.create_group()
    assert group is not None
    assert renderer._current_group == group
    renderer.add_to_drawing()
    save_test_result(dwg, 'test_create_group')

def test_set_transformation(renderer, dwg):
    """Test setting transformations."""
    # Test rotation
    renderer.create_group()
    renderer.set_transformation('R90', (100, 200))
    renderer.add_to_drawing()
    save_test_result(dwg, 'test_set_transformation_rotation')
    
    # Test mirroring
    dwg = svgwrite.Drawing()
    renderer = SymbolRenderer(dwg)
    renderer.create_group()
    renderer.set_transformation('M90', (100, 200))
    renderer.add_to_drawing()
    save_test_result(dwg, 'test_set_transformation_mirror')
    
    # Test invalid rotation
    dwg = svgwrite.Drawing()
    renderer = SymbolRenderer(dwg)
    renderer.create_group()
    renderer.set_transformation('Rinvalid', (100, 200))
    renderer.add_to_drawing()
    save_test_result(dwg, 'test_set_transformation_invalid')

def test_render_shapes(renderer, dwg, sample_shapes):
    """Test rendering shapes."""
    renderer.create_group()
    renderer.render_shapes(sample_shapes, stroke_width=2.0)
    renderer.add_to_drawing()
    save_test_result(dwg, 'test_render_shapes')

def test_render_texts(renderer, dwg, sample_texts):
    """Test rendering texts."""
    renderer.create_group()
    renderer.render_texts(sample_texts, font_size=24.0)
    renderer.add_to_drawing()
    save_test_result(dwg, 'test_render_texts')

def test_add_to_drawing(renderer, dwg):
    """Test adding group to drawing."""
    renderer.create_group()
    renderer.add_to_drawing()
    save_test_result(dwg, 'test_add_to_drawing')

def test_error_no_group(renderer):
    """Test error when no group is created."""
    with pytest.raises(ValueError, match="No group created"):
        renderer.set_transformation('R0', (0, 0))
    
    with pytest.raises(ValueError, match="No group created"):
        renderer.render_shapes({})
    
    with pytest.raises(ValueError, match="No group created"):
        renderer.render_texts([])
    
    with pytest.raises(ValueError, match="No group created"):
        renderer.add_to_drawing()

def test_full_rendering_sequence(renderer, dwg, sample_shapes, sample_texts):
    """Test complete rendering sequence."""
    # Create group
    renderer.create_group()
    
    # Set transformation
    renderer.set_transformation('R90', (100, 200))
    
    # Render shapes and texts
    renderer.render_shapes(sample_shapes, stroke_width=2.0)
    renderer.render_texts(sample_texts, font_size=24.0)
    
    # Add to drawing
    renderer.add_to_drawing()
    
    # Verify results
    assert len(dwg.elements) > 0
    assert renderer._current_group is None
    
    # Save the result
    save_test_result(dwg, 'test_full_rendering_sequence')

def test_actual_symbol_rendering(renderer, dwg):
    """Test rendering with actual symbol data."""
    # Load test data
    with open('tests/test_symbol_renderer/parsed_symbols.json', 'r') as f:
        test_data = json.load(f)
    
    # Create a group for each symbol
    for symbol in test_data['symbols']:
        renderer.create_group()
        
        # Set transformation
        renderer.set_transformation(symbol['rotation'], (symbol['x'], symbol['y']))
        
        # Add placeholder shapes and texts
        shapes = {
            'lines': [
                {'x1': -5, 'y1': -5, 'x2': 5, 'y2': 5},
                {'x1': 5, 'y1': -5, 'x2': -5, 'y2': 5}
            ]
        }
        texts = [
            {
                'x': 0,
                'y': 0,
                'text': symbol['instance_name'],
                'justification': 'Center'
            }
        ]
        
        # Render shapes and texts
        renderer.render_shapes(shapes, stroke_width=1.0)
        renderer.render_texts(texts, font_size=22.0)
        
        # Add to drawing
        renderer.add_to_drawing()
    
    # Save the result
    save_test_result(dwg, 'test_actual_symbol_rendering') 