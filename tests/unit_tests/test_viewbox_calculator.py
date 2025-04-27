"""
Tests for ViewboxCalculator class.
Tests the calculation of viewbox dimensions based on schematic elements.
"""
import pytest
from src.renderers.viewbox_calculator import ViewboxCalculator
from src.renderers.rendering_config import RenderingConfig

def test_empty_schematic():
    """Test viewbox calculation with empty schematic."""
    calculator = ViewboxCalculator()
    viewbox = calculator.calculate({})
    
    # Default size for empty schematic is 100x100
    assert viewbox == (0, 0, 100, 100)

def test_simple_wire_schematic():
    """Test viewbox calculation with a simple wire."""
    calculator = ViewboxCalculator()
    
    # Create a schematic with a single horizontal wire
    schematic = {
        'wires': [
            {'x1': 100, 'y1': 200, 'x2': 300, 'y2': 200}
        ]
    }
    
    viewbox = calculator.calculate(schematic)
    min_x, min_y, width, height = viewbox
    
    # The wire is 200 units wide (300-100), and 10% margin on each side
    # so the padding should be 20 units (10% of 200)
    assert min_x == pytest.approx(100 - 20)
    assert min_y == pytest.approx(200 - 20)
    assert width == pytest.approx(200 + 40)  # Wire width + padding on both sides
    
    # Since the wire has zero height, the calculator applies a minimum height of 1.0
    # So the total height should be 1.0 + 2*padding = 1.0 + 2*20 = 41.0
    assert height == pytest.approx(41.0)  # 1.0 (min height) + padding on both sides

def test_complex_schematic():
    """Test viewbox calculation with multiple elements."""
    calculator = ViewboxCalculator()
    
    # Create a schematic with wires, shapes, and flags
    schematic = {
        'wires': [
            {'x1': 0, 'y1': 0, 'x2': 100, 'y2': 0},
            {'x1': 0, 'y1': 0, 'x2': 0, 'y2': 100}
        ],
        'shapes': {
            'rectangles': [
                {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150}
            ],
            'circles': [
                {'x1': 200, 'y1': 200, 'x2': 300, 'y2': 300}
            ]
        },
        'flags': [
            {'x': 250, 'y': 50, 'type': 'ground'}
        ]
    }
    
    viewbox = calculator.calculate(schematic)
    min_x, min_y, width, height = viewbox
    
    # The max dimensions are (0 to 300) for x and (0 to 300) for y
    # with 10% padding (30 units each side)
    assert min_x == pytest.approx(-30)
    assert min_y == pytest.approx(-30)
    assert width == pytest.approx(360)  # 300 + 60 (padding)
    assert height == pytest.approx(360)  # 300 + 60 (padding)

def test_custom_margin():
    """Test viewbox calculation with custom margin setting."""
    # Create config with 5% margin instead of default 10%
    config = RenderingConfig(viewbox_margin=5.0)
    calculator = ViewboxCalculator(config=config)
    
    # Create a schematic with a simple rectangle
    schematic = {
        'shapes': {
            'rectangles': [
                {'x1': 100, 'y1': 100, 'x2': 300, 'y2': 300}
            ]
        }
    }
    
    viewbox = calculator.calculate(schematic)
    min_x, min_y, width, height = viewbox
    
    # The rectangle is 200x200, margin should be 5% of 200 = 10 units
    assert min_x == pytest.approx(100 - 10)
    assert min_y == pytest.approx(100 - 10)
    assert width == pytest.approx(200 + 20)  # Width + padding on both sides
    assert height == pytest.approx(200 + 20)  # Height + padding on both sides

def test_zero_margin():
    """Test viewbox calculation with zero margin."""
    # Create config with 0% margin
    config = RenderingConfig(viewbox_margin=0.0)
    calculator = ViewboxCalculator(config=config)
    
    # Create a schematic with a simple wire
    schematic = {
        'wires': [
            {'x1': 100, 'y1': 100, 'x2': 300, 'y2': 300}
        ]
    }
    
    viewbox = calculator.calculate(schematic)
    min_x, min_y, width, height = viewbox
    
    # The wire goes from (100,100) to (300,300), with no margin
    assert min_x == pytest.approx(100)
    assert min_y == pytest.approx(100)
    assert width == pytest.approx(200)  # Just the wire width
    assert height == pytest.approx(200)  # Just the wire height

def test_large_margin():
    """Test viewbox calculation with a large margin."""
    # Create config with 50% margin
    config = RenderingConfig(viewbox_margin=50.0)
    calculator = ViewboxCalculator(config=config)
    
    # Create a schematic with a simple circle
    schematic = {
        'shapes': {
            'circles': [
                {'x1': 100, 'y1': 100, 'x2': 200, 'y2': 200}
            ]
        }
    }
    
    viewbox = calculator.calculate(schematic)
    min_x, min_y, width, height = viewbox
    
    # The circle is effectively 100x100, with 50% margin (50 units)
    assert min_x == pytest.approx(100 - 50)
    assert min_y == pytest.approx(100 - 50)
    assert width == pytest.approx(100 + 100)  # Width + padding on both sides
    assert height == pytest.approx(100 + 100)  # Height + padding on both sides 