"""
Symbol renderer for LTspice schematics.
Handles rendering of circuit symbols in SVG format.
"""
import svgwrite
from typing import Dict, List, Optional
import math
import warnings

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
        no_text: Whether to skip rendering text elements
        no_symbol_text: Whether to skip rendering symbol text elements
    """
    symbol_name = symbol['symbol_name']
    
    # Skip if no drawing data available
    if symbol_name not in symbols_data:
        warnings.warn(f"No drawing data for symbol {symbol_name}")
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
        # Get window settings for instance name (type 0)
        window_settings = None
        
        # Only use window defaults from symbol
        if 'windows' in symbols_data[symbol_name]:
            for window in symbols_data[symbol_name]['windows']:
                if window['property_id'] == 0:
                    window_settings = {
                        'x': window['x'],
                        'y': window['y'],
                        'justification': window['justification'],
                        'size': window['size_multiplier']
                    }
                    print(f"[DEBUG] Using window default for {instance_name}")
                    break
        
        if window_settings:
            # Create text data with position relative to symbol origin
            text_data = {
                'x': window_settings['x'],
                'y': window_settings['y'],
                'text': instance_name,
                'justification': window_settings['justification'],
                'size_multiplier': window_settings['size']
            }
            print(f"[DEBUG] Rendering {instance_name} with window settings: {window_settings}")
            _add_symbol_text(dwg, g, text_data, scale, font_size, size_multipliers)
        else:
            # Default position if no window settings found
            text_data = {
                'x': 0,
                'y': -16,  # Above the symbol
                'text': instance_name,
                'justification': 'Center',
                'size_multiplier': 2
            }
            print(f"[DEBUG] Rendering {instance_name} with default settings")
            _add_symbol_text(dwg, g, text_data, scale, font_size, size_multipliers)
    
    # Add value text if available
    value = symbol.get('value', '')
    if value and not no_text:
        # Get window settings for value (type 3)
        window_settings = None
        
        # Only use window defaults from symbol
        if 'windows' in symbols_data[symbol_name]:
            for window in symbols_data[symbol_name]['windows']:
                if window['property_id'] == 3:
                    window_settings = {
                        'x': window['x'],
                        'y': window['y'],
                        'justification': window['justification'],
                        'size': window['size_multiplier']
                    }
                    print(f"[DEBUG] Using window default for value {value}")
                    break
        
        # Render value text if we have window settings
        if window_settings:
            # Create text data with position relative to symbol origin
            text_data = {
                'x': window_settings['x'],
                'y': window_settings['y'],
                'text': value,
                'justification': window_settings['justification'],
                'size_multiplier': window_settings['size']
            }
            print(f"[DEBUG] Rendering value {value} with window settings: {text_data}")
            _add_symbol_text(dwg, g, text_data, scale, font_size, size_multipliers)
    
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
            print(f"[DEBUG] Rendering symbol text '{text['text']}' with settings: {text_data}")
            _add_symbol_text(dwg, g, text_data, scale, font_size, size_multipliers)
    
    # Add lines with scaling
    for line in symbols_data[symbol_name]['lines']:
        line_attrs = {
            'stroke': 'black',
            'stroke-width': stroke_width,
            'stroke-linecap': 'round'
        }
        if 'style' in line:
            from .shape_renderer import _scale_dash_array
            scaled_style = _scale_dash_array(line['style'], stroke_width)
            if scaled_style:
                line_attrs['stroke-dasharray'] = scaled_style
        g.add(dwg.line(
            (line['x1'] * scale, line['y1'] * scale),
            (line['x2'] * scale, line['y2'] * scale),
            **line_attrs
        ))
    
    # Add circles with scaling
    for circle in symbols_data[symbol_name].get('circles', []):
        # Calculate center and radius from bounding box
        cx = (circle['x1'] + circle['x2']) / 2 * scale
        cy = (circle['y1'] + circle['y2']) / 2 * scale
        rx = abs(circle['x2'] - circle['x1']) / 2 * scale
        ry = abs(circle['y2'] - circle['y1']) / 2 * scale
        
        circle_attrs = {
            'stroke': 'black',
            'stroke-width': stroke_width,
            'fill': 'none'
        }
        if 'style' in circle:
            from .shape_renderer import _scale_dash_array
            scaled_style = _scale_dash_array(circle['style'], stroke_width)
            if scaled_style:
                circle_attrs['stroke-dasharray'] = scaled_style
        
        # For perfect circles, use circle element
        if abs(rx - ry) < 0.01:  # Allow small difference due to rounding
            g.add(dwg.circle(
                center=(cx, cy),
                r=rx,  # Use rx as radius
                **circle_attrs
            ))
        else:
            # For ellipses, use ellipse element
            g.add(dwg.ellipse(
                center=(cx, cy),
                r=(rx, ry),
                **circle_attrs
            ))
    
    # Add rectangles with scaling
    for rect in symbols_data[symbol_name].get('rectangles', []):
        rect_attrs = {
            'stroke': 'black',
            'stroke-width': stroke_width,
            'fill': 'none'
        }
        if 'style' in rect:
            from .shape_renderer import _scale_dash_array
            scaled_style = _scale_dash_array(rect['style'], stroke_width)
            if scaled_style:
                rect_attrs['stroke-dasharray'] = scaled_style
        g.add(dwg.rect(
            insert=(rect['x1'] * scale, rect['y1'] * scale),
            size=(
                (rect['x2'] - rect['x1']) * scale,
                (rect['y2'] - rect['y1']) * scale
            ),
            **rect_attrs
        ))
    
    # Add arcs with scaling
    for arc in symbols_data[symbol_name].get('arcs', []):
        # Calculate center and radii
        cx = (arc['x1'] + arc['x2']) / 2 * scale
        cy = (arc['y1'] + arc['y2']) / 2 * scale
        rx = abs(arc['x2'] - arc['x1']) / 2 * scale
        ry = abs(arc['y2'] - arc['y1']) / 2 * scale
        
        # Get start and end angles
        start_angle = arc['start_angle']
        end_angle = arc['end_angle']
        
        # SVG arc flags
        large_arc_flag = '1' if (end_angle - start_angle) % 360 > 180 else '0'
        sweep_flag = '1'  # Always draw arc clockwise
        
        # Calculate start and end points
        start_x = cx + rx * math.cos(math.radians(start_angle))
        start_y = cy + ry * math.sin(math.radians(start_angle))
        end_x = cx + rx * math.cos(math.radians(end_angle))
        end_y = cy + ry * math.sin(math.radians(end_angle))
        
        # Create SVG path for arc
        path_data = f"M {start_x},{start_y} A {rx},{ry} 0 {large_arc_flag} {sweep_flag} {end_x},{end_y}"
        
        arc_attrs = {
            'stroke': 'black',
            'stroke-width': stroke_width,
            'fill': 'none'
        }
        if 'style' in arc:
            from .shape_renderer import _scale_dash_array
            scaled_style = _scale_dash_array(arc['style'], stroke_width)
            if scaled_style:
                arc_attrs['stroke-dasharray'] = scaled_style
        g.add(dwg.path(
            d=path_data,
            **arc_attrs
        ))
    
    # Add the group to the drawing
    dwg.add(g)

def _add_symbol_text(dwg: svgwrite.Drawing, group: svgwrite.container.Group, 
                    text_data: Dict, scale: float, font_size: float, 
                    size_multipliers: Dict[int, float]) -> None:
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
    """
    print(f"[DEBUG] _add_symbol_text: Rendering text '{text_data['text']}'")
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