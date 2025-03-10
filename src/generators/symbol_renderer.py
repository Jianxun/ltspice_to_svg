"""
Symbol renderer for LTspice schematics.
Handles rendering of circuit symbols in SVG format.
"""
import svgwrite
from typing import Dict, List, Optional
import math
import warnings
from .shape_renderer import (
    render_line,
    render_circle,
    render_rectangle,
    render_arc
)

def _render_window_text(dwg: svgwrite.Drawing, group: svgwrite.container.Group,
                       symbols_data: Dict[str, Dict], symbol_name: str,
                       text: str, property_id: int, default_settings: Dict,
                       scale: float, font_size: float, size_multipliers: Dict[int, float],
                       is_mirrored: bool = False) -> None:
    """Render text using window settings from symbol definition.
    
    Args:
        dwg: SVG drawing object
        group: SVG group object to add text to
        symbols_data: Dictionary mapping symbol names to their drawing data
        symbol_name: Name of the symbol
        text: Text content to render
        property_id: Window property ID (0 for instance name, 3 for value)
        default_settings: Default text settings if no window found
        scale: Scale factor for coordinates
        font_size: Base font size in pixels
        size_multipliers: Dictionary mapping size indices to font size multipliers
        is_mirrored: Whether the symbol is mirrored
    """
    # Get window settings from symbol
    window_settings = None
    if 'windows' in symbols_data[symbol_name]:
        for window in symbols_data[symbol_name]['windows']:
            if window['property_id'] == property_id:
                window_settings = {
                    'x': window['x'],
                    'y': window['y'],
                    'justification': window['justification'],
                    'size': window['size_multiplier']
                }
                break
    
    # Get justification from window settings or default
    justification = window_settings['justification'] if window_settings else default_settings['justification']
    
    # Flip horizontal justification if mirrored
    if is_mirrored:
        if justification == 'Left':
            justification = 'Right'
        elif justification == 'Right':
            justification = 'Left'
        # Center, VTop, VBottom remain unchanged
    
    # Create text data with position relative to symbol origin
    text_data = {
        'x': window_settings['x'] if window_settings else default_settings['x'],
        'y': window_settings['y'] if window_settings else default_settings['y'],
        'text': text,
        'justification': justification,
        'size_multiplier': window_settings['size'] if window_settings else default_settings['size_multiplier']
    }
    
    _add_symbol_text(dwg, group, text_data, scale, font_size, size_multipliers, is_mirrored=is_mirrored)

def render_symbol(dwg: svgwrite.Drawing, symbol: Dict, symbols_data: Dict[str, Dict], 
                 scale: float, stroke_width: float, font_size: float, 
                 size_multipliers: Dict[int, float], no_text: bool = False, 
                 no_symbol_text: bool = False) -> None:
    """Add a symbol to the SVG drawing.
    
    Args:
        dwg: SVG drawing object
        symbol: Dictionary containing symbol properties:
            - symbol_name: Name of the symbol
            - x: X coordinate
            - y: Y coordinate
            - rotation: Rotation string (e.g. 'R0', 'M90')
            - instance_name: Optional instance name
            - value: Optional value text
        symbols_data: Dictionary mapping symbol names to their drawing data
        scale: Scale factor for coordinates
        stroke_width: Width of lines
        font_size: Base font size in pixels
        size_multipliers: Dictionary mapping size indices to font size multipliers
        no_text: Whether to skip rendering text
        no_symbol_text: Whether to skip rendering symbol text
    """
    # Get symbol name and data
    symbol_name = symbol['symbol_name']
    if symbol_name not in symbols_data:
        warnings.warn(f"Symbol {symbol_name} not found in symbols data")
        return

    # Create a group for the symbol
    g = dwg.g()
    
    # Apply transformations
    rotation_str = symbol.get('rotation', 'R0')
    rotation_type = rotation_str[0]  # 'R' or 'M'
    try:
        angle = int(rotation_str[1:])
    except ValueError:
        print(f"Warning: Invalid rotation value: {rotation_str}")
        angle = 0
        
    # Build transform string
    transform = []
    
    # First translate to origin
    transform.append(f"translate({symbol['x'] * scale},{symbol['y'] * scale})")
    
    # Then apply mirroring if needed
    if rotation_type == 'M':
        transform.append("scale(-1,1)")  # Mirror across Y axis
        
    # Then apply rotation
    if angle != 0:
        transform.append(f"rotate({angle})")
        
    # Set the transform
    g.attribs['transform'] = ' '.join(transform)
    
    # Add instance name if text rendering is enabled
    instance_name = symbol.get('instance_name', '')
    if instance_name and not no_text:
        default_settings = {
            'x': 0,
            'y': -16,  # Above the symbol
            'justification': 'Center',
            'size_multiplier': 2
        }
        _render_window_text(dwg, g, symbols_data, symbol_name, instance_name, 0, default_settings, scale, font_size, size_multipliers, rotation_type == 'M')
    
    # Add value text if available
    value = symbol.get('value', '')
    if value and not no_text:
        default_settings = {
            'x': 0,
            'y': 16,  # Below the symbol
            'justification': 'Center',
            'size_multiplier': 2
        }
        _render_window_text(dwg, g, symbols_data, symbol_name, value, 3, default_settings, scale, font_size, size_multipliers, rotation_type == 'M')
    
    # Add regular text elements from symbol definition
    if not no_symbol_text:
        for text in symbols_data[symbol_name].get('texts', []):
            text_data = {
                'x': text['x'],
                'y': text['y'],
                'text': text['text'],
                'justification': text['justification'],
                'size_multiplier': text.get('size_multiplier', 2)  # Default to size 2 (1.5x)
            }
            _add_symbol_text(dwg, g, text_data, scale, font_size, size_multipliers, angle, rotation_type == 'M')
    
    # Add lines with scaling
    for line in symbols_data[symbol_name].get('lines', []):
        print(f"  Rendering line: ({line['x1']}, {line['y1']}) -> ({line['x2']}, {line['y2']})")
        render_line(
            dwg,
            line,
            scale,
            stroke_width,
            group=g
        )
    
    # Add circles with scaling
    for circle in symbols_data[symbol_name].get('circles', []):
        print(f"  Rendering circle: ({circle['x1']}, {circle['y1']}) -> ({circle['x2']}, {circle['y2']})")
        render_circle(
            dwg,
            circle,
            scale,
            stroke_width,
            group=g
        )
    
    # Add rectangles with scaling
    for rect in symbols_data[symbol_name].get('rectangles', []):
        print(f"  Rendering rectangle: ({rect['x1']}, {rect['y1']}) -> ({rect['x2']}, {rect['y2']})")
        render_rectangle(
            dwg,
            rect,
            scale,
            stroke_width,
            group=g
        )
    
    # Add arcs with scaling
    for arc in symbols_data[symbol_name].get('arcs', []):
        print(f"  Rendering arc: ({arc['x1']}, {arc['y1']}) -> ({arc['x2']}, {arc['y2']})")
        render_arc(
            dwg,
            arc,
            scale,
            stroke_width,
            group=g
        )
    
    # Add the group to the drawing
    dwg.add(g)

def _add_symbol_text(dwg: svgwrite.Drawing, group: svgwrite.container.Group, 
                    text_data: Dict, scale: float, font_size: float, 
                    size_multipliers: Dict[int, float], rotation: int = 0,
                    is_mirrored: bool = False) -> None:
    """Add a text element to the SVG drawing.
    
    Args:
        dwg: SVG drawing object
        group: SVG group object to add text to
        text_data: Dictionary containing text properties:
            - x: X coordinate
            - y: Y coordinate
            - text: Text content
            - justification: Text alignment ('Left', 'Right', 'Center', 'Top', 'Bottom', 'VTop', 'VBottom')
            - size_multiplier: Font size multiplier index (0-7)
        scale: Scale factor for coordinates
        font_size: Base font size in pixels
        size_multipliers: Dictionary mapping size indices to font size multipliers
        rotation: Symbol rotation angle in degrees (only used for regular symbol texts)
        is_mirrored: Whether the symbol is mirrored
    """
    # Get text properties with defaults
    x = text_data.get('x', 0)
    y = text_data.get('y', 0)
    content = text_data.get('text', '')
    justification = text_data.get('justification', 'Left')
    size_multiplier = text_data.get('size_multiplier', 2)  # Default to size 2 (1.5x)
    
    # Calculate font size
    font_size = font_size * size_multipliers[size_multiplier]
    
    # Create text group for rotation
    text_group = dwg.g()  # Use drawing to create group
    
    # Handle vertical text (VTop, VBottom)
    if justification in ['VTop', 'VBottom']:
        # Rotate text 90 degrees for vertical orientation
        text_group.attribs['transform'] = f"rotate(90, {x * scale}, {y * scale})"
        # Convert VTop/VBottom to Top/Bottom for standard alignment
        justification = 'Top' if justification == 'VTop' else 'Bottom'
    
    # Set text alignment
    if justification == 'Left':
        text_anchor = 'start'
    elif justification == 'Right':
        text_anchor = 'end'
    else:  # Center, Top, Bottom all use middle horizontal alignment
        text_anchor = 'middle'
    
    # Adjust vertical position based on justification
    if justification in ['Left', 'Center', 'Right']:
        y_offset = font_size * 0.3  # Move up to center vertically
    elif justification == 'Top':
        y_offset = font_size * 0.6  # Move down
    else:  # Bottom
        y_offset = font_size * 0.0  # Move up
    
    # Create text element
    text_element = _create_multiline_text(
        dwg,  # Use drawing for text creation
        content,
        x * scale,
        y * scale + y_offset,
        font_size,
        text_anchor
    )
    
    # Apply transformations
    if rotation != 0 or is_mirrored:
        transforms = []
        
        # Handle vertical text first if needed
        if justification in ['VTop', 'VBottom']:
            transforms.append(f"rotate(90, {x * scale}, {y * scale})")
        
        # Handle symbol rotation (only for regular symbol texts)
        if rotation != 0:
            # Counter-rotate to keep text upright
            transforms.append(f"rotate({-rotation}, {x * scale}, {y * scale})")
        
        # Handle mirroring (for both regular and window texts)
        if is_mirrored:
            # For mirrored symbols:
            # 1. Flip text anchor
            if text_anchor == 'start':
                text_anchor = 'end'
            elif text_anchor == 'end':
                text_anchor = 'start'
            # 2. Add horizontal flip at the text position
            # First translate to origin, then scale, then translate back
            transforms.append(f"translate({x * scale}, {y * scale}) scale(-1, 1) translate({-x * scale}, {-y * scale})")
        
        # Apply all transforms in sequence
        if transforms:
            text_group.attribs['transform'] = ' '.join(transforms)
    
    # Add text to group and group to parent
    text_group.add(text_element)
    group.add(text_group)

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