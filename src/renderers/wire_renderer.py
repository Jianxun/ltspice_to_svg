"""
Wire rendering functions for SVG generation.
Handles rendering of wires with proper scaling and styling.
"""
import svgwrite
from typing import Dict, List, Tuple, Optional, Union
from .base_renderer import BaseRenderer

class WireRenderer(BaseRenderer):
    """Renderer for wire connections in the schematic."""
    
    def __init__(self, dwg: svgwrite.Drawing):
        super().__init__(dwg)
        
    def render(self, wire: Dict, stroke_width: float = None, target_group: Optional[svgwrite.container.Group] = None) -> None:
        """Render a single wire based on its properties.
        
        Args:
            wire: Dictionary containing wire properties
            stroke_width: Width of the stroke. If None, uses the default stroke width.
            target_group: Optional group to add the wire to. If None, adds to drawing.
        """
        # Use default stroke width if not specified
        if stroke_width is None:
            stroke_width = self.DEFAULT_STROKE_WIDTH
            
        style = {
            'stroke': 'black',
            'stroke-width': str(stroke_width),
            'stroke-linecap': 'round'
        }
        
        if 'style' in wire and wire['style'] is not None:
            style['stroke-dasharray'] = self._scale_dash_array(wire['style'], stroke_width)
            
        line_element = self.dwg.line(
            (str(wire['x1']), str(wire['y1'])),
            (str(wire['x2']), str(wire['y2'])),
            **style
        )
        
        if target_group is not None:
            target_group.add(line_element)
        else:
            self.dwg.add(line_element)
        
    def render_t_junction(self, x: float, y: float, dot_size: float) -> None:
        """
        Render a T-junction dot at the specified coordinates.
        
        Args:
            x: X coordinate of the junction
            y: Y coordinate of the junction
            dot_size: Size of the junction dot
        """
        self.logger.info(f"Rendering T-junction at ({x}, {y}) with size {dot_size}")
        
        # Create the circle element for the junction dot
        circle = self.dwg.circle(
            center=(x, y),
            r=dot_size,
            fill='black'
        )
        
        # Add the circle to the drawing
        self.dwg.add(circle) 