"""
Test cases for ground flag rendering.
"""
import pytest
import svgwrite
import os
from src.renderers.flag_renderer import FlagRenderer

@pytest.fixture
def dwg():
    """Create a new SVG drawing for each test."""
    return svgwrite.Drawing(size=('1000px', '1000px'))

@pytest.fixture
def renderer(dwg):
    """Create a new FlagRenderer for each test."""
    return FlagRenderer(dwg)

def test_render_ground_flag_basic(renderer, dwg):
    """Test basic ground flag rendering."""
    # Create a ground flag at (100, 100) pointing right (0°)
    flag = {
        'x': 100,
        'y': 100,
        'orientation': 0
    }
    
    # Render the flag
    renderer.render_ground_flag(flag)
    
    # Get the SVG content
    svg_content = dwg.tostring()
    
    # Verify the SVG contains the expected elements
    assert 'translate(100,100)' in svg_content
    assert 'rotate(0)' in svg_content
    assert 'line' in svg_content  # Should have three lines for the V shape
    
def test_render_ground_flag_orientation():
    """Test ground flag rendering with different orientations."""
    # Test orientations: 0° (right), 90° (up), 180° (left), 270° (down)
    orientations = [0, 90, 180, 270] 
    
    for orientation in orientations:
        # Create a new drawing and renderer for each orientation
        dwg = svgwrite.Drawing(size=('1000px', '1000px'))
        renderer = FlagRenderer(dwg)
        
        # Create a ground flag at (100, 100) with current orientation
        flag = {
            'x': 100,
            'y': 100,
            'orientation': orientation
        }
        
        # Render the flag
        renderer.render_ground_flag(flag)
        
        # Get the SVG content
        svg_content = dwg.tostring()
        
        # Verify the SVG contains the expected transform
        assert f'translate(100,100)' in svg_content
        assert f'rotate({orientation})' in svg_content

def test_render_ground_flag_stroke_width(renderer, dwg):
    """Test ground flag rendering with custom stroke width."""
    # Set custom stroke width
    renderer.stroke_width = 3.0
    
    # Create a ground flag
    flag = {
        'x': 100,
        'y': 100,
        'orientation': 0
    }
    
    # Render the flag
    renderer.render_ground_flag(flag)
    
    # Get the SVG content
    svg_content = dwg.tostring()
    
    # Verify the SVG contains the expected stroke width
    assert 'stroke-width="3.0"' in svg_content

def test_render_ground_flag_target_group(renderer, dwg):
    """Test ground flag rendering with target group."""
    # Create a target group
    target_group = dwg.g()
    
    # Create a ground flag
    flag = {
        'x': 100,
        'y': 100,
        'orientation': 0
    }
    
    # Render the flag into the target group
    renderer.render_ground_flag(flag, target_group)
    
    # Verify the target group contains the flag elements
    assert len(target_group.elements) > 0
    assert 'line' in target_group.tostring()

def test_render_ground_flag_visual():
    """Generate SVG file with all orientations for visual inspection."""
    # Create a new drawing with a white background
    dwg = svgwrite.Drawing(size=('400px', '400px'), profile='full')
    dwg.viewbox(0, 0, 400, 400)
    
    # Add white background
    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='white'))
    
    # Add title
    dwg.add(dwg.text('Ground Flag Orientations', insert=(200, 30), 
                     text_anchor='middle', font_family='Arial', font_size=20))
    
    # Create renderer
    renderer = FlagRenderer(dwg)
    renderer.stroke_width = 2.0
    
    # Positions for each orientation
    positions = [
        (100, 100, 0, 'Right (0°)'),
        (300, 100, 90, 'Up (90°)'),
        (100, 300, 180, 'Left (180°)'),
        (300, 300, 270, 'Down (270°)')
    ]
    
    # Render each orientation with label
    for x, y, orientation, label in positions:
        # Add label
        dwg.add(dwg.text(label, insert=(x, y - 30), 
                        text_anchor='middle', font_family='Arial', font_size=14))
        
        # Render ground flag
        flag = {
            'x': x,
            'y': y,
            'orientation': orientation
        }
        renderer.render_ground_flag(flag)
    
    # Create results directory if it doesn't exist
    results_dir = os.path.join('tests', 'test_flag_renderer', 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    # Save the SVG file
    svg_path = os.path.join(results_dir, 'ground_flags.svg')
    dwg.saveas(svg_path)
    
    # Verify file was created
    assert os.path.exists(svg_path) 