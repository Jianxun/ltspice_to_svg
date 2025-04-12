import svgwrite
from typing import Dict, Optional
from src.renderers.base_renderer import BaseRenderer
from src.renderers.wire_renderer import WireRenderer
from src.renderers.symbol_renderer import SymbolRenderer
from src.renderers.text_renderer import TextRenderer
from src.renderers.shape_renderer import ShapeRenderer

class SVGRenderer:
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
        
    def _initialize_renderers(self):
        """Initialize all renderers."""
        self._renderers = {
            'wire': WireRenderer(self.dwg),
            'symbol': SymbolRenderer(self.dwg),
            'text': TextRenderer(self.dwg),
            'shape': ShapeRenderer(self.dwg)
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
            
        # Validate required top-level keys
        required_keys = ['wires', 'symbols', 'texts', 'shapes']
        for key in required_keys:
            if key not in schematic_data:
                schematic_data[key] = []
            elif not isinstance(schematic_data[key], list):
                raise ValueError(f"{key} must be a list")
                
        self.schematic_data = schematic_data
        self.symbol_data = symbol_data or {}  # Store symbol data
        self.view_box = self._calculate_viewbox()
        
    def create_drawing(self, output_path: str) -> None:
        """Create a new SVG drawing.
        
        Args:
            output_path (str): Path where the SVG will be saved.
        """
        self.dwg = svgwrite.Drawing(output_path)
        self.dwg.viewbox(*self.view_box)
        self._initialize_renderers()
        
    def render_wires(self, stroke_width: float = 1.0, dot_size_multiplier: float = 0.75) -> None:
        """Render all wires in the schematic.
        
        Args:
            stroke_width (float): Width of the wire lines.
            dot_size_multiplier (float): Size multiplier for T-junction dots.
        """
        if not self.schematic_data or not self.dwg:
            raise ValueError("Schematic not loaded or drawing not created")
            
        wire_renderer = self._renderers['wire']
        for wire in self.schematic_data.get('wires', []):
            wire_renderer.render(wire, stroke_width)
            
        # Add T-junction dots
        t_junctions = self._find_t_junctions(self.schematic_data['wires'])
        for x, y in t_junctions:
            wire_renderer.render_t_junction(x, y, stroke_width * dot_size_multiplier)
            
    def render_symbols(self) -> None:
        """Render all symbols in the schematic."""
        if not self.schematic_data or not self.dwg:
            raise ValueError("Schematic not loaded or drawing not created")
            
        symbol_renderer = self._renderers['symbol']
        for symbol in self.schematic_data.get('symbols', []):
            # Get symbol data
            symbol_name = symbol['symbol_name']
            if symbol_name not in self.symbol_data:
                print(f"Warning: Symbol {symbol_name} not found in symbol data")
                continue
                
            symbol_def = self.symbol_data[symbol_name]
            
            # Create a group for the symbol
            symbol_renderer.create_group()
            
            # Convert rotation to string format if it's an integer
            rotation = symbol.get('rotation', 'R0')
            if isinstance(rotation, int):
                rotation = f'R{rotation}'
            
            # Set transformation
            symbol_renderer.set_transformation(rotation, (symbol['x'], symbol['y']))
            
            # Render shapes
            shapes = {
                'lines': symbol_def.get('lines', []),
                'circles': symbol_def.get('circles', []),
                'rectangles': symbol_def.get('rectangles', []),
                'arcs': symbol_def.get('arcs', [])
            }
            symbol_renderer.render_shapes(shapes)
            
            # Render texts
            texts = symbol_def.get('texts', [])
            symbol_renderer.render_texts(texts)
            
            # Add the group to the drawing
            symbol_renderer.add_to_drawing()
            
    def render_texts(self, font_size: float = 22.0) -> None:
        """Render all text elements in the schematic.
        
        Args:
            font_size (float): Size of the text.
        """
        if not self.schematic_data or not self.dwg:
            raise ValueError("Schematic not loaded or drawing not created")
            
        text_renderer = self._renderers['text']
        for text in self.schematic_data.get('texts', []):
            text_renderer.render(text, font_size)
            
    def render_shapes(self, stroke_width: float = 1.0) -> None:
        """Render all shapes in the schematic.
        
        Args:
            stroke_width (float): Width of the shape lines.
        """
        if not self.schematic_data or not self.dwg:
            raise ValueError("Schematic not loaded or drawing not created")
            
        shape_renderer = self._renderers['shape']
        for shape in self.schematic_data.get('shapes', []):
            shape_renderer.render(shape, stroke_width)
            
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
        
        # Check if there are any elements to process
        has_elements = False
        
        # Scan wires
        for wire in self.schematic_data.get('wires', []):
            has_elements = True
            self._update_bounds(wire['x1'], wire['y1'], wire['x2'], wire['y2'])
            
        # Scan symbols
        for symbol in self.schematic_data.get('symbols', []):
            has_elements = True
            # Symbols can have multiple shapes and texts
            for shape_type, shapes in symbol.get('shapes', {}).items():
                for shape in shapes:
                    self._update_bounds(shape['x1'], shape['y1'], shape['x2'], shape['y2'])
                        
            # Handle symbol texts
            for text in symbol.get('texts', []):
                self._update_bounds(text['x'], text['y'])
                
        # Scan standalone texts
        for text in self.schematic_data.get('texts', []):
            has_elements = True
            self._update_bounds(text['x'], text['y'])
            
        # Scan standalone shapes
        for shape in self.schematic_data.get('shapes', []):
            has_elements = True
            self._update_bounds(shape['x1'], shape['y1'], shape['x2'], shape['y2'])
                
        # If no elements were found, return default size
        if not has_elements:
            return (0, 0, 100, 100)
                
        # Add padding (10% of the total size)
        width = self._max_x - self._min_x
        height = self._max_y - self._min_y
        padding = max(width, height) * 0.1
        
        self._min_x -= padding
        self._min_y -= padding
        self._max_x += padding
        self._max_y += padding
        
        # Ensure minimum size
        if width == 0:
            self._max_x = self._min_x + 100
        if height == 0:
            self._max_y = self._min_y + 100
            
        return (self._min_x, self._min_y, self._max_x - self._min_x, self._max_y - self._min_y)
        
    def _find_t_junctions(self, wires: list) -> list:
        """Find all T-junctions in the wire list.
        
        Args:
            wires (list): List of wire dictionaries.
            
        Returns:
            list: List of (x, y) coordinates where T-junctions occur.
        """
        junctions = []
        # Create a dictionary to count connections at each point
        point_connections = {}
        
        # First, add all wire endpoints
        for wire in wires:
            start = (wire['x1'], wire['y1'])
            end = (wire['x2'], wire['y2'])
            
            # Count connections at start point
            point_connections[start] = point_connections.get(start, 0) + 1
            # Count connections at end point
            point_connections[end] = point_connections.get(end, 0) + 1
            
        # Then check for wire intersections
        for i, wire1 in enumerate(wires):
            for wire2 in wires[i+1:]:
                intersection = self._find_wire_intersection(wire1, wire2)
                if intersection:
                    point_connections[intersection] = point_connections.get(intersection, 0) + 2
        
        # A T-junction is a point where exactly 3 wires meet
        for point, count in point_connections.items():
            if count == 3:
                junctions.append(point)
                
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