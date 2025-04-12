import pytest
import svgwrite
import os
from src.renderers.wire_renderer import WireRenderer

# Default values from ltspice_to_svg.py
DEFAULT_STROKE_WIDTH = 3.0
DEFAULT_DOT_SIZE_MULTIPLIER = 1.5

# Create results directory if it doesn't exist
os.makedirs('tests/test_wire_renderer/results', exist_ok=True)

@pytest.fixture
def drawing():
    """Create a new SVG drawing for testing."""
    return svgwrite.Drawing(size=('1000px', '1000px'))

@pytest.fixture
def wire_renderer(drawing):
    """Create a WireRenderer instance for testing."""
    return WireRenderer(drawing)

def save_svg(dwg, test_name):
    """Save the SVG drawing to the results directory."""
    output_path = f'tests/test_wire_renderer/results/{test_name}.svg'
    dwg.saveas(output_path)
    return output_path

def get_shape_elements(dwg):
    """Get all shape elements from the drawing, excluding Defs."""
    return [elem for elem in dwg.elements if not isinstance(elem, svgwrite.container.Defs)]

def test_wire_renderer_initialization(wire_renderer, drawing):
    """Test that WireRenderer is properly initialized."""
    assert wire_renderer.dwg == drawing

def test_render_wire_with_custom_stroke_width(wire_renderer):
    """Test rendering wires with different stroke widths."""
    # Define wires with different stroke widths and positions
    wires = [
        {
            'wire': {'x1': 100, 'y1': 100, 'x2': 300, 'y2': 100},  # horizontal wire
            'stroke_width': DEFAULT_STROKE_WIDTH,  # default
            'label': 'default'
        },
        {
            'wire': {'x1': 100, 'y1': 200, 'x2': 300, 'y2': 200},  # horizontal wire
            'stroke_width': 0.5,  # thin
            'label': 'thin'
        },
        {
            'wire': {'x1': 100, 'y1': 300, 'x2': 300, 'y2': 300},  # horizontal wire
            'stroke_width': 5.0,  # thick
            'label': 'thick'
        }
    ]
    
    # Render all wires
    for wire_info in wires:
        wire_renderer.render(wire_info['wire'], stroke_width=wire_info['stroke_width'])
    
    # Verify all lines were added with correct stroke widths
    shape_elements = get_shape_elements(wire_renderer.dwg)
    assert len(shape_elements) == 3
    
    # Verify each wire's properties
    for i, wire_info in enumerate(wires):
        line = shape_elements[i]
        assert float(line.attribs['x1']) == wire_info['wire']['x1']
        assert float(line.attribs['y1']) == wire_info['wire']['y1']
        assert float(line.attribs['x2']) == wire_info['wire']['x2']
        assert float(line.attribs['y2']) == wire_info['wire']['y2']
        assert float(line.attribs['stroke-width']) == wire_info['stroke_width']
        assert line.attribs['stroke'] == 'black'
    
    # Save SVG for manual inspection
    save_svg(wire_renderer.dwg, 'custom_stroke_widths')

def test_render_multiple_wires_with_t_junction(wire_renderer):
    """Test rendering multiple wires with a T-junction at their common point."""
    # Define the common point and wires
    common_point = (100, 100)
    wires = [
        {'x1': common_point[0], 'y1': common_point[1], 'x2': 200, 'y2': 100},  # horizontal
        {'x1': common_point[0], 'y1': common_point[1], 'x2': 100, 'y2': 200},  # vertical
        {'x1': common_point[0], 'y1': common_point[1], 'x2': 200, 'y2': 200}   # diagonal
    ]
    
    # Render all wires
    for wire in wires:
        wire_renderer.render(wire, stroke_width=DEFAULT_STROKE_WIDTH)
    
    # Add T-junction at the common point
    dot_size = DEFAULT_STROKE_WIDTH * DEFAULT_DOT_SIZE_MULTIPLIER
    wire_renderer.render_t_junction(common_point[0], common_point[1], dot_size)
    
    # Get all shape elements
    shape_elements = get_shape_elements(wire_renderer.dwg)
    assert len(shape_elements) == 4  # 3 wires + 1 T-junction
    
    # Verify each wire's properties
    for i, wire in enumerate(wires):
        line = shape_elements[i]
        assert float(line.attribs['x1']) == wire['x1']
        assert float(line.attribs['y1']) == wire['y1']
        assert float(line.attribs['x2']) == wire['x2']
        assert float(line.attribs['y2']) == wire['y2']
        assert float(line.attribs['stroke-width']) == DEFAULT_STROKE_WIDTH
        assert line.attribs['stroke'] == 'black'
    
    # Verify T-junction properties
    circle = shape_elements[3]  # T-junction is the last element
    assert float(circle.attribs['cx']) == common_point[0]
    assert float(circle.attribs['cy']) == common_point[1]
    assert float(circle.attribs['r']) == dot_size
    assert circle.attribs['fill'] == 'black'
    
    # Save SVG for manual inspection
    save_svg(wire_renderer.dwg, 'multiple_wires_with_t_junction')

def test_render_t_junction_sizes(wire_renderer):
    """Test rendering T-junctions with different sizes along a horizontal wire."""
    # Define a horizontal wire
    wire = {
        'x1': 100,
        'y1': 100,
        'x2': 500,
        'y2': 100
    }
    
    # Define T-junctions with different sizes at different positions along the wire
    t_junctions = [
        {
            'x': wire['x1'],  # start of wire
            'y': wire['y1'],
            'size': DEFAULT_STROKE_WIDTH * DEFAULT_DOT_SIZE_MULTIPLIER,  # default
            'label': 'default'
        },
        {
            'x': (wire['x1'] + wire['x2']) / 2,  # middle of wire
            'y': wire['y1'],
            'size': DEFAULT_STROKE_WIDTH * 0.5,  # small
            'label': 'small'
        },
        {
            'x': wire['x2'],  # end of wire
            'y': wire['y1'],
            'size': DEFAULT_STROKE_WIDTH * 2.0,  # large
            'label': 'large'
        }
    ]
    
    # Render the wire first
    wire_renderer.render(wire, stroke_width=1.0)
    
    # Render all T-junctions
    for t_junction in t_junctions:
        wire_renderer.render_t_junction(t_junction['x'], t_junction['y'], t_junction['size'])
    
    # Get all shape elements
    shape_elements = get_shape_elements(wire_renderer.dwg)
    assert len(shape_elements) == 4  # 1 wire + 3 T-junctions
    
    # Verify wire properties
    line = shape_elements[0]
    assert float(line.attribs['x1']) == wire['x1']
    assert float(line.attribs['y1']) == wire['y1']
    assert float(line.attribs['x2']) == wire['x2']
    assert float(line.attribs['y2']) == wire['y2']
    assert float(line.attribs['stroke-width']) == 1.0
    assert line.attribs['stroke'] == 'black'
    
    # Verify each T-junction's properties
    for i, t_junction in enumerate(t_junctions):
        circle = shape_elements[i + 1]  # T-junctions start after the wire
        assert float(circle.attribs['cx']) == t_junction['x']
        assert float(circle.attribs['cy']) == t_junction['y']
        assert float(circle.attribs['r']) == t_junction['size']
        assert circle.attribs['fill'] == 'black'
    
    # Save SVG for manual inspection
    save_svg(wire_renderer.dwg, 't_junction_sizes') 