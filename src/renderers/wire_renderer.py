from src.renderers.base_renderer import BaseRenderer
import svgwrite

class WireRenderer(BaseRenderer):
    """Renderer for wire elements in the schematic."""
    
    def render(self, wire: dict, stroke_width: float = 1.0) -> None:
        """
        Render a wire element.
        
        Args:
            wire: Dictionary containing wire coordinates
                {
                    'x1': float,  # Start x coordinate
                    'y1': float,  # Start y coordinate
                    'x2': float,  # End x coordinate
                    'y2': float   # End y coordinate
                }
            stroke_width: Width of the wire line
        """
        self.logger.info(f"Rendering wire from ({wire['x1']}, {wire['y1']}) to ({wire['x2']}, {wire['y2']})")
        
        # Create the line element
        line = self.dwg.line(
            start=(wire['x1'], wire['y1']),
            end=(wire['x2'], wire['y2']),
            stroke='black',
            stroke_width=stroke_width
        )
        
        # Add the line to the drawing
        self.dwg.add(line)
        
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