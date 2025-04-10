# Project Memory

## Project Overview
The project aims to convert LTspice schematics to SVG format. We are currently in the process of refactoring the codebase to improve its structure and maintainability.

## Current State
- We have analyzed the existing SVGGenerator implementation
- Created a comprehensive refactor plan for SVGRenderer
- Designed a modular architecture with specialized renderers
- Simplified the logging system design

## Architecture Design
### New SVGRenderer Structure
- Base renderer class for common functionality
- Specialized renderers for different element types:
  - WireRenderer
  - SymbolRenderer
  - TextRenderer
  - ShapeRenderer
- Main SVGRenderer class for orchestration

### Logging System
- Simple, single-file logging
- Focus on important events and errors
- Minimal impact on code readability
- Basic configuration in `src/utils/logger.py`

## Implementation Plan
1. Create initial file structure
2. Implement base renderer class
3. Implement specialized renderers
4. Implement main SVGRenderer class
5. Setup testing structure
6. Implement logging system

## Key Decisions
1. Using SVGRenderer name to avoid conflicts with existing SVGGenerator
2. Modular design with separate renderer classes
3. Simplified logging system with single log file
4. Explicit rendering control through method calls
5. Clear separation of concerns between renderers

## Technical Notes
- All renderers will inherit from BaseRenderer
- Each renderer will have its own file
- Logging will be integrated at the base renderer level
- Testing will be comprehensive for each component
- Error handling will be consistent across renderers

## Next Steps
- Start implementation in new chat
- Follow the implementation plan in order
- Maintain clear separation between components
- Keep logging simple and focused
- Test each component thoroughly

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