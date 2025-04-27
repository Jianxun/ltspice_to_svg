# Project Memory

## Project Purpose
The project aims to convert LTspice schematics (.asc files) and symbols (.asy files) into SVG format for easier sharing and inclusion in documentation.

## Architecture

The project is structured as follows:

### Core Components
- **Parsers:** Parse LTspice ASC/ASY files into Python objects (`asc_parser.py` and `asy_parser.py`)
- **Renderers:** Convert parsed objects into SVG (`svg_renderer.py`)
- **Main Entry Point:** `ltspice_to_svg.py` - Handles CLI arguments and orchestrates the conversion

### Detailed Component Breakdown

1. **File Parsing**
   - ASC Parser: Parses LTspice schematics
   - ASY Parser: Parses LTspice symbols
   - Support for UTF-16LE encoding (typical for LTspice files)

2. **Symbol Management**
   - Symbol Library: Loads and manages LTspice symbols
   - Symbol Resolver: Finds symbol files for components in schematics

3. **SVG Generation**
   - SVG Renderer: Creates SVG elements for different LTspice components
   - ViewboxCalculator: Computes optimal SVG viewbox based on schematic content
   - Includes support for:
     - Wires and connections
     - Components and symbols
     - Text elements (labels, values, etc.)
     - Junction points

4. **Configuration**
   - RenderingConfig: Controls SVG output appearance
   - Command-line options for customization

## Current Status

The project is functional and can convert both LTspice schematics (.asc) and symbols (.asy) to SVG format.

### Recently Completed Features
- Fixed text mirroring issues in symbols
- Implemented proper text alignment for symbol pins
- Added support for component name and value text rendering
- Added proper SVG header and namespace declarations
- Implemented CSS styling for consistent appearance
- Added metadata to SVG file
- Created utilities to detect and fix file encoding
- Enhanced CLI with rendering options:
  - Stroke width for wires
  - Dot size for junctions
  - Base font size control
  - Text rendering control switches
- Added viewbox margin option to control padding around the schematic
  - Implemented in RenderingConfig with validation
  - Updated ViewboxCalculator to utilize the margin
  - Added margin parameter to command-line interface
  - Fixed edge cases with invalid bounds and zero margin
- Added font family option for text elements
  - Added font_family option to RenderingConfig
  - Updated TextRenderer to use the configured font
  - Added font-family parameter to command-line interface
  - Added tests to verify font rendering
  - Updated README with documentation and examples

### In Progress Features
- None at this time

### Known Issues
- None at this time

## Testing
- Comprehensive test suite with pytest
- Test files organized under `/tests/`
- Test results stored in `/tests/{test_name}/results`
- Current test coverage is good
- All tests now passing (76 tests)