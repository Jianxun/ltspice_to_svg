"""
Flag renderer for LTspice schematics.
Handles rendering of various flags (ground, IO pins, net labels) in SVG format.
"""
import svgwrite
from typing import Dict, List
from .net_label_renderer import render_net_label

def render_ground_flag(dwg: svgwrite.Drawing, flag: Dict, scale: float, stroke_width: float) -> None:
    """Add a ground flag to the SVG drawing with a V shape.
    
    The ground flag is rendered with a V shape pointing in the direction of the flag's orientation.
    The shape is based on the gnd.asy reference file:
    - Horizontal line at top: (-16,0) to (16,0)
    - Two diagonal lines forming a V:
      - Left line: (-16,0) to (0,16)
      - Right line: (16,0) to (0,16)
    
    Args:
        dwg: SVG drawing object
        flag: Dictionary containing flag properties:
            - x: X coordinate
            - y: Y coordinate
            - orientation: Rotation angle in degrees
        scale: Scale factor for coordinates
        stroke_width: Width of lines
    """
    # Create a group for the ground flag
    g = dwg.g()
    
    # Apply translation and rotation
    transform = [
        f"translate({flag['x'] * scale},{flag['y'] * scale})",
        f"rotate({flag['orientation']})"
    ]
    g.attribs['transform'] = ' '.join(transform)
    
    # Add V shape
    # Horizontal line
    g.add(dwg.line(
        (-16 * scale, 0), (16 * scale, 0),
        stroke='black', stroke_width=stroke_width, stroke_linecap='round'
    ))
    # Left diagonal line
    g.add(dwg.line(
        (-16 * scale, 0), (0, 16 * scale),
        stroke='black', stroke_width=stroke_width, stroke_linecap='round'
    ))
    # Right diagonal line
    g.add(dwg.line(
        (16 * scale, 0), (0, 16 * scale),
        stroke='black', stroke_width=stroke_width, stroke_linecap='round'
    ))
    
    # Add the group to the drawing
    dwg.add(g)

def render_io_pin(dwg: svgwrite.Drawing, io_pin: Dict, scale: float, stroke_width: float, 
                 font_size: float, size_multipliers: Dict[int, float], 
                 text_centering_compensation: float) -> None:
    """Add an IO pin flag to the SVG drawing with direction-specific shapes.
    
    Args:
        dwg: SVG drawing object
        io_pin: Dictionary containing IO pin properties:
            - x: X coordinate
            - y: Y coordinate
            - net_name: Name of the net/signal
            - orientation: Rotation angle in degrees
            - direction: Pin direction ('BiDir', 'In', or 'Out')
        scale: Scale factor for coordinates
        stroke_width: Width of lines
        font_size: Base font size in pixels
        size_multipliers: Dictionary mapping size indices to font size multipliers
        text_centering_compensation: Factor for text centering compensation
    """
    print(f"\n[DEBUG] render_io_pin: Start rendering IO pin '{io_pin['net_name']}'")
    print(f"[DEBUG] render_io_pin: Pin position: ({io_pin['x']}, {io_pin['y']}), orientation: {io_pin['orientation']}°")
    print(f"[DEBUG] render_io_pin: Scale factor: {scale}")
    
    # Create a group for the IO pin shape only
    g = dwg.g()
    
    # Apply translation and rotation for the shape
    transform = [
        f"translate({io_pin['x'] * scale},{io_pin['y'] * scale})",
        f"rotate({io_pin['orientation']})"
    ]
    g.attribs['transform'] = ' '.join(transform)
    print(f"[DEBUG] render_io_pin: Shape group transform: {g.attribs['transform']}")
    
    # Add shape based on direction
    if io_pin['direction'] == 'BiDir':
        # BiDir shape from io_pin_bi_dir.asy
        g.add(dwg.line(
            (16 * scale, 16 * scale), (0, 0),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
        g.add(dwg.line(
            (-16 * scale, 84 * scale), (-16 * scale, 16 * scale),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
        g.add(dwg.line(
            (16 * scale, 16 * scale), (16 * scale, 84 * scale),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
        g.add(dwg.line(
            (0, 0), (-16 * scale, 16 * scale),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
        g.add(dwg.line(
            (0, 100 * scale), (-16 * scale, 84 * scale),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
        g.add(dwg.line(
            (0, 100 * scale), (16 * scale, 84 * scale),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
    elif io_pin['direction'] == 'In':
        # Input shape from io_pin_input.asy
        g.add(dwg.line(
            (0, 0), (16 * scale, 16 * scale),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
        g.add(dwg.line(
            (16 * scale, 16 * scale), (16 * scale, 80 * scale),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
        g.add(dwg.line(
            (16 * scale, 80 * scale), (-16 * scale, 80 * scale),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
        g.add(dwg.line(
            (-16 * scale, 80 * scale), (-16 * scale, 16 * scale),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
        g.add(dwg.line(
            (-16 * scale, 16 * scale), (0, 0),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
    else:  # Out
        # Output shape from io_pin_output.asy
        g.add(dwg.line(
            (-16 * scale, 80 * scale), (0, 96 * scale),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
        g.add(dwg.line(
            (16 * scale, 16 * scale), (16 * scale, 80 * scale),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
        g.add(dwg.line(
            (16 * scale, 16 * scale), (-16 * scale, 16 * scale),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
        g.add(dwg.line(
            (-16 * scale, 80 * scale), (-16 * scale, 16 * scale),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
        g.add(dwg.line(
            (0, 96 * scale), (16 * scale, 80 * scale),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
        g.add(dwg.line(
            (0, 16 * scale), (0, 0),
            stroke='black', stroke_width=stroke_width, stroke_linecap='round'
        ))
    
    # Add the shape group to the drawing
    dwg.add(g)
    
    # Calculate absolute text position and rotation
    orientation = io_pin['orientation']
    text_distance = 52  # Distance from pin point
    font_size = font_size * size_multipliers[2]  # Size 2 (1.5x)
    
    # Calculate text position based on pin orientation
    if orientation == 0:  # Right
        text_x = io_pin['x'] * scale
        text_y = (io_pin['y'] + text_distance) * scale
        text_rotation = -90
        # For vertical text, shift right by compensation factor of the font size
        text_x += font_size * text_centering_compensation
    elif orientation == 90:  # Up
        text_x = (io_pin['x'] - text_distance) * scale
        text_y = io_pin['y'] * scale
        text_rotation = 0
        # For horizontal text, shift down by compensation factor of the font size
        text_y += font_size * text_centering_compensation
    elif orientation == 180:  # Left
        text_x = io_pin['x'] * scale
        text_y = (io_pin['y'] - text_distance) * scale
        text_rotation = -90
        # For vertical text, shift right by compensation factor of the font size
        text_x += font_size * text_centering_compensation
    else:  # 270, Down
        text_x = (io_pin['x'] + text_distance) * scale
        text_y = io_pin['y'] * scale
        text_rotation = 0
        # For horizontal text, shift down by compensation factor of the font size
        text_y += font_size * text_centering_compensation
        
    print(f"[DEBUG] render_io_pin: Text absolute position: ({text_x}, {text_y})")
    print(f"[DEBUG] render_io_pin: Text rotation: {text_rotation}°")
    print(f"[DEBUG] render_io_pin: Font size: {font_size}px")
    
    # Create text group with rotation only
    text_group = dwg.g()
    if text_rotation != 0:
        text_group.attribs['transform'] = f'rotate({text_rotation} {text_x} {text_y})'
    
    # Add text element
    text_element = dwg.text(
        io_pin['net_name'],
        insert=(text_x, text_y),
        font_family='Arial',
        font_size=f'{font_size}px',
        text_anchor='middle',  # Center-justified
        fill='black'
    )
    
    # Add text to group and group to drawing
    text_group.add(text_element)
    dwg.add(text_group)

def render_flags(dwg: svgwrite.Drawing, flags: List[Dict], io_pins: List[Dict], 
                scale: float, stroke_width: float, font_size: float, 
                size_multipliers: Dict[int, float], net_label_distance: float,
                text_centering_compensation: float) -> None:
    """Render all flags in the schematic.
    
    Args:
        dwg: SVG drawing object
        flags: List of flag dictionaries, each containing:
            - type: Flag type ('net_label' or 'gnd')
            - x: X coordinate
            - y: Y coordinate
            - orientation: Rotation angle in degrees
            - net_name: Name of the net/signal (for net labels)
        io_pins: List of IO pin dictionaries, each containing:
            - x: X coordinate
            - y: Y coordinate
            - net_name: Name of the net/signal
            - orientation: Rotation angle in degrees
            - direction: Pin direction ('BiDir', 'In', or 'Out')
        scale: Scale factor for coordinates
        stroke_width: Width of lines
        font_size: Base font size in pixels
        size_multipliers: Dictionary mapping size indices to font size multipliers
        net_label_distance: Distance of net label text from origin
        text_centering_compensation: Factor for text centering compensation
    """
    # Add net labels and ground flags
    for flag in flags:
        if flag['type'] == 'net_label':
            render_net_label(
                dwg,
                flag,
                scale,
                font_size,
                size_multipliers,
                net_label_distance
            )
        elif flag['type'] == 'gnd':
            render_ground_flag(
                dwg,
                flag,
                scale,
                stroke_width
            )
    
    # Add IO pins
    for io_pin in io_pins:
        render_io_pin(
            dwg,
            io_pin,
            scale,
            stroke_width,
            font_size,
            size_multipliers,
            text_centering_compensation
        ) 