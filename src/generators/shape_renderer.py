"""
Shape rendering functions for SVG generation.
Handles rendering of lines, circles, rectangles, and arcs with proper scaling and styling.
"""
import svgwrite
from typing import Dict, List, Tuple, Optional, Union
import math

def _scale_dash_array(dash_array: str, stroke_width: float) -> str:
    """Scale a dash array pattern by the stroke width."""
    if not dash_array:
        return None
    return ','.join(str(float(x) * stroke_width) for x in dash_array.split(','))

def render_line(dwg: svgwrite.Drawing, line: Dict, scale: float, stroke_width: float, group: Optional[svgwrite.container.Group] = None) -> None:
    """Render a line shape.
    
    Args:
        dwg: SVG drawing object used to create elements
        line: Dictionary containing line properties (x1, y1, x2, y2, style)
        scale: Scale factor for coordinates
        stroke_width: Width of the stroke
        group: Optional group to add the line to. If None, adds to drawing
    """
    style = {}
    style['stroke'] = 'black'
    style['stroke_width'] = stroke_width
    style['stroke_linecap'] = 'round'
    
    if 'style' in line:
        style['stroke_dasharray'] = _scale_dash_array(line['style'], stroke_width)
        
    line_element = dwg.line(
        (line['x1'] * scale, line['y1'] * scale),
        (line['x2'] * scale, line['y2'] * scale),
        **style
    )
    
    if group is not None:
        group.add(line_element)
    else:
        dwg.add(line_element)

def render_circle(dwg: svgwrite.Drawing, circle: Dict, scale: float, stroke_width: float, group: Optional[svgwrite.container.Group] = None) -> None:
    """Render a circle or ellipse shape.
    
    Args:
        dwg: SVG drawing object used to create elements
        circle: Dictionary containing circle properties (x1, y1, x2, y2, style)
        scale: Scale factor for coordinates
        stroke_width: Width of the stroke
        group: Optional group to add the circle to. If None, adds to drawing
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
        style['stroke_linecap'] = 'round'  # Add round line caps for dotted/dashed styles
        
    if rx == ry:  # Perfect circle
        element = dwg.circle(
            center=(cx * scale, cy * scale),
            r=rx * scale,
            **style
        )
    else:  # Ellipse
        element = dwg.ellipse(
            center=(cx * scale, cy * scale),
            r=(rx * scale, ry * scale),
            **style
        )
    
    if group is not None:
        group.add(element)
    else:
        dwg.add(element)

def render_rectangle(dwg: svgwrite.Drawing, rect: Dict, scale: float, stroke_width: float, group: Optional[svgwrite.container.Group] = None) -> None:
    """Render a rectangle shape.
    
    Args:
        dwg: SVG drawing object used to create elements
        rect: Dictionary containing rectangle properties (x1, y1, x2, y2, style)
        scale: Scale factor for coordinates
        stroke_width: Width of the stroke
        group: Optional group to add the rectangle to. If None, adds to drawing
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
        element = dwg.path(d=path_data, **style)
    else:
        # For solid rectangles, use rect element
        element = dwg.rect(
            insert=(x * scale, y * scale),
            size=(width * scale, height * scale),
            **style
        )
    
    if group is not None:
        group.add(element)
    else:
        dwg.add(element)

def render_arc(dwg: svgwrite.Drawing, arc: Dict, scale: float, stroke_width: float, group: Optional[svgwrite.container.Group] = None) -> None:
    """Render an arc shape.
    
    Args:
        dwg: SVG drawing object used to create elements
        arc: Dictionary containing arc properties (x1, y1, x2, y2, start_angle, end_angle, style)
        scale: Scale factor for coordinates
        stroke_width: Width of the stroke
        group: Optional group to add the arc to. If None, adds to drawing
    """
    # Calculate center and radius
    cx = (arc['x1'] + arc['x2']) / 2
    cy = (arc['y1'] + arc['y2']) / 2
    rx = abs(arc['x2'] - arc['x1']) / 2
    ry = abs(arc['y2'] - arc['y1']) / 2
    
    # Use control points directly for start and end points
    start_x = arc['x1']
    start_y = arc['y1']
    end_x = arc['x2']
    end_y = arc['y2']
    
    # Convert angles to radians for path calculation
    start_angle = math.radians(arc['start_angle'])
    end_angle = math.radians(arc['end_angle'])
    
    # Determine if arc should be drawn clockwise or counterclockwise
    angle_diff = (end_angle - start_angle + 2 * math.pi) % (2 * math.pi)
    large_arc = angle_diff > math.pi
    sweep = angle_diff > 0
    
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
        style['stroke_linecap'] = 'round'  # Add round line caps for dotted/dashed styles
        
    element = dwg.path(d=path_data, **style)
    
    if group is not None:
        group.add(element)
    else:
        dwg.add(element)

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

def render_t_junction(dwg, x: float, y: float, scale: float, stroke_width: float, dot_size_multiplier: float) -> None:
    """Render a T-junction with a dot.
    
    Args:
        dwg: SVG drawing object
        x, y: Junction coordinates
        scale: Scale factor for coordinates
        stroke_width: Width of the line
        dot_size_multiplier: Size of junction dot relative to stroke width
    """
    # Draw the dot
    dot_radius = stroke_width * dot_size_multiplier
    dwg.add(dwg.circle(
        center=(x * scale, y * scale),
        r=dot_radius,
        fill='black'
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