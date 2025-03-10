"""
Parser for LTspice ASY symbol files.
Extracts drawing information from the symbol file.
"""
from typing import Dict, List, Tuple, Optional
from . import shape_parser

class ASYParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.lines: List[Dict[str, any]] = []
        self.circles: List[Dict[str, any]] = []
        self.rectangles: List[Dict[str, any]] = []
        self.arcs: List[Dict[str, any]] = []
        self.windows: List[Dict[str, any]] = []
        self.texts: List[Dict[str, any]] = []  # Add texts list
        self._parsed_data: Dict[str, any] = None  # Cache for parsed data

    def parse(self) -> Dict[str, any]:
        """Parse the ASY file and return a dictionary containing drawing elements."""
        # Return cached data if available
        if self._parsed_data is not None:
            return self._parsed_data

        # Try different encodings
        encodings = ['utf-16', 'utf-8', 'ascii']
        lines = None

        for encoding in encodings:
            try:
                with open(self.file_path, 'r', encoding=encoding) as f:
                    lines = f.readlines()
                break
            except UnicodeError:
                continue

        if lines is None:
            raise ValueError(f"Could not read {self.file_path} with any of the supported encodings")

        for line in lines:
            # Clean up the line by removing any hidden characters
            line = ''.join(c for c in line.strip() if c.isprintable())

            if line:  # Skip empty lines
                parts = line.split()
                if not parts:
                    continue

                first_word = parts[0]

                if first_word == 'LINE':
                    shape_data = shape_parser.parse_line(line, is_symbol=True)
                    if shape_data:
                        self.lines.append(shape_data)
                elif first_word == 'CIRCLE':
                    shape_data = shape_parser.parse_circle(line, is_symbol=True)
                    if shape_data:
                        self.circles.append(shape_data)
                elif first_word == 'RECTANGLE':
                    shape_data = shape_parser.parse_rectangle(line, is_symbol=True)
                    if shape_data:
                        self.rectangles.append(shape_data)
                elif first_word == 'ARC':
                    shape_data = shape_parser.parse_arc(line, is_symbol=True)
                    if shape_data:
                        self.arcs.append(shape_data)
                elif first_word == 'WINDOW':
                    window_data = self._parse_window(line)
                    if window_data:
                        self.windows.append(window_data)
                elif first_word == 'TEXT':
                    text_data = self._parse_text(line)
                    if text_data:
                        self.texts.append(text_data)

        # Cache the parsed data
        self._parsed_data = {
            'lines': self.lines,
            'circles': self.circles,
            'rectangles': self.rectangles,
            'arcs': self.arcs,
            'windows': self.windows,
            'texts': self.texts  # Add texts to output
        }
        return self._parsed_data

    def _parse_window(self, line: str) -> Dict:
        """Parse a WINDOW entry and extract properties.
        Format: WINDOW property_id x y justification [size_multiplier]
        """
        parts = line.split()
        if len(parts) >= 5:  # WINDOW + property_id + x + y + justification
            try:
                property_id = int(parts[1])
                x = int(parts[2])
                y = int(parts[3])
                justification = parts[4]
                window_data = {
                    'property_id': property_id,
                    'x': x,
                    'y': y,
                    'justification': justification
                }
                # Add size multiplier if present
                if len(parts) > 5:
                    try:
                        size_multiplier = int(parts[5])
                        window_data['size_multiplier'] = size_multiplier
                    except ValueError:
                        pass
                return window_data
            except ValueError:
                pass
        return None

    def _parse_text(self, line: str) -> Dict:
        """Parse a TEXT entry and extract properties.
        Format: TEXT x y justification fontsize_index text
        
        Args:
            line: The text line to parse
            
        Returns:
            Dictionary containing text properties or None if parsing fails
        """
        try:
            # Split on first space after the first 4 parts to preserve spaces in text content
            parts = line.split(maxsplit=4)
            if len(parts) >= 5:  # TEXT + x + y + justification + fontsize_index + text
                x = int(parts[1])
                y = int(parts[2])
                justification = parts[3]
                
                # Split the remaining part to get fontsize_index and text
                remaining = parts[4].split(maxsplit=1)
                if len(remaining) == 2:
                    fontsize_index = int(remaining[0])
                    text_content = remaining[1]
                    
                    return {
                        'x': x,
                        'y': y,
                        'justification': justification,
                        'size_multiplier': fontsize_index,  # Store as size_multiplier for consistency
                        'text': text_content
                    }
        except (ValueError, IndexError) as e:
            print(f"Warning: Invalid text format in line: {line} - {e}")
        return None

    def export_json(self, output_path: str):
        """Export the parsed data to a JSON file."""
        import json
        with open(output_path, 'w') as f:
            json.dump(self.parse(), f, indent=2)

def parse_shape(line: str) -> Optional[Dict]:
    """Parse a shape line by detecting its type and calling the appropriate parser.
    
    Args:
        line: The line to parse
        
    Returns:
        Parsed shape data or None if parsing fails
    """
    parts = line.split()
    if not parts:
        return None
        
    shape_type = parts[0]
    if shape_type not in shape_parser.SUPPORTED_SHAPES:
        return None
    
    # Map shape types to their parser functions
    parser_map = {
        'LINE': lambda l: shape_parser.parse_line(l, is_symbol=True),
        'CIRCLE': lambda l: shape_parser.parse_circle(l, is_symbol=True),
        'RECTANGLE': lambda l: shape_parser.parse_rectangle(l, is_symbol=True),
        'ARC': lambda l: shape_parser.parse_arc(l, is_symbol=True)
    }
    
    return parser_map[shape_type](line) 