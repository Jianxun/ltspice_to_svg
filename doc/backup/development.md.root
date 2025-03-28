# Development Guide

This document provides an overview of the LTspice to SVG converter project's architecture and development guidelines.

## Project Structure

```
src/
├── generators/           # SVG generation components
│   ├── svg_generator.py  # Main SVG generation coordinator
│   ├── shape_renderer.py # Shape rendering (wires, lines, circles, etc.)
│   ├── text_renderer.py  # Text element rendering
│   ├── flag_renderer.py  # Flag and IO pin rendering
│   ├── symbol_renderer.py # Symbol rendering
│   └── net_label_renderer.py # Net label rendering
├── parsers/             # LTspice file parsing components
│   ├── asc_parser.py    # Schematic (.asc) file parser
│   └── asy_parser.py    # Symbol (.asy) file parser
└── ltspice_to_svg.py    # Main entry point
```

## Architecture Overview

### Core Components

1. **SVG Generator** (`svg_generator.py`)
   - Main coordinator for SVG generation
   - Manages configuration (scale, stroke width, font size, etc.)
   - Coordinates rendering process
   - Handles debug data export
   - Key methods:
     - `generate()`: Main entry point for SVG generation
     - `_calculate_viewbox()`: Calculates SVG viewBox dimensions
     - `_find_t_junctions()`: Identifies wire connection points

2. **Shape Renderer** (`shape_renderer.py`)
   - Handles all shape-related rendering
   - Supports:
     - Wires
     - Lines
     - Circles
     - Rectangles
     - Arcs
     - T-junctions
   - Pure functions with explicit parameters

3. **Text Renderer** (`text_renderer.py`)
   - Manages text element rendering
   - Handles:
     - Text justification
     - Multiline text
     - Font size scaling
     - Text positioning

4. **Flag Renderer** (`flag_renderer.py`)
   - Handles flag and IO pin rendering
   - Manages:
     - Flag positioning
     - IO pin connections
     - Net label placement
     - Text orientation

5. **Symbol Renderer** (`symbol_renderer.py`)
   - Manages symbol rendering
   - Handles:
     - Symbol shapes
     - Pin connections
     - Symbol text
     - Rotation and mirroring

6. **Net Label Renderer** (`net_label_renderer.py`)
   - Handles net label rendering
   - Manages:
     - Label positioning
     - Text orientation
     - Connection points

### Data Flow

1. **Input Processing**
   - LTspice schematic (.asc) and symbol (.asy) files are parsed
   - Parsed data is converted to internal data structures

2. **SVG Generation**
   - SVGGenerator coordinates the rendering process
   - Each renderer handles its specific component
   - Configuration is centralized in SVGGenerator
   - Debug data is exported if requested

3. **Output Generation**
   - SVG file is created with proper viewBox
   - All elements are rendered in correct order
   - Debug JSON is exported if enabled

## Configuration

Key configuration parameters in SVGGenerator:
- `stroke_width`: Line thickness
- `dot_size_multiplier`: Size of junction dots
- `scale`: Coordinate scaling factor
- `font_size`: Base font size
- `text_centering_compensation`: Text alignment adjustment
- `net_label_distance`: Distance of net labels from origin
- `size_multipliers`: Font size scaling factors

## Debug Features

Debug features can be enabled through SVGGenerator:
- `export_json`: Exports debug data to JSON file
- Debug data includes:
  - Wires
  - Symbols
  - Texts
  - Flags
  - IO pins
  - Shapes
  - Symbol data
  - T-junctions

## Development Guidelines

1. **Modularity**
   - Each renderer has a single responsibility
   - Pure functions with explicit parameters
   - Minimal dependencies between components

2. **Configuration**
   - Centralize configuration in SVGGenerator
   - Pass configuration explicitly to renderers
   - Avoid hardcoded values

3. **Debug Support**
   - Include debug logging where appropriate
   - Export debug data for troubleshooting
   - Maintain clear error messages

4. **Code Style**
   - Follow PEP 8 guidelines
   - Use type hints
   - Document public interfaces
   - Keep functions focused and small

## Future Improvements

1. **Performance**
   - Optimize rendering for large schematics
   - Implement caching where beneficial
   - Profile and optimize critical paths

2. **Features**
   - Add support for more LTspice elements
   - Improve text rendering quality
   - Enhance symbol handling

3. **Testing**
   - Add unit tests for each component
   - Implement integration tests
   - Add visual regression tests

4. **Documentation**
   - Add API documentation
   - Create usage examples
   - Document common issues and solutions

## Shape Rendering

### Line Styles

All shapes in the SVG output use round line caps (`stroke-linecap="round"`) for consistent appearance:
- Solid lines use round caps for better visual quality
- Dotted lines (style code 2) use round caps to create proper dots
- Dashed lines (style code 1) use round caps for consistent ends

For dotted/dashed styles:
- Dots are created using a very small dash length (0.1) followed by a gap (2)
- Dashes use a length of 4 times the stroke width
- Gaps between elements are 2 times the stroke width

Example style codes:
```
0: solid
1: dash (4,2)
2: dot (0.1,2)
3: dash dot (4,2,0.1,2)
4: dash dot dot (4,2,0.1,2,0.1,2)
```

Implementation details:
- Rectangles with styles use SVG path elements to ensure proper line caps
- Circles and ellipses with styles use the stroke-linecap attribute
- Arcs with styles use SVG path elements with proper line caps

### Scale Factor

The default scale factor (0.1) may make shapes too small to be visible. Use a larger scale factor (e.g. 1.0) if shapes appear too small:

```bash
python ./src/ltspice_to_svg.py input.asc --scale 1.0
``` 