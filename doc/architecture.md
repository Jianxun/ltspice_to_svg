# Architecture Overview

## System Design

The LTspice to SVG converter is a Python-based tool that converts LTspice schematic files (.asc) to SVG format. The system follows a modular architecture with clear separation of concerns between parsing and rendering components.

### Core Components

1. **Main Module** (`ltspice_to_svg.py`)
   - Entry point for the application
   - Handles command-line arguments and configuration
   - Coordinates the parsing and rendering process

2. **Parsers** (`src/parsers/`)
   - `schematic_parser.py`: Main parser that coordinates the parsing process
   - `asc_parser.py`: Parses LTspice schematic files (.asc)
   - `asy_parser.py`: Parses LTspice symbol files (.asy)
   - `shape_parser.py`: Handles parsing of geometric shapes

3. **Renderers** (`src/renderers/`)
   - `svg_renderer.py`: Main renderer that coordinates the SVG generation
   - `symbol_renderer.py`: Renders schematic symbols
   - `text_renderer.py`: Handles text rendering
   - `wire_renderer.py`: Renders wires and connections
   - `shape_renderer.py`: Renders geometric shapes
   - `flag_renderer.py`: Renders schematic flags and annotations
   - `base_renderer.py`: Base class for all renderers

### Data Flow

1. **Input Processing**
   - LTspice schematic file (.asc) is read
   - Symbol files (.asy) are loaded as needed
   - Text encoding is handled appropriately (UTF-16LE)

2. **Parsing**
   - Schematic elements are parsed into an intermediate representation
   - Symbols are parsed and stored in a symbol library
   - Geometric shapes and text are extracted

3. **Rendering**
   - SVG document is created
   - Elements are rendered in appropriate order:
     1. Wires and connections
     2. Symbols
     3. Text
     4. Shapes
     5. Flags and annotations

### Configuration Options

The system supports various configuration options:
- Stroke width for lines
- Dot size multiplier for junctions
- Scale factor for coordinates
- Font size for text
- JSON export for debugging
- Text rendering toggle

### Error Handling

- File encoding issues are handled gracefully
- Missing symbol files are reported
- Invalid schematic elements are logged
- SVG rendering errors are caught and reported

## Core Components

### 1. SVG Generator (`svg_generator.py`)
- Main coordinator for SVG generation
- Manages configuration (scale, stroke width, font size, etc.)
- Coordinates rendering process
- Handles debug data export
- Key methods:
  - `generate()`: Main entry point for SVG generation
  - `_calculate_viewbox()`: Calculates SVG viewBox dimensions
  - `_find_t_junctions()`: Identifies wire connection points

### 2. Shape Renderer (`shape_renderer.py`)
- Handles all shape-related rendering
- Supports:
  - Wires
  - Lines
  - Circles
  - Rectangles
  - Arcs
  - T-junctions
- Pure functions with explicit parameters

### 3. Text Renderer (`text_renderer.py`)
- Manages text element rendering
- Handles:
  - Text justification
  - Multiline text
  - Font size scaling
  - Text positioning

### 4. Flag Renderer (`flag_renderer.py`)
- Handles flag rendering
- Manages:
  - Flag positioning
  - Flag orientation
  - Flag text placement

### 5. IO Pin Renderer (`io_pin_renderer.py`)
- Handles IO pin rendering
- Manages:
  - Pin positioning
  - Pin orientation
  - Pin text placement
  - Pin connections

### 6. Symbol Renderer (`symbol_renderer.py`)
- Manages symbol rendering
- Handles:
  - Symbol shapes
  - Pin connections
  - Symbol text
  - Rotation and mirroring

### 7. Net Label Renderer (`net_label_renderer.py`)
- Handles net label rendering
- Manages:
  - Label positioning
  - Text orientation
  - Connection points

## Parser Components

### 1. ASC Parser (`asc_parser.py`)
- Parses schematic (.asc) files
- Extracts:
  - Wires and connections
  - Symbol instances
  - Text elements
  - Flags and IO pins
  - Net labels

### 2. ASY Parser (`asy_parser.py`)
- Parses symbol (.asy) files
- Extracts:
  - Symbol shapes
  - Pin definitions
  - Text attributes
  - WINDOW settings

### 3. Shape Parser (`shape_parser.py`)
- Parses shape elements from both ASC and ASY files
- Handles:
  - Line styles
  - Geometric shapes
  - Transformations
  - Common shape attributes

## Data Flow

### 1. Input Processing
- LTspice schematic (.asc) and symbol (.asy) files are parsed
- Parsed data is converted to internal data structures
- Shape elements are processed by shape_parser.py

### 2. SVG Generation
- SVGGenerator coordinates the rendering process
- Each renderer handles its specific component
- Configuration is centralized in SVGGenerator
- Debug data is exported if requested

### 3. Output Generation
- SVG file is created with proper viewBox
- All elements are rendered in correct order
- Debug JSON is exported if enabled

## Configuration

Key configuration parameters in SVGGenerator:
- `stroke_width`: Line thickness
- `dot_size_multiplier`: Size of junction dots (default: 0.75)
- `scale`: Coordinate scaling factor (default: 0.1)
- `font_size`: Base font size (default: 22.0)
- `text_centering_compensation`: Text alignment adjustment (default: 0.35)
- `net_label_distance`: Distance of net labels from origin (default: 8)
- `no_text`: Skip rendering all text elements
- `no_symbol_text`: Skip rendering symbol text elements only
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

## Coordinate System

- LTspice uses a coordinate system where:
  - Origin is at the center of the schematic
  - Y-axis points upward
  - Units are in LTspice grid points
- SVG coordinates are scaled by the `scale` parameter
- Viewbox is automatically calculated to fit all elements

## Symbol Transformations

### Rotation Types
- R0: No rotation
- R90: 90 degrees clockwise
- R180: 180 degrees
- R270: 270 degrees clockwise

### Mirroring
- M0: Mirror across Y-axis, no rotation
- M90: Mirror across Y-axis, then rotate 90 degrees
- M180: Mirror across Y-axis, then rotate 180 degrees
- M270: Mirror across Y-axis, then rotate 270 degrees

## Text Handling

### Font Sizes
Font sizes are determined by a multiplier index (0-7):
- 0: 0.625x base size
- 1: 1.0x base size
- 2: 1.5x base size (default)
- 3: 2.0x base size
- 4: 2.5x base size
- 5: 3.5x base size
- 6: 5.0x base size
- 7: 7.0x base size

### Text Alignment Options
- Left: Left-aligned, vertically centered
- Center: Horizontally and vertically centered
- Right: Right-aligned, vertically centered
- Top: Top-aligned, horizontally centered
- Bottom: Bottom-aligned, horizontally centered
- VTop: Vertically oriented, top-aligned
- VBottom: Vertically oriented, bottom-aligned

## WINDOW Line Handling

### In Symbol Files (.asy)
- Define default text rendering rules for component attributes
- WINDOW 0: Default position/style for component name (e.g., "R1", "M1")
- WINDOW 3: Default position/style for component value (e.g., "1k", "10u")
- Part of symbol's template/definition

### In Schematic Files (.asc)
- Follow SYMBOL lines to override default text rendering
- Customize text position/style for specific component instances
- If no override provided, use defaults from symbol definition

### Format
```
WINDOW <type> <x> <y> <justification> [size_multiplier]
```
- `type`: 0 (name) or 3 (value)
- `x, y`: Relative coordinates from symbol origin
- `justification`: Text alignment (Left, Right, Center, Top, Bottom, VTop, VBottom)
- `size_multiplier`: Optional font size index (0-7)

## T-Junction Detection

- Identifies points where 3 or more wires meet
- Excludes symbol terminal points
- Verifies wire directions to avoid false positives
- Adds dots with size relative to stroke width 