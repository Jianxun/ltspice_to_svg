"""
IO pin renderer for LTspice schematics.
Handles rendering of IO pins in SVG format with direction-specific shapes.
"""
import svgwrite
from typing import Dict

def render_io_pin(dwg: svgwrite.Drawing, io_pin: Dict, scale: float, stroke_width: float, font_size: float, size_multipliers: Dict[int, float], text_centering_compensation: float) -> None:
    """Add an IO pin flag to the SVG drawing with direction-specific shapes.
    
    Args:
        dwg: SVG drawing object
        io_pin: Dictionary containing IO pin properties:
            - x: X coordinate
            - y: Y coordinate
            - net_name: Name of the net/signal
            - orientation: Rotation angle in degrees
            - direction: Pin direction ('BiDir', 'In', or 'Out')
        scale: Scale factor for coordinates
        stroke_width: Width of lines
        font_size: Base font size in pixels
        size_multipliers: Dictionary mapping size indices to font size multipliers
        text_centering_compensation: Factor for text centering compensation
    """
    # Create a group for the IO pin shape only
    g = dwg.g()
    
    # Apply translation and rotation for the shape
    transform = [
        f"translate({io_pin['x'] * scale},{io_pin['y'] * scale})",
        f"rotate({io_pin['orientation']})"
    ]
    g.attribs['transform'] = ' '.join(transform)
    
    # Add shape based on direction
    if io_pin['direction'] == 'BiDir':
        # BiDir shape from io_pin_bi_dir.asy
        g.add(dwg.line(
            (16 * scale, 16 * scale), (0, 0),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
        g.add(dwg.line(
            (-16 * scale, 84 * scale), (-16 * scale, 16 * scale),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
        g.add(dwg.line(
            (16 * scale, 16 * scale), (16 * scale, 84 * scale),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
        g.add(dwg.line(
            (0, 0), (-16 * scale, 16 * scale),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
        g.add(dwg.line(
            (0, 100 * scale), (-16 * scale, 84 * scale),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
        g.add(dwg.line(
            (0, 100 * scale), (16 * scale, 84 * scale),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
    elif io_pin['direction'] == 'In':
        # Input shape from io_pin_input.asy
        g.add(dwg.line(
            (0, 0), (16 * scale, 16 * scale),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
        g.add(dwg.line(
            (16 * scale, 16 * scale), (16 * scale, 80 * scale),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
        g.add(dwg.line(
            (16 * scale, 80 * scale), (-16 * scale, 80 * scale),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
        g.add(dwg.line(
            (-16 * scale, 80 * scale), (-16 * scale, 16 * scale),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
        g.add(dwg.line(
            (-16 * scale, 16 * scale), (0, 0),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
    else:  # Out
        # Output shape from io_pin_output.asy
        g.add(dwg.line(
            (-16 * scale, 80 * scale), (0, 96 * scale),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
        g.add(dwg.line(
            (16 * scale, 16 * scale), (16 * scale, 80 * scale),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
        g.add(dwg.line(
            (16 * scale, 16 * scale), (-16 * scale, 16 * scale),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
        g.add(dwg.line(
            (-16 * scale, 80 * scale), (-16 * scale, 16 * scale),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
        g.add(dwg.line(
            (0, 96 * scale), (16 * scale, 80 * scale),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
        g.add(dwg.line(
            (0, 16 * scale), (0, 0),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
    
    # Add the shape group to the drawing
    dwg.add(g)
    
    # Calculate absolute text position and rotation
    orientation = io_pin['orientation']
    text_distance = 52  # Distance from pin point
    font_size = font_size * size_multipliers[2]  # Size 2 (1.5x)
    
    # Calculate text position based on pin orientation
    if orientation == 0:  # Right
        text_x = io_pin['x'] * scale
        text_y = (io_pin['y'] + text_distance) * scale
        text_rotation = -90
        # For vertical text, shift right by compensation factor of the font size
        text_x += font_size * text_centering_compensation
    elif orientation == 90:  # Up
        text_x = (io_pin['x'] - text_distance) * scale
        text_y = io_pin['y'] * scale
        text_rotation = 0
        # For horizontal text, shift down by compensation factor of the font size
        text_y += font_size * text_centering_compensation
    elif orientation == 180:  # Left
        text_x = io_pin['x'] * scale
        text_y = (io_pin['y'] - text_distance) * scale
        text_rotation = -90
        # For vertical text, shift right by compensation factor of the font size
        text_x += font_size * text_centering_compensation
    else:  # 270, Down
        text_x = (io_pin['x'] + text_distance) * scale
        text_y = io_pin['y'] * scale
        text_rotation = 0
        # For horizontal text, shift down by compensation factor of the font size
        text_y += font_size * text_centering_compensation
        
    # Create text group with rotation only
    text_group = dwg.g()
    if text_rotation != 0:
        text_group.attribs['transform'] = f'rotate({text_rotation} {text_x} {text_y})'
    
    # Add text element
    text_element = dwg.text(
        io_pin['net_name'],
        insert=(text_x, text_y),
        font_family='Arial',
        font_size=f'{font_size}px',
        text_anchor='middle',  # Center-justified
        fill='black'
    )
    
    # Add text to group and group to drawing
    text_group.add(text_element)
    dwg.add(text_group) 