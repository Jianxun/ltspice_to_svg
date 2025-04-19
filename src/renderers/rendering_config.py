"""
Configuration class for SVG rendering options.
"""
import logging
from typing import Any, Dict, Optional, Union


class RenderingConfig:
    """Configuration class for SVG rendering options."""

    # Default values for all rendering options
    DEFAULT_OPTIONS = {
        # Text rendering options
        "no_schematic_comment": False,
        "no_spice_directive": False,
        "no_nested_symbol_text": False,
        "no_component_name": False,
        "no_component_value": False,
        
        # General rendering options
        "stroke_width": 3.0,
        "base_font_size": 16.0,
        "dot_size_multiplier": 1.5,
    }
    
    def __init__(self, **kwargs) -> None:
        """Initialize the configuration with default values and any overrides.
        
        Args:
            **kwargs: Keyword arguments to override default options.
            
        Raises:
            ValueError: If any of the provided options are not recognized.
        """
        self._options = self.DEFAULT_OPTIONS.copy()
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Apply any provided overrides
        if kwargs:
            self.update_options(**kwargs)
    
    def update_options(self, **kwargs) -> None:
        """Update multiple configuration options at once.
        
        Args:
            **kwargs: Keyword arguments with option names and values.
            
        Raises:
            ValueError: If any of the provided options are not recognized.
        """
        # Validate the option names
        invalid_options = [key for key in kwargs if key not in self._options]
        if invalid_options:
            raise ValueError(f"Unknown configuration options: {', '.join(invalid_options)}")
        
        # Update the options
        for key, value in kwargs.items():
            self._validate_option_value(key, value)
            self._options[key] = value
            self.logger.debug(f"Updated option '{key}' to {value}")
    
    def set_option(self, name: str, value: Any) -> None:
        """Set a single configuration option.
        
        Args:
            name: The name of the option to set.
            value: The new value for the option.
            
        Raises:
            ValueError: If the option name is not recognized or the value is invalid.
        """
        if name not in self._options:
            raise ValueError(f"Unknown configuration option: {name}")
        
        self._validate_option_value(name, value)
        self._options[name] = value
        self.logger.debug(f"Set option '{name}' to {value}")
    
    def get_option(self, name: str, default: Optional[Any] = None) -> Any:
        """Get the value of a configuration option.
        
        Args:
            name: The name of the option to get.
            default: The default value to return if the option is not found.
            
        Returns:
            The value of the option, or the default if not found.
        """
        return self._options.get(name, default)
    
    def set_text_options(self, **kwargs) -> None:
        """Set multiple text rendering options at once.
        
        Args:
            **kwargs: Keyword arguments with text option names and boolean values.
                Supported options: no_schematic_comment, no_spice_directive,
                no_nested_symbol_text, no_component_name, no_component_value
                
        Raises:
            ValueError: If any of the provided options are not text options or values are not boolean.
        """
        # Define all text options
        text_options = {
            "no_schematic_comment",
            "no_spice_directive",
            "no_nested_symbol_text",
            "no_component_name",
            "no_component_value"
        }
        
        # Validate that all provided options are text options
        non_text_options = [key for key in kwargs if key not in text_options]
        if non_text_options:
            raise ValueError(f"Not text rendering options: {', '.join(non_text_options)}")
        
        # Update the options
        self.update_options(**kwargs)
    
    def get_all_options(self) -> Dict[str, Any]:
        """Get a copy of all configuration options.
        
        Returns:
            Dict[str, Any]: A copy of all configuration options.
        """
        return self._options.copy()
    
    def _validate_option_value(self, name: str, value: Any) -> None:
        """Validate that the option value is of the correct type.
        
        Args:
            name: The name of the option.
            value: The value to validate.
            
        Raises:
            ValueError: If the value is not of the correct type.
        """
        # Define the expected types for each option category
        text_options = {
            "no_schematic_comment",
            "no_spice_directive",
            "no_nested_symbol_text",
            "no_component_name",
            "no_component_value"
        }
        numeric_options = {
            "stroke_width",
            "base_font_size",
            "dot_size_multiplier"
        }
        
        # Validate based on option category
        if name in text_options and not isinstance(value, bool):
            raise ValueError(f"Option '{name}' must be a boolean, got {type(value).__name__}")
        elif name in numeric_options and not isinstance(value, (int, float)):
            raise ValueError(f"Option '{name}' must be a number, got {type(value).__name__}")
        
        # Additional validation for numeric values
        if name in numeric_options and value <= 0:
            raise ValueError(f"Option '{name}' must be positive, got {value}") 