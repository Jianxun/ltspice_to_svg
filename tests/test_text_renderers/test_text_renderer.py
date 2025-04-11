"""
Tests for TextRenderer class.
Tests various text rendering features including:
- Font sizes (0-7)
- Justification modes (Left, Center, Right, Top, Bottom)
- Multi-line text
- Special characters
"""
import os
import pytest
import svgwrite
from pathlib import Path
from src.renderers.text_renderer import TextRenderer

# Default values
DEFAULT_FONT_SIZE = 22.0
DEFAULT_VIEWBOX = (-1000, -1000, 2000, 2000)

# Create results directory if it doesn't exist
os.makedirs('tests/test_text_renderers/results', exist_ok=True)

@pytest.fixture
def drawing():
    """Create a new SVG drawing for testing."""
    dwg = svgwrite.Drawing(
        'tests/test_text_renderers/results/temp.svg',
        profile='tiny',
        size=('100%', '100%')
    )
    dwg.viewbox(*DEFAULT_VIEWBOX)
    return dwg

@pytest.fixture
def text_renderer(drawing):
    """Create a TextRenderer instance for testing."""
    return TextRenderer(drawing)

def save_svg(dwg, test_name):
    """Save the SVG drawing to the results directory."""
    output_path = f'tests/test_text_renderers/results/{test_name}.svg'
    dwg.saveas(output_path)
    return output_path

def get_text_elements(dwg):
    """Get all text elements from the drawing."""
    return [elem for elem in dwg.elements if isinstance(elem, svgwrite.container.Group)]

def test_text_renderer_initialization(text_renderer, drawing):
    """Test that TextRenderer is properly initialized."""
    assert text_renderer.dwg == drawing

def test_font_sizes(text_renderer, drawing):
    """Test rendering text with different font sizes."""
    # Test all font sizes
    for size_index in range(8):
        text = {
            'x': -800,
            'y': -800 + (size_index * 100),
            'text': f'Font Size {size_index}',
            'justification': 'Left',
            'size_multiplier': size_index
        }
        text_renderer.render(text, font_size=DEFAULT_FONT_SIZE)
    
    # Save SVG
    output_path = save_svg(drawing, 'test_font_sizes')
    
    # Verify SVG content
    with open(output_path, 'r') as f:
        content = f.read()
        
    # Check that all font sizes are rendered
    for size_index in range(8):
        assert f'Font Size {size_index}' in content
        # Check that font size is set correctly
        expected_size = DEFAULT_FONT_SIZE * TextRenderer.SIZE_MULTIPLIERS[size_index]
        assert f'font-size="{expected_size}px"' in content

def test_justification(text_renderer, drawing):
    """Test text justification modes."""
    # Test horizontal justification
    for i, justification in enumerate(['Left', 'Center', 'Right']):
        text = {
            'x': -400 + (i * 400),
            'y': -400,
            'text': f'{justification} Justified',
            'justification': justification,
            'size_multiplier': 2
        }
        text_renderer.render(text, font_size=DEFAULT_FONT_SIZE)
    
    # Test vertical justification
    for i, justification in enumerate(['Top', 'Bottom']):
        text = {
            'x': 0,
            'y': -300 + (i * 600),
            'text': f'{justification} Justified',
            'justification': justification,
            'size_multiplier': 2
        }
        text_renderer.render(text, font_size=DEFAULT_FONT_SIZE)
    
    # Save SVG
    output_path = save_svg(drawing, 'test_justification')
    
    # Verify SVG content
    with open(output_path, 'r') as f:
        content = f.read()
        
    # Check that all justification modes are rendered
    for justification in ['Left', 'Center', 'Right', 'Top', 'Bottom']:
        assert f'{justification} Justified' in content
        
    # Check text-anchor attributes
    assert 'text-anchor="start"' in content  # Left
    assert 'text-anchor="middle"' in content  # Center
    assert 'text-anchor="end"' in content  # Right

def test_multiline_text(text_renderer, drawing):
    """Test rendering multi-line text."""
    text = {
        'x': 0,
        'y': 0,
        'text': 'Line 1\nLine 2\nLine 3',
        'justification': 'Center',
        'size_multiplier': 2
    }
    text_renderer.render(text, font_size=DEFAULT_FONT_SIZE)
    
    # Save SVG
    output_path = save_svg(drawing, 'test_multiline_text')
    
    # Verify SVG content
    with open(output_path, 'r') as f:
        content = f.read()
        
    # Check that all lines are rendered
    for i in range(1, 4):
        assert f'Line {i}' in content
        
    # Check that text-anchor is set correctly
    assert 'text-anchor="middle"' in content

def test_special_characters(text_renderer, drawing):
    """Test rendering text with special characters."""
    special_chars = 'A#$%^&*()_+-={}[]|\\:;"\'<>,.?/~`'
    text = {
        'x': 0,
        'y': 200,
        'text': special_chars,
        'justification': 'Center',
        'size_multiplier': 2
    }
    text_renderer.render(text, font_size=DEFAULT_FONT_SIZE)
    
    # Save SVG
    output_path = save_svg(drawing, 'test_special_characters')
    
    # Verify SVG content
    with open(output_path, 'r') as f:
        content = f.read()
        
    # Check that special characters are properly escaped
    # svgwrite handles escaping:
    # & -> &amp;
    # < -> &lt;
    # > -> &gt;
    # Other characters are preserved as is
    assert '&amp;' in content  # & is escaped as &amp;
    assert '&lt;' in content   # < is escaped as &lt;
    assert '&gt;' in content   # > is escaped as &gt;
    
    # Check that other special characters are preserved
    for char in '#$%^*()_+-={}[]|\\:;"\',?/~`':
        assert char in content

def test_empty_text(text_renderer, drawing):
    """Test handling of empty text."""
    text = {
        'x': 0,
        'y': 0,
        'text': '',
        'justification': 'Center',
        'size_multiplier': 2
    }
    text_renderer.render(text, font_size=DEFAULT_FONT_SIZE)  # Should not raise an exception
    
    # Save SVG
    output_path = save_svg(drawing, 'test_empty_text')
    
    # Verify SVG content
    with open(output_path, 'r') as f:
        content = f.read()
        
    # Check that no text element is created for empty text
    assert '<text' not in content

def test_default_values(text_renderer, drawing):
    """Test rendering with default values."""
    text = {
        'x': 0,
        'y': 0,
        'text': 'Default Values'
    }
    text_renderer.render(text, font_size=DEFAULT_FONT_SIZE)
    
    # Save SVG
    output_path = save_svg(drawing, 'test_default_values')
    
    # Verify SVG content
    with open(output_path, 'r') as f:
        content = f.read()
        
    # Check that text is rendered
    assert 'Default Values' in content
    
    # Check that default values are used
    assert 'text-anchor="start"' in content  # Default justification is Left
    assert 'font-size="33.0px"' in content  # Default size is 2 (1.5x * 22.0) 