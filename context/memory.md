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
- Configured project for PyPI and GitHub pip installation
  - Updated package metadata and created necessary files
  - Enabled direct installation via pip from GitHub
  - Added installation documentation in README
- **Enhanced SVG Output with Symbol Metadata (Current Session)**
  - Added pretty formatting to SVG output using svgwrite's `pretty=True` parameter
  - Implemented custom namespace support: `xmlns:s="https://github.com/nturley/netlistsvg"`
  - Added `s:type` attribute to symbol groups with actual symbol names
  - Added `s:width` and `s:height` attributes with calculated symbol dimensions
  - Fixed viewbox calculation to properly include symbols (was missing symbols before)
  - Disabled svgwrite validation for custom attributes to avoid conflicts
  - Enhanced symbol dimension calculation from actual shape bounds

### In Progress Features
- Documentation Improvement
  - Currently auditing and enhancing all documentation files
  - Planning to add better architecture diagrams and code examples
  - Will improve inline code documentation with better docstrings
  - Creating more comprehensive user guides with examples

### Documentation Status
The project has a dedicated `/doc` directory with several markdown files:
- architecture.md: High-level system design
- api.md: API documentation
- user_guide.md: Usage instructions
- development.md: Development guidelines
- renderers.md: Renderer component documentation
- testing.md: Testing procedures
- window_text_rendering_logic.md: Special case documentation

The documentation needs improvement in several areas:
- More diagrams to visualize component relationships
- Better examples of common use cases
- More detailed explanation of configuration options
- Clearer contributor guidelines
- Better inline code documentation

### Known Issues
- None at this time

### SVG Output Features
The project now generates SVG files with advanced metadata and proper formatting:

#### Pretty Formatted Output
- SVG files are now formatted with proper indentation for readability
- Implemented using svgwrite's `save(pretty=True)` parameter
- Makes SVG files easy to inspect and debug

#### Custom Symbol Metadata
- Custom namespace: `xmlns:s="https://github.com/nturley/netlistsvg"`
- Symbol groups include semantic attributes:
  - `s:type="symbol_name"` - Identifies the type of component (e.g., "nmos", "pmos", "cap", "res")
  - `s:width="64"` - Calculated width of the symbol in pixels
  - `s:height="128"` - Calculated height of the symbol in pixels
- Symbol dimensions are calculated from actual shape bounds (lines, rectangles, circles, arcs)
- Enables advanced SVG processing by external tools

#### Example SVG Output Structure
```xml
<svg xmlns="http://www.w3.org/2000/svg" 
     xmlns:s="https://github.com/nturley/netlistsvg">
  <g s:type="nmos" s:width="64" s:height="128" transform="translate(704,336)">
    <!-- symbol shapes and text -->
  </g>
</svg>
```

## Testing
- Comprehensive test suite with pytest
- Test files organized under `/tests/`
- Test results stored in `/tests/{test_name}/results`
- Current test coverage is good
- All tests now passing (76 tests)