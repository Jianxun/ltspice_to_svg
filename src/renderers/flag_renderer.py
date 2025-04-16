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
from .text_renderer import TextRenderer
import logging

@dataclass
class LineDefinition:
    start: Tuple[float, float]
    end: Tuple[float, float]
    stroke: str
    stroke_linecap: str

@dataclass
class TextDefinition:
    font_family: str
    font_size: int
    text_anchor: str
    fill: str
    distance: float

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
        self._flag_definitions: Dict[FlagType, List[LineDefinition]] = {}
        self._text_definitions: Dict[FlagType, TextDefinition] = {}
        self._text_renderer = TextRenderer(dwg)
        self._text_renderer.base_font_size = self.base_font_size  # Initialize with parent's base font size
        self._load_flag_definitions()
        
    @BaseRenderer.base_font_size.setter
    def base_font_size(self, value: float) -> None:
        """Override base_font_size setter to update TextRenderer's font size.
        
        Args:
            value: The new base font size
        """
        BaseRenderer.base_font_size.fset(self, value)  # Call parent's setter
        self._text_renderer.base_font_size = value  # Update TextRenderer's font size

    def _load_flag_definitions(self):
        """Load flag definitions from JSON files."""
        definitions_dir = os.path.join(os.path.dirname(__file__), "flag_definitions")
        for flag_type in FlagType:
            json_path = os.path.join(definitions_dir, f"{flag_type.value}_flag.json")
            if os.path.exists(json_path):
                with open(json_path, 'r') as f:
                    data = json.load(f)
                    if "lines" in data:
                        self._flag_definitions[flag_type] = [
                            LineDefinition(
                                start=tuple(line["start"]),
                                end=tuple(line["end"]),
                                stroke=line["stroke"],
                                stroke_linecap=line["stroke_linecap"]
                            )
                            for line in data["lines"]
                        ]
                    if "text" in data:
                        self._text_definitions[flag_type] = TextDefinition(
                            font_family=data["text"]["font_family"],
                            font_size=data["text"]["font_size"],
                            text_anchor=data["text"]["text_anchor"],
                            fill=data["text"]["fill"],
                            distance=data["text"]["distance"]
                        )

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
        
        # Add lines from flag definition
        for line in self._flag_definitions[FlagType.GROUND]:
            g.add(self.dwg.line(
                line.start, line.end,
                stroke=line.stroke,
                stroke_width=self.stroke_width,
                stroke_linecap=line.stroke_linecap
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
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("Rendering net label:")
        self.logger.debug(f"  Position: ({flag.get('x', 0)}, {flag.get('y', 0)})")
        self.logger.debug(f"  Net name: {flag.get('net_name', '')}")
        self.logger.debug(f"  Orientation: {flag.get('orientation', 0)}")
        self.logger.debug(f"  Target group provided: {target_group is not None}")
        
        # Use the provided group or create a new one
        g = target_group if target_group is not None else self.dwg.g()
        
        # Apply translation and rotation
        transform = [
            f"translate({flag['x']},{flag['y']})",
            f"rotate({flag['orientation']})"
        ]
        g.attribs['transform'] = ' '.join(transform)
        self.logger.debug(f"  Applied transform: {g.attribs['transform']}")
        
        # Get text definition
        text_def = self._text_definitions[FlagType.NET_LABEL]
        self.logger.debug(f"  Text definition: {text_def}")
        
        # Create text group with normalized rotation
        text_group = self.dwg.g()
        self.logger.debug("  Created text group")
        
        # For 180° orientation, counter-rotate the text to make it appear as 0°
        if flag['orientation'] == 180:
            text_group.attribs['transform'] = f"rotate(-180)"
            self.logger.debug("  Applied counter-rotation for 180° orientation")
        
        # Create text properties for TextRenderer
        text_properties = {
            'x': 0,
            'y': 0,  # Position above the pin point
            'text': flag['net_name'],
            'justification': 'Bottom',  # Bottom-justified
            'size_multiplier': text_def.font_size,
            'type': 'comment',  # Net labels are treated as comments
            'is_mirrored': False  # No mirroring for net labels
        }
        self.logger.debug(f"  Text properties: {text_properties}")
        
        # Use TextRenderer to render the text
        self._text_renderer.render(text_properties, text_group)
        self.logger.debug("  Rendered text using TextRenderer")
        
        # Add text group to main group
        g.add(text_group)
        self.logger.debug("  Added text group to main group")
        
        # Add the group to the drawing if no target group was provided
        if target_group is None:
            self.dwg.add(g)
            self.logger.debug("  Added net label group directly to drawing")
        
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