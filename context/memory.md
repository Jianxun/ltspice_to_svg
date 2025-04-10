# Project: LTspice to SVG Converter

## Project Overview
- Project name: LTspice to SVG Converter
- Current focus: Refactoring the SVG Generator component to improve modularity and maintainability. Successfully completed Phase 4 with the isolation of flag rendering logic into a dedicated FlagRenderer class, including comprehensive test coverage.
- Recent actions: Created FlagRenderer class to handle all flag-related rendering (net labels, ground flags, IO pins), moved flag rendering methods from SVGGenerator to FlagRenderer, added comprehensive test suite for FlagRenderer with all tests passing, updated SVGGenerator to use the new FlagRenderer class, fixed test assertions to handle floating-point precision in SVG coordinates.

## Key Components
1. SVGGenerator (src/generators/svg_generator.py)
   - Main class for generating SVG output
   - Now uses FlagRenderer for flag-related rendering
   - Now uses TextRenderer for text-related rendering
   - Cleaner and more focused after flag and text rendering extraction

2. FlagRenderer (src/renderers/flag_renderer.py)
   - Handles all flag-related rendering
   - Supports net labels, ground flags, and IO pins
   - Manages text positioning and rotation
   - Fully tested with comprehensive test suite

3. TextRenderer (src/renderers/text_renderer.py)
   - Handles all text-related rendering
   - Supports multiline text
   - Handles text rotation and positioning
   - Manages font sizes and text alignment
   - Fully tested with comprehensive test suite

4. ShapeRenderer (src/renderers/shape_renderer.py)
   - Handles basic shape rendering
   - Supports lines, rectangles, circles, etc.

## Recent Changes
- Created TextRenderer class to handle all text-related rendering
- Moved all text-related methods from SVGGenerator to TextRenderer
- Updated SVGGenerator to use the new TextRenderer
- Added comprehensive test suite for TextRenderer
- Maintained all existing functionality while improving code organization
- Successfully implemented and tested text rendering functionality with rotation and positioning
- Configured LTSPICE_LIB_PATH environment variable for symbol finding
- Completed symbol finding tests with proper environment setup
- Organized test files into dedicated directories with results for manual inspection
- Deprecated scale parameter from method signatures
- Successfully generated SVG output for miller_ota schematic
- Refactored symbol geometry rendering to use ShapeRenderer for better modularity
- Removed scaling from coordinate calculations, using fixed scale=1.0 for future compatibility
- Modified viewBox calculation to start from minimum coordinates
- Removed scale multiplication from viewBox coordinates
- Added padding to ensure elements near the edges are fully visible

## Next Steps
- Implement support for custom symbol libraries
- Add symbol caching mechanism for improved performance
- Enhance error handling for missing symbols
- Document symbol path configuration process
- Plan migration path for removing scale parameter completely

## Project Structure
- src/
  - generators/
    - svg_generator.py
  - renderers/
    - shape_renderer.py
    - flag_renderer.py
    - text_renderer.py
- tests/
  - test_text_renderer/
    - test_text_renderer.py
    - results/
  - test_flag_renderer/
    - results/
  - test_shape_renderer/
    - results/
  - test_symbol_finding/
  - test_symbol_texts/
  - test_flags/
  - test_schematic_shapes/
  - test_schematic_texts/
- schematics/
- doc/

## Environment
- Python virtual environment (venv)
- Key dependencies managed via requirements.txt
- Development tools: pytest for testing
- LTSPICE_LIB_PATH environment variable set to "/Users/$USER/Library/Application Support/LTspice/lib/sym"
- Required dependencies installed via pip
- Git repository initialized with .gitignore and README.md

## Project State
- Project: LTspice to SVG Converter
- Current Focus: Refactoring SVG Generator
- Last Action: Attempted to remove symbol terminal finding methods
- Status: Changes rejected, preparing for new chat

## Current Architecture
- Main Components:
  - `SVGGenerator` class (main generator)
  - `ShapeRenderer` class (handles basic shapes)
  - Transformation system (currently mixed with rendering logic)

## Recent Changes
- Created `ShapeRenderer` class for basic shape rendering
- Added comprehensive tests for shape rendering
- Attempted to remove symbol terminal finding methods (rejected)
- Pending: Need to properly handle symbol terminal removal

## Notes
- Symbol terminal finding methods are currently used in T-junction detection
- Need to carefully consider the impact of removing these methods
- May need to revise the T-junction detection logic
- The viewBox calculation now properly handles negative coordinates
- The scale is forced to 1.0 to maintain the original coordinates
- Padding is added to ensure elements near the edges are fully visible

## Project Overview
LTspice to SVG Converter - A tool to convert LTspice schematics (.asc files) to SVG format while preserving visual layout.

## Current State
- Basic repository structure is set up
- Main implementation file: src/ltspice_to_svg.py
- Project uses Python with required dependencies:
  - svgwrite>=1.4.3
  - pytest>=7.3.1

## Project Structure
- src/
  - ltspice_to_svg.py: Main conversion script
  - parsers/: Directory for parsing LTspice files
  - generators/: Directory for SVG generation
- tests/: Test cases directory
- tools/: Custom tools directory
- doc/: Documentation
- schematics/: Example or test schematics
- fig/: Figure outputs

## Environment Setup
- Python virtual environment required
- LTspice library path needs to be configured via environment variable LTSPICE_LIB_PATH

## Features
- Converts .asc files to SVG
- Preserves schematic elements (wires, symbols, labels, etc.)
- Supports local and LTspice library symbols
- Customizable output (line width, font size, scale)

## Lessons
- Test Organization and Output:
  - Each test module should have its own dedicated directory under tests/
  - Don't create test scripts directly under /tests
  - Use a consistent structure:
    ```
    tests/
    ├── test_module_name/
    │   ├── test_module_name.py
    │   ├── results/
    │   └── fixtures/ (if needed)
    ```
  - Keep test outputs organized in the results/ subdirectory
  - Use fixtures/ subdirectory for test data when needed

- SVG Test Outputs:
  - Save SVG outputs during testing for manual inspection
  - Each test should generate a visual output when possible
  - Use a white background for better visibility
  - Add visual markers (circles, lines) to show alignment points
  - Save files with descriptive names based on test cases
  - Organize test outputs in dedicated directories (e.g., tests/test_text_renderer/results/)

## Flag Renderer Tests
- Currently using scale=1.0 for testing
- SVG output files saved in tests/flag_renderer/results/
- Test results show potential rendering issues

## Completed
- Text rendering with rotation and positioning
- Symbol finding functionality
- Basic SVG generation
- Wire rendering
- Test organization and result verification
- Shape rendering with dedicated ShapeRenderer class
- Scale-independent coordinate system

## In Progress
- Custom symbol library support
- Symbol caching mechanism
- Error handling for missing symbols

## Planned
- Wire rendering optimization
- Symbol rendering improvements
- Integration testing
- Complete removal of scale parameter

## Lessons Learned
- Environment variables are crucial for symbol finding functionality
- Test organization with dedicated directories improves maintainability
- Manual inspection of SVG outputs helps verify rendering correctness
- Proper error handling for missing symbols is essential
- Using dedicated renderer classes improves code modularity and maintainability
- Coordinate scaling should be handled at the group level rather than globally 