"""
Test cases for the ShapeRenderer class.
"""
import pytest
import svgwrite
import os
from src.renderers.shape_renderer import ShapeRenderer

@pytest.fixture
def dwg():
    """Create a new SVG drawing for each test."""
    return svgwrite.Drawing()

@pytest.fixture
def renderer(dwg):
    """Create a new ShapeRenderer instance for each test."""
    return ShapeRenderer(dwg)

def test_render_line(renderer, dwg):
    """Test rendering a basic line."""
    line = {
        'type': 'line',
        'x1': 10,
        'y1': 10,
        'x2': 50,
        'y2': 50
    }
    renderer.render(line, stroke_width=2.0)
    
    # Save for manual inspection
    dwg.saveas('tests/test_shape_renderer/results/line.svg')
    
    # Verify line was added (accounting for defs element)
    assert len(dwg.elements) == 2  # defs + line
    line_element = dwg.elements[1]  # line is the second element
    assert line_element.elementname == 'line'
    assert line_element.attribs['x1'] == '10'
    assert line_element.attribs['y1'] == '10'
    assert line_element.attribs['x2'] == '50'
    assert line_element.attribs['y2'] == '50'
    assert line_element.attribs['stroke-width'] == '2.0'

def test_render_dashed_line(renderer, dwg):
    """Test rendering a dashed line."""
    line = {
        'type': 'line',
        'x1': 10,
        'y1': 10,
        'x2': 50,
        'y2': 50,
        'style': '5,5'
    }
    renderer.render(line, stroke_width=2.0)
    
    # Save for manual inspection
    dwg.saveas('tests/test_shape_renderer/results/dashed_line.svg')
    
    # Verify line was added with dash pattern (accounting for defs element)
    assert len(dwg.elements) == 2  # defs + line
    line_element = dwg.elements[1]  # line is the second element
    assert line_element.attribs['stroke-dasharray'] == '10.0,10.0'

def test_render_circle(renderer, dwg):
    """Test rendering a perfect circle."""
    circle = {
        'type': 'circle',
        'x1': 10,
        'y1': 10,
        'x2': 30,
        'y2': 30
    }
    renderer.render(circle, stroke_width=2.0)
    
    # Save for manual inspection
    dwg.saveas('tests/test_shape_renderer/results/circle.svg')
    
    # Verify circle was added (accounting for defs element)
    assert len(dwg.elements) == 2  # defs + circle
    circle_element = dwg.elements[1]  # circle is the second element
    assert circle_element.elementname == 'circle'
    assert float(circle_element.attribs['cx']) == 20.0
    assert float(circle_element.attribs['cy']) == 20.0
    assert float(circle_element.attribs['r']) == 10.0

def test_render_ellipse(renderer, dwg):
    """Test rendering an ellipse."""
    ellipse = {
        'type': 'circle',
        'x1': 10,
        'y1': 10,
        'x2': 30,
        'y2': 50
    }
    renderer.render(ellipse, stroke_width=2.0)
    
    # Save for manual inspection
    dwg.saveas('tests/test_shape_renderer/results/ellipse.svg')
    
    # Verify ellipse was added (accounting for defs element)
    assert len(dwg.elements) == 2  # defs + ellipse
    ellipse_element = dwg.elements[1]  # ellipse is the second element
    assert ellipse_element.elementname == 'ellipse'
    assert float(ellipse_element.attribs['cx']) == 20.0
    assert float(ellipse_element.attribs['cy']) == 30.0
    assert float(ellipse_element.attribs['rx']) == 10.0
    assert float(ellipse_element.attribs['ry']) == 20.0

def test_render_rectangle(renderer, dwg):
    """Test rendering a basic rectangle."""
    rect = {
        'type': 'rectangle',
        'x1': 10,
        'y1': 10,
        'x2': 50,
        'y2': 30
    }
    renderer.render(rect, stroke_width=2.0)
    
    # Save for manual inspection
    dwg.saveas('tests/test_shape_renderer/results/rectangle.svg')
    
    # Verify rectangle was added (accounting for defs element)
    assert len(dwg.elements) == 2  # defs + rectangle
    rect_element = dwg.elements[1]  # rectangle is the second element
    assert rect_element.elementname == 'rect'
    assert rect_element.attribs['x'] == '10'
    assert rect_element.attribs['y'] == '10'
    assert rect_element.attribs['width'] == '40'
    assert rect_element.attribs['height'] == '20'

def test_render_dashed_rectangle(renderer, dwg):
    """Test rendering a dashed rectangle."""
    rect = {
        'type': 'rectangle',
        'x1': 10,
        'y1': 10,
        'x2': 50,
        'y2': 30,
        'style': '5,5'
    }
    renderer.render(rect, stroke_width=2.0)
    
    # Save for manual inspection
    dwg.saveas('tests/test_shape_renderer/results/dashed_rectangle.svg')
    
    # Verify rectangle was added as path with dash pattern (accounting for defs element)
    assert len(dwg.elements) == 2  # defs + path
    path_element = dwg.elements[1]  # path is the second element
    assert path_element.elementname == 'path'
    assert path_element.attribs['stroke-dasharray'] == '10.0,10.0'

def test_render_arc(renderer, dwg):
    """Test rendering an arc."""
    arc = {
        'type': 'arc',
        'x1': 10,
        'y1': 10,
        'x2': 50,
        'y2': 50,
        'start_angle': 0,
        'end_angle': 90
    }
    renderer.render(arc, stroke_width=2.0)
    
    # Save for manual inspection
    dwg.saveas('tests/test_shape_renderer/results/arc.svg')
    
    # Verify arc was added as path (accounting for defs element)
    assert len(dwg.elements) == 2  # defs + path
    path_element = dwg.elements[1]  # path is the second element
    assert path_element.elementname == 'path'
    assert 'M' in path_element.attribs['d']
    assert 'A' in path_element.attribs['d']

def test_render_dashed_arc(renderer, dwg):
    """Test rendering a dashed arc."""
    arc = {
        'type': 'arc',
        'x1': 10,
        'y1': 10,
        'x2': 50,
        'y2': 50,
        'start_angle': 0,
        'end_angle': 90,
        'style': '5,5'
    }
    renderer.render(arc, stroke_width=2.0)
    
    # Save for manual inspection
    dwg.saveas('tests/test_shape_renderer/results/dashed_arc.svg')
    
    # Verify arc was added with dash pattern (accounting for defs element)
    assert len(dwg.elements) == 2  # defs + path
    path_element = dwg.elements[1]  # path is the second element
    assert path_element.attribs['stroke-dasharray'] == '10.0,10.0'

def test_unknown_shape_type(renderer, dwg):
    """Test handling of unknown shape type."""
    unknown = {
        'type': 'unknown',
        'x1': 10,
        'y1': 10,
        'x2': 50,
        'y2': 50
    }
    renderer.render(unknown, stroke_width=2.0)
    
    # Verify only defs element exists
    assert len(dwg.elements) == 1  # only defs
    assert dwg.elements[0].elementname == 'defs'

def test_visual_line_styles(renderer, dwg):
    """Test visual rendering of all line styles."""
    # Set drawing size
    dwg['width'] = '400px'
    dwg['height'] = '200px'
    
    # Define line parameters
    y_spacing = 30
    start_x = 50
    end_x = 350
    stroke_width = 2.0
    
    # Render each line style
    styles = [
        (None, "Solid Line"),  # No style for solid line
        (ShapeRenderer.LINE_STYLE_DASH, "Dash Pattern"),
        (ShapeRenderer.LINE_STYLE_DOT, "Dot Pattern"),
        (ShapeRenderer.LINE_STYLE_DASH_DOT, "Dash-Dot Pattern"),
        (ShapeRenderer.LINE_STYLE_DASH_DOT_DOT, "Dash-Dot-Dot Pattern")
    ]
    
    for i, (style, label) in enumerate(styles):
        y = 50 + i * y_spacing
        
        # Add the line
        line = {
            'type': 'line',
            'x1': start_x,
            'y1': y,
            'x2': end_x,
            'y2': y
        }
        if style is not None:
            line['style'] = style
            
        renderer.render(line, stroke_width)
        
        # Add label
        dwg.add(dwg.text(label, insert=(start_x - 40, y + 5), 
                       font_size='12px', text_anchor='end'))
    
    # Save for manual inspection
    dwg.saveas('tests/test_shape_renderer/results/line_styles.svg')
    
    # Verify the file was created
    assert os.path.exists('tests/test_shape_renderer/results/line_styles.svg')
    
    # Verify all lines were added (accounting for defs element and text elements)
    assert len(dwg.elements) == 1 + len(styles) * 2  # defs + (line + text) for each style 