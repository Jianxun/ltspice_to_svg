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

### Tool Execution Improvements
- Fixed import issues in the main script (removing relative imports)
- Created a shell script wrapper for easier execution
- Added setup.py for installation as a package
- Updated README with comprehensive usage instructions
- Provided three different methods to run the tool:
  1. Using the shell script (./ltspice_to_svg.sh)
  2. Setting PYTHONPATH manually
  3. Installing as a package with pip

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

### Symbol Window Texts
- Window texts are special text elements in symbols used for displaying property values like component names and values
- Key components in window text rendering:
  - `SymbolRenderer` manages window definitions and overrides
  - `_render_window_property` method handles window property rendering
  - Properties are identified by ID, with '0' for component name and '3' for component value
  - Window overrides can modify position, justification, and size of text
- The renderer supports two key property IDs by default:
  - Property 0: Component name (e.g., "V1", "R1")
  - Property 3: Component value (e.g., "12mV", "1k")
- Key issues discovered in testing:
  - String vs. integer key handling in window overrides dictionary
  - The renderer now checks for both string and integer format keys when looking up window overrides
  - Integration test `test_symbol_window_texts` verifies correct handling of window overrides

### Test Cases for Window Texts
The integration test suite includes specific tests for window text rendering:
- `test_symbol_window_texts`: Validates full rendering with window overrides
- `test_symbol_window_texts_property_0`: Tests rendering only component names
- `test_symbol_window_texts_property_3`: Tests rendering only component values
These tests verify that:
- Window overrides are correctly applied
- Selective property rendering works as expected
- Text positioning and justification are correctly handled

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
- Fixed failing test in `test_text_rendering_switches.py` by properly connecting direct property access to the configuration system
- Improved configuration interface by removing property getters/setters and using `config.set_option()` directly
- Updated tests to use the configuration interface directly
- Fixed and renamed window text tests to better reflect their functionality

### Recent Fixes
- Added property getters and setters to SVGRenderer to handle direct property access for text rendering options
- Fixed failing test in `test_text_rendering_switches.py` by properly connecting direct property access to the configuration system
- Improved configuration interface by removing property getters/setters and using `config.set_option()` directly
- Updated tests to use the configuration interface directly
- Fixed window text rendering tests by:
  - Renaming tests from property-based naming to function-based naming
  - Replacing direct property access with configuration API calls
  - Updating test assertions to match the expected output
  - Removing the dependency on property_id for rendering specific text types
  - Using `set_text_options` to control which text elements are rendered

### Current Task
- Implementing text rendering options:
  - Need to document API changes for users
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
- Selective rendering of net label flags with the --no-net-label option

The text rendering architecture consists of:
1. `SVGRenderer` - High-level control of which texts to render
2. `TextRenderer` - Detailed positioning and styling of text elements
3. `SymbolRenderer` - Specialized handling for text in symbols

## Architecture

- `src/parsers/` - Contains parsers for LTspice files
- `src/renderers/` - Contains SVG rendering classes
- `tests/` - Test cases organized by functionality

The renderer architecture follows a modular design with specialized renderers for different schematic elements, and a configuration system for controlling rendering options.

### Recent Issues
- **Command Line Tests TypeError**: Fixed an issue in command line tests related to `MagicMock` objects being used where string/bytes/bytearray is expected during JSON loading
- **FlagRenderer Issue**: The `FlagRenderer` class loads flag definitions from a JSON file, but in the test environment, mocks caused issues with this JSON loading process
- The error was occurring because the `_load_flag_definitions` method was trying to load a JSON file, but the mock for `open()` was returning a `MagicMock` instead of file content

### Mock Handling for JSON Files
To fix the issue with MagicMock and JSON loading in the tests:
1. Identified that the error occurred in the `FlagRenderer._load_flag_definitions` method when trying to call `json.load()` on a MagicMock object
2. Updated the `mock_open_file` fixture to provide a more sophisticated mock that:
   - Contains a simplified version of the flag definitions JSON data
   - Returns the JSON string when `read()` is called on the file handle
   - Uses a side_effect function to only return the JSON data when the flags.json file is opened
3. Fixed the import paths in the test mocks:
   - Changed from mocking specific modules (e.g., 'src.renderers.svg_renderer.SVGRenderer') to mocking at the import level (e.g., 'src.ltspice_to_svg.SVGRenderer')
   - This ensured that our mocks were actually being used in the test

This approach allows the tests to run without accessing the file system while still providing valid JSON data for the functionality being tested.