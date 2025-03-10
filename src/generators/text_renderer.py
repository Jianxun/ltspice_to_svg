"""
Text rendering functions for SVG generation.
Handles rendering of text elements with proper justification, scaling, and multiline support.
"""
import svgwrite
from typing import Dict, List

def render_text(dwg: svgwrite.Drawing, text: Dict, scale: float, font_size: float, no_text: bool = False) -> None:
    """Render a text element with proper justification and scaling.
    
    Args:
        dwg: SVG drawing object
        text: Dictionary containing text properties (x, y, text, justification, size_multiplier)
        scale: Scale factor for coordinates
        font_size: Base font size in pixels
        no_text: Whether to skip text rendering
    """
    # Skip text rendering if no_text is True
    if no_text:
        return
        
    # Scale coordinates only (not font size)
    x = text['x'] * scale
    y = text['y'] * scale
    
    # Get size multiplier (already converted from index)
    size_multiplier = text.get('size_multiplier', 1.5)  # Default to 1.5x
    font_size = font_size * size_multiplier
    
    # Set text alignment based on justification
    if text['justification'] == 'Left':
        text_anchor = 'start'
    elif text['justification'] == 'Right':
        text_anchor = 'end'
    else:  # Center, Top, Bottom all use middle horizontal alignment
        text_anchor = 'middle'
    
    # Adjust vertical position based on justification
    # For Left/Center/Right, move up by half the font size to center vertically
    # For Top/Bottom, adjust by a third of the font size
    if text['justification'] in ['Left', 'Center', 'Right']:
        y_offset = font_size * 0.3  # Move up to center vertically
    elif text['justification'] == 'Top':
        y_offset = font_size * 0.6  # Move down
    else:  # Bottom
        y_offset = font_size * 0.0  # Move up
    
    # Use the text content directly without adding prefix markers
    content = text['text']
    
    # Create multiline text element
    text_element = _create_multiline_text(
        dwg,
        content,
        x,
        y + y_offset,
        font_size,
        text_anchor
    )
    dwg.add(text_element)

def _create_multiline_text(dwg: svgwrite.Drawing, text_content: str, x: float, y: float, 
                        font_size: float, text_anchor: str = 'start', 
                        line_spacing: float = 1.2) -> svgwrite.container.Group:
    """Create a group of text elements for multiline text.
    
    Args:
        dwg: SVG drawing object
        text_content: The text to render, may contain newlines
        x: X coordinate
        y: Y coordinate
        font_size: Font size in pixels
        text_anchor: Text alignment ('start', 'middle', or 'end')
        line_spacing: Line spacing multiplier (1.2 = 120% of font size)
        
    Returns:
        A group containing text elements for each line
    """
    # Create a group to hold all text elements
    group = dwg.g()
    
    # Split text into lines
    lines = text_content.split('\n')
    
    # Calculate line height
    line_height = font_size * line_spacing
    
    # Add each line as a separate text element
    for i, line in enumerate(lines):
        # Calculate y position for this line
        line_y = y + (i * line_height)
        
        # Create text element
        text_element = dwg.text(line,
                              insert=(x, line_y),
                              font_family='Arial',
                              font_size=f'{font_size}px',
                              text_anchor=text_anchor,
                              fill='black')
        group.add(text_element)
        
    return group 