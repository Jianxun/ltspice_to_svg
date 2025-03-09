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

### SVG Generation

#### SVG Generator (`svg_generator.py`)
- Uses `svgwrite` library for SVG creation
- Implements the following features:
  - Wire drawing with configurable stroke width
  - Symbol rendering with proper transformations
  - T-junction detection and dot placement
  - Text rendering with proper alignment
  - Built-in symbol definitions (GND, etc.)

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