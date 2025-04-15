"""
Text renderer for LTspice schematics.
Handles rendering of text elements in SVG format.
"""
import svgwrite
from typing import Dict, Optional
import logging
from .base_renderer import BaseRenderer

class TextRenderer(BaseRenderer):
    """Renderer for text elements."""
    
    def __init__(self, dwg: svgwrite.Drawing):
        """Initialize the text renderer.
        
        Args:
            dwg: The SVG drawing to render into
        """
        super().__init__(dwg)
        self.logger = logging.getLogger(self.__class__.__name__)
        self._base_font_size = 16.0  # Default base font size
    
    # Font size multiplier mapping
    SIZE_MULTIPLIERS = {
        0: 0.625,  # 0.625x base size
        1: 1.0,    # 1.0x base size
        2: 1.5,    # 1.5x base size (default)
        3: 2.0,    # 2.0x base size
        4: 2.5,    # 2.5x base size
        5: 3.5,    # 3.5x base size
        6: 5.0,    # 5.0x base size
        7: 7.0     # 7.0x base size
    }
    
    # Vertical offset multipliers for normal text justification
    TEXT_OFFSETS = {
        'Top': 0.9,     # Move down from baseline
        'Bottom': -0.2,  # Move up from baseline
        'Center': 0.35,   # Center vertically
        'VTop': 0.8,     # Move right from baseline
        'VBottom': -0.2,  # Move left from baseline
        'VCenter': 0   # Center horizontally
    }
    
    @property
    def base_font_size(self) -> float:
        """Get the base font size in pixels."""
        return self._base_font_size
    
    @base_font_size.setter
    def base_font_size(self, value: float) -> None:
        """Set the base font size in pixels.
        
        Args:
            value: The new base font size in pixels
        """
        if value <= 0:
            raise ValueError("Base font size must be positive")
        self._base_font_size = value
        self.logger.debug(f"Base font size set to {value}px")
    
    def render(self, text: Dict, target_group: Optional[svgwrite.container.Group] = None) -> None:
        """Render a text element.
        
        Args:
            text: Dictionary containing text properties:
                - x: X coordinate
                - y: Y coordinate
                - text: Text content
                - justification: Text alignment ('Left', 'Right', 'Center', 'Top', 'Bottom', 'VLeft', 'VRight', 'VCenter', 'VTop', 'VBottom')
                - size_multiplier: Font size multiplier index (0-7)
                - type: Text type ('spice' or 'comment')
                - is_mirrored: Whether the text is in a mirrored symbol
            target_group: Optional group to add the text to. If None, adds to drawing.
        """
        # Skip if no text content
        if not text.get('text'):
            self.logger.warning("Skipping text element with no content")
            return
            
        # Get text properties with defaults
        x = text.get('x', 0)
        y = text.get('y', 0)
        content = text.get('text', '')
        justification = text.get('justification', 'Left')
        size_multiplier = text.get('size_multiplier', 2)  # Default to size 2 (1.5x)
        text_type = text.get('type', 'comment')  # Default to comment type
        is_mirrored = text.get('is_mirrored', False)  # Default to not mirrored
        
        self.logger.info(f"Rendering text: '{content}' at ({x},{y})")
        self.logger.info(f"Properties: justification={justification}, size_multiplier={size_multiplier}, "
                         f"text_type={text_type}, is_mirrored={is_mirrored}")
        
        # Strip prefix based on text type
        if text_type == 'spice' and content.startswith('!'):
            content = content[1:]  # Remove ! prefix
            #self.logger.debug("Removed '!' prefix from spice text")
        elif text_type == 'comment' and content.startswith(';'):
            content = content[1:]  # Remove ; prefix
            #self.logger.debug("Removed ';' prefix from comment text")
            
        # Calculate actual font size
        font_size = self._base_font_size * self.SIZE_MULTIPLIERS.get(size_multiplier, self.SIZE_MULTIPLIERS[2])
        self.logger.debug(f"Calculated font size: {font_size}px")
        
        # Handle vertical text (rotated 90 degrees counter-clockwise)
        is_vertical = justification.startswith('V')
        if is_vertical:
            # Remove 'V' prefix for alignment handling
            justification = justification[1:]
            # Create a group for the rotated text
            group = self.dwg.g()
            # Add rotation transform
            group.attribs['transform'] = f"rotate(-90, {x}, {y})"
            self.logger.debug(f"Vertical text rotation: {group.attribs['transform']}")
        
        # Set text alignment based on justification
        if justification == 'Left':
            text_anchor = 'start' if not is_mirrored else 'end'
            x_offset = 0
        elif justification == 'Right':
            text_anchor = 'end' if not is_mirrored else 'start'
            x_offset = 0
        else:  # Center, Top, Bottom
            text_anchor = 'middle'
            x_offset = 0
        
        self.logger.info(f"Text anchor: {text_anchor} (original justification: {justification}, mirrored: {is_mirrored})")
        
        # Adjust vertical position based on justification
        if justification in ['Left', 'Center', 'Right']:
            y_offset = font_size * self.TEXT_OFFSETS['Center']  # Move up to center vertically
        elif justification == 'Top':
            y_offset = font_size * (self.TEXT_OFFSETS['Top'] if is_vertical else self.TEXT_OFFSETS['Top'])  # Move down
        elif justification == 'Bottom':
            y_offset = font_size * (self.TEXT_OFFSETS['Bottom'] if is_vertical else self.TEXT_OFFSETS['Bottom'])  # Move up slightly

        # Adjust vertical position based on justification
        if justification in ['VLeft', 'VCenter', 'VRight']:
            y_offset = font_size * self.TEXT_OFFSETS['VCenter']  # Move up to center vertically
        elif justification == 'VTop':
            y_offset = font_size * (self.TEXT_OFFSETS['VTop'] if is_vertical else self.TEXT_OFFSETS['Top'])  # Move down
        elif justification == 'VBottom':
            y_offset = font_size * (self.TEXT_OFFSETS['VBottom'] if is_vertical else self.TEXT_OFFSETS['Bottom'])  # Move up slightly
        

        self.logger.debug(f"Position offsets: x={x_offset}, y={y_offset}")
        
        # Create multiline text element
        text_element = self._create_multiline_text(
            content,
            x + x_offset,
            y + y_offset,
            font_size,
            text_anchor
        )
        
        # If the symbol is mirrored, we need to counter-mirror the text
        if is_mirrored:
            # Create a group for the text with counter-mirroring
            text_group = self.dwg.g()
            text_group.attribs['transform'] = f"scale(-1,1) translate({-2*(x + x_offset)},0)"
            text_group.add(text_element)
            text_element = text_group
            self.logger.debug(f"Added counter-mirroring transform: {text_group.attribs['transform']}")
        
        # For vertical text (VTop, VBottom), we need to rotate the text 90 degrees
        if is_vertical:
            # Create a group for the text with rotation
            text_group = self.dwg.g()
            # Rotate around the text position
            text_group.attribs['transform'] = f"rotate(-90, {x}, {y})"
            text_group.add(text_element)
            text_element = text_group
            self.logger.debug(f"Added vertical text rotation transform: {text_group.attribs['transform']}")
        
        # Add text to target group or drawing
        if target_group is not None:
            target_group.add(text_element)
            self.logger.debug("Added text element to target group")
        else:
            self.dwg.add(text_element)
            self.logger.debug("Added text element to drawing")
        
    def _create_multiline_text(self, text_content: str, x: float, y: float, 
                            font_size: float, text_anchor: str = 'start', 
                            line_spacing: float = 1.2) -> svgwrite.container.Group:
        """Create a group of text elements for multiline text.
        
        Args:
            text_content: The text to render, may contain newlines
            x: X coordinate
            y: Y coordinate
            font_size: Font size in pixels
            text_anchor: Text alignment ('start', 'middle', or 'end')
            line_spacing: Line spacing multiplier (1.2 = 120% of font size)
            
        Returns:
            A group containing text elements for each line
        """
        # Create a group to hold all text elements
        group = self.dwg.g()
        group.attribs['class'] = 'text-group'  # Add class for testing
        
        # Split text into lines
        lines = text_content.split('\n')
        
        # Calculate line height
        line_height = font_size * line_spacing
        
        self.logger.debug(f"Creating multiline text at ({x},{y}) with {len(lines)} lines")
        
        # Add each line as a separate text element
        for i, line in enumerate(lines):
            # Calculate y position for this line
            line_y = y + (i * line_height)
            
            # Create text element
            text_element = self.dwg.text(line,
                                      insert=(x, line_y),
                                      font_family='Arial',
                                      font_size=f'{font_size}px',
                                      text_anchor=text_anchor,
                                      fill='black')
            self.logger.debug(f"Line {i}: '{line}' at ({x},{line_y}) with anchor {text_anchor}")
            group.add(text_element)
            
        return group 