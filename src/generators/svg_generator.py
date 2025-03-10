"""
SVG generator for LTspice schematics.
Converts parsed schematic and symbol data into SVG format.
"""
import svgwrite
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
import json
import os
import warnings
import math
from .shape_renderer import render_shapes, _scale_dash_array
from .net_label_renderer import render_net_label
from .flag_renderer import render_flags
from .symbol_renderer import render_symbol
from .text_renderer import render_text

class SVGGenerator:
    def __init__(self, stroke_width: float = 1.0, dot_size_multiplier: float = 0.75, scale: float = 0.1, font_size: float = 22.0, export_json: bool = False, no_text: bool = False, no_symbol_text: bool = False):
        self.stroke_width = stroke_width
        self.dot_size_multiplier = dot_size_multiplier  # Controls size of junction dots relative to stroke width
        self.scale = scale  # Scale factor for coordinates (default: 0.1 = 10x scale down)
        self.font_size = font_size  # Font size in pixels
        self.symbols_cache: Dict[str, Dict] = {}  # Cache for parsed symbol data
        self.export_json = export_json  # Whether to export debug JSON files
        self.no_text = no_text  # Whether to skip rendering text elements
        self.no_symbol_text = no_symbol_text  # Whether to skip rendering symbol text elements
        self.text_centering_compensation = 0.35  # Controls text centering compensation (0.35 = 35% of font size)
        self.net_label_distance = 8  # Controls distance of net label text from origin (default: 12 units)
        # Font size multiplier mapping
        self.size_multipliers = {
            0: 0.625,
            1: 1.0,
            2: 1.5,  # default
            3: 2.0,
            4: 2.5,
            5: 3.5,
            6: 5.0,
            7: 7.0
        }
        
    def generate(self, schematic_data: Dict, output_path: str, symbols_data: Optional[Dict] = None) -> None:
        """Generate SVG from schematic data."""
        self.schematic_data = schematic_data
        self.symbol_data = symbols_data or {}
        
        # Find T-junctions
        t_junctions = self._find_t_junctions(self.schematic_data.get('wires', []), self.schematic_data.get('symbols', []))
        

        # Calculate viewBox dimensions
        min_x, min_y, width, height = self._calculate_viewbox()
        
        # Create SVG
        dwg = svgwrite.Drawing(output_path, profile='tiny', size=('100%', '100%'))
        dwg.viewbox(min_x, min_y, width, height)
            
        # Add shapes using the shape renderer (includes wires and T-junctions)
        shapes_data = self.schematic_data.get('shapes', {})
        shapes_data['wires'] = self.schematic_data.get('wires', [])
        shapes_data['t_junctions'] = t_junctions
        render_shapes(dwg, shapes_data, self.scale, self.stroke_width, self.dot_size_multiplier)
            
        # Add symbols
        for symbol in self.schematic_data.get('symbols', []):
            render_symbol(
                dwg,
                symbol,
                self.symbol_data,
                self.scale,
                self.stroke_width,
                self.font_size,
                self.size_multipliers,
                self.no_text,
                self.no_symbol_text
            )
        
        # Add text elements
        for text in self.schematic_data.get('texts', []):
            render_text(dwg, text, self.scale, self.font_size, self.no_text)
            
        # Add flags
        if not self.no_text:
            render_flags(
                dwg,
                self.schematic_data.get('flags', []),
                self.schematic_data.get('io_pins', []),
                self.scale,
                self.stroke_width,
                self.font_size,
                self.size_multipliers,
                self.net_label_distance,
                self.text_centering_compensation
            )
        
        # Save the drawing
        dwg.save()
        
        # Save debug data if requested
        if self.export_json:
            self._export_json(output_path, t_junctions)
                
        # Print summary
        print(f"Generated SVG: {output_path}")
        if self.no_text:
            print("Text rendering disabled")

    def _export_json(self, output_path: str, t_junctions: List[Tuple[float, float]]) -> None:
        """Export debug data to a JSON file.
        
        Args:
            output_path: Path to the output SVG file
            t_junctions: List of (x, y) coordinates for T-junctions
        """
        output_dir = os.path.dirname(output_path)
        base_name = os.path.splitext(os.path.basename(output_path))[0]
        debug_data = {
            'wires': self.schematic_data.get('wires', []),
            'symbols': self.schematic_data.get('symbols', []),
            'texts': self.schematic_data.get('texts', []),
            'flags': self.schematic_data.get('flags', []),
            'io_pins': self.schematic_data.get('io_pins', []),  # Include io_pins in debug data
            'shapes': self.schematic_data.get('shapes', {}),
            'symbol_data': self.symbol_data,
            't_junctions': [{'x': x, 'y': y} for x, y in t_junctions]
        }
        debug_file = os.path.join(output_dir, f"{base_name}_debug.json")
        with open(debug_file, 'w') as f:
            json.dump(debug_data, f, indent=2)
        print(f"Exported debug data to {debug_file}")

    def _calculate_viewbox(self) -> Tuple[float, float, float, float]:
        """Calculate the viewBox dimensions for the SVG.
        
        Returns:
            Tuple containing (min_x, min_y, width, height) for the viewBox.
            All values are already scaled according to self.scale.
        """
        min_x = float('inf')
        max_x = float('-inf')
        min_y = float('inf')
        max_y = float('-inf')
        has_elements = False

        # Include wire coordinates
        for wire in self.schematic_data.get('wires', []):
            has_elements = True
            min_x = min(min_x, wire['x1'], wire['x2'])
            max_x = max(max_x, wire['x1'], wire['x2'])
            min_y = min(min_y, wire['y1'], wire['y2'])
            max_y = max(max_y, wire['y1'], wire['y2'])

        # Include symbol coordinates with their extents
        symbol_extent = 100  # Typical size of LTspice symbols
        for symbol in self.schematic_data.get('symbols', []):
            has_elements = True
            min_x = min(min_x, symbol['x'] - symbol_extent)
            max_x = max(max_x, symbol['x'] + symbol_extent)
            min_y = min(min_y, symbol['y'] - symbol_extent)
            max_y = max(max_y, symbol['y'] + symbol_extent)
            
        # Include text coordinates
        for text in self.schematic_data.get('texts', []):
            has_elements = True
            min_x = min(min_x, text['x'] - 50)  # Add some margin for text
            max_x = max(max_x, text['x'] + 50)
            min_y = min(min_y, text['y'] - 20)
            max_y = max(max_y, text['y'] + 20)
            
        # Include flag coordinates
        for flag in self.schematic_data.get('flags', []):
            has_elements = True
            min_x = min(min_x, flag['x'] - 20)  # Add some margin for net names
            max_x = max(max_x, flag['x'] + 20)
            min_y = min(min_y, flag['y'] - 10)
            max_y = max(max_y, flag['y'] + 10)

        # Include shape coordinates
        for shape_type, shapes in self.schematic_data.get('shapes', {}).items():
            for shape in shapes:
                has_elements = True
                min_x = min(min_x, shape['x1'], shape['x2'])
                max_x = max(max_x, shape['x1'], shape['x2'])
                min_y = min(min_y, shape['y1'], shape['y2'])
                max_y = max(max_y, shape['y1'], shape['y2'])

        # If no elements found, use default viewBox
        if not has_elements:
            min_x = -100
            max_x = 100
            min_y = -100
            max_y = 100

        # Add padding and apply scale
        padding = 50 * self.scale  # Scale the padding too
        min_x = (min_x - padding) * self.scale
        max_x = (max_x + padding) * self.scale
        min_y = (min_y - padding) * self.scale
        max_y = (max_y + padding) * self.scale

        width = max_x - min_x
        height = max_y - min_y

        return min_x, min_y, width, height

    def _find_t_junctions(self, wires: List[Dict], symbols: List[Dict]) -> List[Tuple[float, float]]:
        """Find points where three or more wire ends meet."""
        # Create a mapping of points to wire ends that meet there
        point_to_ends = defaultdict(int)
        
        # Count wire ends at each point
        for wire in wires:
            point_to_ends[(wire['x1'], wire['y1'])] += 1
            point_to_ends[(wire['x2'], wire['y2'])] += 1
        
        # Find points where 3 or more wire ends meet
        t_junctions = []
        for point, count in point_to_ends.items():
            # Only add points where 3 or more wires meet
            if count >= 3:
                # Check if this is a real T-junction by counting unique wire directions
                wire_directions = set()
                for wire in wires:
                    # Check both endpoints of each wire
                    if (wire['x1'], wire['y1']) == point:
                        dx = wire['x2'] - wire['x1']
                        dy = wire['y2'] - wire['y1']
                    elif (wire['x2'], wire['y2']) == point:
                        dx = wire['x1'] - wire['x2']
                        dy = wire['y1'] - wire['y2']
                    else:
                        continue
                        
                    # Normalize direction to avoid floating point issues
                    length = (dx * dx + dy * dy) ** 0.5
                    if length > 0:
                        dx, dy = dx / length, dy / length
                        # Round to handle floating point precision
                        dx, dy = round(dx, 6), round(dy, 6)
                        wire_directions.add((dx, dy))
                
                # Only add if we have at least 3 different wire directions
                if len(wire_directions) >= 3:
                    t_junctions.append(point)
                    
        return t_junctions