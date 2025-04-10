import svgwrite
from typing import Dict
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
        
    def _initialize_renderers(self):
        """Initialize all renderers."""
        self._renderers = {
            'wire': WireRenderer(self.dwg),
            'symbol': SymbolRenderer(self.dwg),
            'text': TextRenderer(self.dwg),
            'shape': ShapeRenderer(self.dwg)
        }
        
    def load_schematic(self, schematic_data: Dict) -> None:
        """Load schematic data for rendering.
        
        Args:
            schematic_data (Dict): The schematic data to render.
        """
        self.schematic_data = schematic_data
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
            symbol_renderer.render(symbol)
            
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
        
    def _calculate_viewbox(self) -> tuple:
        """Calculate the viewBox for the SVG based on schematic bounds.
        
        Returns:
            tuple: (min_x, min_y, width, height)
        """
        # TODO: Implement viewBox calculation
        return (0, 0, 1000, 1000)
        
    def _find_t_junctions(self, wires: list) -> list:
        """Find all T-junctions in the wire list.
        
        Args:
            wires (list): List of wire dictionaries.
            
        Returns:
            list: List of (x, y) coordinates where T-junctions occur.
        """
        # TODO: Implement T-junction detection
        return [] 