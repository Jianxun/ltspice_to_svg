"""
Parser for LTspice ASC schematic files.
Extracts wire and symbol information from the schematic.
"""
import re
from typing import Dict, List, Tuple

class ASCParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.wires: List[Dict[str, int]] = []
        self.symbols: List[Dict[str, any]] = []
        self.texts: List[Dict[str, any]] = []  # Add text list
        
    def parse(self) -> Dict[str, any]:
        """Parse the ASC file and return a dictionary containing wires and symbols."""
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
                
                if first_word == 'WIRE':
                    self._parse_wire(line)
                elif first_word == 'SYMBOL':
                    self._parse_symbol(line)
                elif first_word == 'TEXT':
                    self._parse_text(line)
                
        print(f"Found {len(self.wires)} wires, {len(self.symbols)} symbols, and {len(self.texts)} text elements")
        return {
            'wires': self.wires,
            'symbols': self.symbols,
            'texts': self.texts
        }
    
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
                    'name': parts[1],
                    'x': x,
                    'y': y,
                    'rotation': rotation
                }
                self.symbols.append(symbol)
            except ValueError as e:
                print(f"Warning: Invalid symbol data in line: {line} - {e}")
    
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
                    
                    # Extract size index if available
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
                        'size_multiplier': size_multiplier
                    }
                    self.texts.append(text)
                except ValueError as e:
                    print(f"Warning: Invalid text coordinates in line: {line} - {e}")
        except ValueError:
            print(f"Warning: Invalid text format in line: {line}")
    
    def export_json(self, output_path: str):
        """Export the parsed data to a JSON file."""
        import json
        with open(output_path, 'w') as f:
            json.dump(self.parse(), f, indent=2) 