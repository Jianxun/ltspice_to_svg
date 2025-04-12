"""
Shape rendering functions for SVG generation.
Handles rendering of lines, circles, rectangles, and arcs with proper scaling and styling.
"""
import svgwrite
from typing import Dict, List, Tuple, Optional, Union
import math
from .base_renderer import BaseRenderer

class ShapeRenderer(BaseRenderer):
    """Renderer for various shape types in the schematic."""
    
    # Line style patterns
    LINE_STYLE_SOLID = None  # No dash array for solid lines
    LINE_STYLE_DASH = "4,2"  # 4 units dash, 2 units gap
    LINE_STYLE_DOT = "0.001,2"  # Very small dash to create dots, 2 units gap
    LINE_STYLE_DASH_DOT = "4,2,0.001,2"  # Dash, gap, dot, gap
    LINE_STYLE_DASH_DOT_DOT = "4,2,0.001,2,0.001,2"  # Dash, gap, dot, gap, dot, gap
    
    def __init__(self, dwg: svgwrite.Drawing):
        super().__init__(dwg)
        
    def _scale_dash_array(self, pattern: str, stroke_width: float) -> str:
        """Scale a dash array pattern by the stroke width.
        
        Args:
            pattern: The dash array pattern string (e.g., "5,5")
            stroke_width: The stroke width to scale by
            
        Returns:
            The scaled dash array pattern
        """
        if not pattern:
            return ""
            
        # Split the pattern into individual lengths
        lengths = [float(x) for x in pattern.split(',')]
        
        # Scale each length by the stroke width
        scaled_lengths = [str(length * stroke_width) for length in lengths]
        
        # Join the scaled lengths back into a pattern string
        return ','.join(scaled_lengths)
        
    def render(self, shape: Dict, stroke_width: float = None, target_group: Optional[svgwrite.container.Group] = None) -> None:
        """Render a single shape based on its type.
        
        Args:
            shape: Dictionary containing shape properties
            stroke_width: Width of the stroke. If None, uses the default stroke width.
            target_group: Optional group to add the shape to. If None, adds to drawing.
        """
        # Use default stroke width if not specified
        if stroke_width is None:
            stroke_width = self.DEFAULT_STROKE_WIDTH
            
        shape_type = shape.get('type')
        if shape_type == 'line':
            self._render_line(shape, stroke_width, target_group)
        elif shape_type == 'circle':
            self._render_circle(shape, stroke_width, target_group)
        elif shape_type == 'rectangle':
            self._render_rectangle(shape, stroke_width, target_group)
        elif shape_type == 'arc':
            self._render_arc(shape, stroke_width, target_group)
        else:
            self.logger.warning(f"Unknown shape type: {shape_type}")
            
    def _render_line(self, line: Dict, stroke_width: float, target_group: Optional[svgwrite.container.Group] = None) -> None:
        """Render a line shape."""
        style = {
            'stroke': 'black',
            'stroke-width': str(stroke_width),
            'stroke-linecap': 'round'
        }
        
        if 'style' in line and line['style'] is not None:
            style['stroke-dasharray'] = self._scale_dash_array(line['style'], stroke_width)
            
        line_element = self.dwg.line(
            (str(line['x1']), str(line['y1'])),
            (str(line['x2']), str(line['y2'])),
            **style
        )
        
        if target_group is not None:
            target_group.add(line_element)
        else:
            self.dwg.add(line_element)
        
    def _render_circle(self, circle: Dict, stroke_width: float, target_group: Optional[svgwrite.container.Group] = None) -> None:
        """Render a circle or ellipse shape.
        
        Supports two formats:
        1. Bounding box format: {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
        2. Center-radius format: {'cx': cx, 'cy': cy, 'r': r}
        """
        # Check which format is being used
        if 'cx' in circle and 'cy' in circle and 'r' in circle:
            # Center-radius format
            cx = circle['cx']
            cy = circle['cy']
            rx = ry = circle['r']
        else:
            # Bounding box format
            rx = abs(circle['x2'] - circle['x1']) / 2
            ry = abs(circle['y2'] - circle['y1']) / 2
            cx = (circle['x1'] + circle['x2']) / 2
            cy = (circle['y1'] + circle['y2']) / 2
        
        style = {
            'stroke': 'black',
            'stroke-width': str(stroke_width),
            'fill': 'none'
        }
        
        if 'style' in circle:
            style['stroke-dasharray'] = self._scale_dash_array(circle['style'], stroke_width)
            style['stroke-linecap'] = 'round'
            
        if rx == ry:  # Perfect circle
            element = self.dwg.circle(
                center=(str(cx), str(cy)),
                r=str(rx),
                **style
            )
        else:  # Ellipse
            element = self.dwg.ellipse(
                center=(str(cx), str(cy)),
                r=(str(rx), str(ry)),
                **style
            )
            
        if target_group is not None:
            target_group.add(element)
        else:
            self.dwg.add(element)
            
    def _render_rectangle(self, rect: Dict, stroke_width: float, target_group: Optional[svgwrite.container.Group] = None) -> None:
        """Render a rectangle shape.
        
        Supports two formats:
        1. Bounding box format: {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
        2. Position-size format: {'x': x, 'y': y, 'width': width, 'height': height}
        """
        # Check which format is being used
        if 'x1' in rect and 'y1' in rect and 'x2' in rect and 'y2' in rect:
            # Bounding box format
            x = min(rect['x1'], rect['x2'])
            y = min(rect['y1'], rect['y2'])
            width = abs(rect['x2'] - rect['x1'])
            height = abs(rect['y2'] - rect['y1'])
        elif 'x' in rect and 'y' in rect and 'width' in rect and 'height' in rect:
            # Position-size format
            x = rect['x']
            y = rect['y']
            width = rect['width']
            height = rect['height']
        else:
            raise ValueError("Invalid rectangle format. Must use either x1,y1,x2,y2 or x,y,width,height")
        
        style = {
            'stroke': 'black',
            'stroke-width': str(stroke_width),
            'fill': 'none'
        }
        
        if 'style' in rect:
            style['stroke-dasharray'] = self._scale_dash_array(rect['style'], stroke_width)
            style['stroke-linecap'] = 'round'
            
            # For dotted/dashed rectangles, use path instead of rect
            path_data = [
                ('M', [(str(x), str(y))]),
                ('L', [(str(x + width), str(y))]),
                ('L', [(str(x + width), str(y + height))]),
                ('L', [(str(x), str(y + height))]),
                ('Z', [])
            ]
            element = self.dwg.path(d=path_data, **style)
        else:
            # For solid rectangles, use rect element
            element = self.dwg.rect(
                insert=(str(x), str(y)),
                size=(str(width), str(height)),
                **style
            )
            
        if target_group is not None:
            target_group.add(element)
        else:
            self.dwg.add(element)
            
    def _render_arc(self, arc: Dict, stroke_width: float, target_group: Optional[svgwrite.container.Group] = None) -> None:
        """Render an arc shape."""
        # Calculate center and radius
        cx = (arc['x1'] + arc['x2']) / 2
        cy = (arc['y1'] + arc['y2']) / 2
        rx = abs(arc['x2'] - arc['x1']) / 2
        ry = abs(arc['y2'] - arc['y1']) / 2
        
        # Convert angles to radians for path calculation
        start_angle = math.radians(arc['start_angle'])
        end_angle = math.radians(arc['end_angle'])
        
        # Calculate start and end points on the ellipse
        start_x = cx + rx * math.cos(start_angle)
        start_y = cy + ry * math.sin(start_angle)
        end_x = cx + rx * math.cos(end_angle)
        end_y = cy + ry * math.sin(end_angle)
        
        # Calculate angle difference
        angle_diff = (arc['end_angle'] - arc['start_angle'] + 360) % 360
        
        # Determine if arc should be drawn clockwise or counterclockwise
        # For counter-clockwise arcs, sweep should be 1
        sweep = 1  # Always draw counter-clockwise
        
        # Determine if we need to use the large arc
        # For angles > 180 degrees, large_arc should be 1
        large_arc = 1 if angle_diff > 180 else 0
        
        # Create path data
        path_data = [
            ('M', [(str(start_x), str(start_y))]),
            ('A', [
                str(rx), str(ry),  # radii
                '0',  # x-axis-rotation
                str(int(large_arc)), str(int(sweep)),  # large-arc and sweep flags
                str(end_x), str(end_y)  # end point
            ])
        ]
        
        style = {
            'stroke': 'black',
            'stroke-width': str(stroke_width),
            'fill': 'none',
            'stroke-linecap': 'round'
        }
        
        if 'style' in arc:
            style['stroke-dasharray'] = self._scale_dash_array(arc['style'], stroke_width)
            
        element = self.dwg.path(d=path_data, **style)
        
        if target_group is not None:
            target_group.add(element)
        else:
            self.dwg.add(element) 