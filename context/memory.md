# Project Memory

## Project Overview
The project aims to convert LTspice schematics to SVG format. We are currently in the process of refactoring the codebase to improve its structure and maintainability.

## Current State
- Successfully implemented and tested the WireRenderer class
- Default values for stroke width (3.0) and dot size multiplier (1.5) are now consistently used across the codebase
- Test cases for WireRenderer are passing with 100% success rate
- SVG output files are being saved in the test results directory for manual inspection
- Working on implementing ShapeRenderer with comprehensive test cases

## Architecture Design
### New SVGRenderer Structure
- Base renderer class for common functionality
- Specialized renderers for different element types:
  - WireRenderer (implemented)
  - SymbolRenderer (pending implementation)
  - TextRenderer (pending implementation)
  - ShapeRenderer (in progress)
- Main SVGRenderer class for orchestration

### Logging System
- Simple, single-file logging implemented
- Focus on important events and errors
- Minimal impact on code readability
- Basic configuration in `src/utils/logger.py`

## Implementation Progress
1. [X] Create initial file structure
2. [X] Implement base renderer class
3. [ ] Implement specialized renderers
   - [X] WireRenderer
   - [ ] SymbolRenderer
   - [ ] TextRenderer
   - [ ] ShapeRenderer
4. [X] Implement main SVGRenderer class
5. [X] Setup testing structure
6. [X] Implement logging system

## Key Decisions
1. Using SVGRenderer name to avoid conflicts with existing SVGGenerator
2. Modular design with separate renderer classes
3. Simplified logging system with single log file
4. Explicit rendering control through method calls
5. Clear separation of concerns between renderers
6. SVG attribute values stored as numbers in renderers

## Technical Notes
- All renderers inherit from BaseRenderer
- Each renderer has its own file
- Logging is integrated at the base renderer level
- Testing structure is set up for each component
- Error handling is consistent across renderers
- SVG attributes are stored as numeric values and converted to strings when needed

## Technical Details
- WireRenderer implementation includes:
  - Basic wire rendering (horizontal, vertical, diagonal)
  - T-junction dot rendering
  - Custom stroke width support
  - Multiple wire rendering
- Test coverage includes:
  - Initialization testing
  - Wire orientation testing
  - Custom parameter testing
  - T-junction testing
  - Multiple element testing

## Next Steps
- Continue with the refactor plan as outlined in `refactor_plan.md`
- Implement remaining renderer classes
- Set up logging system
- Test integration between renderers

## Project Structure
- src/
  - generators/
    - svg_generator.py
    - svg_renderer.py (new)
  - renderers/
    - base_renderer.py (new)
    - wire_renderer.py (new)
    - shape_renderer.py
    - flag_renderer.py
    - text_renderer.py
  - utils/
    - logger.py (new)
- tests/
  - test_svg_renderer/
    - test_svg_renderer.py
    - results/
  - test_wire_renderer/
    - test_wire_renderer.py
    - results/
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

## Recent Changes
- Created new SVGRenderer architecture
- Implemented base renderer class
- Created comprehensive test suite
- Set up logging system
- Organized test files in dedicated directories
- Implemented WireRenderer with tests
- Added SVG output verification

## Notes
- Need to implement remaining specialized renderers
- ViewBox calculation needs to be implemented
- T-junction detection needs to be implemented
- Test coverage needs to be expanded
- Documentation needs to be updated

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

- SVG Attribute Handling:
  - SVG attributes are stored as numeric values in renderers
  - Convert numeric values to strings when asserting in tests
  - Use float() for numeric attribute comparisons
  - Keep consistent attribute types across renderers

- SVGWrite Drawing Behavior:
  - Each svgwrite.Drawing instance automatically creates a <defs> element
  - The <defs> element is always the first element in the drawing.elements list
  - When writing tests, account for this automatic element:
    - For empty drawings, expect len(elements) == 1
    - For drawings with one shape, expect len(elements) == 2
    - The actual shape element is always at index 1 or higher
  - This behavior affects element counting and indexing in tests

## Flag Renderer Tests
- Currently using scale=1.0 for testing
- SVG output files saved in tests/flag_renderer/results/
- Test results show potential rendering issues

## Completed
- Text rendering with rotation and positioning
- Symbol finding functionality
- Basic SVG generation
- Wire rendering with T-junction support
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
- SVG attributes should be stored as numeric values for consistency

- SVG Attribute Type Handling:
  - SVGWrite expects all attribute values to be strings
  - Common type mismatches:
    - Coordinates (x, y, cx, cy): Must convert numeric values to strings
    - Dimensions (width, height, r): Must convert numeric values to strings
    - Stroke width: Must convert numeric values to strings
    - Path data values: Must convert all numeric values to strings
  - Best practice: Convert all numeric values to strings using str() before passing to svgwrite
  - Test assertions should expect string values (e.g., '10' not 10, '20.0' not 20.0)

- SVG Style Attributes:
  - Dash array patterns require special handling:
    - Must be set in the style dictionary as 'stroke_dasharray'
    - Pattern values must be scaled by stroke width
    - Must be properly formatted as comma-separated string values
    - Must be set before adding element to drawing
  - Style attributes like stroke-width and stroke-dasharray use hyphens in SVG but underscores in svgwrite
  - Always set stroke_linecap='round' for dashed/dotted lines for better appearance

## Project State

### Test Coverage
- Comprehensive test suite for line style patterns implemented
- Tests cover all five line styles:
  - Solid line (no dash array)
  - Dash pattern (4 units dash, 2 units gap)
  - Dot pattern (very small dash to create dots, 2 units gap)
  - Dash-dot pattern (dash, gap, dot, gap)
  - Dash-dot-dot pattern (dash, gap, dot, gap, dot, gap)
- Edge cases covered:
  - Empty pattern handling
  - Invalid pattern handling
- Visual test case added:
  - Generates SVG file with all line styles for visual comparison
  - Located at tests/test_shape_renderer/results/line_styles.svg
- All tests passing successfully

### SVG Attribute Handling
- SVG attributes use hyphen format (e.g., stroke-width, stroke-dasharray)
- Style attributes are set in the style dictionary before adding elements
- Coordinate values are stored as floats and converted to strings when needed
- Test assertions handle floating-point comparisons appropriately
- Test outputs saved in dedicated results directories for manual inspection 