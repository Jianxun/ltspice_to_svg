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

@pytest.fixture
def pin_shapes():
    """Shapes that make up a pin symbol."""
    return {
        'lines': [
            # Normal line
            {'x1': 0, 'y1': 0, 'x2': -8, 'y2': 0, 'type': 'line'},
            # Diagonal line
            {'x1': -24, 'y1': 8, 'x2': -8, 'y2': -8, 'type': 'line'}
        ],
        'circles': [
            # Circle using bounding box format
            {'x1': -24, 'y1': -8, 'x2': -8, 'y2': 8, 'type': 'circle'}
        ]
    }

@pytest.fixture
def parsed_symbols():
    """Load parsed symbols data."""
    with open('tests/test_symbol_renderer/parsed_symbols.json', 'r') as f:
        return json.load(f)

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
    #save_test_result(dwg, 'test_create_group')


def test_render_texts(renderer, dwg, sample_texts):
    """Test rendering texts."""
    renderer.create_group()
    renderer.render_texts(sample_texts, font_size=24.0)
    renderer.add_to_drawing()
    save_test_result(dwg, 'test_render_texts')



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

def test_pin_symbol_rendering(renderer, dwg, pin_shapes, parsed_symbols):
    """Test rendering pins with various transformations.
    
    This test verifies the symbol renderer's ability to handle:
    - Multiple symbols in a single drawing
    - Various rotation angles (R0, R90, R180, R270)
    - Mirror transformations (M0, M90)
    - Combined transformations
    - Proper positioning of symbols
    """
    # Set up drawing with appropriate viewbox
    dwg.viewbox(-400, -200, 200, 200)
    
    # Render each pin from the JSON data
    for symbol in parsed_symbols['symbols']:
        if symbol['symbol_name'] == 'pin':
            renderer.create_group()
            renderer.set_transformation(symbol['rotation'], (symbol['x'], symbol['y']))
            renderer.render_shapes(pin_shapes, stroke_width=2.0)
            renderer.add_to_drawing()
    
    # Save the result
    save_test_result(dwg, 'test_pin_symbols')
