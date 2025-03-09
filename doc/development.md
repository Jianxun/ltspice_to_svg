# Development Guide

This document provides technical details about the implementation of the LTspice to SVG converter and guidelines for contributing to the project.

## Project Structure

```
ltspice_to_svg/
├── src/
│   ├── parsers/
│   │   ├── asc_parser.py    # Parses .asc schematic files
│   │   └── asy_parser.py    # Parses .asy symbol files
│   ├── generators/
│   │   └── svg_generator.py # Generates SVG output
│   └── ltspice_to_svg.py    # Main script
├── tests/
│   └── test_ltspice_to_svg.py
├── doc/
│   └── development.md       # This file
└── requirements.txt
```

## Implementation Details

### File Parsing

#### ASC Parser (`asc_parser.py`)
- Handles both UTF-16 and UTF-8 encoded files
- Extracts the following elements:
  - Wires: Coordinates (x1, y1) to (x2, y2)
  - Symbols: Name, instance name, position, rotation
  - Text: Content, position, justification, size
  - Flags: Net names and positions
  - IO Pins: Port definitions
- Automatically adds GND symbols for ground flags
- Caches parsed data to avoid re-parsing

##### Flag and Wire Direction Handling
- Wire directions are calculated using a 90-degree grid system:
  - 0°: Left (negative X)
  - 90°: Up (negative Y)
  - 180°: Right (positive X)
  - 270°: Down (positive Y)
- Flag orientation rules:
  1. Single wire connection:
     - Flag points in the same direction as the wire
  2. Two opposite wires:
     - Vertical wires (90° or 270°): Flag points right (180°)
     - Horizontal wires (0° or 180°): Flag points down (270°)
  3. Default cases:
     - No connected wires: Points left (0°)
     - Non-opposite wire pairs: Points left (0°)
     - More than two wires: Points left (0°)
- Implementation considerations:
  - Wire direction calculation uses atan2 for angle computation
  - Angles are normalized to the 90-degree grid system
  - Flag orientation ensures consistent rendering across the schematic
  - Special handling for ground flags and IO pins to maintain visual consistency

#### ASY Parser (`asy_parser.py`)
- Parses symbol definition files
- Extracts geometric elements:
  - Lines with styles (solid, dashed)
  - Circles and ellipses
  - Rectangles
  - Arcs with start/end angles
- Handles text elements for pin labels and properties
- Supports symbol-specific text positioning

##### WINDOW Line Parsing Strategy
WINDOW lines in LTspice symbol files define text positioning and properties for various symbol attributes.

1. **Format**
```
WINDOW <type> <x> <y> <justification> [size_multiplier]
```

2. **Window Types**
- `WINDOW 0`: Instance name position (e.g., "M1", "R1")
- `WINDOW 3`: Component value position (e.g., "1k", "10u")
- Other types may exist for symbol-specific text

3. **Parameters**
- `x, y`: Relative coordinates from symbol origin
- `justification`: Text alignment
  - Basic: Left, Right, Center
  - Vertical variants: Top, Bottom
  - Combined: VTop, VBottom (for vertical text)
- `size_multiplier`: Optional font size index (0-7)

4. **Implementation Structure**
```python
# Enums for type safety
class WindowType(Enum):
    INSTANCE_NAME = 0  # Component name (M1, R1, etc.)
    VALUE = 3         # Component value (1k, 10u, etc.)

class TextJustification(Enum):
    LEFT = "Left"
    RIGHT = "Right"
    CENTER = "Center"
    TOP = "Top"
    BOTTOM = "Bottom"
    VTOP = "VTop"      # Vertical text, top aligned
    VBOTTOM = "VBottom"  # Vertical text, bottom aligned

# Data structure for parsed window data
@dataclass
class WindowData:
    window_type: WindowType
    x: float
    y: float
    justification: TextJustification
    size_multiplier: int = 2  # Default size multiplier
    is_vertical: bool = False  # Derived from justification
```

5. **Parsing Process**
- Split line into components
- Validate window type and convert to enum
- Parse coordinates as floats
- Convert justification string to enum
- Handle optional size multiplier
- Detect vertical text variants
- Store structured data for symbol rendering

6. **Integration with Symbol Rendering**
- Calculate absolute position from symbol origin
- Apply symbol rotation and mirroring
- Handle vertical text orientation
- Apply text justification rules
- Set font size based on multiplier
- Render text with proper attributes

7. **Error Handling**
- Validate line format and required fields
- Handle missing optional parameters
- Provide default values where appropriate
- Log warnings for unknown window types
- Skip malformed lines gracefully

8. **Example Usage**
```python
# Example WINDOW lines from symbol files
WINDOW 0 36 8 Left 2    # Instance name for capacitor
WINDOW 3 36 56 Left 2   # Value for capacitor
WINDOW 0 8 -48 Left 2   # Instance name for NMOS
```

9. **Considerations**
- Text rotation must account for both symbol rotation and text orientation
- Vertical variants (VTop, VBottom) need special handling
- Text position should be adjusted based on justification
- Symbol mirroring affects text position and orientation
- Font size multiplier affects text positioning calculations

### SVG Generation

#### SVG Generator (`svg_generator.py`)
- Uses `svgwrite` library for SVG creation
- Implements the following features:
  - Wire drawing with configurable stroke width
  - Symbol rendering with proper transformations
  - T-junction detection and dot placement
  - Text rendering with proper alignment
  - Built-in symbol definitions (GND, etc.)

##### Recent Developments
- Text positioning improvements:
  - Added configurable text centering compensation (default: 0.35 = 35% of font size)
  - Added configurable net label distance from origin (default: 12 units)
  - Fixed text orientation for net labels at 180° to prevent upside-down text
  - Improved IO pin text positioning with proper rotation and alignment
  - Added debug logging for text positioning and transformations

##### Current Issues and TODOs
1. Symbol Text Rendering
   - Need to improve handling of symbol names and values
   - Better support needed for different text positions based on symbol type
   - Consider symbol-specific text placement rules

2. WINDOW Line Parsing
   - Current parser needs enhancement to properly handle WINDOW lines in symbol files
   - WINDOW attributes affect text positioning and visibility
   - Need to implement proper parsing of:
     - WINDOW 0: Instance name position
     - WINDOW 3: Value position
     - Other WINDOW types for symbol-specific text

3. Text Alignment
   - Current implementation uses SVG's text-anchor for horizontal alignment
   - Vertical alignment is handled through manual position adjustments
   - Consider implementing more robust text alignment system

##### Coordinate System
- LTspice uses a coordinate system where:
  - Origin is at the center of the schematic
  - Y-axis points upward
  - Units are in LTspice grid points
- SVG coordinates are scaled by the `scale` parameter
- Viewbox is automatically calculated to fit all elements

##### Symbol Transformations
- Rotation types:
  - R0: No rotation
  - R90: 90 degrees clockwise
  - R180: 180 degrees
  - R270: 270 degrees clockwise
- Mirroring:
  - M0: Mirror across Y-axis, no rotation
  - M90: Mirror across Y-axis, then rotate 90 degrees
  - M180: Mirror across Y-axis, then rotate 180 degrees
  - M270: Mirror across Y-axis, then rotate 270 degrees

##### Text Handling
- Font sizes are determined by a multiplier index (0-7):
  - 0: 0.625x base size
  - 1: 1.0x base size
  - 2: 1.5x base size (default)
  - 3: 2.0x base size
  - 4: 2.5x base size
  - 5: 3.5x base size
  - 6: 5.0x base size
  - 7: 7.0x base size
- Text rendering is handled by a clean interface:
  - Single dictionary input for text properties
  - Caller handles transformations (rotation, mirroring)
  - Renderer focuses on text placement and styling
- Text alignment options:
  - Left: Left-aligned, vertically centered
  - Center: Horizontally and vertically centered
  - Right: Right-aligned, vertically centered
  - Top: Top-aligned, horizontally centered
  - Bottom: Bottom-aligned, horizontally centered
- Instance names and symbol texts:
  - Position is determined by WINDOW or property_id attributes
  - Falls back to default position above symbol if no position specified

##### T-Junction Detection
- Identifies points where 3 or more wires meet
- Excludes symbol terminal points
- Verifies wire directions to avoid false positives
- Adds dots with size relative to stroke width

## Contributing

### Setting Up Development Environment

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ltspice_to_svg.git
cd ltspice_to_svg
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -r requirements.txt
pip install pytest pytest-cov black mypy
```

### Development Workflow

1. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes following these guidelines:
   - Use type hints for all function parameters and return values
   - Add docstrings for all functions and classes
   - Follow PEP 8 style guidelines
   - Keep functions focused and modular
   - Add appropriate error handling

3. Run tests:
```bash
python -m pytest tests/
```

4. Format your code:
```bash
black src/ tests/
```

5. Run type checking:
```bash
mypy src/
```

6. Submit a pull request with:
   - Clear description of changes
   - Any new dependencies added
   - Test coverage for new features
   - Documentation updates if needed

### Testing Guidelines

- Write unit tests for all new functionality
- Use pytest fixtures for common test setup
- Test edge cases and error conditions
- Maintain test coverage above 80%
- Test with various LTspice files:
  - Different symbol types
  - Various rotations and mirrors
  - Complex wire connections
  - Different text alignments and sizes

### Documentation

- Update README.md for user-facing changes
- Update this development guide for implementation changes
- Document any new command-line options
- Add comments for complex algorithms
- Include examples for new features

## Future Improvements

1. Symbol Support
   - Add more built-in symbols
   - Support for custom symbol libraries
   - Better handling of complex symbols

2. Text Rendering
   - Support for more font styles
   - Better text placement algorithms
   - Multi-line text support

3. Performance
   - Optimize T-junction detection
   - Cache commonly used symbols
   - Parallel processing for large schematics

4. Export Options
   - PNG export with configurable DPI
   - Dark mode support
   - Custom color schemes

5. Integration
   - Web interface
   - Batch processing
   - Integration with other EDA tools 