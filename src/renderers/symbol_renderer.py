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
        self._is_mirrored = False
        
    def create_group(self) -> svgwrite.container.Group:
        """Create a new group for a symbol.
        
        Returns:
            An SVG group element
        """
        self._current_group = self.dwg.g()
        self._is_mirrored = False
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
                
            # Set mirrored state
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
            self.logger.info(f"Rendering {len(texts)} text elements for {'mirrored' if self._is_mirrored else 'normal'} symbol")
            for text in texts:
                # Add mirrored state to text data
                text_data = text.copy()
                text_data['is_mirrored'] = self._is_mirrored
                self.logger.info(f"Text data before rendering: {text_data}")
                self.text_renderer.render(text_data, font_size, target_group=self._current_group)
                
        except Exception as e:
            self.logger.error(f"Failed to render texts: {str(e)}")
            raise

    def render_window_texts(self, symbol: Dict, symbol_def: Dict, font_size: float = 22.0) -> None:
        """Render window texts for the current symbol.
        
        Args:
            symbol: Dictionary containing symbol instance data
            symbol_def: Dictionary containing symbol definition
            font_size: Base font size in pixels
        """
        if not self._current_group:
            raise ValueError("No group created. Call create_group() first.")

        try:
            # Get window definitions from symbol definition
            windows = symbol_def.get('windows', {})
            self.logger.debug(f"Window definitions from symbol_def: {windows}")
            
            if not windows:
                self.logger.debug("No window definitions found in symbol")
                return

            # Get window overrides from symbol instance
            window_overrides = symbol.get('window_overrides', {})
            self.logger.debug(f"Window overrides from symbol: {window_overrides}")
            
            instance_name = symbol.get('property_0', 'Unknown')
            self.logger.debug(f"Processing window texts for symbol: {instance_name}")

            # Process each window
            for property_id, window_def in windows.items():
                self.logger.debug(f"Processing window {property_id} with default definition: {window_def}")
                
                # Convert property_id from string to integer for comparison (if possible)
                try:
                    int_property_id = int(property_id)
                    self.logger.debug(f"Converted property_id '{property_id}' to integer: {int_property_id}")
                except ValueError:
                    int_property_id = None
                    self.logger.debug(f"Could not convert property_id '{property_id}' to integer")
                
                # Check if there's an override for this window (using integer key)
                has_override = False
                if int_property_id is not None and int_property_id in window_overrides:
                    self.logger.debug(f"Found integer override for window {property_id}: {window_overrides[int_property_id]}")
                    has_override = True
                elif property_id in window_overrides:
                    self.logger.debug(f"Found string override for window {property_id}: {window_overrides[property_id]}")
                    has_override = True
                
                # Get the property value from the symbol instance
                property_value = symbol.get(f'property_{property_id}')
                self.logger.debug(f"Property value for {property_id}: {property_value}")
                
                if not property_value:
                    self.logger.debug(f"No value found for property {property_id}")
                    continue

                # Get window settings, using overrides if available
                window_settings = window_def
                if has_override:
                    self.logger.debug(f"Using override settings for window {property_id}")
                    if int_property_id is not None and int_property_id in window_overrides:
                        window_settings = window_overrides[int_property_id]
                    else:
                        window_settings = window_overrides[property_id]
                else:
                    self.logger.debug(f"Using default settings for window {property_id}")

                # Create text data
                text_data = {
                    'x': window_settings['x'],
                    'y': window_settings['y'],
                    'text': property_value,
                    'justification': window_settings['justification'],
                    'size_multiplier': window_settings['size_multiplier'],
                    'is_mirrored': self._is_mirrored
                }

                # Render the text
                self.logger.info(f"Rendering window text for property {property_id}: {text_data}")
                self.text_renderer.render(text_data, font_size, target_group=self._current_group)

        except Exception as e:
            self.logger.error(f"Failed to render window texts: {str(e)}")
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
            self._is_mirrored = False  # Reset mirrored state
            
        except Exception as e:
            self.logger.error(f"Failed to add group to drawing: {str(e)}")
            raise

    def render(self, symbol: Dict, stroke_width: float = 1.0) -> None:
        """Render a complete symbol.
        
        Args:
            symbol: Dictionary containing symbol data
            stroke_width: Width of lines
        """
        try:
            # Create a new group for the symbol
            self.create_group()
            
            # Set transformation if provided
            if 'rotation' in symbol and 'translation' in symbol:
                self.set_transformation(symbol['rotation'], symbol['translation'])
            
            # Render shapes if present
            if 'shapes' in symbol:
                self.render_shapes(symbol['shapes'], stroke_width)
            
            # Render texts if present
            if 'texts' in symbol:
                self.render_texts(symbol['texts'])
            
            # Debug log the contents of the symbol dict
            self.logger.debug(f"Symbol data keys: {list(symbol.keys())}")
            if 'symbol_def' in symbol:
                self.logger.debug(f"Symbol definition keys: {list(symbol['symbol_def'].keys())}")
            if 'window_overrides' in symbol:
                self.logger.debug(f"Window overrides present: {symbol['window_overrides']}")
            
            # Render window texts if present
            if 'symbol_def' in symbol:
                self.render_window_texts(symbol, symbol['symbol_def'])
            
            # Add the group to the drawing
            self.add_to_drawing()
            
        except Exception as e:
            self.logger.error(f"Failed to render symbol: {str(e)}")
            raise 