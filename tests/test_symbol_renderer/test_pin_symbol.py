"""
Test rendering pin symbols using coordinates and orientations from parsed_symbols.json.
"""
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

def test_pin_from_json(renderer, dwg, pin_shapes, parsed_symbols):
    """Test rendering pins using coordinates and orientations from JSON."""
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