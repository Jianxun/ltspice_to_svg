"""
Base renderer class that all other renderers inherit from.
"""
import svgwrite
import logging
from abc import ABC
from typing import Optional
from src.renderers.rendering_config import RenderingConfig

class BaseRenderer(ABC):
    """Base renderer class that provides common functionality."""
    
    # Default stroke width for all renderers (for backward compatibility)
    DEFAULT_STROKE_WIDTH = 2.0
    
    # Default base font size for all renderers (for backward compatibility)
    DEFAULT_BASE_FONT_SIZE = 16.0
    
    @classmethod
    def set_default_stroke_width(cls, width: float) -> None:
        """Set the default stroke width for all renderers.
        
        Args:
            width: The new default stroke width
        """
        cls.DEFAULT_STROKE_WIDTH = width
        
    def __init__(self, dwg: Optional[svgwrite.Drawing] = None, config: Optional[RenderingConfig] = None):
        """Initialize the base renderer.
        
        Args:
            dwg: The SVG drawing object
            config: Optional configuration object. If None, a default one will be created.
        """
        self.dwg = dwg
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Use the provided config or create a default one
        self._config = config or RenderingConfig(
            stroke_width=self.DEFAULT_STROKE_WIDTH,
            base_font_size=self.DEFAULT_BASE_FONT_SIZE
        )
        
    @property
    def config(self) -> RenderingConfig:
        """Get the configuration object."""
        return self._config
        
    @config.setter
    def config(self, value: RenderingConfig) -> None:
        """Set the configuration object.
        
        Args:
            value: The new configuration object
            
        Raises:
            TypeError: If value is not a RenderingConfig
        """
        if not isinstance(value, RenderingConfig):
            raise TypeError(f"Configuration must be a RenderingConfig object, got {type(value).__name__}")
        self._config = value
        self.logger.debug("Updated configuration object")
        
    @property
    def stroke_width(self) -> float:
        """Get the stroke width from the configuration."""
        return self._config.get_option("stroke_width")
        
    @stroke_width.setter
    def stroke_width(self, value: float) -> None:
        """Set the stroke width in the configuration.
        
        Args:
            value: The new stroke width
            
        Raises:
            ValueError: If stroke_width is not positive.
        """
        # Validation happens in the config class
        self._config.set_option("stroke_width", value)
        self.logger.debug(f"Stroke width set to {value}px")
        
    @property
    def base_font_size(self) -> float:
        """Get the base font size from the configuration."""
        return self._config.get_option("base_font_size")
        
    @base_font_size.setter
    def base_font_size(self, value: float) -> None:
        """Set the base font size in the configuration.
        
        Args:
            value: The new base font size
            
        Raises:
            ValueError: If base_font_size is not positive.
        """
        # Validation happens in the config class
        self._config.set_option("base_font_size", value)
        self.logger.debug(f"Base font size set to {value}px") 