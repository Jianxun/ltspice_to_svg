"""
Base renderer class that all other renderers inherit from.
"""
import svgwrite
import logging
from abc import ABC
from typing import Optional

class BaseRenderer(ABC):
    """Base renderer class that provides common functionality."""
    
    # Default stroke width for all renderers
    DEFAULT_STROKE_WIDTH = 2.0
    
    # Default base font size for all renderers
    DEFAULT_BASE_FONT_SIZE = 16.0
    
    @classmethod
    def set_default_stroke_width(cls, width: float) -> None:
        """Set the default stroke width for all renderers.
        
        Args:
            width: The new default stroke width
        """
        cls.DEFAULT_STROKE_WIDTH = width
        
    def __init__(self, dwg: Optional[svgwrite.Drawing] = None):
        self.dwg = dwg
        self.logger = logging.getLogger(self.__class__.__name__)
        self._stroke_width = self.DEFAULT_STROKE_WIDTH
        self._base_font_size = self.DEFAULT_BASE_FONT_SIZE
        
    @property
    def stroke_width(self) -> float:
        """Get the stroke width."""
        return self._stroke_width
        
    @stroke_width.setter
    def stroke_width(self, value: float) -> None:
        """Set the stroke width.
        
        Args:
            value: The new stroke width
            
        Raises:
            ValueError: If stroke_width is not positive.
        """
        if value <= 0:
            raise ValueError("Stroke width must be positive")
        self._stroke_width = value
        self.logger.debug(f"Stroke width set to {value}px")
        
    @property
    def base_font_size(self) -> float:
        """Get the base font size."""
        return self._base_font_size
        
    @base_font_size.setter
    def base_font_size(self, value: float) -> None:
        """Set the base font size.
        
        Args:
            value: The new base font size
            
        Raises:
            ValueError: If base_font_size is not positive.
        """
        if value <= 0:
            raise ValueError("Base font size must be positive")
        self._base_font_size = value
        self.logger.debug(f"Base font size set to {value}px") 