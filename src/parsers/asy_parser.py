"""
Parser for LTspice ASY symbol files.
Extracts line drawing information from symbol files.
"""
from typing import Dict, List, Tuple

class ASYParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.lines: List[Dict[str, int]] = []
        self.circles: List[Dict[str, int]] = []  # Add circles list
        
    def parse(self) -> Dict[str, any]:
        """Parse the ASY file and return a dictionary containing line and circle information."""
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
                
        return {
            'lines': self.lines,
            'circles': self.circles
        }
    
    def _parse_line(self, line: str):
        """Parse a LINE entry and extract coordinates."""
        # Format: LINE Normal x1 y1 x2 y2
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
                # Add any additional attributes if present
                if len(parts) > 6:
                    line_data['attributes'] = ' '.join(parts[6:])
                self.lines.append(line_data)
            except ValueError as e:
                print(f"Warning: Invalid line coordinates in line: {line} - {e}")
    
    def _parse_circle(self, line: str):
        """Parse a CIRCLE entry and extract coordinates.
        Format: CIRCLE Normal x1 y1 x2 y2
        where (x1,y1) and (x2,y2) define the bounding box
        """
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
                # Add any additional attributes if present
                if len(parts) > 6:
                    circle_data['attributes'] = ' '.join(parts[6:])
                self.circles.append(circle_data)
            except ValueError as e:
                print(f"Warning: Invalid circle coordinates in line: {line} - {e}")
    
    def export_json(self, output_path: str):
        """Export the parsed data to a JSON file."""
        import json
        with open(output_path, 'w') as f:
            json.dump(self.parse(), f, indent=2) 