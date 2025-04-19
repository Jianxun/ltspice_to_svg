# Project Memory

## Project Overview
This project is a Python-based tool for converting LTspice schematics to SVG format. The tool consists of several key components:

1. **Parsers** for LTspice files (.asc and .asy)
2. **Renderers** for converting parsed data to SVG
3. **Command-line interface** for user interaction
4. **Test suite** for verifying functionality

## Current Architecture

### Renderer Structure
- `BaseRenderer`: Provides common properties (stroke width, font size)
- Specialized renderers:
  - `SVGRenderer`: Main renderer coordinating all others
  - `WireRenderer`: Handles wires and T-junctions
  - `ShapeRenderer`: Renders lines, rectangles, circles, and arcs
  - `SymbolRenderer`: Renders schematic symbols and their subcomponents
  - `TextRenderer`: Handles text elements with various justifications
  - `FlagRenderer`: Renders ground flags, net labels, and IO pins
  - `ViewboxCalculator`: Calculates SVG viewbox dimensions

### Key Capabilities
- Convert LTspice `.asc` schematics to SVG format
- Support for all basic schematic elements:
  - Wires with T-junction detection
  - Shapes (lines, rectangles, circles, arcs)
  - Text elements (comments, SPICE directives)
  - Symbols with rotation and mirroring
  - Flags (ground symbols, net labels, IO pins)
- Configurable rendering options:
  - Stroke width for shapes and wires
  - Base font size for text elements
  - Selective text rendering control

## Recent Improvements

### Refactoring
- Refactored `SVGRenderer` to use specialized renderer components
- Unified flag data structure in ASCParser (combining flags and IO pins)
- Extracted viewbox calculation to dedicated `ViewboxCalculator` class
- Simplified shape rendering with a type-based approach
- Improved text rendering with focused type checking

### API Enhancements
- Added consistent input validation and default handling
- Improved error messages with type information
- Enhanced logging with type-specific counts and details
- Implemented immutable data handling patterns

### Documentation and Testing
- Added comprehensive documentation to all key methods
- Improved organization of test structure
- Added specific tests for different element types
- Updated test fixtures for better reuse

## Technical Details
- **Python version**: 3.12.9
- **Testing framework**: pytest
- **SVG generation**: svgwrite library
- **Encoding**: UTF-16LE support for LTspice files
- **File structure**:
  - Command-line entry point: `src/ltspice_to_svg.py`
  - Parsers in `src/parsers/`
  - Renderers in `src/renderers/`
  - Tests organized in `tests/unit_tests/` and `tests/integration/`

## Code Insights

### Text Rendering
- Standalone schematic texts come in two types: 'comment' and 'spice'
- Justification affects text anchoring ('start', 'middle', 'end')
- Vertical text requires special rotation handling
- Text rendering options are currently controlled by boolean flags:
  - `no_schematic_comment`: Skip rendering schematic comments
  - `no_spice_directive`: Skip rendering SPICE directives
  - `no_nested_symbol_text`: Skip rendering text in symbols
  - `no_component_name`: Skip rendering component names
  - `no_component_value`: Skip rendering component values

### Text Rendering Options
- Currently, options are set individually via direct property access
- The command-line interface (`ltspice_to_svg.py`) sets these options directly
- A `set_text_rendering_option()` method exists to set individual options
- A `set_text_rendering_options()` method is expected by tests but not implemented

### Flag Rendering
- All flags (ground, net labels, IO pins) use a unified data structure
- Flag types are distinguished by the 'type' field
- Orientation is calculated based on connected wire directions

### Shape Rendering
- Shapes use a uniform rendering interface with type-based dispatching
- Arc rendering requires careful calculation of SVG path parameters
- Dash patterns are scaled by stroke width for consistent appearance

## Command Line Interface
- Main entry point is `ltspice_to_svg.py`
- Supports various options:
  - `--stroke-width`: Width of lines in SVG
  - `--dot-size`: Size of junction dots
  - `--base-font-size`: Base font size in pixels
  - Text rendering options:
    - `--no-text`: Skip all text elements
    - `--no-schematic-comment`: Skip schematic comments
    - `--no-spice-directive`: Skip SPICE directives
    - `--no-nested-symbol-text`: Skip nested symbol text
    - `--no-component-name`: Skip component names
    - `--no-component-value`: Skip component values
  - `--export-json`: Export intermediate JSON files
  - `--ltspice-lib`: Path to LTspice symbol library

## Current Development Status

### Completed Tasks
- Refactored SVG Renderer
- Updated Flag Rendering
- Improved Text Rendering
- Fixed text rendering options in SVGRenderer

### Recent Fixes
- Added property getters and setters to SVGRenderer to handle direct property access for text rendering options
- Fixed failing test in `test_text_rendering_switches.py` by properly connecting direct property access to the configuration system
- Ensured consistent handling of text rendering options across the renderer

### Current Task
- Implementing text rendering options:
  - Need to connect command line options to rendering logic
  - Update BaseRenderer to accept config parameter
  - Add unit tests for configuration class

### Future Tasks
- Clean up old code
- Improve documentation
- Performance optimization
- Add new features like netlist export and interactive SVG

# Project State

We're building a Python library that converts LTspice schematics and symbols to SVG format for documentation and web display.

## Current Features

- Parse LTspice schematic (.asc) files and extract components, wires, symbols, and texts
- Parse LTspice symbol (.asy) files
- Render schematics as SVG with proper sizing and styling
- Support for symbols with nested components and text
- Handle text rendering with proper font sizing and alignment
- Support schematic elements like: wires, components, ground flags, IO pins, net labels
- Fix encoding of LTspice files (UTF-16LE without BOM)

## Text Rendering Capabilities

The SVG renderer provides flexible text rendering with the following features:

- Separate rendering control for SPICE directives and schematic comments
- Text sizing through configurable base font size and size multipliers (8 levels)
- Support for different text justification modes (Left, Right, Center, Top, Bottom)
- Vertical text support with rotation
- Special handling for mirrored text in symbols with automatic counter-mirroring
- Multiline text support with proper line spacing
- Text in window definitions for symbols

The text rendering architecture consists of:
1. `SVGRenderer` - High-level control of which texts to render
2. `TextRenderer` - Detailed positioning and styling of text elements
3. `SymbolRenderer` - Specialized handling for text in symbols

## Architecture

- `src/parsers/` - Contains parsers for LTspice files
- `src/renderers/` - Contains SVG rendering classes
- `tests/` - Test cases organized by functionality

The renderer architecture follows a modular design with specialized renderers for different schematic elements, and a configuration system for controlling rendering options.