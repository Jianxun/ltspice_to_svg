"""
Text renderer for LTspice schematics.
Handles rendering of text elements in SVG format.
"""
import svgwrite
from typing import Dict
from .base_renderer import BaseRenderer

class TextRenderer(BaseRenderer):
    """Renderer for text elements."""
    
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
    
    def render(self, text: Dict, font_size: float = 22.0) -> None:
        """Render a text element.
        
        Args:
            text: Dictionary containing text properties:
                - x: X coordinate
                - y: Y coordinate
                - text: Text content
                - justification: Text alignment ('Left', 'Right', 'Center', 'Top', 'Bottom')
                - size_multiplier: Font size multiplier index (0-7)
            font_size: Base font size in pixels
        """
        # Skip if no text content
        if not text.get('text'):
            return
            
        # Get text properties with defaults
        x = text.get('x', 0)
        y = text.get('y', 0)
        content = text.get('text', '')
        justification = text.get('justification', 'Left')
        size_multiplier = text.get('size_multiplier', 2)  # Default to size 2 (1.5x)
        
        # Calculate actual font size
        font_size = font_size * self.SIZE_MULTIPLIERS.get(size_multiplier, self.SIZE_MULTIPLIERS[2])
        
        # Set text alignment based on justification
        if justification == 'Left':
            text_anchor = 'start'
        elif justification == 'Right':
            text_anchor = 'end'
        else:  # Center, Top, Bottom all use middle horizontal alignment
            text_anchor = 'middle'
        
        # Adjust vertical position based on justification
        if justification in ['Left', 'Center', 'Right']:
            y_offset = font_size * 0.3  # Move up to center vertically
        elif justification == 'Top':
            y_offset = font_size * 0.6  # Move down
        else:  # Bottom
            y_offset = font_size * 0.0  # Move up
        
        # Create multiline text element
        text_element = self._create_multiline_text(
            content,
            x,
            y + y_offset,
            font_size,
            text_anchor
        )
        self.dwg.add(text_element)
        
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
        
        # Split text into lines
        lines = text_content.split('\n')
        
        # Calculate line height
        line_height = font_size * line_spacing
        
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
            group.add(text_element)
            
        return group 