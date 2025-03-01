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

class SVGGenerator:
    # Built-in symbol geometries
    BUILTIN_SYMBOLS = {
        'GND': {
            'lines': [
                # Horizontal line
                {'x1': -16, 'y1': 0, 'x2': 16, 'y2': 0},
                # First V line
                {'x1': 16, 'y1': 0, 'x2': 0, 'y2': 16},
                # Second V line
                {'x1': 0, 'y1': 16, 'x2': -16, 'y2': 0}
            ],
            'circles': [],
            'rectangles': [],
            'arcs': []
        }
    }
    
    def __init__(self, stroke_width: float = 1.0, dot_size_multiplier: float = 0.75, scale: float = 0.1, font_size: float = 22.0, export_json: bool = False, no_text: bool = False):
        self.stroke_width = stroke_width
        self.dot_size_multiplier = dot_size_multiplier  # Controls size of junction dots relative to stroke width
        self.scale = scale  # Scale factor for coordinates (default: 0.1 = 10x scale down)
        self.font_size = font_size  # Font size in pixels
        self.symbols_cache: Dict[str, Dict] = {}  # Cache for parsed symbol data
        self.export_json = export_json  # Whether to export debug JSON files
        self.no_text = no_text  # Whether to skip rendering text elements
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
        self.wires = schematic_data.get('wires', [])
        self.symbols = schematic_data.get('symbols', [])
        self.texts = schematic_data.get('texts', [])
        self.flags = schematic_data.get('flags', [])  # Add flags
        self.shapes = schematic_data.get('shapes', {})  # Add shapes
        self.symbol_data = symbols_data or {}
        
        # Add built-in symbols only if they don't exist in the parsed data
        for name, geometry in self.BUILTIN_SYMBOLS.items():
            if name.upper() not in self.symbol_data:  # Case-insensitive check
                self.symbol_data[name] = geometry
        
        # Find T-junctions and terminal points
        t_junctions = self._find_t_junctions(self.wires, self.symbols)
        terminal_points = self._get_symbol_terminals(self.symbols)
        
        # Save debug data if requested
        if self.export_json:
            output_dir = os.path.dirname(output_path)
            base_name = os.path.splitext(os.path.basename(output_path))[0]
            debug_data = {
                'wires': self.wires,
                'symbols': self.symbols,
                'texts': self.texts,
                'flags': self.flags,
                'shapes': self.shapes,
                'symbol_data': self.symbol_data,
                't_junctions': [{'x': x, 'y': y} for x, y in t_junctions],
                'terminal_points': [{'x': x, 'y': y} for x, y in terminal_points]
            }
            debug_file = os.path.join(output_dir, f"{base_name}_debug.json")
            with open(debug_file, 'w') as f:
                json.dump(debug_data, f, indent=2)
            print(f"Exported debug data to {debug_file}")
        
        # Calculate viewBox dimensions
        min_x = float('inf')
        max_x = float('-inf')
        min_y = float('inf')
        max_y = float('-inf')
        has_elements = False

        # Include wire coordinates
        for wire in self.wires:
            has_elements = True
            min_x = min(min_x, wire['x1'], wire['x2'])
            max_x = max(max_x, wire['x1'], wire['x2'])
            min_y = min(min_y, wire['y1'], wire['y2'])
            max_y = max(max_y, wire['y1'], wire['y2'])

        # Include symbol coordinates with their extents
        symbol_extent = 100  # Typical size of LTspice symbols
        for symbol in self.symbols:
            has_elements = True
            min_x = min(min_x, symbol['x'] - symbol_extent)
            max_x = max(max_x, symbol['x'] + symbol_extent)
            min_y = min(min_y, symbol['y'] - symbol_extent)
            max_y = max(max_y, symbol['y'] + symbol_extent)
            
        # Include text coordinates
        for text in self.texts:
            has_elements = True
            min_x = min(min_x, text['x'] - 50)  # Add some margin for text
            max_x = max(max_x, text['x'] + 50)
            min_y = min(min_y, text['y'] - 20)
            max_y = max(max_y, text['y'] + 20)
            
        # Include flag coordinates
        for flag in self.flags:
            has_elements = True
            min_x = min(min_x, flag['x'] - 20)  # Add some margin for net names
            max_x = max(max_x, flag['x'] + 20)
            min_y = min(min_y, flag['y'] - 10)
            max_y = max(max_y, flag['y'] + 10)

        # Include shape coordinates
        for shape_type, shapes in self.shapes.items():
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

        # Create SVG
        dwg = svgwrite.Drawing(output_path, profile='tiny', size=('100%', '100%'))
        dwg.viewbox(min_x, min_y, width, height)
        
        # Add wires with scaling
        for wire in self.wires:
            dwg.add(dwg.line(
                (wire['x1'] * self.scale, wire['y1'] * self.scale),
                (wire['x2'] * self.scale, wire['y2'] * self.scale),
                stroke='black',
                stroke_width=self.stroke_width,
                stroke_linecap='round'
            ))
            
        # Add T-junction dots with scaling
        for x, y in t_junctions:
            dwg.add(dwg.circle(
                center=(x * self.scale, y * self.scale),
                r=self.stroke_width * self.dot_size_multiplier,
                fill='black',
                stroke='none'
            ))
            
        # Add shapes
        self._add_shapes(dwg, self.shapes)
            
        # Add symbols
        self._add_symbols(dwg, self.symbols, self.symbol_data)
        
        # Add text elements
        self._add_texts(dwg, self.texts)
            
        # Save the drawing
        dwg.save()
        
        # Print summary
        print(f"Generated SVG: {output_path}")
        if self.no_text:
            print("Text rendering disabled")

    def _get_symbol_terminals(self, symbols: List[Dict]) -> Set[Tuple[float, float]]:
        """Get all terminal points of symbols to exclude from dot placement."""
        terminal_points = set()
        
        for symbol in symbols:
            x, y = symbol['x'], symbol['y']
            
            # For NMOS and PMOS: drain (64,64), source (64,-64), and gate (0,0) relative to symbol position
            if symbol['symbol_name'] in ['NMOS', 'PMOS']:
                terminal_points.add((x + 64, y + 64))  # drain
                terminal_points.add((x + 64, y - 64))  # source
                terminal_points.add((x, y))  # gate
            # For VDD: bottom terminal (0,0) relative to symbol position
            elif symbol['symbol_name'] == 'VDD':
                terminal_points.add((x, y))
            # For GND: top terminal (0,0) relative to symbol position
            elif symbol['symbol_name'] == 'GND':
                terminal_points.add((x, y))
                
        return terminal_points
    
    def _get_single_symbol_terminals(self, symbol: Dict) -> Set[Tuple[float, float]]:
        """Get the terminal points of a single symbol."""
        x, y = symbol['x'], symbol['y']
        terminals = set()
        
        # Get base terminal points relative to symbol origin
        base_terminals = []
        if symbol['symbol_name'] in ['NMOS', 'PMOS']:
            base_terminals = [
                (64, 64),   # drain
                (64, -64),  # source
                (0, 0)      # gate
            ]
        elif symbol['symbol_name'] == 'VDD':
            base_terminals = [(0, 0)]  # bottom terminal
        elif symbol['symbol_name'] == 'GND':
            base_terminals = [(0, 0)]  # top terminal
            
        if not base_terminals:
            return terminals
            
        # Parse rotation value and type
        rotation_str = symbol.get('rotation', 'R0')
        rotation_type = rotation_str[0]  # 'R' or 'M'
        try:
            angle = int(rotation_str[1:])
        except ValueError:
            print(f"Warning: Invalid rotation value: {rotation_str}")
            angle = 0
            
        # Transform each terminal point
        for tx, ty in base_terminals:
            # Apply mirroring if needed
            if rotation_type == 'M':
                tx = -tx  # Mirror across Y axis
                
            # Apply rotation
            if angle == 90:
                tx, ty = -ty, tx
            elif angle == 180:
                tx, ty = -tx, -ty
            elif angle == 270:
                tx, ty = ty, -tx
                
            # Add translated point
            terminals.add((x + tx, y + ty))
            
        return terminals

    def _find_t_junctions(self, wires: List[Dict], symbols: List[Dict]) -> List[Tuple[float, float]]:
        """Find points where three or more wire ends meet, excluding symbol terminals."""
        # Get terminal points to exclude
        terminal_points = self._get_symbol_terminals(symbols)
        
        # Create a mapping of points to wire ends that meet there
        point_to_ends = defaultdict(int)
        
        # Count wire ends at each point
        for wire in wires:
            point_to_ends[(wire['x1'], wire['y1'])] += 1
            point_to_ends[(wire['x2'], wire['y2'])] += 1
        
        # Find points where 3 or more wire ends meet
        t_junctions = []
        for point, count in point_to_ends.items():
            # Only add points where 3 or more wires meet and not at symbol terminals
            if count >= 3 and point not in terminal_points:
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

    def _scale_dash_array(self, dash_array: str, stroke_width: float) -> str:
        """Scale a dash array pattern by the stroke width."""
        if not dash_array:
            return None
        return ','.join(str(float(x) * stroke_width) for x in dash_array.split(','))

    def _add_shapes(self, dwg, shapes: Dict[str, List[Dict]]):
        """Add shapes from the schematic to the SVG."""
        # Add lines
        for line in shapes.get('lines', []):
            style = {}
            style['stroke'] = 'black'
            style['stroke_width'] = self.stroke_width
            style['stroke_linecap'] = 'round'
            
            if 'style' in line:
                style['stroke_dasharray'] = self._scale_dash_array(line['style'], self.stroke_width)
                
            dwg.add(dwg.line(
                (line['x1'] * self.scale, line['y1'] * self.scale),
                (line['x2'] * self.scale, line['y2'] * self.scale),
                **style
            ))
            
        # Add circles
        for circle in shapes.get('circles', []):
            # Calculate radius from bounding box
            rx = abs(circle['x2'] - circle['x1']) / 2
            ry = abs(circle['y2'] - circle['y1']) / 2
            cx = (circle['x1'] + circle['x2']) / 2
            cy = (circle['y1'] + circle['y2']) / 2
            
            style = {}
            style['stroke'] = 'black'
            style['stroke_width'] = self.stroke_width
            style['fill'] = 'none'
            
            if 'style' in circle:
                style['stroke_dasharray'] = self._scale_dash_array(circle['style'], self.stroke_width)
                
            if rx == ry:  # Perfect circle
                dwg.add(dwg.circle(
                    center=(cx * self.scale, cy * self.scale),
                    r=rx * self.scale,
                    **style
                ))
            else:  # Ellipse
                dwg.add(dwg.ellipse(
                    center=(cx * self.scale, cy * self.scale),
                    r=(rx * self.scale, ry * self.scale),
                    **style
                ))
                
        # Add rectangles
        for rect in shapes.get('rectangles', []):
            x = min(rect['x1'], rect['x2'])
            y = min(rect['y1'], rect['y2'])
            width = abs(rect['x2'] - rect['x1'])
            height = abs(rect['y2'] - rect['y1'])
            
            style = {}
            style['stroke'] = 'black'
            style['stroke_width'] = self.stroke_width
            style['fill'] = 'none'
            
            if 'style' in rect:
                style['stroke_dasharray'] = self._scale_dash_array(rect['style'], self.stroke_width)
                style['stroke_linecap'] = 'round'  # Add round line caps for dotted/dashed styles
                
                # For dotted/dashed rectangles, use path instead of rect to get proper line caps
                # Create path data for the rectangle
                path_data = [
                    # Move to top-left corner
                    ('M', [(x * self.scale, y * self.scale)]),
                    # Draw top line
                    ('L', [(x * self.scale + width * self.scale, y * self.scale)]),
                    # Draw right line
                    ('L', [(x * self.scale + width * self.scale, y * self.scale + height * self.scale)]),
                    # Draw bottom line
                    ('L', [(x * self.scale, y * self.scale + height * self.scale)]),
                    # Close path (back to top-left)
                    ('Z', [])
                ]
                dwg.add(dwg.path(d=path_data, **style))
            else:
                # For solid rectangles, use rect element
                dwg.add(dwg.rect(
                    insert=(x * self.scale, y * self.scale),
                    size=(width * self.scale, height * self.scale),
                    **style
                ))
            
        # Add arcs
        for arc in shapes.get('arcs', []):
            # Calculate center and radius
            cx = (arc['x1'] + arc['x2']) / 2
            cy = (arc['y1'] + arc['y2']) / 2
            rx = abs(arc['x2'] - arc['x1']) / 2
            ry = abs(arc['y2'] - arc['y1']) / 2
            
            # Convert angles to radians for path calculation
            start_angle = math.radians(arc['start_angle'])
            end_angle = math.radians(arc['end_angle'])
            
            # Calculate start and end points
            start_x = cx + rx * math.cos(start_angle)
            start_y = cy + ry * math.sin(start_angle)
            end_x = cx + rx * math.cos(end_angle)
            end_y = cy + ry * math.sin(end_angle)
            
            # Determine if arc should be drawn clockwise or counterclockwise
            large_arc = abs(end_angle - start_angle) > math.pi
            sweep = end_angle > start_angle
            
            # Create path data
            path_data = [
                ('M', [(start_x * self.scale, start_y * self.scale)]),
                ('A', [
                    rx * self.scale, ry * self.scale,  # radii
                    0,  # x-axis-rotation
                    int(large_arc), int(sweep),  # large-arc and sweep flags
                    end_x * self.scale, end_y * self.scale  # end point
                ])
            ]
            
            style = {}
            style['stroke'] = 'black'
            style['stroke_width'] = self.stroke_width
            style['fill'] = 'none'
            
            if 'style' in arc:
                style['stroke_dasharray'] = self._scale_dash_array(arc['style'], self.stroke_width)
                
            dwg.add(dwg.path(d=path_data, **style))

    def _add_symbols(self, dwg, symbols: List[Dict], symbols_data: Dict[str, Dict]):
        """Add symbols to the SVG drawing."""
        for symbol in symbols:
            symbol_name = symbol['symbol_name']
            
            # Skip if no drawing data available
            if symbol_name not in symbols_data:
                warnings.warn(f"No drawing data for symbol {symbol_name}")
                continue
                
            # Create a group for the symbol
            g = dwg.g()
            
            # Apply transformations
            rotation_str = symbol.get('rotation', 'R0')
            rotation_type = rotation_str[0]  # 'R' or 'M'
            try:
                angle = int(rotation_str[1:])
            except ValueError:
                print(f"Warning: Invalid rotation value: {rotation_str}")
                angle = 0
                
            # Build transform string
            transform = []
            
            # First translate to origin
            transform.append(f"translate({symbol['x'] * self.scale},{symbol['y'] * self.scale})")
            
            # Then apply mirroring if needed
            if rotation_type == 'M':
                transform.append("scale(-1,1)")  # Mirror across Y axis
                
            # Then apply rotation
            if angle != 0:
                transform.append(f"rotate({angle})")
                
            # Set the transform
            g.attribs['transform'] = ' '.join(transform)
            
            # Add lines with scaling
            for line in symbols_data[symbol_name]['lines']:
                line_attrs = {
                    'stroke': 'black',
                    'stroke-width': self.stroke_width,
                    'stroke-linecap': 'round'
                }
                if 'style' in line:
                    scaled_style = self._scale_dash_array(line['style'], self.stroke_width)
                    if scaled_style:
                        line_attrs['stroke-dasharray'] = scaled_style
                g.add(dwg.line(
                    (line['x1'] * self.scale, line['y1'] * self.scale),
                    (line['x2'] * self.scale, line['y2'] * self.scale),
                    **line_attrs
                ))
            
            # Add circles with scaling
            for circle in symbols_data[symbol_name].get('circles', []):
                # Calculate center and radius from bounding box
                cx = (circle['x1'] + circle['x2']) / 2 * self.scale
                cy = (circle['y1'] + circle['y2']) / 2 * self.scale
                rx = abs(circle['x2'] - circle['x1']) / 2 * self.scale
                ry = abs(circle['y2'] - circle['y1']) / 2 * self.scale
                
                circle_attrs = {
                    'stroke': 'black',
                    'stroke-width': self.stroke_width,
                    'fill': 'none'
                }
                if 'style' in circle:
                    scaled_style = self._scale_dash_array(circle['style'], self.stroke_width)
                    if scaled_style:
                        circle_attrs['stroke-dasharray'] = scaled_style
                
                # For perfect circles, use circle element
                if abs(rx - ry) < 0.01:  # Allow small difference due to rounding
                    g.add(dwg.circle(
                        center=(cx, cy),
                        r=rx,  # Use rx as radius
                        **circle_attrs
                    ))
                else:
                    # For ellipses, use ellipse element
                    g.add(dwg.ellipse(
                        center=(cx, cy),
                        r=(rx, ry),
                        **circle_attrs
                    ))
            
            # Add rectangles with scaling
            for rect in symbols_data[symbol_name].get('rectangles', []):
                rect_attrs = {
                    'stroke': 'black',
                    'stroke-width': self.stroke_width,
                    'fill': 'none'
                }
                if 'style' in rect:
                    scaled_style = self._scale_dash_array(rect['style'], self.stroke_width)
                    if scaled_style:
                        rect_attrs['stroke-dasharray'] = scaled_style
                g.add(dwg.rect(
                    insert=(rect['x1'] * self.scale, rect['y1'] * self.scale),
                    size=(
                        (rect['x2'] - rect['x1']) * self.scale,
                        (rect['y2'] - rect['y1']) * self.scale
                    ),
                    **rect_attrs
                ))
            
            # Add arcs with scaling
            for arc in symbols_data[symbol_name].get('arcs', []):
                # Calculate center and radii
                cx = (arc['x1'] + arc['x2']) / 2 * self.scale
                cy = (arc['y1'] + arc['y2']) / 2 * self.scale
                rx = abs(arc['x2'] - arc['x1']) / 2 * self.scale
                ry = abs(arc['y2'] - arc['y1']) / 2 * self.scale
                
                # Get start and end angles
                start_angle = arc['start_angle']
                end_angle = arc['end_angle']
                
                # SVG arc flags
                large_arc_flag = '1' if (end_angle - start_angle) % 360 > 180 else '0'
                sweep_flag = '1'  # Always draw arc clockwise
                
                # Calculate start and end points
                start_x = cx + rx * math.cos(math.radians(start_angle))
                start_y = cy + ry * math.sin(math.radians(start_angle))
                end_x = cx + rx * math.cos(math.radians(end_angle))
                end_y = cy + ry * math.sin(math.radians(end_angle))
                
                # Create SVG path for arc
                path_data = f"M {start_x},{start_y} A {rx},{ry} 0 {large_arc_flag} {sweep_flag} {end_x},{end_y}"
                
                arc_attrs = {
                    'stroke': 'black',
                    'stroke-width': self.stroke_width,
                    'fill': 'none'
                }
                if 'style' in arc:
                    scaled_style = self._scale_dash_array(arc['style'], self.stroke_width)
                    if scaled_style:
                        arc_attrs['stroke-dasharray'] = scaled_style
                g.add(dwg.path(
                    d=path_data,
                    **arc_attrs
                ))
            
            # Add instance name if text position is defined and text rendering is enabled
            instance_name = symbol.get('instance_name', '')
            if instance_name and not self.no_text:
                # Find text entry with property_id=0 (instance name position)
                for text in symbols_data[symbol_name].get('texts', []):
                    if text.get('property_id') == 0:
                        # Get size multiplier (already converted from index)
                        size_multiplier = text.get('size_multiplier', 1.5)  # Default to 1.5x
                        font_size = self.font_size * size_multiplier
                        
                        # Get original justification
                        justification = text.get('justification', 'Left')
                        
                        # Flip justification if mirrored
                        if rotation_type == 'M':
                            # Flip horizontal justification
                            justification = {
                                'Left': 'Right',
                                'Right': 'Left',
                                'Center': 'Center',
                                'Top': 'Top',
                                'Bottom': 'Bottom'
                            }[justification]
                        
                        # Set text alignment based on flipped justification
                        if justification == 'Left':
                            text_anchor = 'start'
                        elif justification == 'Right':
                            text_anchor = 'end'
                        else:  # Center, Top, Bottom all use middle horizontal alignment
                            text_anchor = 'middle'
                        
                        # Adjust vertical position based on justification
                        # For Left/Center/Right, move up by half the font size to center vertically
                        # For Top/Bottom, adjust by a third of the font size
                        if justification in ['Left', 'Center', 'Right']:
                            y_offset = font_size * 0.3  # Move up to center vertically
                        elif justification == 'Top':
                            y_offset = font_size * 0.6  # Move down
                        else:  # Bottom
                            y_offset = font_size * 0.0  # Move up
                        
                        # Transform text position according to symbol transformation
                        text_x = text['x']
                        text_y = text['y']
                        
                        # Apply mirroring to position if needed
                        if rotation_type == 'M':
                            text_x = -text_x
                            
                        # Apply rotation to position
                        if angle == 90:
                            text_x, text_y = -text_y, text_x
                        elif angle == 180:
                            text_x, text_y = -text_x, -text_y
                        elif angle == 270:
                            text_x, text_y = text_y, -text_x
                        
                        # Create text element with transformed position but no rotation/mirroring
                        text_element = dwg.text(
                            instance_name,
                            insert=((symbol['x'] + text_x) * self.scale, (symbol['y'] + text_y) * self.scale + y_offset),
                            font_family='Arial',
                            font_size=f'{font_size}px',
                            text_anchor=text_anchor,
                            fill='black'  # Ensure text is visible
                        )
                        # Add text directly to drawing, not to the transformed group
                        dwg.add(text_element)
                        break  # Only use the first instance name text entry
            
            # Add the group to the drawing
            dwg.add(g)

    def _add_texts(self, dwg, texts):
        """Add text elements to the SVG drawing.
        Handles LTspice text justification options:
        - Left: Left-aligned, vertically centered
        - Center: Horizontally and vertically centered
        - Right: Right-aligned, vertically centered
        - Top: Top-aligned, horizontally centered
        - Bottom: Bottom-aligned, horizontally centered
        
        Font size is calculated by multiplying the base font size with the size_multiplier from the ASC file.
        Horizontal alignment is handled using text-anchor.
        Vertical alignment is handled by adjusting the y-coordinate.
        """
        # Skip text rendering if no_text is True
        if self.no_text:
            return
            
        for text in texts:
            # Scale coordinates only (not font size)
            x = text['x'] * self.scale
            y = text['y'] * self.scale
            
            # Get size multiplier (already converted from index)
            size_multiplier = text.get('size_multiplier', 1.5)  # Default to 1.5x
            font_size = self.font_size * size_multiplier
            
            # Set text alignment based on justification
            if text['justification'] == 'Left':
                text_anchor = 'start'
            elif text['justification'] == 'Right':
                text_anchor = 'end'
            else:  # Center, Top, Bottom all use middle horizontal alignment
                text_anchor = 'middle'
            
            # Adjust vertical position based on justification
            # For Left/Center/Right, move up by half the font size to center vertically
            # For Top/Bottom, adjust by a third of the font size
            if text['justification'] in ['Left', 'Center', 'Right']:
                y_offset = font_size * 0.3  # Move up to center vertically
            elif text['justification'] == 'Top':
                y_offset = font_size * 0.6  # Move down
            else:  # Bottom
                y_offset = font_size * 0.0  # Move up
            
            # Add text element with all attributes
            text_element = dwg.text(
                text['text'],
                insert=(x, y + y_offset),
                font_family='Arial',
                font_size=f'{font_size}px',
                text_anchor=text_anchor,
                fill='black'  # Ensure text is visible
            )
            dwg.add(text_element)