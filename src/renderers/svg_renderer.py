import svgwrite
import logging
from typing import Dict, Optional
from src.renderers.base_renderer import BaseRenderer
from src.renderers.wire_renderer import WireRenderer
from src.renderers.symbol_renderer import SymbolRenderer
from src.renderers.text_renderer import TextRenderer
from src.renderers.shape_renderer import ShapeRenderer
from src.renderers.flag_renderer import FlagRenderer
from src.renderers.viewbox_calculator import ViewboxCalculator
from src.renderers.rendering_config import RenderingConfig

class SVGRenderer(BaseRenderer):
    def __init__(self, config: Optional[RenderingConfig] = None):
        self.dwg = None
        self.schematic_data = None
        self.view_box = None
        self._renderers = {}
        self.symbol_data = None  # Add symbol data storage
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Initialize BaseRenderer with None for dwg and the config
        # The drawing will be set later in create_drawing
        super().__init__(None, config)
        
        # Initialize viewbox calculator
        self._viewbox_calculator = ViewboxCalculator()
        
    # Property getters and setters for text rendering options
    @property
    def no_schematic_comment(self) -> bool:
        """Gets the no_schematic_comment option."""
        return self.config.get_option('no_schematic_comment')
        
    @no_schematic_comment.setter
    def no_schematic_comment(self, value: bool) -> None:
        """Sets the no_schematic_comment option."""
        self.config.set_option('no_schematic_comment', value)
        
    @property
    def no_spice_directive(self) -> bool:
        """Gets the no_spice_directive option."""
        return self.config.get_option('no_spice_directive')
        
    @no_spice_directive.setter
    def no_spice_directive(self, value: bool) -> None:
        """Sets the no_spice_directive option."""
        self.config.set_option('no_spice_directive', value)
        
    @property
    def no_nested_symbol_text(self) -> bool:
        """Gets the no_nested_symbol_text option."""
        return self.config.get_option('no_nested_symbol_text')
        
    @no_nested_symbol_text.setter
    def no_nested_symbol_text(self, value: bool) -> None:
        """Sets the no_nested_symbol_text option."""
        self.config.set_option('no_nested_symbol_text', value)
        
    @property
    def no_component_name(self) -> bool:
        """Gets the no_component_name option."""
        return self.config.get_option('no_component_name')
        
    @no_component_name.setter
    def no_component_name(self, value: bool) -> None:
        """Sets the no_component_name option."""
        self.config.set_option('no_component_name', value)
        
    @property
    def no_component_value(self) -> bool:
        """Gets the no_component_value option."""
        return self.config.get_option('no_component_value')
        
    @no_component_value.setter
    def no_component_value(self, value: bool) -> None:
        """Sets the no_component_value option."""
        self.config.set_option('no_component_value', value)
        
    def set_text_rendering_options(self, **kwargs) -> None:
        """Set multiple text rendering options at once.
        
        Args:
            **kwargs: Keyword arguments with text option names and boolean values.
                Supported options: no_schematic_comment, no_spice_directive,
                no_nested_symbol_text, no_component_name, no_component_value
                
        Raises:
            ValueError: If any of the provided options are not text options or values are not boolean.
        """
        self.config.set_text_options(**kwargs)
        self.logger.debug(f"Updated text rendering options: {', '.join(f'{k}={v}' for k, v in kwargs.items())}")
        
    def set_text_rendering_option(self, option: str, value: bool) -> None:
        """Set a text rendering option and log the change.
        
        Args:
            option: The option name (e.g., 'no_schematic_comment')
            value: The new value
            
        Raises:
            ValueError: If the option name is invalid
        """
        # Forward to the config object
        self.config.set_option(option, value)
        self.logger.debug(f"Text rendering option '{option}' set to {value}")
    
    def set_stroke_width(self, stroke_width: float) -> None:
        """Set the stroke width for all renderers.
        
        Args:
            stroke_width: The new stroke width
        """
        # Update in the config
        self.config.set_option("stroke_width", stroke_width)
        
        # Update stroke width for all renderers that have the property
        for renderer in self._renderers.values():
            if hasattr(renderer, 'stroke_width'):
                renderer.stroke_width = stroke_width
        
    def set_base_font_size(self, base_font_size: float) -> None:
        """Set the base font size for all text elements.
        
        Args:
            base_font_size (float): The base font size in pixels.
            
        Raises:
            ValueError: If base_font_size is not positive.
        """
        # Update in the config
        self.config.set_option("base_font_size", base_font_size)
        
        # Update base font size for all renderers
        for renderer in self._renderers.values():
            renderer.base_font_size = base_font_size
    
    def _initialize_renderers(self):
        """Initialize all renderers."""
        self._renderers = {
            'wire': WireRenderer(self.dwg, self.config),
            'symbol': SymbolRenderer(self.dwg, self.config),
            'text': TextRenderer(self.dwg, self.config),
            'shape': ShapeRenderer(self.dwg, self.config),
            'flag': FlagRenderer(self.dwg, self.config)
        }
        
    def load_schematic(self, schematic_data: Dict, symbol_data: Optional[Dict] = None) -> None:
        """Load schematic data for rendering.
        
        Args:
            schematic_data (Dict): The schematic data to render.
            symbol_data (Optional[Dict]): Dictionary mapping symbol names to their drawing data.
            
        Raises:
            ValueError: If the schematic data is invalid.
        """
        # Validate inputs
        self._validate_schematic_data(schematic_data)
        
        # Apply defaults for missing elements
        schematic_data_with_defaults = self._apply_schematic_defaults(schematic_data)
                
        # Store the validated and defaulted data
        self.schematic_data = schematic_data_with_defaults
        self.symbol_data = symbol_data or {}
        
        # Calculate viewbox using the dedicated calculator
        self.view_box = self._viewbox_calculator.calculate(self.schematic_data)
        self.logger.debug(f"Calculated viewbox: {self.view_box}")
        
    def _validate_schematic_data(self, schematic_data: Dict) -> None:
        """Validate the schematic data structure.
        
        Args:
            schematic_data: The schematic data to validate.
            
        Raises:
            ValueError: If the schematic data is invalid.
        """
        if schematic_data is None:
            raise ValueError("Schematic data cannot be None")
            
        if not isinstance(schematic_data, dict):
            raise ValueError(f"Schematic data must be a dictionary, got {type(schematic_data).__name__}")
        
        # Validate wires if present
        if 'wires' in schematic_data and not isinstance(schematic_data['wires'], list):
            raise ValueError(f"Wires must be a list, got {type(schematic_data['wires']).__name__}")
            
    def _apply_schematic_defaults(self, schematic_data: Dict) -> Dict:
        """Apply default values for missing elements in schematic data.
        
        Args:
            schematic_data: The original schematic data.
            
        Returns:
            A copy of the schematic data with defaults applied.
        """
        # Create a copy to avoid modifying the original
        result = schematic_data.copy()
        
        # Default element collections
        default_collections = {
            'wires': [],
            'symbols': {},
            'texts': {},
            'shapes': {},
            'flags': []
        }
        
        # Apply defaults for any missing collections
        for key, default_value in default_collections.items():
            if key not in result:
                result[key] = default_value
                
        return result
        
    def create_drawing(self, output_path: str) -> None:
        """Create a new SVG drawing.
        
        Args:
            output_path (str): Path where the SVG will be saved.
        """
        self.dwg = svgwrite.Drawing(output_path)
        min_x, min_y, width, height = self.view_box
        self.dwg.viewbox(min_x, min_y, width, height)
        self._initialize_renderers()
        
    def render_wires(self, dot_size_multiplier: float = 1.5) -> None:
        """Render all wires in the schematic.
        
        Args:
            dot_size_multiplier (float): Size multiplier for T-junction dots.
        """
        if not self.schematic_data or not self.dwg:
            raise ValueError("Schematic not loaded or drawing not created")
            
        wire_renderer = self._renderers['wire']
        for wire in self.schematic_data.get('wires', []):
            wire_renderer.render(wire, self.stroke_width)
            
        # Add T-junction dots
        t_junctions = self._find_t_junctions(self.schematic_data['wires'])
        for x, y in t_junctions:
            wire_renderer.render_t_junction(x, y, self.stroke_width * dot_size_multiplier)
            
    def render_symbols(self, property_id: Optional[str] = None) -> None:
        """Render all symbols in the schematic.
        
        Args:
            property_id: Optional property ID to render. If provided, only renders window text for this property.
                        If None, renders all defined window texts.
        """
        if not self.schematic_data or not self.dwg:
            raise ValueError("Schematic not loaded or drawing not created")
            
        symbol_renderer = self._renderers['symbol']
        symbols = self.schematic_data.get('symbols', [])
        self.logger.info(f"Found {len(symbols)} symbols to render")
        
        for i, symbol in enumerate(symbols):
            self.logger.info(f"Rendering symbol {i+1}/{len(symbols)}:")
            symbol_name = symbol.get('symbol_name', 'Unknown')
            rotation = symbol.get('rotation', 'R0')
            is_mirrored = rotation.startswith('M')
            instance_name = symbol.get('instance_name', 'Unknown')
            
            self.logger.debug(f"  Name: {symbol_name}")
            self.logger.debug(f"  Instance: {instance_name}")
            self.logger.debug(f"  Position: ({symbol.get('x', 0)}, {symbol.get('y', 0)})")
            self.logger.debug(f"  Rotation: {rotation} (mirrored: {is_mirrored})")
            
            # Log window overrides if present
            if 'window_overrides' in symbol:
                self.logger.debug(f"  Window overrides for {instance_name}: {symbol['window_overrides']}")
            
            # Get symbol definition
            if not symbol_name or symbol_name not in self.symbol_data:
                self.logger.warning(f"Symbol definition not found for {symbol_name}")
                continue
                
            symbol_def = self.symbol_data[symbol_name]
            
            # Skip rendering if text should be excluded and this is a text-only symbol
            if self.config.get_option('no_nested_symbol_text') and not any([
                symbol_def.get('lines', []),
                symbol_def.get('circles', []),
                symbol_def.get('rectangles', []),
                symbol_def.get('arcs', [])
            ]):
                self.logger.debug(f"Skipping text-only symbol: {symbol_name}")
                continue
            
            # Prepare rendering data for the symbol renderer
            render_data = {
                'symbol_name': symbol_name,
                'rotation': rotation,
                'rotation_degrees': symbol.get('rotation_degrees', 0),
                'translation': (symbol.get('x', 0), symbol.get('y', 0)),
                'shapes': {
                    'lines': symbol_def.get('lines', []),
                    'circles': symbol_def.get('circles', []),
                    'rectangles': symbol_def.get('rectangles', []),
                    'arcs': symbol_def.get('arcs', [])
                },
                'texts': symbol_def.get('texts', []),
                'symbol_def': symbol_def,  # Add symbol definition for window text rendering
                'window_overrides': symbol.get('window_overrides', {}),  # Add window overrides
                'property_0': symbol.get('instance_name', ''),  # Add instance name as property_0
                'property_3': symbol.get('value', ''),  # Add value as property_3
                'property_id': property_id,  # Add property_id for window text rendering
                'no_component_name': self.config.get_option('no_component_name'),
                'no_component_value': self.config.get_option('no_component_value')
            }
            
            # Debug log: Check if window_overrides is correctly added to render_data
            if 'window_overrides' in symbol:
                self.logger.debug(f"  Added window_overrides to render_data: {render_data['window_overrides']}")
            
            # Render the symbol
            symbol_renderer.render(render_data, self.stroke_width)
            
    def render_texts(self) -> None:
        """Render all text elements in the schematic.
        
        This method renders standalone text elements that are part of the schematic.
        There are only two types of schematic texts:
        - 'comment': Regular comments and annotations
        - 'spice': SPICE directives that begin with '.'
        """
        if not self.schematic_data or not self.dwg:
            raise ValueError("Schematic not loaded or drawing not created")
            
        text_renderer = self._renderers['text']
        texts = self.schematic_data.get('texts', [])
        self.logger.info(f"Found {len(texts)} text elements to render")
        
        # Track counts for logging
        rendered_counts = {
            'comment': 0,
            'spice': 0
        }
        skipped_counts = {
            'comment': 0,
            'spice': 0
        }
        
        for i, text in enumerate(texts):
            # Default to 'comment' if type not specified
            text_type = text.get('type', 'comment')
            
            # Skip if not a schematic text type (should be either 'comment' or 'spice')
            if text_type not in ['comment', 'spice']:
                self.logger.warning(f"Skipping unknown text type: {text_type}")
                continue
                
            # Skip rendering based on text type and options
            if text_type == 'comment' and self.config.get_option('no_schematic_comment'):
                self.logger.debug(f"Skipping schematic comment: {text.get('text', '')}")
                skipped_counts['comment'] += 1
                continue
            elif text_type == 'spice' and self.config.get_option('no_spice_directive'):
                self.logger.debug(f"Skipping SPICE directive: {text.get('text', '')}")
                skipped_counts['spice'] += 1
                continue
                
            # Render the text
            text_renderer.render(text)
            rendered_counts[text_type] += 1
            
        # Log rendering statistics
        for text_type, count in rendered_counts.items():
            if count > 0:
                self.logger.info(f"  Rendered {count} {text_type} texts")
        for text_type, count in skipped_counts.items():
            if count > 0:
                self.logger.info(f"  Skipped {count} {text_type} texts")
            
    def render_shapes(self) -> None:
        """Render all shapes in the schematic."""
        if not self.schematic_data or not self.dwg:
            raise ValueError("Schematic not loaded or drawing not created")
            
        shape_renderer = self._renderers['shape']
        shapes = self.schematic_data.get('shapes', {})
        
        # Define shape types to process in singular form
        shape_types = ['line', 'rectangle', 'circle', 'arc']
        
        # Process each shape type
        for shape_type in shape_types:
            # Get the collection name by appending 's'
            collection_name = f"{shape_type}s"
            
            # Render all shapes of this type
            for shape in shapes.get(collection_name, []):
                shape_data = shape.copy()
                shape_data['type'] = shape_type
                shape_renderer.render(shape_data, self.stroke_width)
            
    def render_flags(self) -> None:
        """Render all flags and IO pins in the schematic."""
        if not self.schematic_data or not self.dwg:
            raise ValueError("Schematic not loaded or drawing not created")
        
        flag_renderer = self._renderers['flag']
        
        # Get all flags
        flags = self.schematic_data.get('flags', [])
        self.logger.info(f"Found {len(flags)} flags to render")
        
        # Count flag types for logging
        flag_counts = {
            'gnd': 0,
            'net_label': 0,
            'io_pin': 0
        }
        
        # Process each flag
        for i, flag in enumerate(flags):
            flag_type = flag.get('type', 'net_label')
            flag_counts[flag_type] = flag_counts.get(flag_type, 0) + 1
            
            self.logger.debug(f"Rendering flag {i+1}/{len(flags)}:")
            self.logger.debug(f"  Type: {flag_type}")
            self.logger.debug(f"  Position: ({flag.get('x', 0)}, {flag.get('y', 0)})")
            self.logger.debug(f"  Orientation: {flag.get('orientation', 0)}")
            
            # Create a group for the flag
            g = self.dwg.g()
            
            # Determine CSS class and rendering method based on flag type
            if flag_type == 'gnd':
                g.attribs['class'] = 'ground-flag'
                flag_renderer.render_ground_flag(flag, g)
            elif flag_type == 'net_label':
                g.attribs['class'] = 'net-label'
                flag_renderer.render_net_label(flag, g)
            elif flag_type == 'io_pin':
                g.attribs['class'] = 'io-pin'
                flag_renderer.render_io_pin(flag, g)
            else:
                self.logger.warning(f"Unknown flag type: {flag_type}")
                continue
            
            # Add the group to the drawing
            self.dwg.add(g)
            self.logger.debug(f"  Added {flag_type} flag to drawing")
            
        # Log flag counts by type
        for flag_type, count in flag_counts.items():
            if count > 0:
                self.logger.info(f"  Rendered {count} {flag_type} flags")
        
    def save(self) -> None:
        """Save the SVG drawing to file."""
        if not self.dwg:
            raise ValueError("Drawing not created")
        self.dwg.save()
        
    def _find_t_junctions(self, wires: list) -> list:
        """Find all T-junctions in the wire list.
        
        Args:
            wires (list): List of wire dictionaries.
            
        Returns:
            list: List of (x, y) coordinates where T-junctions occur.
        """
        # Create a list to track endpoint coordinates and their occurrences
        endpoint_coords = []
        
        # Process each wire
        for wire in wires:
            # Process start point
            start = {'x': wire['x1'], 'y': wire['y1'], 'occurrence': 1}
            # Process end point
            end = {'x': wire['x2'], 'y': wire['y2'], 'occurrence': 1}
            
            # Check if start point already exists
            start_found = False
            for coord in endpoint_coords:
                if coord['x'] == start['x'] and coord['y'] == start['y']:
                    coord['occurrence'] += 1
                    start_found = True
                    break
            if not start_found:
                endpoint_coords.append(start)
                
            # Check if end point already exists
            end_found = False
            for coord in endpoint_coords:
                if coord['x'] == end['x'] and coord['y'] == end['y']:
                    coord['occurrence'] += 1
                    end_found = True
                    break
            if not end_found:
                endpoint_coords.append(end)
        
        # Find coordinates that appear 3 or more times
        junctions = [(coord['x'], coord['y']) for coord in endpoint_coords if coord['occurrence'] >= 3]
        
        return junctions 