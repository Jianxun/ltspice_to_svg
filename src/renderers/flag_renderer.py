"""
Flag rendering functions for SVG generation.
Handles rendering of various flags (ground, IO pins, net labels) with proper scaling and styling.
"""
import svgwrite
import json
import os
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
from .base_renderer import BaseRenderer

@dataclass
class LineDefinition:
    start: Tuple[float, float]
    end: Tuple[float, float]
    stroke: str
    stroke_linecap: str

class FlagType(Enum):
    GROUND = "ground"
    NET_LABEL = "net_label"
    IO_PIN = "io_pin"

class FlagOrientation(Enum):
    RIGHT = "right"
    LEFT = "left"
    UP = "up"
    DOWN = "down"

class FlagRenderer(BaseRenderer):
    """Renderer for flags in the schematic."""
    
    # Constants
    NET_LABEL_DISTANCE = 52.0  # Distance of net label text from origin
    
    def __init__(self, dwg: svgwrite.Drawing):
        super().__init__(dwg)
        self._base_font_size = 12.0
        self._stroke_width = self.DEFAULT_STROKE_WIDTH
        self._flag_definitions: Dict[FlagType, List[LineDefinition]] = {}
        self._load_flag_definitions()
        
    @property
    def base_font_size(self) -> float:
        """Get the base font size."""
        return self._base_font_size
        
    @base_font_size.setter
    def base_font_size(self, value: float) -> None:
        """Set the base font size.
        
        Args:
            value: The new base font size
        """
        self._base_font_size = value
        
    @property
    def stroke_width(self) -> float:
        """Get the stroke width."""
        return self._stroke_width
        
    @stroke_width.setter
    def stroke_width(self, value: float) -> None:
        """Set the stroke width.
        
        Args:
            value: The new stroke width
        """
        self._stroke_width = value
        
    def _load_flag_definitions(self):
        """Load flag definitions from JSON files."""
        definitions_dir = os.path.join(os.path.dirname(__file__), "flag_definitions")
        for flag_type in FlagType:
            json_path = os.path.join(definitions_dir, f"{flag_type.value}_flag.json")
            if os.path.exists(json_path):
                with open(json_path, 'r') as f:
                    data = json.load(f)
                    self._flag_definitions[flag_type] = [
                        LineDefinition(
                            start=tuple(line["start"]),
                            end=tuple(line["end"]),
                            stroke=line["stroke"],
                            stroke_linecap=line["stroke_linecap"]
                        )
                        for line in data["lines"]
                    ]

    def render_ground_flag(self, flag: Dict,
                          target_group: Optional[svgwrite.container.Group] = None) -> None:
        """Render a ground flag.
        
        The ground flag is rendered with a V shape pointing in the direction of the flag's orientation.
        The shape is based on the gnd.asy reference file:
        - Horizontal line at top: (-16,0) to (16,0)
        - Two diagonal lines forming a V:
          - Left line: (-16,0) to (0,16)
          - Right line: (16,0) to (0,16)
        
        Args:
            flag: Dictionary containing ground flag properties:
                - x: X coordinate
                - y: Y coordinate
                - orientation: Rotation angle in degrees
            target_group: Optional group to add the flag to
        """
        # Create a group for the ground flag
        g = self.dwg.g()
        
        # Apply translation and rotation
        transform = [
            f"translate({flag['x']},{flag['y']})",
            f"rotate({flag['orientation']})"
        ]
        g.attribs['transform'] = ' '.join(transform)
        
        # Add V shape
        # Horizontal line
        g.add(self.dwg.line(
            (-16, 0), (16, 0),
            stroke='black', stroke_width=self.stroke_width, stroke_linecap='round'
        ))
        # Left diagonal line
        g.add(self.dwg.line(
            (-16, 0), (0, 16),
            stroke='black', stroke_width=self.stroke_width, stroke_linecap='round'
        ))
        # Right diagonal line
        g.add(self.dwg.line(
            (16, 0), (0, 16),
            stroke='black', stroke_width=self.stroke_width, stroke_linecap='round'
        ))
        
        # Add the group to the target group or drawing
        if target_group is not None:
            target_group.add(g)
        else:
            self.dwg.add(g)
        
    def render_net_label(self, flag: Dict,
                        target_group: Optional[svgwrite.container.Group] = None) -> None:
        """Render a net label.
        
        Args:
            flag: Dictionary containing net label properties:
                - x: X coordinate
                - y: Y coordinate
                - net_name: Name of the net/signal
                - orientation: Rotation angle in degrees
            target_group: Optional group to add the flag to
        """
        # TODO: Implement net label rendering
        pass
        
    def render_io_pin(self, flag: Dict,
                     target_group: Optional[svgwrite.container.Group] = None) -> None:
        """Render an IO pin.
        
        Args:
            flag: Dictionary containing IO pin properties:
                - x: X coordinate
                - y: Y coordinate
                - net_name: Name of the net/signal
                - orientation: Rotation angle in degrees
                - direction: Pin direction ('BiDir', 'In', or 'Out')
            target_group: Optional group to add the flag to
        """
        # TODO: Implement IO pin rendering
        pass 