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

def test_render_horizontal_wire(wire_renderer):
    """Test rendering a horizontal wire."""
    wire = {
        'x1': 100,
        'y1': 100,
        'x2': 200,
        'y2': 100
    }
    wire_renderer.render(wire, stroke_width=DEFAULT_STROKE_WIDTH)
    
    # Verify the line was added to the drawing
    shape_elements = get_shape_elements(wire_renderer.dwg)
    assert len(shape_elements) == 1
    line = shape_elements[0]
    assert float(line.attribs['x1']) == 100
    assert float(line.attribs['y1']) == 100
    assert float(line.attribs['x2']) == 200
    assert float(line.attribs['y2']) == 100
    assert line.attribs['stroke'] == 'black'
    assert float(line.attribs['stroke-width']) == DEFAULT_STROKE_WIDTH
    
    # Save SVG for manual inspection
    save_svg(wire_renderer.dwg, 'horizontal_wire')

def test_render_vertical_wire(wire_renderer):
    """Test rendering a vertical wire."""
    wire = {
        'x1': 100,
        'y1': 100,
        'x2': 100,
        'y2': 200
    }
    wire_renderer.render(wire, stroke_width=DEFAULT_STROKE_WIDTH)
    
    # Verify the line was added to the drawing
    shape_elements = get_shape_elements(wire_renderer.dwg)
    assert len(shape_elements) == 1
    line = shape_elements[0]
    assert float(line.attribs['x1']) == 100
    assert float(line.attribs['y1']) == 100
    assert float(line.attribs['x2']) == 100
    assert float(line.attribs['y2']) == 200
    assert float(line.attribs['stroke-width']) == DEFAULT_STROKE_WIDTH
    
    # Save SVG for manual inspection
    save_svg(wire_renderer.dwg, 'vertical_wire')

def test_render_diagonal_wire(wire_renderer):
    """Test rendering a diagonal wire."""
    wire = {
        'x1': 100,
        'y1': 100,
        'x2': 200,
        'y2': 200
    }
    wire_renderer.render(wire, stroke_width=DEFAULT_STROKE_WIDTH)
    
    # Verify the line was added to the drawing
    shape_elements = get_shape_elements(wire_renderer.dwg)
    assert len(shape_elements) == 1
    line = shape_elements[0]
    assert float(line.attribs['x1']) == 100
    assert float(line.attribs['y1']) == 100
    assert float(line.attribs['x2']) == 200
    assert float(line.attribs['y2']) == 200
    assert float(line.attribs['stroke-width']) == DEFAULT_STROKE_WIDTH
    
    # Save SVG for manual inspection
    save_svg(wire_renderer.dwg, 'diagonal_wire')

def test_render_wire_with_custom_stroke_width(wire_renderer):
    """Test rendering a wire with custom stroke width."""
    wire = {
        'x1': 100,
        'y1': 100,
        'x2': 200,
        'y2': 100
    }
    custom_stroke_width = 2.5
    wire_renderer.render(wire, stroke_width=custom_stroke_width)
    
    # Verify the line was added with custom stroke width
    shape_elements = get_shape_elements(wire_renderer.dwg)
    assert len(shape_elements) == 1
    line = shape_elements[0]
    assert float(line.attribs['stroke-width']) == custom_stroke_width
    
    # Save SVG for manual inspection
    save_svg(wire_renderer.dwg, 'custom_stroke_width')

def test_render_t_junction(wire_renderer):
    """Test rendering a T-junction dot."""
    x, y = 100, 100
    dot_size = DEFAULT_STROKE_WIDTH * DEFAULT_DOT_SIZE_MULTIPLIER
    wire_renderer.render_t_junction(x, y, dot_size)
    
    # Verify the circle was added to the drawing
    shape_elements = get_shape_elements(wire_renderer.dwg)
    assert len(shape_elements) == 1
    circle = shape_elements[0]
    assert float(circle.attribs['cx']) == 100
    assert float(circle.attribs['cy']) == 100
    assert float(circle.attribs['r']) == dot_size
    assert circle.attribs['fill'] == 'black'
    
    # Save SVG for manual inspection
    save_svg(wire_renderer.dwg, 't_junction')

def test_render_multiple_wires(wire_renderer):
    """Test rendering multiple wires."""
    wires = [
        {'x1': 100, 'y1': 100, 'x2': 200, 'y2': 100},
        {'x1': 100, 'y1': 100, 'x2': 100, 'y2': 200},
        {'x1': 100, 'y1': 100, 'x2': 200, 'y2': 200}
    ]
    
    for wire in wires:
        wire_renderer.render(wire, stroke_width=DEFAULT_STROKE_WIDTH)
    
    # Verify all lines were added to the drawing
    shape_elements = get_shape_elements(wire_renderer.dwg)
    assert len(shape_elements) == 3
    
    # Save SVG for manual inspection
    save_svg(wire_renderer.dwg, 'multiple_wires')

def test_render_wire_with_t_junction(wire_renderer):
    """Test rendering a wire with a T-junction."""
    wire = {
        'x1': 100,
        'y1': 100,
        'x2': 200,
        'y2': 100
    }
    wire_renderer.render(wire, stroke_width=DEFAULT_STROKE_WIDTH)
    dot_size = DEFAULT_STROKE_WIDTH * DEFAULT_DOT_SIZE_MULTIPLIER
    wire_renderer.render_t_junction(150, 100, dot_size)
    
    # Verify both line and circle were added
    shape_elements = get_shape_elements(wire_renderer.dwg)
    assert len(shape_elements) == 2
    line = shape_elements[0]
    circle = shape_elements[1]
    
    assert float(line.attribs['x1']) == 100
    assert float(line.attribs['y1']) == 100
    assert float(line.attribs['x2']) == 200
    assert float(line.attribs['y2']) == 100
    assert float(line.attribs['stroke-width']) == DEFAULT_STROKE_WIDTH
    
    assert float(circle.attribs['cx']) == 150
    assert float(circle.attribs['cy']) == 100
    assert float(circle.attribs['r']) == dot_size
    
    # Save SVG for manual inspection
    save_svg(wire_renderer.dwg, 'wire_with_t_junction') 