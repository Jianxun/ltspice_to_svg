# Project Memory

## Current State
- Project is undergoing a major refactor of the SVG rendering system
- Replacing existing SVGGenerator class with new SVGRenderer class
- Following a modular design with specialized renderers
- Using pytest for all test cases
- Completed implementations:
  - BaseRenderer (abstract class)
  - WireRenderer (with tests)
  - TextRenderer (with tests)
  - ShapeRenderer (with tests)
  - SymbolRenderer (with tests)
- Documentation:
  - Created comprehensive API documentation for all renderers
  - Added standalone usage examples for each renderer
  - Documented shape types, text properties, and wire rendering
- Test Configuration:
  - Set up pytest.ini with proper configuration
  - Excluded archived tests
  - Configured logging and test output format
  - All active tests are passing (51 tests)
- Recent Test Improvements:
  - Consolidated wire renderer tests
  - Added comprehensive stroke width tests
  - Added T-junction size tests
  - Improved test organization and readability
  - Added visual test results for manual inspection

## Architecture Design
1. Base Renderer (abstract class)
   - Provides common functionality
   - Defines render interface
   - Handles logging

2. Specialized Renderers
   - WireRenderer: Handles wire and T-junction rendering
     - Supports different stroke widths
     - Supports different T-junction sizes
     - Handles horizontal, vertical, and diagonal wires
     - Supports T-junctions at wire intersections
   - TextRenderer: Handles text rendering with:
     - Font size multiplier mapping (0-7)
     - Text justification (Left, Center, Right, Top, Bottom)
     - Multi-line text support
     - Special character handling
     - Default values
   - ShapeRenderer: Handles various shape types:
     - Lines (with different styles)
     - Circles (both center-radius and bounding box formats)
     - Rectangles (both x1,y1,x2,y2 and x,y,width,height formats)
     - Arcs
   - SymbolRenderer: Handles symbol rendering with:
     - Group creation and management
     - Transformation handling
     - Shape and text rendering delegation

3. Main SVGRenderer Class
   - Manages renderers
   - Handles state transitions
   - Provides high-level interface

## Implementation Status
- Base renderer: Complete
- Wire renderer: Complete with tests
  - Added stroke width tests
  - Added T-junction size tests
  - Improved test organization
- Text renderer: Complete with tests
- Shape renderer: Complete with tests
- Symbol renderer: Complete with tests
- Logging system: In progress
  - Need to create logging configuration
  - Need to add logging to base renderer
  - Need to implement logging in specialized renderers
  - Need to add performance monitoring
  - Need to create logging utilities

## Dependencies
- svgwrite: For SVG generation
- pytest: For testing
- Python standard library: For logging

## Notes
- All test cases use pytest framework
- Test files follow consistent structure:
  - Fixtures for drawing and renderer
  - Helper functions for saving SVG and getting elements
  - Clear test organization with descriptive names
  - Results saved in dedicated directories
- Special character handling in TextRenderer:
  - & -> &amp;
  - < -> &lt;
  - > -> &gt;
  - Other characters preserved as is
- Shape Renderer supports multiple line styles:
  - Solid (default)
  - Dashed
  - Dotted
  - Dash-dot
  - Dash-dot-dot
- Rectangle rendering supports two formats:
  - Bounding box: x1,y1,x2,y2
  - Position-size: x,y,width,height
- Logging System Requirements:
  - Need to support different log levels (DEBUG, INFO, WARNING, ERROR)
  - Should include performance metrics
  - Must be configurable through environment variables
  - Should support file and console output
  - Need to include context information in logs