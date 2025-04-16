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

def test_basic_shapes(renderer, dwg):
    """Test rendering basic shapes arranged horizontally."""
    # Set drawing size
    dwg['width'] = '600px'
    dwg['height'] = '200px'
    
    # Define common parameters
    y_center = 100
    shape_spacing = 80
    start_x = 50
    
    # Line
    line = {
        'type': 'line',
        'x1': start_x,
        'y1': y_center - 20,
        'x2': start_x + 40,
        'y2': y_center + 20
    }
    renderer.render(line)
    
    # Rectangle
    rect = {
        'type': 'rectangle',
        'x1': start_x + shape_spacing,
        'y1': y_center - 20,
        'x2': start_x + shape_spacing + 40,
        'y2': y_center + 20
    }
    renderer.render(rect)
    
    # Circle
    circle = {
        'type': 'circle',
        'x1': start_x + shape_spacing * 2,
        'y1': y_center - 20,
        'x2': start_x + shape_spacing * 2 + 40,
        'y2': y_center + 20
    }
    renderer.render(circle)
    
    # Ellipse
    ellipse = {
        'type': 'circle',
        'x1': start_x + shape_spacing * 3,
        'y1': y_center - 30,
        'x2': start_x + shape_spacing * 3 + 40,
        'y2': y_center + 30
    }
    renderer.render(ellipse)
    
    # Arc (90 degrees)
    arc_90 = {
        'type': 'arc',
        'x1': start_x + shape_spacing * 4,
        'y1': y_center - 20,
        'x2': start_x + shape_spacing * 4 + 40,
        'y2': y_center + 20,
        'start_angle': 0,
        'end_angle': 90
    }
    renderer.render(arc_90)
    
    # Arc (270 degrees)
    arc_270 = {
        'type': 'arc',
        'x1': start_x + shape_spacing * 5,
        'y1': y_center - 20,
        'x2': start_x + shape_spacing * 5 + 40,
        'y2': y_center + 20,
        'start_angle': 0,
        'end_angle': 270
    }
    renderer.render(arc_270)
    
    # Save for manual inspection
    save_test_result(dwg, 'basic_shapes')

def test_dotted_shapes(renderer, dwg):
    """Test rendering shapes with dotted style."""
    # Set drawing size
    dwg['width'] = '600px'
    dwg['height'] = '200px'
    
    # Define common parameters
    y_center = 100
    shape_spacing = 80
    start_x = 50
    
    # Line
    line = {
        'type': 'line',
        'x1': start_x,
        'y1': y_center - 20,
        'x2': start_x + 40,
        'y2': y_center + 20,
        'style': ShapeRenderer.LINE_STYLE_DOT
    }
    renderer.render(line)
    
    # Rectangle
    rect = {
        'type': 'rectangle',
        'x1': start_x + shape_spacing,
        'y1': y_center - 20,
        'x2': start_x + shape_spacing + 40,
        'y2': y_center + 20,
        'style': ShapeRenderer.LINE_STYLE_DOT
    }
    renderer.render(rect)
    
    # Circle
    circle = {
        'type': 'circle',
        'x1': start_x + shape_spacing * 2,
        'y1': y_center - 20,
        'x2': start_x + shape_spacing * 2 + 40,
        'y2': y_center + 20,
        'style': ShapeRenderer.LINE_STYLE_DOT
    }
    renderer.render(circle)
    
    # Ellipse
    ellipse = {
        'type': 'circle',
        'x1': start_x + shape_spacing * 3,
        'y1': y_center - 30,
        'x2': start_x + shape_spacing * 3 + 40,
        'y2': y_center + 30,
        'style': ShapeRenderer.LINE_STYLE_DOT
    }
    renderer.render(ellipse)
    
    # Arc (90 degrees)
    arc_90 = {
        'type': 'arc',
        'x1': start_x + shape_spacing * 4,
        'y1': y_center - 20,
        'x2': start_x + shape_spacing * 4 + 40,
        'y2': y_center + 20,
        'start_angle': 0,
        'end_angle': 90,
        'style': ShapeRenderer.LINE_STYLE_DOT
    }
    renderer.render(arc_90)
    
    # Arc (270 degrees)
    arc_270 = {
        'type': 'arc',
        'x1': start_x + shape_spacing * 5,
        'y1': y_center - 20,
        'x2': start_x + shape_spacing * 5 + 40,
        'y2': y_center + 20,
        'start_angle': 0,
        'end_angle': 270,
        'style': ShapeRenderer.LINE_STYLE_DOT
    }
    renderer.render(arc_270)
    
    # Save for manual inspection
    save_test_result(dwg, 'dotted_shapes')

def test_thick_shapes(renderer, dwg):
    """Test rendering shapes with thick stroke width."""
    # Set drawing size
    dwg['width'] = '600px'
    dwg['height'] = '200px'
    
    # Define common parameters
    y_center = 100
    shape_spacing = 80
    start_x = 50
    stroke_width = 5.0
    
    # Line
    line = {
        'type': 'line',
        'x1': start_x,
        'y1': y_center - 20,
        'x2': start_x + 40,
        'y2': y_center + 20
    }
    renderer.render(line, stroke_width=stroke_width)
    
    # Rectangle
    rect = {
        'type': 'rectangle',
        'x1': start_x + shape_spacing,
        'y1': y_center - 20,
        'x2': start_x + shape_spacing + 40,
        'y2': y_center + 20
    }
    renderer.render(rect, stroke_width=stroke_width)
    
    # Circle
    circle = {
        'type': 'circle',
        'x1': start_x + shape_spacing * 2,
        'y1': y_center - 20,
        'x2': start_x + shape_spacing * 2 + 40,
        'y2': y_center + 20
    }
    renderer.render(circle, stroke_width=stroke_width)
    
    # Ellipse
    ellipse = {
        'type': 'circle',
        'x1': start_x + shape_spacing * 3,
        'y1': y_center - 30,
        'x2': start_x + shape_spacing * 3 + 40,
        'y2': y_center + 30
    }
    renderer.render(ellipse, stroke_width=stroke_width)
    
    # Arc (90 degrees)
    arc_90 = {
        'type': 'arc',
        'x1': start_x + shape_spacing * 4,
        'y1': y_center - 20,
        'x2': start_x + shape_spacing * 4 + 40,
        'y2': y_center + 20,
        'start_angle': 0,
        'end_angle': 90
    }
    renderer.render(arc_90, stroke_width=stroke_width)
    
    # Arc (270 degrees)
    arc_270 = {
        'type': 'arc',
        'x1': start_x + shape_spacing * 5,
        'y1': y_center - 20,
        'x2': start_x + shape_spacing * 5 + 40,
        'y2': y_center + 20,
        'start_angle': 0,
        'end_angle': 270
    }
    renderer.render(arc_270, stroke_width=stroke_width)
    
    # Save for manual inspection
    save_test_result(dwg, 'thick_shapes')

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
                        font_size='12px', font_family='Arial'))
    
    # Save for manual inspection
    save_test_result(dwg, 'line_styles')
    
    # Verify the file was created
    assert os.path.exists('tests/unit_tests/test_shape_renderer/results/line_styles.svg')
    
    # Verify all lines were added (accounting for defs element and text elements)
    assert len(dwg.elements) == 1 + len(styles) * 2  # defs + (line + text) for each style 

def test_group_rendering(renderer, dwg):
    """Test rendering triangles both directly and to a group."""
    # Set drawing size
    dwg['width'] = '400px'
    dwg['height'] = '200px'
    
    # Create a group for the second triangle
    group = dwg.g(id='triangle_group')
    
    # Define triangle vertices (equilateral triangle)
    # First triangle (direct rendering)
    vertices1 = [
        (50, 150),  # bottom left
        (150, 150),  # bottom right
        (100, 50)   # top
    ]
    
    # Second triangle (group rendering)
    vertices2 = [
        (250, 150),  # bottom left
        (350, 150),  # bottom right
        (300, 50)    # top
    ]
    
    # Render first triangle directly to drawing
    for i in range(3):
        line = {
            'type': 'line',
            'x1': vertices1[i][0],
            'y1': vertices1[i][1],
            'x2': vertices1[(i + 1) % 3][0],
            'y2': vertices1[(i + 1) % 3][1]
        }
        renderer.render(line)
    
    # Render second triangle to group
    for i in range(3):
        line = {
            'type': 'line',
            'x1': vertices2[i][0],
            'y1': vertices2[i][1],
            'x2': vertices2[(i + 1) % 3][0],
            'y2': vertices2[(i + 1) % 3][1]
        }
        renderer.render(line, target_group=group)
    
    # Add group to drawing
    dwg.add(group)
    
    # Save for manual inspection
    save_test_result(dwg, 'group_rendering')
    
    # Verify elements are in correct containers
    # Main drawing should have defs + 3 lines + group
    assert len(dwg.elements) == 5  # defs + 3 lines + group
    
    # Group should have 3 lines
    assert len(group.elements) == 3
    for element in group.elements:
        assert element.elementname == 'line' 

def save_test_result(dwg, test_name):
    """Save the test result as an SVG file."""
    os.makedirs('tests/unit_tests/test_shape_renderer/results', exist_ok=True)
    dwg.saveas(f'tests/unit_tests/test_shape_renderer/results/{test_name}.svg') 