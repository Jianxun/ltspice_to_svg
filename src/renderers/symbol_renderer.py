"""
Symbol renderer for LTspice schematics.
Handles rendering of circuit symbols in SVG format.
"""
import svgwrite
from typing import Dict, Optional, Tuple, List, Union, Any
import logging
import warnings
from .base_renderer import BaseRenderer
from .shape_renderer import ShapeRenderer
from .text_renderer import TextRenderer
from .rendering_config import RenderingConfig
import os

class SymbolRenderer(BaseRenderer):
    """Renders LTspice symbols as SVG groups.
    
    This renderer creates a group for each symbol and delegates the rendering
    of individual elements (shapes and text) to specialized renderers.
    """
    
    def __init__(self, dwg: svgwrite.Drawing, config: Optional[RenderingConfig] = None):
        """Initialize the symbol renderer.
        
        Args:
            dwg: The SVG drawing to render into
            config: Optional configuration object. If None, a default one will be created.
        """
        super().__init__(dwg, config)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.shape_renderer = ShapeRenderer(dwg, config)
        self.text_renderer = TextRenderer(dwg, config)
        self._current_group = None
        self._is_mirrored = False
        self._symbol_def = None
        self._window_overrides = {}
        self._rotation_angle = 0
        
        # Initialize child renderers with base properties
        self.shape_renderer.stroke_width = self.stroke_width
        self.text_renderer.base_font_size = self.base_font_size
        
    @BaseRenderer.base_font_size.setter
    def base_font_size(self, value: float) -> None:
        """Override base_font_size setter to update TextRenderer's font size.
        
        Args:
            value: The new base font size
        """
        BaseRenderer.base_font_size.fset(self, value)  # Call parent's setter
        self.text_renderer.base_font_size = value  # Update TextRenderer's font size
        
    @BaseRenderer.stroke_width.setter
    def stroke_width(self, value: float) -> None:
        """Override stroke_width setter to update ShapeRenderer's stroke width.
        
        Args:
            value: The new stroke width
        """
        BaseRenderer.stroke_width.fset(self, value)  # Call parent's setter
        self.shape_renderer.stroke_width = value  # Update ShapeRenderer's stroke width
        
    def _calculate_symbol_dimensions(self, symbol_def: Dict) -> Tuple[float, float]:
        """Calculate the width and height of a symbol from its shapes.
        
        Args:
            symbol_def: Dictionary containing symbol definition with shapes
            
        Returns:
            Tuple of (width, height)
        """
        if not symbol_def:
            return (64.0, 64.0)  # Default size
            
        min_x = float('inf')
        min_y = float('inf')
        max_x = float('-inf')
        max_y = float('-inf')
        
        # Process all shape types
        for shape_type in ['lines', 'circles', 'rectangles', 'arcs']:
            shapes = symbol_def.get(shape_type, [])
            for shape in shapes:
                if shape_type == 'lines':
                    min_x = min(min_x, shape.get('x1', 0), shape.get('x2', 0))
                    min_y = min(min_y, shape.get('y1', 0), shape.get('y2', 0))
                    max_x = max(max_x, shape.get('x1', 0), shape.get('x2', 0))
                    max_y = max(max_y, shape.get('y1', 0), shape.get('y2', 0))
                elif shape_type == 'rectangles':
                    min_x = min(min_x, shape.get('x1', 0), shape.get('x2', 0))
                    min_y = min(min_y, shape.get('y1', 0), shape.get('y2', 0))
                    max_x = max(max_x, shape.get('x1', 0), shape.get('x2', 0))
                    max_y = max(max_y, shape.get('y1', 0), shape.get('y2', 0))
                elif shape_type == 'circles':
                    min_x = min(min_x, shape.get('x1', 0), shape.get('x2', 0))
                    min_y = min(min_y, shape.get('y1', 0), shape.get('y2', 0))
                    max_x = max(max_x, shape.get('x1', 0), shape.get('x2', 0))
                    max_y = max(max_y, shape.get('y1', 0), shape.get('y2', 0))
                elif shape_type == 'arcs':
                    min_x = min(min_x, shape.get('x1', 0), shape.get('x2', 0))
                    min_y = min(min_y, shape.get('y1', 0), shape.get('y2', 0))
                    max_x = max(max_x, shape.get('x1', 0), shape.get('x2', 0))
                    max_y = max(max_y, shape.get('y1', 0), shape.get('y2', 0))
        
        # If no shapes found, return default size
        if min_x == float('inf') or min_y == float('inf'):
            return (64.0, 64.0)
            
        width = max_x - min_x
        height = max_y - min_y
        
        # Ensure minimum size
        width = max(width, 1.0)
        height = max(height, 1.0)
        
        return (width, height)

    def begin_symbol(self, symbol_name: Optional[str] = None, symbol_def: Optional[Dict] = None) -> svgwrite.container.Group:
        """Begin rendering a new symbol by creating a group.
        
        Args:
            symbol_name: Optional name of the symbol to add as metadata
            symbol_def: Optional symbol definition to calculate dimensions
        
        Returns:
            An SVG group element
        """
        self._current_group = self.dwg.g()
        self._is_mirrored = False
        self._symbol_def = None
        self._window_overrides = {}
        self._rotation_angle = 0
        
        # Add symbol name as custom attribute if provided
        if symbol_name:
            self._current_group.attribs['s:type'] = symbol_name
            self.logger.debug(f"Added symbol type attribute: s:type={symbol_name}")
        
        # Add symbol dimensions as custom attributes if symbol definition is provided
        if symbol_def:
            width, height = self._calculate_symbol_dimensions(symbol_def)
            self._current_group.attribs['s:width'] = str(int(width))
            self._current_group.attribs['s:height'] = str(int(height))
            self.logger.debug(f"Added symbol dimensions: s:width={int(width)}, s:height={int(height)}")
        
        return self._current_group
        
    def set_transformation(self, rotation: str, translation: Tuple[float, float]) -> None:
        """Set the transformation for the current symbol group.
        
        Args:
            rotation: Rotation string (e.g. 'R0', 'M90')
            translation: Tuple of (x, y) coordinates
        
        Raises:
            ValueError: If begin_symbol() has not been called
        """
        if not self._current_group:
            raise ValueError("No symbol started. Call begin_symbol() first.")
            
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
                
            # Store rotation angle and set mirrored state
            self._rotation_angle = angle
            self._is_mirrored = (rotation_type == 'M')
            self.logger.info(f"Setting symbol transformation - Position: ({x},{y}), "
                           f"Rotation: {rotation}, Mirrored: {self._is_mirrored}")
                
            # Apply rotation first
            if angle != 0:
                transform.append(f"rotate({angle})")
                self.logger.debug(f"Added rotation transform: rotate({angle})")
                
            # Apply mirroring after rotation
            if self._is_mirrored:
                transform.append("scale(-1,1)")  # Mirror across Y axis
                self.logger.debug("Added mirroring transform: scale(-1,1)")
                
            # Set the transform
            self._current_group.attribs['transform'] = ' '.join(transform)
            self.logger.info(f"Final transform: {self._current_group.attribs['transform']}")
            
        except Exception as e:
            self.logger.error(f"Failed to set transformation: {str(e)}")
            raise
    
    def set_symbol_definition(self, symbol_def: Dict) -> None:
        """Set the symbol definition for window text rendering.
        
        Args:
            symbol_def: Dictionary containing symbol definition
            
        Raises:
            ValueError: If begin_symbol() has not been called
        """
        if not self._current_group:
            raise ValueError("No symbol started. Call begin_symbol() first.")
            
        self._symbol_def = symbol_def
    
    def set_window_overrides(self, window_overrides: Dict) -> None:
        """Set window overrides for the current symbol.
        
        Args:
            window_overrides: Dictionary mapping window IDs to override settings
            
        Raises:
            ValueError: If begin_symbol() has not been called
        """
        if not self._current_group:
            raise ValueError("No symbol started. Call begin_symbol() first.")
            
        self._window_overrides = window_overrides or {}
            
    def render_shapes(self, shapes: Dict[str, List[Dict]], stroke_width: float = None) -> None:
        """Render shapes for the current symbol.
        
        Args:
            shapes: Dictionary containing shape definitions by type
            stroke_width: Width of lines. If None, uses the instance's stroke width.
            
        Raises:
            ValueError: If begin_symbol() has not been called
        """
        if not self._current_group:
            raise ValueError("No symbol started. Call begin_symbol() first.")
            
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
            
    def render_texts(self, texts: List[Dict]) -> None:
        """Render text elements for the current symbol.
        
        Args:
            texts: List containing text element definitions
            
        Raises:
            ValueError: If begin_symbol() has not been called
        """
        if not self._current_group:
            raise ValueError("No symbol started. Call begin_symbol() first.")
        
        # Skip if text rendering is disabled
        if self.config.get_option('no_nested_symbol_text'):
            self.logger.debug("Skipping text rendering due to no_nested_symbol_text option")
            return
            
        try:
            self.logger.info(f"Rendering {len(texts)} text elements for {'mirrored' if self._is_mirrored else 'normal'} symbol")
            for text in texts:
                # Add mirrored state to text data
                text_data = text.copy()
                text_data['is_mirrored'] = self._is_mirrored
                self.logger.info(f"Text data before rendering: {text_data}")
                self.text_renderer.render(text_data, target_group=self._current_group)
                
        except Exception as e:
            self.logger.error(f"Failed to render texts: {str(e)}")
            raise

    def render_component_name(self, instance_name: str) -> None:
        """Render the component name (instance name) for the current symbol.
        
        Args:
            instance_name: The instance name of the component (e.g., "R1")
            
        Raises:
            ValueError: If begin_symbol() has not been called or symbol definition is not set
        """
        if not self._current_group:
            raise ValueError("No symbol started. Call begin_symbol() first.")
            
        if not self._symbol_def:
            raise ValueError("Symbol definition not set. Call set_symbol_definition() first.")
            
        # Skip if component name rendering is disabled
        if self.config.get_option('no_component_name'):
            self.logger.debug("Skipping component name rendering due to no_component_name option")
            return
            
        # Skip if instance name is empty
        if not instance_name:
            self.logger.debug("Skipping component name rendering: empty instance name")
            return
            
        # Render window for property 0 (instance name)
        self._render_window_property("0", instance_name)
        
    def render_component_value(self, value: str) -> None:
        """Render the component value for the current symbol.
        
        Args:
            value: The value of the component (e.g., "10k")
            
        Raises:
            ValueError: If begin_symbol() has not been called or symbol definition is not set
        """
        if not self._current_group:
            raise ValueError("No symbol started. Call begin_symbol() first.")
            
        if not self._symbol_def:
            raise ValueError("Symbol definition not set. Call set_symbol_definition() first.")
            
        # Skip if component value rendering is disabled
        if self.config.get_option('no_component_value'):
            self.logger.debug("Skipping component value rendering due to no_component_value option")
            return
            
        # Skip if value is empty
        if not value:
            self.logger.debug("Skipping component value rendering: empty value")
            return
            
        # Render window for property 3 (value)
        self._render_window_property("3", value)
        
    def _calculate_text_rotation_compensation(self, justification: str) -> tuple[int, str]:
        """Calculate rotation compensation and justification adjustment needed to keep text readable.
        
        Args:
            justification: Text justification ('Left', 'Right', 'Center', 'VTop', 'VBottom', etc.)
            
        Returns:
            Tuple of (rotation angle in degrees, adjusted justification)
        """
        if self._rotation_angle == 0 or self._rotation_angle == 90:
            # R0 and R90 work correctly (R90 by coincidence)
            return 0, justification
        elif self._rotation_angle == 180 or self._rotation_angle == 270:
            # R180 and R270: apply 180° counter-rotation and swap justifications 
            adjusted_justification = self._swap_justification(justification)
            return 180, adjusted_justification
        else:
            # Other rotation angles not handled yet
            self.logger.warning(f"Unhandled rotation angle: {self._rotation_angle}")
            return 0, justification
    
    def _swap_justification(self, justification: str) -> str:
        """Swap justification for rotated symbols.
        
        Args:
            justification: Original justification
            
        Returns:
            Swapped justification
        """
        justification_swaps = {
            'Left': 'Right',
            'Right': 'Left', 
            'VTop': 'VBottom',
            'VBottom': 'VTop',
            # Center justifications don't change
            'Center': 'Center',
            'VCenter': 'VCenter',
            'Top': 'Top',
            'Bottom': 'Bottom'
        }
        return justification_swaps.get(justification, justification)
    
    def _render_window_property(self, property_id: str, property_value: str) -> None:
        """Render a window text for a specific property.
        
        Args:
            property_id: The ID of the property (e.g., "0" for instance name)
            property_value: The value to render
            
        Raises:
            ValueError: If begin_symbol() has not been called or symbol definition is not set
        """
        if not self._current_group:
            raise ValueError("No symbol started. Call begin_symbol() first.")
            
        if not self._symbol_def:
            raise ValueError("Symbol definition not set. Call set_symbol_definition() first.")
            
        try:
            # Get window definitions from symbol definition
            windows = self._symbol_def.get('windows', {})
            
            if not windows:
                self.logger.debug("No window definitions found in symbol")
                return
                
            # Skip if this property doesn't have a window definition
            if property_id not in windows:
                self.logger.debug(f"No window definition for property {property_id}")
                return
                
            # Get window definition
            window_def = windows[property_id]
            
            # Try to convert property_id to integer for override lookup
            try:
                int_property_id = int(property_id)
            except ValueError:
                int_property_id = None
                
            # Check for overrides
            window_settings = window_def
            
            # Check integer key first, then string key
            if int_property_id is not None and int_property_id in self._window_overrides:
                window_settings = self._window_overrides[int_property_id]
                self.logger.debug(f"Using integer key override for window {property_id}")
            elif property_id in self._window_overrides:
                window_settings = self._window_overrides[property_id]
                self.logger.debug(f"Using string key override for window {property_id}")
                
            # Calculate rotation compensation for symbol rotation
            original_justification = window_settings['justification']
            rotation_compensation, adjusted_justification = self._calculate_text_rotation_compensation(original_justification)
            
            # Create text data
            text_data = {
                'x': window_settings['x'],
                'y': window_settings['y'],
                'text': property_value,
                'justification': adjusted_justification,
                'size_multiplier': window_settings.get('size_multiplier', 0),
                'is_mirrored': self._is_mirrored
            }
            
            # Add rotation compensation if needed
            if rotation_compensation != 0:
                text_data['rotation'] = rotation_compensation
                self.logger.debug(f"Adding rotation compensation: {rotation_compensation}° and justification swap '{original_justification}' -> '{adjusted_justification}' at symbol rotation {self._rotation_angle}°")
            
            # Render the text
            self.logger.debug(f"Rendering window text for property {property_id}: {text_data}")
            self.text_renderer.render(text_data, target_group=self._current_group)
                
        except Exception as e:
            self.logger.error(f"Failed to render window property {property_id}: {str(e)}")
            raise
            
    def render_custom_window_property(self, property_id: str, property_value: str) -> None:
        """Render a custom window property not handled by component name or value.
        
        Args:
            property_id: The ID of the property
            property_value: The value to render
            
        Raises:
            ValueError: If begin_symbol() has not been called or symbol definition is not set
        """
        if not self._current_group:
            raise ValueError("No symbol started. Call begin_symbol() first.")
            
        if not self._symbol_def:
            raise ValueError("Symbol definition not set. Call set_symbol_definition() first.")
            
        # Skip standard properties that have their own methods
        if property_id in ["0", "3"]:
            return
            
        # Render the window property
        self.logger.debug(f"Rendering custom window property {property_id} with value: {property_value}")
        self._render_window_property(property_id, property_value)
            
    def finish_symbol(self) -> None:
        """Finish rendering the current symbol and add it to the drawing.
        
        This should be called after all rendering operations are complete.
        
        Raises:
            ValueError: If begin_symbol() has not been called
        """
        if not self._current_group:
            raise ValueError("No symbol started. Call begin_symbol() first.")
            
        try:
            self.dwg.add(self._current_group)
            self._current_group = None  # Reset current group
            self._is_mirrored = False  # Reset mirrored state
            self._symbol_def = None  # Reset symbol definition
            self._window_overrides = {}  # Reset window overrides
            self._rotation_angle = 0  # Reset rotation angle
            
        except Exception as e:
            self.logger.error(f"Failed to add symbol to drawing: {str(e)}")
            raise

    # Legacy render method for backward compatibility
    def render(self, symbol: Dict, stroke_width: float = None) -> None:
        """DEPRECATED: Use specific rendering methods instead.
        
        This method is maintained for backward compatibility only and may be removed in future versions.
        The preferred approach is to use the individual rendering methods:
        
        ```python
        symbol_renderer.begin_symbol()
        symbol_renderer.set_transformation(rotation, position)
        symbol_renderer.set_symbol_definition(symbol_def)
        symbol_renderer.render_shapes(shapes)
        symbol_renderer.render_texts(texts)
        symbol_renderer.render_component_name(name)
        symbol_renderer.render_component_value(value)
        symbol_renderer.finish_symbol()
        ```
        
        Args:
            symbol: Dictionary containing symbol data
            stroke_width: Width of lines. If None, uses the instance's stroke width.
        """
        warnings.warn(
            "SymbolRenderer.render() is deprecated and will be removed in a future version. "
            "Use individual rendering methods instead.", 
            DeprecationWarning, 
            stacklevel=2
        )
        
        try:
            # Begin symbol
            symbol_name = symbol.get('symbol_name')
            symbol_def = symbol.get('symbol_def')
            self.begin_symbol(symbol_name, symbol_def)
            
            # Set transformation if provided
            if 'rotation' in symbol and 'translation' in symbol:
                self.set_transformation(symbol['rotation'], symbol['translation'])
            
            # Set symbol definition if present
            if 'symbol_def' in symbol:
                self.set_symbol_definition(symbol['symbol_def'])
                
            # Set window overrides if present
            if 'window_overrides' in symbol:
                self.set_window_overrides(symbol['window_overrides'])
            
            # Render shapes if present
            if 'shapes' in symbol:
                self.render_shapes(symbol['shapes'], stroke_width)
            
            # Render texts if present and not disabled
            if 'texts' in symbol and not symbol.get('no_nested_symbol_text', False):
                self.render_texts(symbol['texts'])
            
            # Render component name if present and not disabled
            if 'property_0' in symbol and not symbol.get('no_component_name', False):
                self.render_component_name(symbol['property_0'])
                
            # Render component value if present and not disabled
            if 'property_3' in symbol and not symbol.get('no_component_value', False):
                self.render_component_value(symbol['property_3'])
                
            # Finish symbol
            self.finish_symbol()
            
        except Exception as e:
            self.logger.error(f"Failed to render symbol: {str(e)}")
            raise 