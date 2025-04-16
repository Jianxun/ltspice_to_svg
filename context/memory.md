# Project Memory

## Project Overview
This project aims to convert LTspice schematic files (.asc) to SVG format, maintaining high fidelity and accuracy in the conversion process.

## Current State
- The project is a tool to convert LTspice schematics to SVG format
- We have implemented basic SVG rendering including:
  - Wire rendering
  - Symbol rendering
  - Text rendering
  - Flag rendering (ground flags and net labels)
- Successfully refactored renderer classes to use base properties from BaseRenderer:
  - WireRenderer: Now uses stroke_width from BaseRenderer
  - TextRenderer: Now uses base_font_size from BaseRenderer
  - ShapeRenderer: Now uses stroke_width from BaseRenderer
  - SymbolRenderer: Now properly propagates base properties to child renderers
  - FlagRenderer: Now uses base_font_size and stroke_width from BaseRenderer
- All integration tests passing:
  - test1_wires_and_tjunctions: Wire and T-junction rendering
  - test2_text: Text rendering with various properties
  - test3_shapes: Basic shape rendering
  - test4_symbols: Symbol rendering with transformations
  - test5_symbol_texts: Symbol text rendering
  - test6_symbol_window_texts: Window text rendering
  - test7_flag_ground: Ground flag rendering
  - test8_flag_net_label: Net label rendering
- The test suite has been updated to include flag rendering tests
- The Miller OTA test case has been modified for manual inspection of rendered elements
- Successfully implemented and tested core rendering components:
  - BaseRenderer: Abstract base class with common functionality
  - WireRenderer: Handles wire rendering with T-junction support
  - TextRenderer: Handles text rendering with comprehensive support for justification, size, and transformations
  - ShapeRenderer: Handles basic shape rendering
  - SymbolRenderer: Handles symbol rendering with proper text delegation
- All tests passing for implemented components
- Comprehensive test coverage for T-junctions, shapes, symbols, and symbol texts
- TextRenderer successfully integrated with base_font_size property and proper delegation
- Ready to proceed with Test2 implementation for standalone text elements
- Successfully implemented and tested text rendering with proper font size handling
- Fixed bug in ASC parser where size multipliers were being stored instead of size indexes
- Text renderer now correctly handles:
  - Different text types (spice directives and comments)
  - Multi-line text splitting
  - Font size multipliers based on size indexes (0-7)
  - Text justification (Left, Center, Right)
  - Vertical text rendering
  - Text mirroring for symbols
- Ground flag rendering is working correctly
- Integration test `test7_flag_ground` passes successfully
- Ground flags are rendered with proper V shape and orientation
- Wires are rendered before ground flags for proper visual inspection
- T-junctions are properly rendered at wire intersections
- We are working on fixing the net label rendering issue
- The problem appears to be double rendering of net labels (12 instead of 6)
- We have identified that there are two places where net labels are being rendered:
  1. In `SVGRenderer.render_flags()` using the new `FlagRenderer` class
  2. In `src/generators/flag_renderer.py` which still has a reference to the old `net_label_renderer` module
- We have removed the old net label rendering code from `flag_renderer.py`, but the double rendering issue persists
- The test case `test_net_label_rendering` in `tests/integration/test_svg_renderer/test8_flag_net_label/test_flag_net_label.py` is failing

## Key Features
- Text rendering capabilities:
  - Multiple justification options (left, center, right)
  - Font size multipliers
  - Special character support
  - Multi-line text support
  - Text transformations (rotation, mirroring)
- Symbol rendering with proper text delegation
- Comprehensive test coverage with visual verification
- Proper property delegation between renderers

## Technical Details
- Python version: 3.12.9
- Testing framework: pytest
- SVG generation: svgwrite library
- UTF-16LE encoding support for LTspice files
- Property-based architecture for renderer configuration
- BaseRenderer class provides common properties:
  - base_font_size: Default font size for text rendering
  - stroke_width: Default stroke width for shapes and wires

## Lessons Learned
- Manual inspection is valuable for visual elements like text and flags
- Different stroke widths and font sizes can help find optimal rendering parameters
- Window overrides can affect text positioning and size
- Text rendering is sensitive to coordinate system and transformations
- Proper property delegation between renderers is crucial for consistent behavior
- Text positioning requires careful consideration of justification and transformation
- Comprehensive test coverage helps catch edge cases early
- Visual verification is essential for complex rendering tasks
- Flag orientation must match wire direction for proper connection
- Rendering order matters (wires before flags)
- Proper class attributes in SVG help with testing and identification
- Integration tests should include visual inspection components
- Proper property inheritance and delegation is crucial for maintainable code
- BaseRenderer class provides a solid foundation for consistent rendering properties
- Integration tests help verify that changes don't break existing functionality
- Property propagation through renderer hierarchy ensures consistent styling
- Clear separation of concerns between renderer classes improves code organization

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

## Next Steps
- Calibrate text rendering parameters
- Fine-tune font sizes and positioning
- Adjust text justification and alignment
- Handle special characters and symbols
- Implement text mirroring for mirrored symbols
- Implement Test2 (Text) to handle standalone text elements:
  - Create test schematic with various text attributes
  - Verify text rendering in different contexts
  - Ensure proper handling of special cases
  - Document any new insights or requirements
- Implement flag rendering (net labels, ground symbols, IO pins)
- Add tests for flag rendering
- Verify flag positioning and orientation
- Handle flag text properties (size, justification)
- Implement net label rendering
- Create integration test for net labels
- Ensure proper text positioning and orientation for net labels
- Handle different net label sizes and styles
- Need to investigate why net labels are still being rendered twice
- Check if there are any other places in the codebase where net labels might be rendered
- Consider removing the old `net_label_renderer.py` file once the issue is fixed

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
- Text rendering calibration is complete with optimized parameters for different text types
- Vertical and horizontal offsets have been fine-tuned for better alignment
- Text justification settings have been calibrated for normal and vertical text
- Text mirroring for mirrored symbols has been implemented and tested
- Special characters and symbols are handled correctly

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
10. Net label rendering with proper orientation and text positioning

### Net Label Rendering
- Fixed issue with duplicate net label groups in SVG output
- Implemented proper group handling in FlagRenderer:
  - Uses provided group from SVGRenderer instead of creating a new one
  - Only creates new group when no target group is provided
  - Properly handles text orientation and positioning
  - Supports all net label orientations (0°, 90°, 180°, 270°)
  - Counter-rotates text for 180° orientation to maintain readability
- Integration test `test8_flag_net_label` passes successfully
- Net labels are rendered with:
  - Proper text justification (center)
  - Correct distance from connection point
  - Proper font size and family
  - Correct orientation based on flag direction

### Lessons from Net Label Implementation
- Group management is crucial for SVG structure
- Avoid creating duplicate groups by properly using target groups
- Text orientation needs special handling for readability
- Debug logging helps track rendering flow and identify issues
- Integration tests should verify both structure and visual appearance

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
- `src/renderers/flag_renderer.py`: New implementation of flag rendering
- `src/generators/net_label_renderer.py`: Old implementation (should be removed)
- `tests/integration/test_svg_renderer/test8_flag_net_label/test_flag_net_label.py`: Test case for net label rendering

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

## Recent Changes
- Updated the Miller OTA test case to include flag rendering
- Removed automated verification from the test to focus on manual inspection
- Added support for different stroke widths and font sizes in SVG generation

## Text Rendering Status
- Current text rendering implementation needs calibration
- Font sizes and positioning may need adjustment
- Text justification and alignment may need fine-tuning
- Special characters and symbols in text may need special handling

## Known Issues
- Text positioning may be off in some cases
- Font sizes may not be optimal for all cases
- Text justification may need adjustment
- Special characters may not render correctly
- Text mirroring may need improvement

## Next Steps
- Calibrate text rendering parameters
- Fine-tune font sizes and positioning
- Adjust text justification and alignment
- Handle special characters and symbols
- Implement text mirroring for mirrored symbols

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
10. Net label rendering with proper orientation and text positioning

### Net Label Rendering
- Fixed issue with duplicate net label groups in SVG output
- Implemented proper group handling in FlagRenderer:
  - Uses provided group from SVGRenderer instead of creating a new one
  - Only creates new group when no target group is provided
  - Properly handles text orientation and positioning
  - Supports all net label orientations (0°, 90°, 180°, 270°)
  - Counter-rotates text for 180° orientation to maintain readability
- Integration test `test8_flag_net_label` passes successfully
- Net labels are rendered with:
  - Proper text justification (center)
  - Correct distance from connection point
  - Proper font size and family
  - Correct orientation based on flag direction

### Lessons from Net Label Implementation
- Group management is crucial for SVG structure
- Avoid creating duplicate groups by properly using target groups
- Text orientation needs special handling for readability
- Debug logging helps track rendering flow and identify issues
- Integration tests should verify both structure and visual appearance

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
- `src/renderers/flag_renderer.py`: New implementation of flag rendering
- `src/generators/net_label_renderer.py`: Old implementation (should be removed)
- `tests/integration/test_svg_renderer/test8_flag_net_label/test_flag_net_label.py`: Test case for net label rendering

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

## Integration Testing
- All integration tests are passing
- Test cases cover:
  - Wire rendering and T-junctions
  - Text rendering (normal, vertical, mirrored)
  - Shape rendering
  - Symbol rendering
  - Symbol text and window text
  - Flag rendering (ground, net labels, IO pins)
  - Miller OTA schematic

## Renderer Architecture
- BaseRenderer class now includes common properties:
  - stroke_width (default: 2.0)
  - base_font_size (default: 16.0)
- SVGRenderer manages stroke width updates across all renderers
- Text rendering parameters are centralized for consistency

## Current Focus
- Performance optimization
- Documentation improvements
- Code quality enhancements