"""
Parser for LTspice ASC schematic files.
Extracts wire and symbol information from the schematic.
"""
import re
from typing import Dict, List, Tuple, Set
from . import shape_parser

class ASCParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.wires: List[Dict[str, int]] = []
        self.symbols: List[Dict[str, any]] = []
        self.texts: List[Dict[str, any]] = []
        self.flags: List[Dict[str, any]] = []
        self.io_pins: List[Dict[str, any]] = []
        # Shape lists for internal use
        self._lines: List[Dict[str, any]] = []
        self._circles: List[Dict[str, any]] = []
        self._rectangles: List[Dict[str, any]] = []
        self._arcs: List[Dict[str, any]] = []
        self._flag_positions: Set[Tuple[int, int]] = set()  # Track unique flag positions
        self._parsed_data: Dict[str, any] = None  # Cache for parsed data
        self._current_symbol = None  # Track current symbol being parsed
        
    def parse(self) -> Dict[str, any]:
        """Parse the ASC file and return a dictionary containing wires and symbols."""
        # Return cached data if available
        if self._parsed_data is not None:
            return self._parsed_data
            
        print(f"Parsing schematic: {self.file_path}")
        
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
            
        i = 0
        total_lines = len(lines)
        
        while i < total_lines:
            # Clean up the line by removing any hidden characters
            line = ''.join(c for c in lines[i].strip() if c.isprintable())
            
            if line:  # Skip empty lines
                parts = line.split()
                if not parts:
                    i += 1
                    continue
                    
                first_word = parts[0]
                
                if first_word == 'WIRE':
                    self._parse_wire(line)
                elif first_word == 'SYMBOL':
                    self._parse_symbol(line)
                elif first_word == 'SYMATTR':
                    if len(parts) >= 3 and parts[1] == 'InstName':
                        self._parse_instance_name(' '.join(parts[2:]))
                elif first_word == 'TEXT':
                    self._parse_text(line)
                elif first_word == 'FLAG':
                    # Look ahead for IOPIN
                    is_io_pin = False
                    if i + 1 < total_lines:
                        next_line = ''.join(c for c in lines[i + 1].strip() if c.isprintable())
                        if next_line.startswith('IOPIN'):
                            is_io_pin = True
                            self._parse_flag_and_iopin(line, next_line)
                            i += 1  # Skip the IOPIN line since we've processed it
                    
                    if not is_io_pin:
                        self._parse_flag(line)
                # Parse shapes
                elif first_word == 'LINE':
                    print(f"Found LINE entry: {line}")
                    shape_data = shape_parser.parse_line(line)
                    if shape_data:
                        print(f"Adding LINE: {shape_data}")
                        self._lines.append(shape_data)
                    else:
                        print("Failed to parse LINE")
                elif first_word == 'CIRCLE':
                    print(f"Found CIRCLE entry: {line}")
                    shape_data = shape_parser.parse_circle(line)
                    if shape_data:
                        print(f"Adding CIRCLE: {shape_data}")
                        self._circles.append(shape_data)
                    else:
                        print("Failed to parse CIRCLE")
                elif first_word == 'RECTANGLE':
                    print(f"Found RECTANGLE entry: {line}")
                    shape_data = shape_parser.parse_rectangle(line)
                    if shape_data:
                        print(f"Adding RECTANGLE: {shape_data}")
                        self._rectangles.append(shape_data)
                    else:
                        print("Failed to parse RECTANGLE")
                elif first_word == 'ARC':
                    print(f"Found ARC entry: {line}")
                    shape_data = shape_parser.parse_arc(line)
                    if shape_data:
                        print(f"Adding ARC: {shape_data}")
                        self._arcs.append(shape_data)
                    else:
                        print("Failed to parse ARC")
                
                i += 1
            else:
                i += 1  # Make sure we still increment for empty lines
                
        # Add GND symbols for ground flags
        for flag in self.flags:
            if flag['net_name'] == '0':
                # Create a GND symbol at the flag's position
                gnd_symbol = {
                    'symbol_name': 'GND',
                    'instance_name': 'GND',
                    'x': flag['x'],
                    'y': flag['y'],
                    'rotation': 'R0'
                }
                self.symbols.append(gnd_symbol)
                
        print(f"Found {len(self.wires)} wires, {len(self.symbols)} symbols, {len(self.texts)} text elements, "
              f"{len(self.flags)} flags, {len(self.io_pins)} IO pins")
        if any([self._lines, self._circles, self._rectangles, self._arcs]):
            print(f"Found shapes: {len(self._lines)} lines, {len(self._circles)} circles, "
                  f"{len(self._rectangles)} rectangles, {len(self._arcs)} arcs")
              
        # Cache the parsed data
        self._parsed_data = {
            'wires': self.wires,
            'symbols': self.symbols,
            'texts': self.texts,
            'flags': self.flags,
            'io_pins': self.io_pins,
            'shapes': {
                'lines': self._lines,
                'circles': self._circles,
                'rectangles': self._rectangles,
                'arcs': self._arcs
            }
        }
        return self._parsed_data
    
    def _parse_wire(self, line: str):
        """Parse a WIRE line and extract coordinates."""
        # Format: WIRE x1 y1 x2 y2
        parts = line.split()
        if len(parts) == 5:  # WIRE + 4 coordinates
            try:
                # Convert coordinates to integers
                x1, y1, x2, y2 = map(int, parts[1:])
                wire = {
                    'x1': x1,
                    'y1': y1,
                    'x2': x2,
                    'y2': y2
                }
                self.wires.append(wire)
            except ValueError as e:
                print(f"Warning: Invalid wire coordinates in line: {line} - {e}")
    
    def _parse_symbol(self, line: str):
        """Parse a SYMBOL line and extract name and position."""
        # Format: SYMBOL symbol_name x y [rotation]
        parts = line.split()
        if len(parts) >= 4:  # SYMBOL + name + 2 coordinates + optional rotation
            try:
                # Convert coordinates to integers
                x, y = map(int, parts[2:4])
                
                # Parse rotation string (format: R0, R90, R180, R270, M0, M90, M180, M270)
                rotation = 'R0'  # Default to no rotation
                if len(parts) > 4:
                    rotation_str = parts[4]
                    if rotation_str[0] in ['R', 'M'] and rotation_str[1:].isdigit():
                        rotation = rotation_str
                    else:
                        print(f"Warning: Invalid rotation value: {rotation_str}, using R0")
                
                symbol = {
                    'symbol_name': parts[1],
                    'instance_name': '',  # Will be filled by _parse_instance_name
                    'x': x,
                    'y': y,
                    'rotation': rotation
                }
                self.symbols.append(symbol)
                self._current_symbol = symbol  # Track current symbol for instance name parsing
            except ValueError as e:
                print(f"Warning: Invalid symbol data in line: {line} - {e}")
    
    def _parse_flag(self, line: str):
        """Parse a FLAG line and extract position and net name.
        Format: FLAG x y net_name
        """
        parts = line.split()
        if len(parts) >= 4:  # FLAG + x + y + net_name
            try:
                # Convert coordinates to integers
                x, y = map(int, parts[1:3])
                # Skip if we've already seen a flag at this position
                if (x, y) in self._flag_positions:
                    return
                
                # Join remaining parts as net name (in case it contains spaces)
                net_name = ' '.join(parts[3:])
                
                flag = {
                    'x': x,
                    'y': y,
                    'net_name': net_name
                }
                self.flags.append(flag)
                self._flag_positions.add((x, y))
            except ValueError as e:
                print(f"Warning: Invalid flag data in line: {line} - {e}")
    
    def _parse_flag_and_iopin(self, flag_line: str, iopin_line: str):
        """Parse a FLAG line followed by an IOPIN line.
        Format: 
        FLAG x y net_name
        IOPIN x y direction
        """
        flag_parts = flag_line.split()
        iopin_parts = iopin_line.split()
        
        if len(flag_parts) >= 4 and len(iopin_parts) >= 4:  # FLAG/IOPIN + x + y + net_name/direction
            try:
                # Convert coordinates to integers
                x, y = map(int, flag_parts[1:3])
                # Skip if we've already seen a flag at this position
                if (x, y) in self._flag_positions:
                    return
                
                # Get net name from flag
                net_name = ' '.join(flag_parts[3:])
                
                # Get direction from IOPIN
                direction = iopin_parts[3]
                
                # Verify IOPIN coordinates match FLAG coordinates
                iopin_x, iopin_y = map(int, iopin_parts[1:3])
                if (x, y) != (iopin_x, iopin_y):
                    print(f"Warning: IOPIN coordinates ({iopin_x}, {iopin_y}) don't match FLAG coordinates ({x}, {y})")
                    return
                
                # Add flag
                flag = {
                    'x': x,
                    'y': y,
                    'net_name': net_name
                }
                self.flags.append(flag)
                self._flag_positions.add((x, y))
                
                # Add IO pin
                io_pin = {
                    'x': x,
                    'y': y,
                    'net_name': net_name,
                    'direction': direction
                }
                self.io_pins.append(io_pin)
                
            except ValueError as e:
                print(f"Warning: Invalid flag/iopin data in lines: {flag_line} / {iopin_line} - {e}")
    
    def _parse_text(self, line: str):
        """Parse a TEXT line and extract position, justification, and content.
        Format: TEXT x y justification size ;content
        Justification can be: Left, Center, Right, Top, Bottom
        Size is an index that maps to a font size multiplier:
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

        # Find the semicolon that separates attributes from text content
        try:
            attrs, content = line.split(';', 1)
            attrs_parts = attrs.split()
            
            if len(attrs_parts) >= 4:  # TEXT + x + y + justification + size
                try:
                    x = int(attrs_parts[1])
                    y = int(attrs_parts[2])
                    justification = attrs_parts[3]
                    
                    # Extract size index and convert to actual multiplier if available
                    size_multiplier = size_multipliers[2]  # Default to index 2 (1.5x)
                    if len(attrs_parts) >= 5:
                        try:
                            size_index = int(attrs_parts[4])
                            size_multiplier = size_multipliers.get(size_index, size_multipliers[2])
                        except ValueError:
                            print(f"Warning: Invalid size index in line: {line}, using default")
                    
                    text = {
                        'x': x,
                        'y': y,
                        'justification': justification,
                        'text': content.strip(),
                        'size_multiplier': size_multiplier  # Store actual multiplier value
                    }
                    self.texts.append(text)
                except ValueError as e:
                    print(f"Warning: Invalid text coordinates in line: {line} - {e}")
        except ValueError:
            print(f"Warning: Invalid text format in line: {line}")
    
    def _parse_instance_name(self, instance_name: str):
        """Parse the instance name for the current symbol."""
        if self._current_symbol is not None:
            self._current_symbol['instance_name'] = instance_name
    
    def export_json(self, output_path: str):
        """Export the parsed data to a JSON file."""
        import json
        with open(output_path, 'w') as f:
            json.dump(self.parse(), f, indent=2) 