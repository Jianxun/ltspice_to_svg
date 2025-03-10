"""
Net label renderer for LTspice schematics.
Handles rendering of net labels in SVG format.
"""
import svgwrite
from typing import Dict

def render_net_label(dwg: svgwrite.Drawing, flag: Dict, scale: float, font_size: float, size_multipliers: Dict[int, float], net_label_distance: float) -> None:
    """Add a net label flag to the SVG drawing.
    
    Based on net_label.asy reference:
    - Text is positioned net_label_distance units above the pin point
    - Text is center-justified
    - Text uses size 2 (1.5x) font
    - Text orientation is normalized to 0° when net label is at 180° to avoid upside down text
    
    Args:
        dwg: SVG drawing object
        flag: Dictionary containing flag properties:
            - x: X coordinate
            - y: Y coordinate
            - net_name: Name of the net/signal
            - orientation: Rotation angle in degrees
        scale: Scale factor for coordinates
        font_size: Base font size in pixels
        size_multipliers: Dictionary mapping size indices to font size multipliers
        net_label_distance: Distance of net label text from origin
    """
    # Create a group for the net label
    g = dwg.g()
    
    # Apply translation and rotation
    transform = [
        f"translate({flag['x'] * scale},{flag['y'] * scale})",
        f"rotate({flag['orientation']})"
    ]
    g.attribs['transform'] = ' '.join(transform)
    
    # Calculate font size
    font_size = font_size * size_multipliers[2]  # Size 2 (1.5x)
    
    # Create text group with normalized rotation
    text_group = dwg.g()
    
    # For 180° orientation, counter-rotate the text to make it appear as 0°
    if flag['orientation'] == 180:
        text_group.attribs['transform'] = f"rotate(-180)"
    
    # Add text net_label_distance units above the pin point
    # The text coordinates are relative to the transformed group
    text_element = dwg.text(
        flag['net_name'],
        insert=(0, -net_label_distance * scale),  # Position above the pin point
        font_family='Arial',
        font_size=f'{font_size}px',
        text_anchor='middle',  # Center-justified
        fill='black'
    )
    
    # Add text to its group
    text_group.add(text_element)
    
    # Add text group to main group
    g.add(text_group)
    
    # Add the group to the drawing
    dwg.add(g) 