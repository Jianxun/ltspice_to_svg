import svgwrite
import logging
from typing import Dict, Optional
from src.renderers.base_renderer import BaseRenderer
from src.renderers.wire_renderer import WireRenderer
from src.renderers.symbol_renderer import SymbolRenderer
from src.renderers.text_renderer import TextRenderer
from src.renderers.shape_renderer import ShapeRenderer
from src.renderers.flag_renderer import FlagRenderer

class SVGRenderer(BaseRenderer):
    def __init__(self):
        self.dwg = None
        self.schematic_data = None
        self.view_box = None
        self._renderers = {}
        self._min_x = float('inf')
        self._min_y = float('inf')
        self._max_x = float('-inf')
        self._max_y = float('-inf')
        self.symbol_data = None  # Add symbol data storage
        self.logger = logging.getLogger(self.__class__.__name__)
        # Initialize BaseRenderer with None for dwg, it will be set later in initialize_drawing
        super().__init__(None)
        
    def set_stroke_width(self, stroke_width: float) -> None:
        """Set the stroke width for all renderers.
        
        Args:
            stroke_width: The new stroke width
        """
        self.stroke_width = stroke_width
        # Update stroke width for all renderers that have the property
        for renderer in self._renderers.values():
            if hasattr(renderer, 'stroke_width'):
                renderer.stroke_width = stroke_width
        
    def set_base_font_size(self, font_size: float) -> None:
        """Set the base font size for all text elements.
        
        Args:
            font_size (float): The base font size in pixels.
            
        Raises:
            ValueError: If font_size is not positive.
        """
        # Update base font size for all renderers
        for renderer in self._renderers.values():
            renderer.base_font_size = font_size
        
    def _initialize_renderers(self):
        """Initialize all renderers."""
        self._renderers = {
            'wire': WireRenderer(self.dwg),
            'symbol': SymbolRenderer(self.dwg),
            'text': TextRenderer(self.dwg),
            'shape': ShapeRenderer(self.dwg),
            'flag': FlagRenderer(self.dwg)
        }
        
    def load_schematic(self, schematic_data: Dict, symbol_data: Optional[Dict] = None) -> None:
        """Load schematic data for rendering.
        
        Args:
            schematic_data (Dict): The schematic data to render.
            symbol_data (Optional[Dict]): Dictionary mapping symbol names to their drawing data.
            
        Raises:
            ValueError: If the schematic data is invalid.
        """
        if schematic_data is None:
            raise ValueError("Schematic data cannot be None")
            
        if not isinstance(schematic_data, dict):
            raise ValueError("Schematic data must be a dictionary")
            
        # Ensure wires exist and is a list
        if 'wires' not in schematic_data:
            schematic_data['wires'] = []
        elif not isinstance(schematic_data['wires'], list):
            raise ValueError("wires must be a list")
            
        # Initialize optional elements as empty lists
        optional_keys = ['symbols', 'texts', 'shapes']
        for key in optional_keys:
            if key not in schematic_data:
                schematic_data[key] = {}
                
        self.schematic_data = schematic_data
        self.symbol_data = symbol_data or {}  # Store symbol data
        self.view_box = self._calculate_viewbox()
        
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
            wire_renderer.render(wire, self._stroke_width)
            
        # Add T-junction dots
        t_junctions = self._find_t_junctions(self.schematic_data['wires'])
        for x, y in t_junctions:
            wire_renderer.render_t_junction(x, y, self._stroke_width * dot_size_multiplier)
            
    def render_symbols(self) -> None:
        """Render all symbols in the schematic."""
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
            self.logger.debug(f"  Definition found with {len(symbol_def.get('texts', []))} text elements")
            self.logger.debug(f"  Windows in symbol definition: {symbol_def.get('windows', {})}")
            
            # Create symbol data for rendering
            render_data = {
                'rotation': rotation,
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
                'property_3': symbol.get('value', '')  # Add value as property_3
            }
            
            # Debug log: Check if window_overrides is correctly added to render_data
            if 'window_overrides' in symbol:
                self.logger.debug(f"  Added window_overrides to render_data: {render_data['window_overrides']}")
            
            # Render the symbol
            symbol_renderer.render(render_data, self._stroke_width)
            
    def render_texts(self) -> None:
        """Render all text elements in the schematic."""
        if not self.schematic_data or not self.dwg:
            raise ValueError("Schematic not loaded or drawing not created")
            
        text_renderer = self._renderers['text']
        texts = self.schematic_data.get('texts', [])
        self.logger.info(f"Found {len(texts)} text elements to render")
        for i, text in enumerate(texts):
            self.logger.info(f"Rendering text {i+1}/{len(texts)}:")
            self.logger.debug(f"  Content: {text.get('text', '')}")
            self.logger.debug(f"  Position: ({text.get('x', 0)}, {text.get('y', 0)})")
            self.logger.debug(f"  Justification: {text.get('justification', 'Left')}")
            self.logger.debug(f"  Size multiplier: {text.get('size_multiplier', 2)}")
            self.logger.debug(f"  Type: {text.get('type', 'comment')}")
            text_renderer.render(text)
            
    def render_shapes(self) -> None:
        """Render all shapes in the schematic."""
        if not self.schematic_data or not self.dwg:
            raise ValueError("Schematic not loaded or drawing not created")
            
        shape_renderer = self._renderers['shape']
        shapes = self.schematic_data.get('shapes', {})
        
        # Render lines
        for line in shapes.get('lines', []):
            shape_data = line.copy()
            shape_data['type'] = 'line'
            shape_renderer.render(shape_data, self._stroke_width)
            
        # Render rectangles
        for rect in shapes.get('rectangles', []):
            shape_data = rect.copy()
            shape_data['type'] = 'rectangle'
            shape_renderer.render(shape_data, self._stroke_width)
            
        # Render circles
        for circle in shapes.get('circles', []):
            shape_data = circle.copy()
            shape_data['type'] = 'circle'
            shape_renderer.render(shape_data, self._stroke_width)
            
        # Render arcs
        for arc in shapes.get('arcs', []):
            shape_data = arc.copy()
            shape_data['type'] = 'arc'
            shape_renderer.render(shape_data, self._stroke_width)
            
    def render_flags(self) -> None:
        """Render all flags and IO pins in the schematic."""
        if not self.schematic_data or not self.dwg:
            raise ValueError("Schematic not loaded or drawing not created")
        
        # Render flags
        flags = self.schematic_data.get('flags', [])
        self.logger.info(f"Found {len(flags)} flags to render")
        
        for i, flag in enumerate(flags):
            self.logger.debug(f"Rendering flag {i+1}/{len(flags)}:")
            self.logger.debug(f"  Type: {flag['type']}")
            self.logger.debug(f"  Position: ({flag.get('x', 0)}, {flag.get('y', 0)})")
            self.logger.debug(f"  Orientation: {flag.get('orientation', 0)}")
            
            if flag['type'] == 'gnd':  # Note: ASCParser uses 'gnd' for ground flags
                # Create a group for the ground flag
                g = self.dwg.g()
                g.attribs['class'] = 'ground-flag'
                self.logger.debug("  Created ground flag group")
                
                # Add the ground flag to the group
                self._renderers['flag'].render_ground_flag(flag, g)
                
                # Add the group to the drawing
                self.dwg.add(g)
                self.logger.debug("  Added ground flag group to drawing")
            elif flag['type'] == 'net_label':
                # Create a group for the net label
                g = self.dwg.g()
                g.attribs['class'] = 'net-label'
                self.logger.debug("  Created net label group")
                
                # Add the net label to the group
                self._renderers['flag'].render_net_label(flag, g)
                
                # Add the group to the drawing
                self.dwg.add(g)
                self.logger.debug("  Added net label group to drawing")
                
        # Render IO pins
        io_pins = self.schematic_data.get('io_pins', [])
        self.logger.info(f"Found {len(io_pins)} IO pins to render")
        
        for i, pin in enumerate(io_pins):
            self.logger.debug(f"Rendering IO pin {i+1}/{len(io_pins)}:")
            self.logger.debug(f"  Net name: {pin.get('net_name', '')}")
            self.logger.debug(f"  Position: ({pin.get('x', 0)}, {pin.get('y', 0)})")
            self.logger.debug(f"  Direction: {pin.get('direction', 'BiDir')}")
            self.logger.debug(f"  Orientation: {pin.get('orientation', 0)}")
            
            # Create a group for the IO pin
            g = self.dwg.g()
            g.attribs['class'] = 'io-pin'
            self.logger.debug("  Created IO pin group")
            
            # Add the IO pin to the group
            self._renderers['flag'].render_io_pin(pin, g)
            
            # Add the group to the drawing
            self.dwg.add(g)
            self.logger.debug("  Added IO pin group to drawing")
        
    def save(self) -> None:
        """Save the SVG drawing to file."""
        if not self.dwg:
            raise ValueError("Drawing not created")
        self.dwg.save()
        
    def _reset_bounds(self) -> None:
        """Reset the bounds to their initial values."""
        self._min_x = float('inf')
        self._min_y = float('inf')
        self._max_x = float('-inf')
        self._max_y = float('-inf')
        
    def _update_bounds(self, x1: float, y1: float, x2: float = None, y2: float = None) -> None:
        """Update the viewbox bounds with new coordinates.
        
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
        
    def _calculate_viewbox(self) -> tuple:
        """Calculate the viewBox for the SVG based on schematic bounds.
        
        The viewBox is calculated by finding the minimum and maximum coordinates
        of all elements in the schematic, then adding padding around the bounds.
        
        Returns:
            tuple: (min_x, min_y, width, height)
        """
        if not self.schematic_data:
            return (0, 0, 100, 100)  # Default size for empty schematic
            
        # Reset bounds
        self._reset_bounds()
        
        # Calculate bounds from wires
        for wire in self.schematic_data.get('wires', []):
            self._update_bounds(wire['x1'], wire['y1'], wire['x2'], wire['y2'])
            
        # Calculate bounds from shapes
        shapes = self.schematic_data.get('shapes', {})
        
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
            
        # Calculate dimensions
        width = self._max_x - self._min_x
        height = self._max_y - self._min_y
        
        # Add padding (10% of the larger dimension)
        padding = max(width, height) * 0.1
        
        # Update bounds with padding
        min_x = self._min_x - padding
        min_y = self._min_y - padding
        width = width + 2 * padding
        height = height + 2 * padding
        
        # Ensure minimum size
        if width == 0:
            width = 100
        if height == 0:
            height = 100
            
        return (min_x, min_y, width, height)
        
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
        
    def _find_wire_intersection(self, wire1: dict, wire2: dict) -> tuple:
        """Find the intersection point of two wires if they intersect.
        
        Args:
            wire1, wire2: Wire dictionaries with x1, y1, x2, y2 coordinates.
            
        Returns:
            tuple: (x, y) coordinates of intersection point, or None if no intersection.
        """
        # Extract coordinates
        x1, y1 = wire1['x1'], wire1['y1']
        x2, y2 = wire1['x2'], wire1['y2']
        x3, y3 = wire2['x1'], wire2['y1']
        x4, y4 = wire2['x2'], wire2['y2']
        
        # Check if wires are parallel
        if (x2 - x1 == 0 and x4 - x3 == 0) or (y2 - y1 == 0 and y4 - y3 == 0):
            return None
            
        # Handle vertical wires
        if x2 - x1 == 0:  # First wire is vertical
            if y4 - y3 == 0:  # Second wire is horizontal
                x = x1
                y = y3
                if (min(x3, x4) <= x <= max(x3, x4) and
                    min(y1, y2) <= y <= max(y1, y2)):
                    return (x, y)
        elif x4 - x3 == 0:  # Second wire is vertical
            if y2 - y1 == 0:  # First wire is horizontal
                x = x3
                y = y1
                if (min(x1, x2) <= x <= max(x1, x2) and
                    min(y3, y4) <= y <= max(y3, y4)):
                    return (x, y)
                    
        return None 