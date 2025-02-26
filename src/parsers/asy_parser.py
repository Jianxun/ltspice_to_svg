"""
Parser for LTspice ASY symbol files.
Extracts line drawing information from symbol files.
"""
from typing import Dict, List, Tuple
import math

class ASYParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.lines: List[Dict[str, int]] = []
        self.circles: List[Dict[str, int]] = []
        self.rectangles: List[Dict[str, int]] = []  # Add rectangles list
        self.arcs: List[Dict[str, any]] = []  # Add arcs list
        self.texts: List[Dict[str, any]] = []  # Add texts list for WINDOW entries
        
    def parse(self) -> Dict[str, any]:
        """Parse the ASY file and return a dictionary containing line and shape information."""
        # Try different encodings
        encodings = ['utf-16', 'utf-8', 'ascii']
        file_lines = None
        
        for encoding in encodings:
            try:
                with open(self.file_path, 'r', encoding=encoding) as f:
                    file_lines = f.readlines()
                break
            except UnicodeError:
                continue
                
        if file_lines is None:
            raise ValueError(f"Could not read {self.file_path} with any of the supported encodings")
            
        for line in file_lines:
            # Clean up the line by removing any hidden characters
            line = ''.join(c for c in line.strip() if c.isprintable())
            if line.startswith('LINE'):
                self._parse_line(line)
            elif line.startswith('CIRCLE'):
                self._parse_circle(line)
            elif line.startswith('RECTANGLE'):
                self._parse_rectangle(line)
            elif line.startswith('ARC'):
                self._parse_arc(line)
            elif line.startswith('WINDOW'):
                self._parse_window(line)
                
        return {
            'lines': self.lines,
            'circles': self.circles,
            'rectangles': self.rectangles,
            'arcs': self.arcs,
            'texts': self.texts
        }
    
    def _get_line_style(self, style_code: int) -> str:
        """Convert LTspice line style code to SVG dash array.
        0: solid
        1: dash
        2: dot
        3: dash dot
        4: dash dot dot
        
        For dots, we use a nearly zero length to make them round.
        For dashes, we use a length of 4 times the stroke width.
        The gap between elements is 2 times the stroke width.
        """
        # These values will be multiplied by stroke-width in SVG
        style_map = {
            0: None,  # solid
            1: "4,2",  # dash
            2: "0.001,2",  # dot (nearly 0 length makes it round)
            3: "4,2,0.001,2",  # dash dot
            4: "4,2,0.001,2,0.001,2"  # dash dot dot
        }
        return style_map.get(style_code)
    
    def _parse_line(self, line: str):
        """Parse a LINE entry and extract coordinates."""
        # Format: LINE Normal x1 y1 x2 y2 [style]
        parts = line.split()
        if len(parts) >= 6 and parts[1] == 'Normal':  # LINE + Normal + 4 coordinates
            try:
                # Convert coordinates to integers
                x1, y1, x2, y2 = map(int, parts[2:6])
                line_data = {
                    'x1': x1,
                    'y1': y1,
                    'x2': x2,
                    'y2': y2
                }
                # Add line style if present
                if len(parts) > 6:
                    try:
                        style_code = int(parts[6])
                        line_style = self._get_line_style(style_code)
                        if line_style is not None:
                            line_data['style'] = line_style
                    except ValueError:
                        pass
                self.lines.append(line_data)
            except ValueError as e:
                print(f"Warning: Invalid line coordinates in line: {line} - {e}")
    
    def _parse_circle(self, line: str):
        """Parse a CIRCLE entry and extract coordinates."""
        # Format: CIRCLE Normal x1 y1 x2 y2 [style]
        parts = line.split()
        if len(parts) >= 6 and parts[1] == 'Normal':  # CIRCLE + Normal + 4 coordinates
            try:
                # Convert coordinates to integers
                x1, y1, x2, y2 = map(int, parts[2:6])
                circle_data = {
                    'x1': x1,
                    'y1': y1,
                    'x2': x2,
                    'y2': y2
                }
                # Add line style if present
                if len(parts) > 6:
                    try:
                        style_code = int(parts[6])
                        line_style = self._get_line_style(style_code)
                        if line_style is not None:
                            circle_data['style'] = line_style
                    except ValueError:
                        pass
                self.circles.append(circle_data)
            except ValueError as e:
                print(f"Warning: Invalid circle coordinates in line: {line} - {e}")
    
    def _parse_rectangle(self, line: str):
        """Parse a RECTANGLE entry and extract coordinates.
        Format: RECTANGLE Normal x1 y1 x2 y2 [style]
        """
        parts = line.split()
        if len(parts) >= 6 and parts[1] == 'Normal':  # RECTANGLE + Normal + 4 coordinates
            try:
                # Convert coordinates to integers
                x1, y1, x2, y2 = map(int, parts[2:6])
                rect_data = {
                    'x1': x1,
                    'y1': y1,
                    'x2': x2,
                    'y2': y2
                }
                # Add line style if present
                if len(parts) > 6:
                    try:
                        style_code = int(parts[6])
                        line_style = self._get_line_style(style_code)
                        if line_style is not None:
                            rect_data['style'] = line_style
                    except ValueError:
                        pass
                self.rectangles.append(rect_data)
            except ValueError as e:
                print(f"Warning: Invalid rectangle coordinates in line: {line} - {e}")
    
    def _parse_arc(self, line: str):
        """Parse an ARC entry and extract coordinates.
        Format: ARC Normal x1 y1 x2 y2 x3 y3 x4 y4 [style]
        where:
        - (x1,y1) and (x2,y2) define the bounding box of the circle/ellipse
        - (x3,y3) defines the end point of the arc
        - (x4,y4) defines the start point of the arc
        """
        parts = line.split()
        if len(parts) >= 10 and parts[1] == 'Normal':  # ARC + Normal + 8 coordinates
            try:
                # Convert coordinates to integers
                x1, y1, x2, y2, x3, y3, x4, y4 = map(int, parts[2:10])
                
                # Calculate center of the bounding box
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2
                
                # Calculate start and end angles (swap x3,y3 and x4,y4)
                start_angle = math.atan2(y4 - center_y, x4 - center_x)
                end_angle = math.atan2(y3 - center_y, x3 - center_x)
                
                # Convert angles to degrees
                start_angle = math.degrees(start_angle)
                end_angle = math.degrees(end_angle)
                
                # Ensure angles are in [0, 360) range
                start_angle = (start_angle + 360) % 360
                end_angle = (end_angle + 360) % 360
                
                arc_data = {
                    'x1': x1,
                    'y1': y1,
                    'x2': x2,
                    'y2': y2,
                    'start_angle': start_angle,
                    'end_angle': end_angle
                }
                # Add line style if present
                if len(parts) > 10:
                    try:
                        style_code = int(parts[10])
                        line_style = self._get_line_style(style_code)
                        if line_style is not None:
                            arc_data['style'] = line_style
                    except ValueError:
                        pass
                self.arcs.append(arc_data)
            except ValueError as e:
                print(f"Warning: Invalid arc coordinates in line: {line} - {e}")
    
    def _parse_window(self, line: str):
        """Parse a WINDOW entry and extract text information.
        Format: WINDOW property_id x y justification size_multiplier
        
        property_id: Integer identifying the property (0 for instance name)
        x, y: Position coordinates
        justification: Text alignment (Left, Center, Right, Top, Bottom)
        size_multiplier: Font size index (0-7) that maps to actual multiplier:
        0 -> 0.625x
        1 -> 1.0x
        2 -> 1.5x (default)
        3 -> 2.0x
        4 -> 2.5x
        5 -> 3.5x
        6 -> 5.0x
        7 -> 7.0x
        """
        # Font size multiplier mapping
        size_multipliers = {
            0: 0.625,
            1: 1.0,
            2: 1.5,  # default
            3: 2.0,
            4: 2.5,
            5: 3.5,
            6: 5.0,
            7: 7.0
        }

        parts = line.split()
        if len(parts) >= 6:  # WINDOW + property_id + x + y + justification + size
            try:
                # Convert coordinates and property ID to integers
                property_id = int(parts[1])
                x = int(parts[2])
                y = int(parts[3])
                justification = parts[4]
                
                # Convert size index to actual multiplier
                size_index = int(parts[5])
                size_multiplier = size_multipliers.get(size_index, size_multipliers[2])  # Default to 1.5x if invalid
                
                # Create text entry
                text = {
                    'property_id': property_id,
                    'x': x,
                    'y': y,
                    'justification': justification,
                    'size_multiplier': size_multiplier  # Store actual multiplier value
                }
                self.texts.append(text)
            except ValueError as e:
                print(f"Warning: Invalid WINDOW data in line: {line} - {e}")
    
    def export_json(self, output_path: str):
        """Export the parsed data to a JSON file."""
        import json
        with open(output_path, 'w') as f:
            json.dump(self.parse(), f, indent=2) 