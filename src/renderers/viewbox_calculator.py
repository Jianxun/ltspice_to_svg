"""
Viewbox calculation module for SVG rendering.
Calculates the appropriate viewbox dimensions based on schematic elements.
"""
from typing import Dict, Tuple, List, Optional
from src.renderers.rendering_config import RenderingConfig
import logging

class ViewboxCalculator:
    """Calculator for SVG viewbox dimensions based on schematic elements."""
    
    # Default viewbox for empty schematics or when bounds are invalid
    DEFAULT_VIEWBOX = (0, 0, 100, 100)
    
    def __init__(self, config: Optional[RenderingConfig] = None):
        """Initialize the ViewboxCalculator with optional configuration.
        
        Args:
            config: Configuration object with rendering options. If None, 
                   default margin will be used.
        """
        self._reset_bounds()
        self._config = config or RenderingConfig()
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def _reset_bounds(self) -> None:
        """Reset the bounds to their initial values."""
        self._min_x = float('inf')
        self._min_y = float('inf')
        self._max_x = float('-inf')
        self._max_y = float('-inf')
        
    def _update_bounds(self, x1: float, y1: float, x2: float = None, y2: float = None) -> None:
        """Update the bounds with new coordinates.
        
        Args:
            x1, y1: First coordinate point
            x2, y2: Optional second coordinate point
        """
        self._min_x = min(self._min_x, x1)
        self._min_y = min(self._min_y, y1)
        self._max_x = max(self._max_x, x1)
        self._max_y = max(self._max_y, y1)
        
        if x2 is not None and y2 is not None:
            self._min_x = min(self._min_x, x2)
            self._min_y = min(self._min_y, y2)
            self._max_x = max(self._max_x, x2)
            self._max_y = max(self._max_y, y2)
            
    def calculate(self, schematic_data: Dict) -> Tuple[float, float, float, float]:
        """Calculate the viewBox for the SVG based on schematic bounds.
        
        The viewBox is calculated by finding the minimum and maximum coordinates
        of all elements in the schematic, then adding margin around the bounds.
        
        Args:
            schematic_data: Dictionary containing schematic elements
            
        Returns:
            tuple: (min_x, min_y, width, height)
        """
        if not schematic_data:
            self.logger.debug("Empty schematic, using default viewbox")
            return self.DEFAULT_VIEWBOX
            
        # Reset bounds
        self._reset_bounds()
        
        # Calculate bounds from wires
        self._include_wires(schematic_data.get('wires', []))
            
        # Calculate bounds from shapes
        self._include_shapes(schematic_data.get('shapes', {}))
        
        # Calculate bounds from flags
        self._include_flags(schematic_data.get('flags', []))
        
        # Check if any elements were included in the bounds calculation
        if (self._min_x == float('inf') or self._min_y == float('inf') or 
                self._max_x == float('-inf') or self._max_y == float('-inf')):
            self.logger.debug("No elements with coordinates found, using default viewbox")
            return self.DEFAULT_VIEWBOX
            
        # Calculate dimensions
        width = self._max_x - self._min_x
        height = self._max_y - self._min_y
        
        # Ensure there's at least some content (avoid division by zero)
        if width <= 0:
            width = 1.0
        if height <= 0:
            height = 1.0
        
        # Get margin percentage from configuration
        margin_percent = self._config.get_option("viewbox_margin", 10.0)
        
        # Add margin (percentage of the larger dimension)
        padding = max(width, height) * (margin_percent / 100.0)
        
        # Update bounds with padding
        min_x = self._min_x - padding
        min_y = self._min_y - padding
        width = width + 2 * padding
        height = height + 2 * padding
        
        # Ensure minimum size
        if width < 10:
            width = 10
        if height < 10:
            height = 10
            
        self.logger.debug(f"Calculated viewbox: {min_x},{min_y},{width},{height}")
        return (min_x, min_y, width, height)
        
    def _include_wires(self, wires: List[Dict]) -> None:
        """Include wires in the bounds calculation.
        
        Args:
            wires: List of wire dictionaries
        """
        for wire in wires:
            self._update_bounds(wire['x1'], wire['y1'], wire['x2'], wire['y2'])
            
    def _include_shapes(self, shapes: Dict) -> None:
        """Include shapes in the bounds calculation.
        
        Args:
            shapes: Dictionary containing shape lists by type
        """
        # Handle shapes based on format (list or dictionary)
        if isinstance(shapes, list):
            # Handle shapes as a list of shape objects with 'type' field
            for shape in shapes:
                shape_type = shape.get('type', '')
                if shape_type == 'line':
                    self._update_bounds(shape['x1'], shape['y1'], shape['x2'], shape['y2'])
                elif shape_type == 'rectangle':
                    self._update_bounds(shape['x'], shape['y'], shape['x'] + shape['width'], shape['y'] + shape['height'])
                elif shape_type == 'circle':
                    center_x, center_y = shape.get('x', 0), shape.get('y', 0)
                    radius = shape.get('radius', 0)
                    self._update_bounds(center_x - radius, center_y - radius, center_x + radius, center_y + radius)
        else:
            # Original approach: shapes as a dictionary of lists by shape type
            # Lines
            for line in shapes.get('lines', []):
                self._update_bounds(line['x1'], line['y1'], line['x2'], line['y2'])
                
            # Rectangles
            for rect in shapes.get('rectangles', []):
                self._update_bounds(rect['x1'], rect['y1'], rect['x2'], rect['y2'])
                
            # Circles
            for circle in shapes.get('circles', []):
                self._update_bounds(circle['x1'], circle['y1'], circle['x2'], circle['y2'])
                
            # Arcs
            for arc in shapes.get('arcs', []):
                self._update_bounds(arc['x1'], arc['y1'], arc['x2'], arc['y2'])
                
    def _include_flags(self, flags: List[Dict]) -> None:
        """Include flags in the bounds calculation.
        
        Args:
            flags: List of flag dictionaries
        """
        for flag in flags:
            self._update_bounds(flag['x'], flag['y']) 