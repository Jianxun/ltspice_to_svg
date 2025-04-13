# Project Memory

## Project Overview
This project aims to convert LTspice schematic files (.asc) to SVG format. The project is organized into several key components:

1. **Parsers**: Handle the conversion of LTspice schematic files to an intermediate format
2. **Renderers**: Convert the intermediate format to SVG
3. **Generators**: Coordinate the overall conversion process

## Current State
- Python virtual environment is set up
- Core SVG rendering functionality is implemented
- Test1 (Wires and T-junctions) has been successfully implemented and verified
  - Successfully detects and renders 9 T-junctions
  - Uses dot_size_multiplier=2.0 for better visibility
  - Includes assertion to verify T-junction count
- Test3 (Shapes) has been successfully implemented and verified
  - Successfully detects and renders 13 shapes (5 lines, 2 rectangles, 2 circles, 4 arcs)
  - Uses stroke_width=2.0 for better visibility
  - Includes assertions to verify shape counts and types
  - Shapes are organized by type in the JSON output (lines, rectangles, circles, arcs)
  - Fixed shape rendering by implementing proper render_shapes method
  - Fixed viewBox calculation to include shape coordinates
  - Arc rendering is now working correctly:
    - Arcs are rendered on the ellipse defined by the bounding box
    - Arcs are rendered counter-clockwise from start_angle to end_angle
    - Large arc flag is set correctly based on angle difference
    - Test verifies all arc parameters (angles, direction, large arc flag)
- Test4 (Symbols) has been successfully implemented and verified
  - Successfully detects and renders 3 symbols (2 NMOS transistors, 1 voltage source)
  - Symbols are loaded from both local files and LTspice library
  - Supports different orientations (0°, 270°)
  - Symbol shapes are rendered correctly within their groups
  - Symbol transformations (translation, rotation) are applied correctly
  - Stroke width customization is supported for all elements
  - Added detailed assertions for symbol elements:
    - Voltage source: 5 lines, 1 circle
    - NMOS: 14 lines
  - LTSPICE_LIB_PATH environment variable is properly configured
- Test5 (Symbol Texts) has been successfully implemented and verified
  - Successfully implemented basic symbol text rendering
  - Added support for text elements in symbols (pin labels, etc.)
  - Fixed mirrored text rendering issues:
    - Changed transformation order to apply rotation before mirroring
    - Added mirrored state tracking in SymbolRenderer
    - Adjusted text justification based on mirrored state (Left ↔ Right)
    - Preserved font sizes and text content in mirrored symbols
  - Successfully tested with NMOS transistors in different orientations (R0, R270, M0)
  - Added comprehensive tests to verify:
    - Text elements are present in SVG output
    - Text content is preserved
    - Mirroring transformations are applied correctly
    - Text properties (position, justification, size) are maintained
  - Fixed test assertions to expect 5 symbols (3 NMOS and 2 voltage sources)
  - Successfully regenerated test5_symbol_texts.json with correct symbol count
  - Updated window text metadata format to use property IDs as dictionary keys:
    - Changed windows from array to dictionary format
    - Property IDs are now used as keys instead of being stored in the data
    - Structure is consistent between window definitions and overrides
    - Updated documentation to reflect the new format
  - Implemented window text rendering:
    - Added render_window_texts method to SymbolRenderer
    - Handles window definitions from symbol definitions
    - Supports window overrides from symbol instances
    - Properly handles property values (instance names and values)
    - Applies text transformations (mirroring, rotation)
    - Handles text justification and size multipliers
    - Successfully tested with various symbol types and orientations
  - Fixed window text overrides bug:
    - Created Test6 (Symbol Window Texts) to specifically test window text overrides
    - Fixed type mismatch between string keys (in window definitions) and integer keys (in window overrides)
    - Implemented robust key comparison supporting both integer and string keys
    - Added detailed debug logging to track window overrides flow
    - Added assertions to verify text positioning, rotation, and formatting
    - Verified all window text overrides are properly applied in the SVG output

## Technical Details
- The project uses Python 3.12.9
- Testing framework: pytest
- SVG rendering is handled by the SVGRenderer class
- Wire and T-junction detection is implemented in the WireRenderer class
- Shape rendering is implemented in the ShapeRenderer class
- Symbol rendering is implemented in the SymbolRenderer class
- Text rendering is implemented in the TextRenderer class
- Rendering features:
  - Line styles: solid, dashed, dotted, dash-dot, dash-dot-dot
  - Shape types: lines, rectangles, circles/ellipses, arcs
  - Stroke width customization
  - Proper viewBox calculation for all shapes
  - Arc rendering with correct angle handling and direction
  - Symbol group creation and transformation
  - Symbol shape and text rendering
  - Text justification and mirroring support
  - Window text rendering with property resolution and overrides

## Project Structure
```
.
├── src/
│   ├── generators/
│   │   └── svg_renderer.py
│   ├── parsers/
│   │   ├── asc_parser.py
│   │   ├── asy_parser.py
│   │   └── schematic_parser.py
│   └── renderers/
│       ├── wire_renderer.py
│       ├── shape_renderer.py
│       ├── symbol_renderer.py
│       └── text_renderer.py
├── tests/
│   └── integration/
│       └── test_svg_renderer/
│           ├── test1_wires_and_tjunctions/
│           │   ├── test1_wires_and_tjunctions.asc
│           │   ├── test1_wires_and_tjunctions.py
│           │   └── results/
│           │       ├── test1_wires_and_tjunctions.svg
│           │       └── test1_wires_and_tjunctions.json
│           ├── test3_shapes/
│           │   ├── shapes.asc
│           │   ├── test_shapes.py
│           │   └── results/
│           │       ├── shapes.svg
│           │       └── shapes.json
│           ├── test4_symbols/
│           │   ├── test4_symbols.asc
│           │   ├── test_symbols.py
│           │   └── results/
│           │       ├── test4_symbols.svg
│           │       └── test4_symbols.json
│           └── test5_symbol_texts/
│               ├── test5_symbol_texts.asc
│               ├── test_symbol_texts.py
│               └── results/
│                   ├── test5_symbol_texts.svg
│                   └── test5_symbol_texts.json
```

## Lessons Learned
1. T-junction detection requires careful consideration of both direct and indirect connections
2. Visual debugging is important for verifying T-junction detection
3. Using appropriate dot size multipliers improves visibility of T-junctions
4. Assertions should be added to verify expected counts of detected elements
5. Shape data is organized by type in the JSON output, requiring different handling than wire data
6. Line styles in LTspice are represented as strings (e.g., "4,2" for dashed lines)
7. Arc shapes include start and end angles in their definition
8. ViewBox calculation must consider all elements in the schematic, not just wires
9. Shape rendering requires proper type information to be added to each shape
10. Arc rendering requires careful handling of:
    - Ellipse parameters from bounding box
    - Start and end angles
    - Counter-clockwise direction
    - Large arc flag based on angle difference
11. Symbol rendering requires:
    - Proper group creation and transformation
    - Correct handling of symbol definitions from both local files and LTspice library
    - Careful application of transformations (translation, rotation)
    - Proper delegation of shape and text rendering to specialized renderers
12. Detailed assertions for symbol elements help ensure correct parsing and rendering
13. Environment variables (LTSPICE_LIB_PATH) are crucial for accessing LTspice library symbols
14. Window text rendering requires:
    - Proper handling of window definitions and overrides
    - Careful property value resolution
    - Correct application of text transformations
    - Proper handling of text justification in mirrored symbols
    - Consistent font size scaling

## Next Steps
- Implement Test2 (Text) to handle standalone text elements
  - Add text elements with different justifications
  - Add text elements with different font sizes
  - Add text elements with special characters
  - Add text elements with multiple lines
  - Add text elements with different orientations

### Arc Rendering Details
- LTspice specifies arcs using 8 coordinates: `ARC Normal x1 y1 x2 y2 x3 y3 x4 y4`
  - (x1,y1) and (x2,y2): define the bounding box
  - (x3,y3): end point
  - (x4,y4): start point
- SVG arc path format: `M start_x start_y A rx ry 0 large_arc sweep end_x end_y`
  - rx, ry: ellipse radii from bounding box
  - large_arc: 1 if angle difference > 180°
  - sweep: 1 for counter-clockwise direction
  - start/end points calculated from angles on the ellipse

### Implementation Status
1. Shape Parser (`src/parsers/shape_parser.py`):
   - Correctly parses arc data from LTspice format
   - Calculates start and end angles from control points
   - Normalizes angles to [0, 360) range

2. Shape Renderer (`src/renderers/shape_renderer.py`):
   - Uses SVG path with arc command for rendering
   - Calculates start and end points on the ellipse using angles
   - Always renders counter-clockwise (sweep=1)
   - Sets large arc flag based on angle difference

3. Test Status (`tests/integration/test_svg_renderer/test3_shapes/test_shapes.py`):
   - Test verifies all arc parameters
   - Checks ellipse dimensions from bounding box
   - Verifies counter-clockwise direction
   - Verifies large arc flag based on angle difference

### Dependencies
- SVG path command format: `M start_x start_y A rx ry x-axis-rotation large-arc sweep end_x end_y`
- Using svgwrite library for SVG generation
- pytest for testing

## Text Rendering
- Text elements in symbols are rendered using the `TextRenderer` class
- Text properties include position (x,y), justification, size multiplier, and text content
- For mirrored symbols, text is counter-mirrored to maintain readability while preserving position
- Text justification is handled by setting the appropriate SVG text-anchor property
- Font size is calculated based on the size multiplier and base font size
- Window text rendering handles:
  - Window definitions from symbol definitions
  - Window overrides from symbol instances
  - Property values (instance names and values)
  - Text transformations (mirroring, rotation)
  - Text justification and size multipliers

## Project State

The project is focused on converting LTspice schematic files (.asc) to SVG format. We've successfully implemented:

1. Basic parsing of .asc files
2. Rendering of wires, shapes (lines, rectangles, arcs, circles), texts, and symbols
3. Tests for wires, shapes, symbols, symbol texts, and window texts
4. Visual debugging and verification system
5. SVG generation with proper styling and transformations
6. Support for all basic elements in LTspice schematics
7. Symbol rendering with proper transformations, including mirroring and rotation
8. Text rendering including handling of special anchoring and justification
9. Window text rendering with property value resolution and overrides

Current focus is on Test2 (Text), which involves creating a test schematic for standalone text elements with various attributes.

## Technical Details

- Python version: 3.12.9
- Testing framework: pytest with fixtures and parameterized tests
- Core modules:
  - `parsers`: Handle reading and interpreting LTspice files
  - `renderers`: Convert parsed data to SVG elements
  - `generators`: Assemble SVG elements into complete documents

### File Organization
- Source files in `ltspice_to_svg/`
  - `parsers/`: Contains code for parsing different LTspice file formats
  - `renderers/`: Contains renderers for different element types
  - `generators/`: SVG document generation utilities
- Test files in `tests/`
  - Test cases organized by feature (wires, shapes, symbols, texts)
  - Each test directory has schematic (.asc), expected output, and test code

### Important Files
- `ltspice_to_svg/parsers/schematic_parser.py`: Parses .asc files
- `ltspice_to_svg/parsers/symbol_parser.py`: Parses .asy files
- `ltspice_to_svg/renderers/base_renderer.py`: Base class for all renderers
- `ltspice_to_svg/renderers/wire_renderer.py`: Renders wires
- `ltspice_to_svg/renderers/shape_renderer.py`: Renders shapes (lines, rectangles, etc.)
- `ltspice_to_svg/renderers/text_renderer.py`: Renders text elements
- `ltspice_to_svg/renderers/symbol_renderer.py`: Renders symbols with proper transformations
- `tools/fix_encoding.py`: Tool to fix encoding issues in LTspice files

## Rendering Features

1. **Wire Rendering**
   - SVG path generation with proper styling
   - Start and end point transformations
   
2. **Shape Rendering**
   - Lines, rectangles, circles, arcs
   - Fill and stroke styling
   - Proper transformations for all coordinates
   
3. **Text Rendering**
   - Font size and family handling
   - Text rotation and mirroring
   - Proper positioning based on anchor points and justification
   - Special handling for mirrored text to maintain readability
   
4. **Symbol Rendering**
   - Proper group creation with transformations
   - Support for flipping and rotation
   - Pin symbol rendering with correct orientation
   - Text elements within symbols with proper positioning
   - Handling of window texts with property value resolution
   - Correct application of window text overrides with type-aware key handling

## Recent Progress

We've completed the successful implementation of window text rendering in symbols, including a key fix for window text overrides that had a type mismatch between string and integer keys. The implementation now correctly handles both key types when applying overrides.

We also created and completed Test6 (Symbol Window Texts) to specifically test window text overrides with various symbol orientations and property values. This test validates that window text overrides are properly applied and text positioning and formatting are correct.

The project now has comprehensive test coverage for all basic elements in LTspice schematics, including edge cases such as mirrored text rendering and window text overrides.

## Next Steps

The current focus is on Test2 (Text), which will create a comprehensive test for standalone text elements with various attributes, including:
- Different font sizes
- Font styles (bold, italic)
- Text alignment (left, center, right)
- Text rotation
- Special characters
- Multi-line text

After completing Test2, we'll proceed with Test3 (Shapes) and Test4 (Integration), as outlined in the todo list.