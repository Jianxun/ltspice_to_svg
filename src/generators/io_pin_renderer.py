"""
IO pin renderer for LTspice schematics.
Handles rendering of IO pins in SVG format with direction-specific shapes.
"""
import svgwrite
import json
import os
from typing import Dict
from src.renderers.shape_renderer import ShapeRenderer
from src.renderers.text_renderer import TextRenderer

def render_io_pin(dwg: svgwrite.Drawing, io_pin: Dict, stroke_width: float, font_size: float, size_multipliers: Dict[int, float], text_centering_compensation: float) -> None:
    """Add an IO pin flag to the SVG drawing with direction-specific shapes.
    
    Args:
        dwg: SVG drawing object
        io_pin: Dictionary containing IO pin properties:
            - x: X coordinate
            - y: Y coordinate
            - net_name: Name of the net/signal
            - orientation: Rotation angle in degrees
            - direction: Pin direction ('BiDir', 'In', or 'Out')
        stroke_width: Width of lines
        font_size: Base font size in pixels
        size_multipliers: Dictionary mapping size indices to font size multipliers
        text_centering_compensation: Factor for text centering compensation
    """
    # Load flag definitions from JSON
    flag_definitions_path = os.path.join(os.path.dirname(__file__), '..', 'renderers', 'flag_definitions', 'io_pin_flag.json')
    with open(flag_definitions_path, 'r') as f:
        flag_definitions = json.load(f)
    
    # Get the definition for the specific direction
    direction = io_pin['direction']
    if direction not in flag_definitions:
        raise ValueError(f"Unknown IO pin direction: {direction}")
    
    direction_def = flag_definitions[direction]
    
    # Create a group for the IO pin shape only
    g = dwg.g()
    
    # Apply translation and rotation for the shape
    transform = [
        f"translate({io_pin['x']},{io_pin['y']})",
        f"rotate({io_pin['orientation']})"
    ]
    g.attribs['transform'] = ' '.join(transform)
    
    # Initialize shape renderer
    shape_renderer = ShapeRenderer(dwg)
    shape_renderer.stroke_width = stroke_width
    
    # Render lines using shape renderer
    for line in direction_def['lines']:
        shape_renderer.render_line(
            x1=line['start'][0],
            y1=line['start'][1],
            x2=line['end'][0],
            y2=line['end'][1],
            target_group=g
        )
    
    # Add the shape group to the drawing
    dwg.add(g)
    
    # Initialize text renderer
    text_renderer = TextRenderer(dwg)
    text_renderer.base_font_size = font_size
    
    # Calculate text position based on pin orientation
    orientation = io_pin['orientation']
    text_anchor = direction_def['text']['anchor']
    text_x = io_pin['x'] + text_anchor['x']
    text_y = io_pin['y'] + text_anchor['y']
    
    # Create text properties
    text_properties = {
        'x': text_x,
        'y': text_y,
        'text': io_pin['net_name'],
        'justification': direction_def['text']['justification'],
        'size_multiplier': size_multipliers[2],  # Size 2 (1.5x)
        'type': 'comment',
        'is_mirrored': False
    }
    
    # Create text group with rotation
    text_group = dwg.g()
    if orientation != 0:
        text_group.attribs['transform'] = f'rotate({orientation} {text_x} {text_y})'
    
    # Render text using text renderer
    text_renderer.render(text_properties, text_group)
    
    # Add text group to drawing
    dwg.add(text_group) 