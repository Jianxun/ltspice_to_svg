"""
Flag rendering functions for SVG generation.
Handles rendering of various flags (ground, IO pins, net labels) with proper scaling and styling.
"""
import svgwrite
import json
import os
from typing import Dict, Optional
from enum import Enum
from .base_renderer import BaseRenderer
from .text_renderer import TextRenderer
from .rendering_config import RenderingConfig
import logging

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
    
    def __init__(self, dwg: svgwrite.Drawing, config: Optional[RenderingConfig] = None):
        super().__init__(dwg, config)
        self._flag_definitions: Dict = {}
        self._text_renderer = TextRenderer(dwg, config)
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
        """Load flag definitions from JSON file."""
        json_path = os.path.join(os.path.dirname(__file__), "flag_definitions", "flags.json")
        with open(json_path, 'r') as f:
            self._flag_definitions = json.load(f)

    def render_ground_flag(self, flag: Dict,
                          target_group: Optional[svgwrite.container.Group] = None) -> None:
        """Render a ground flag.
        
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
        for line in self._flag_definitions["ground"]["lines"]:
            g.add(self.dwg.line(
                line["start"], line["end"],
                stroke='black',
                stroke_width=self.stroke_width,
                stroke_linecap='round'
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
                - attached_to_wire_end: Boolean indicating if the label is at a wire end
            target_group: Optional group to add the flag to
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("Rendering net label:")
        self.logger.debug(f"  Position: ({flag.get('x', 0)}, {flag.get('y', 0)})")
        self.logger.debug(f"  Net name: {flag.get('net_name', '')}")
        self.logger.debug(f"  Orientation: {flag.get('orientation', 0)}")
        self.logger.debug(f"  Attached to wire end: {flag.get('attached_to_wire_end', False)}")
        
        # Get text definition
        text_def = self._flag_definitions["net_label"]["text"]
        self.logger.debug(f"  Text definition: {text_def}")
        
        # Get anchor point coordinates
        anchor_x = text_def["anchor"]["x"]
        anchor_y = text_def["anchor"]["y"]
        
        # Calculate text position and justification based on orientation
        orientation = flag['orientation']
        if orientation == 0:  # Right
            text_x = flag['x'] + anchor_x
            text_y = flag['y'] + anchor_y
            justification = "VRight" if flag.get('attached_to_wire_end', False) else "VBottom"
        elif orientation == 90:  # Up
            text_x = flag['x'] - anchor_y
            text_y = flag['y'] + anchor_x
            justification = "Right" if flag.get('attached_to_wire_end', False) else "VBottom"
        elif orientation == 180:  # Left
            text_x = flag['x'] - anchor_x
            text_y = flag['y'] - anchor_y
            justification = "VLeft" if flag.get('attached_to_wire_end', False) else "Bottom"
        else:  # 270, Down
            text_x = flag['x'] + anchor_y
            text_y = flag['y'] - anchor_x
            justification = "Left" if flag.get('attached_to_wire_end', False) else "VBottom"
            
        self.logger.debug(f"  Text position: ({text_x}, {text_y})")
        self.logger.debug(f"  Text justification: {justification}")
        
        # Create text properties for TextRenderer
        text_properties = {
            'x': text_x,
            'y': text_y,
            'text': flag['net_name'],
            'justification': justification,
            'size_multiplier': 2,
            'type': 'comment',  # Net labels are treated as comments
            'is_mirrored': False  # No mirroring for net labels
        }
        self.logger.debug(f"  Text properties: {text_properties}")
        
        # Render text directly to the drawing
        self._text_renderer.render(text_properties, self.dwg)
        self.logger.debug("  Rendered text using TextRenderer")
        
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
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("Rendering IO pin:")
        self.logger.debug(f"  Position: ({flag.get('x', 0)}, {flag.get('y', 0)})")
        self.logger.debug(f"  Net name: {flag.get('net_name', '')}")
        self.logger.debug(f"  Orientation: {flag.get('orientation', 0)}")
        self.logger.debug(f"  Direction: {flag.get('direction', 'BiDir')}")
        self.logger.debug(f"  Target group provided: {target_group is not None}")
        
        # Use the provided group or create a new one
        g = target_group if target_group is not None else self.dwg.g()
        
        # Apply translation and rotation for the shape
        transform = [
            f"translate({flag['x']},{flag['y']})",
            f"rotate({flag['orientation']})"
        ]
        g.attribs['transform'] = ' '.join(transform)
        self.logger.debug(f"  Applied transform: {g.attribs['transform']}")
        
        # Get line definitions for the specific direction
        direction = flag.get('direction', 'BiDir')
        if direction not in self._flag_definitions["io_pin"]["directions"]:
            self.logger.warning(f"Unknown IO pin direction: {direction}, using BiDir")
            direction = 'BiDir'
            
        # Add lines for the pin shape
        for line in self._flag_definitions["io_pin"]["directions"][direction]["lines"]:
            g.add(self.dwg.line(
                line["start"], line["end"],
                stroke='black',  # Default stroke color
                stroke_width=self.stroke_width,
                stroke_linecap='round'  # Default line cap style
            ))
        
        # Get text definition for this direction
        text_def = self._flag_definitions["io_pin"]["directions"][direction]["text"]
        self.logger.debug(f"  Text definition: {text_def}")
        
        # Get anchor point coordinates
        anchor_x = text_def["anchor"]["x"]
        anchor_y = text_def["anchor"]["y"]
        
        # Calculate text position and justification based on orientation
        orientation = flag['orientation']
        if orientation == 0:  # Down
            text_x = flag['x'] + anchor_x
            text_y = flag['y'] + anchor_y
            justification = "VRight"
        elif orientation == 90:  # Left
            text_x = flag['x'] - anchor_y
            text_y = flag['y'] + anchor_x
            justification = "Right"
        elif orientation == 180:  # Up
            text_x = flag['x'] - anchor_x
            text_y = flag['y'] - anchor_y
            justification = "VLeft"
        else:  # 270, Right
            text_x = flag['x'] + anchor_y
            text_y = flag['y'] - anchor_x
            justification = "Left"
            
        self.logger.debug(f"  Text position: ({text_x}, {text_y})")
        self.logger.debug(f"  Text justification: {justification}")
        
        # Create text properties for TextRenderer
        text_properties = {
            'x': text_x,
            'y': text_y,
            'text': flag['net_name'],
            'justification': justification,
            'size_multiplier': 2,
            'type': 'comment',  # IO pin labels are treated as comments
            'is_mirrored': False  # No mirroring for IO pin labels
        }
        self.logger.debug(f"  Text properties: {text_properties}")
        
        # Render text directly to the drawing
        self._text_renderer.render(text_properties, self.dwg)
        self.logger.debug("  Rendered text using TextRenderer")
        
        # Add the shape group to the drawing if no target group was provided
        if target_group is None:
            self.dwg.add(g)
            self.logger.debug("  Added IO pin group directly to drawing") 