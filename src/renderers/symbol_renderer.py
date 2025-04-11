"""
Symbol renderer for LTspice schematics.
Handles rendering of circuit symbols in SVG format.
"""
import svgwrite
from typing import Dict, Optional, Tuple
import logging
from .base_renderer import BaseRenderer
from .shape_renderer import ShapeRenderer
from .text_renderer import TextRenderer

class SymbolRenderer(BaseRenderer):
    """Renders LTspice symbols as SVG groups.
    
    This renderer creates a group for each symbol and delegates the rendering
    of individual elements (shapes and text) to specialized renderers.
    """
    
    def __init__(self, dwg: svgwrite.Drawing):
        """Initialize the symbol renderer.
        
        Args:
            dwg: The SVG drawing to render into
        """
        super().__init__(dwg)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.shape_renderer = ShapeRenderer(dwg)
        self.text_renderer = TextRenderer(dwg)
        self._current_group = None
        
    def create_group(self) -> svgwrite.container.Group:
        """Create a new group for a symbol.
        
        Returns:
            An SVG group element
        """
        self._current_group = self.dwg.g()
        return self._current_group
        
    def set_transformation(self, rotation: str, translation: Tuple[float, float]) -> None:
        """Set the transformation for the current group.
        
        Args:
            rotation: Rotation string (e.g. 'R0', 'M90')
            translation: Tuple of (x, y) coordinates
        """
        if not self._current_group:
            raise ValueError("No group created. Call create_group() first.")
            
        try:
            transform = []
            
            # Apply translation
            x, y = translation
            transform.append(f"translate({x},{y})")
            
            # Handle rotation and mirroring
            rotation_type = rotation[0]  # 'R' or 'M'
            try:
                angle = int(rotation[1:])
            except ValueError:
                self.logger.warning(f"Invalid rotation value: {rotation}")
                angle = 0
                
            # Apply mirroring if needed
            if rotation_type == 'M':
                transform.append("scale(-1,1)")  # Mirror across Y axis
                
            # Apply rotation
            if angle != 0:
                transform.append(f"rotate({angle})")
                
            # Set the transform
            self._current_group.attribs['transform'] = ' '.join(transform)
            
        except Exception as e:
            self.logger.error(f"Failed to set transformation: {str(e)}")
            raise
            
    def render_shapes(self, shapes: Dict, stroke_width: float = 1.0) -> None:
        """Render shapes for the current symbol.
        
        Args:
            shapes: Dictionary containing shape definitions
            stroke_width: Width of lines
        """
        if not self._current_group:
            raise ValueError("No group created. Call create_group() first.")
            
        try:
            for shape_type, shape_list in shapes.items():
                for shape in shape_list:
                    # Add type to shape data
                    shape_data = shape.copy()
                    shape_data['type'] = shape_type.rstrip('s')  # Remove plural 's'
                    # Render the shape into the current group
                    self.shape_renderer.render(shape_data, stroke_width, target_group=self._current_group)
                    
        except Exception as e:
            self.logger.error(f"Failed to render shapes: {str(e)}")
            raise
            
    def render_texts(self, texts: Dict, font_size: float = 22.0,
                    size_multipliers: Optional[Dict[int, float]] = None) -> None:
        """Render texts for the current symbol.
        
        Args:
            texts: Dictionary containing text definitions
            font_size: Base font size in pixels
            size_multipliers: Dictionary mapping size indices to font size multipliers
        """
        if not self._current_group:
            raise ValueError("No group created. Call create_group() first.")
            
        try:
            for text in texts:
                self.text_renderer.render(text, font_size, target_group=self._current_group)
                
        except Exception as e:
            self.logger.error(f"Failed to render texts: {str(e)}")
            raise
            
    def add_to_drawing(self) -> None:
        """Add the current group to the drawing.
        
        This should be called after all rendering operations are complete.
        """
        if not self._current_group:
            raise ValueError("No group created. Call create_group() first.")
            
        try:
            self.dwg.add(self._current_group)
            self._current_group = None  # Reset current group
            
        except Exception as e:
            self.logger.error(f"Failed to add group to drawing: {str(e)}")
            raise 