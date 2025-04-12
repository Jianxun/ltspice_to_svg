"""
Base renderer class that all other renderers inherit from.
"""
import svgwrite
import logging
from abc import ABC

class BaseRenderer(ABC):
    """Base renderer class that provides common functionality."""
    
    # Default stroke width for all renderers
    DEFAULT_STROKE_WIDTH = 2.0
    
    @classmethod
    def set_default_stroke_width(cls, width: float) -> None:
        """Set the default stroke width for all renderers.
        
        Args:
            width: The new default stroke width
        """
        cls.DEFAULT_STROKE_WIDTH = width
        
    def __init__(self, dwg: svgwrite.Drawing):
        self.dwg = dwg
        self.logger = logging.getLogger(self.__class__.__name__) 