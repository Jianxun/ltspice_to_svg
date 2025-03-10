"""
Shape rendering functions for SVG generation.
Handles rendering of lines, circles, rectangles, and arcs with proper scaling and styling.
"""
import svgwrite
from typing import Dict, List, Tuple, Optional
import math

def _scale_dash_array(dash_array: str, stroke_width: float) -> str:
    """Scale a dash array pattern by the stroke width."""
    if not dash_array:
        return None
    return ','.join(str(float(x) * stroke_width) for x in dash_array.split(','))

def _create_line(dwg: svgwrite.Drawing, x1: float, y1: float, x2: float, y2: float,
                stroke_width: float, style: Optional[str] = None,
                group: Optional[svgwrite.container.Group] = None) -> svgwrite.base.BaseElement:
    """Create a line element with optional style.
    
    Args:
        dwg: SVG drawing object
        x1, y1: Start point coordinates
        x2, y2: End point coordinates
        stroke_width: Width of the line
        style: Optional dash style
        group: Optional group to add the line to
        
    Returns:
        The created line element
    """
    line_attrs = {
        'stroke': 'black',
        'stroke-width': stroke_width,
        'stroke-linecap': 'round'
    }
    if style:
        scaled_style = _scale_dash_array(style, stroke_width)
        if scaled_style:
            line_attrs['stroke-dasharray'] = scaled_style
            
    line = dwg.line((x1, y1), (x2, y2), **line_attrs)
    if group:
        group.add(line)
    return line

def _create_circle(dwg: svgwrite.Drawing, x1: float, y1: float, x2: float, y2: float,
                  stroke_width: float, style: Optional[str] = None,
                  group: Optional[svgwrite.container.Group] = None) -> svgwrite.base.BaseElement:
    """Create a circle or ellipse element.
    
    Args:
        dwg: SVG drawing object
        x1, y1: First point of bounding box
        x2, y2: Second point of bounding box
        stroke_width: Width of the stroke
        style: Optional dash style
        group: Optional group to add the circle to
        
    Returns:
        The created circle/ellipse element
    """
    # Calculate center and radii
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    rx = abs(x2 - x1) / 2
    ry = abs(y2 - y1) / 2
    
    circle_attrs = {
        'stroke': 'black',
        'stroke-width': stroke_width,
        'fill': 'none'
    }
    if style:
        scaled_style = _scale_dash_array(style, stroke_width)
        if scaled_style:
            circle_attrs['stroke-dasharray'] = scaled_style
    
    # For perfect circles, use circle element
    if abs(rx - ry) < 0.01:  # Allow small difference due to rounding
        circle = dwg.circle(center=(cx, cy), r=rx, **circle_attrs)
    else:
        # For ellipses, use ellipse element
        circle = dwg.ellipse(center=(cx, cy), r=(rx, ry), **circle_attrs)
        
    if group:
        group.add(circle)
    return circle

def _create_rectangle(dwg: svgwrite.Drawing, x1: float, y1: float, x2: float, y2: float,
                     stroke_width: float, style: Optional[str] = None,
                     group: Optional[svgwrite.container.Group] = None) -> svgwrite.base.BaseElement:
    """Create a rectangle element.
    
    Args:
        dwg: SVG drawing object
        x1, y1: First point of rectangle
        x2, y2: Second point of rectangle
        stroke_width: Width of the stroke
        style: Optional dash style
        group: Optional group to add the rectangle to
        
    Returns:
        The created rectangle element
    """
    rect_attrs = {
        'stroke': 'black',
        'stroke-width': stroke_width,
        'fill': 'none'
    }
    if style:
        scaled_style = _scale_dash_array(style, stroke_width)
        if scaled_style:
            rect_attrs['stroke-dasharray'] = scaled_style
            
    rect = dwg.rect(
        insert=(x1, y1),
        size=(x2 - x1, y2 - y1),
        **rect_attrs
    )
    if group:
        group.add(rect)
    return rect

def _create_arc(dwg: svgwrite.Drawing, x1: float, y1: float, x2: float, y2: float,
                start_angle: float, end_angle: float, stroke_width: float,
                style: Optional[str] = None, group: Optional[svgwrite.container.Group] = None) -> svgwrite.base.BaseElement:
    """Create an arc element.
    
    Args:
        dwg: SVG drawing object
        x1, y1: First point of bounding box
        x2, y2: Second point of bounding box
        start_angle: Start angle in degrees
        end_angle: End angle in degrees
        stroke_width: Width of the stroke
        style: Optional dash style
        group: Optional group to add the arc to
        
    Returns:
        The created arc element
    """
    # Calculate center and radii
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    rx = abs(x2 - x1) / 2
    ry = abs(y2 - y1) / 2
    
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
    if style:
        scaled_style = _scale_dash_array(style, stroke_width)
        if scaled_style:
            arc_attrs['stroke-dasharray'] = scaled_style
            
    arc = dwg.path(d=path_data, **arc_attrs)
    if group:
        group.add(arc)
    return arc

def render_line(dwg: svgwrite.Drawing, line: Dict, scale: float, stroke_width: float) -> None:
    """Render a line shape.
    
    Args:
        dwg: SVG drawing object
        line: Dictionary containing line properties (x1, y1, x2, y2, style)
        scale: Scale factor for coordinates
        stroke_width: Width of the stroke
    """
    style = {}
    style['stroke'] = 'black'
    style['stroke_width'] = stroke_width
    style['stroke_linecap'] = 'round'
    
    if 'style' in line:
        style['stroke_dasharray'] = _scale_dash_array(line['style'], stroke_width)
        
    dwg.add(dwg.line(
        (line['x1'] * scale, line['y1'] * scale),
        (line['x2'] * scale, line['y2'] * scale),
        **style
    ))

def render_circle(dwg: svgwrite.Drawing, circle: Dict, scale: float, stroke_width: float) -> None:
    """Render a circle or ellipse shape.
    
    Args:
        dwg: SVG drawing object
        circle: Dictionary containing circle properties (x1, y1, x2, y2, style)
        scale: Scale factor for coordinates
        stroke_width: Width of the stroke
    """
    # Calculate radius from bounding box
    rx = abs(circle['x2'] - circle['x1']) / 2
    ry = abs(circle['y2'] - circle['y1']) / 2
    cx = (circle['x1'] + circle['x2']) / 2
    cy = (circle['y1'] + circle['y2']) / 2
    
    style = {}
    style['stroke'] = 'black'
    style['stroke_width'] = stroke_width
    style['fill'] = 'none'
    
    if 'style' in circle:
        style['stroke_dasharray'] = _scale_dash_array(circle['style'], stroke_width)
        
    if rx == ry:  # Perfect circle
        dwg.add(dwg.circle(
            center=(cx * scale, cy * scale),
            r=rx * scale,
            **style
        ))
    else:  # Ellipse
        dwg.add(dwg.ellipse(
            center=(cx * scale, cy * scale),
            r=(rx * scale, ry * scale),
            **style
        ))

def render_rectangle(dwg: svgwrite.Drawing, rect: Dict, scale: float, stroke_width: float) -> None:
    """Render a rectangle shape.
    
    Args:
        dwg: SVG drawing object
        rect: Dictionary containing rectangle properties (x1, y1, x2, y2, style)
        scale: Scale factor for coordinates
        stroke_width: Width of the stroke
    """
    x = min(rect['x1'], rect['x2'])
    y = min(rect['y1'], rect['y2'])
    width = abs(rect['x2'] - rect['x1'])
    height = abs(rect['y2'] - rect['y1'])
    
    style = {}
    style['stroke'] = 'black'
    style['stroke_width'] = stroke_width
    style['fill'] = 'none'
    
    if 'style' in rect:
        style['stroke_dasharray'] = _scale_dash_array(rect['style'], stroke_width)
        style['stroke_linecap'] = 'round'  # Add round line caps for dotted/dashed styles
        
        # For dotted/dashed rectangles, use path instead of rect to get proper line caps
        # Create path data for the rectangle
        path_data = [
            # Move to top-left corner
            ('M', [(x * scale, y * scale)]),
            # Draw top line
            ('L', [(x * scale + width * scale, y * scale)]),
            # Draw right line
            ('L', [(x * scale + width * scale, y * scale + height * scale)]),
            # Draw bottom line
            ('L', [(x * scale, y * scale + height * scale)]),
            # Close path (back to top-left)
            ('Z', [])
        ]
        dwg.add(dwg.path(d=path_data, **style))
    else:
        # For solid rectangles, use rect element
        dwg.add(dwg.rect(
            insert=(x * scale, y * scale),
            size=(width * scale, height * scale),
            **style
        ))

def render_arc(dwg: svgwrite.Drawing, arc: Dict, scale: float, stroke_width: float) -> None:
    """Render an arc shape.
    
    Args:
        dwg: SVG drawing object
        arc: Dictionary containing arc properties (x1, y1, x2, y2, start_angle, end_angle, style)
        scale: Scale factor for coordinates
        stroke_width: Width of the stroke
    """
    # Calculate center and radius
    cx = (arc['x1'] + arc['x2']) / 2
    cy = (arc['y1'] + arc['y2']) / 2
    rx = abs(arc['x2'] - arc['x1']) / 2
    ry = abs(arc['y2'] - arc['y1']) / 2
    
    # Convert angles to radians for path calculation
    start_angle = math.radians(arc['start_angle'])
    end_angle = math.radians(arc['end_angle'])
    
    # Calculate start and end points
    start_x = cx + rx * math.cos(start_angle)
    start_y = cy + ry * math.sin(start_angle)
    end_x = cx + rx * math.cos(end_angle)
    end_y = cy + ry * math.sin(end_angle)
    
    # Determine if arc should be drawn clockwise or counterclockwise
    large_arc = abs(end_angle - start_angle) > math.pi
    sweep = end_angle > start_angle
    
    # Create path data
    path_data = [
        ('M', [(start_x * scale, start_y * scale)]),
        ('A', [
            rx * scale, ry * scale,  # radii
            0,  # x-axis-rotation
            int(large_arc), int(sweep),  # large-arc and sweep flags
            end_x * scale, end_y * scale  # end point
        ])
    ]
    
    style = {}
    style['stroke'] = 'black'
    style['stroke_width'] = stroke_width
    style['fill'] = 'none'
    
    if 'style' in arc:
        style['stroke_dasharray'] = _scale_dash_array(arc['style'], stroke_width)
        
    dwg.add(dwg.path(d=path_data, **style))

def render_wire(dwg, wire: Dict, scale: float, stroke_width: float) -> None:
    """Render a wire as an SVG line.
    
    Args:
        dwg: SVG drawing object
        wire: Dictionary containing wire properties (x1, y1, x2, y2)
        scale: Scale factor for coordinates
        stroke_width: Width of the line
    """
    dwg.add(dwg.line(
        (wire['x1'] * scale, wire['y1'] * scale),
        (wire['x2'] * scale, wire['y2'] * scale),
        stroke='black',
        stroke_width=stroke_width,
        stroke_linecap='round'
    ))

def render_t_junction(dwg: svgwrite.Drawing, x: float, y: float, scale: float, stroke_width: float, dot_size_multiplier: float) -> None:
    """Render a T-junction dot.
    
    Args:
        dwg: SVG drawing object
        x: X coordinate of the T-junction
        y: Y coordinate of the T-junction
        scale: Scale factor for coordinates
        stroke_width: Width of the stroke
        dot_size_multiplier: Size of junction dots relative to stroke width
    """
    dwg.add(dwg.circle(
        center=(x * scale, y * scale),
        r=stroke_width * dot_size_multiplier,
        fill='black',
        stroke='none'
    ))

def render_shapes(dwg, shapes: Dict, scale: float, stroke_width: float, dot_size_multiplier: float = 0.75) -> None:
    """Render all shapes in the schematic.
    
    Args:
        dwg: SVG drawing object
        shapes: Dictionary containing all shape types
        scale: Scale factor for coordinates
        stroke_width: Width of lines
        dot_size_multiplier: Size of junction dots relative to stroke width
    """
    # Add T-junctions
    for x, y in shapes.get('t_junctions', []):
        render_t_junction(dwg, x, y, scale, stroke_width, dot_size_multiplier)
        
    # Add wires
    for wire in shapes.get('wires', []):
        render_wire(dwg, wire, scale, stroke_width)
        
    # Add lines
    for line in shapes.get('lines', []):
        render_line(dwg, line, scale, stroke_width)
        
    # Add circles
    for circle in shapes.get('circles', []):
        render_circle(dwg, circle, scale, stroke_width)
        
    # Add rectangles
    for rect in shapes.get('rectangles', []):
        render_rectangle(dwg, rect, scale, stroke_width)
        
    # Add arcs
    for arc in shapes.get('arcs', []):
        render_arc(dwg, arc, scale, stroke_width) 