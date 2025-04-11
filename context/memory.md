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

## Architecture Design
1. Base Renderer (abstract class)
   - Provides common functionality
   - Defines render interface
   - Handles logging

2. Specialized Renderers
   - WireRenderer: Handles wire and T-junction rendering
   - TextRenderer: Handles text rendering with:
     - Font size multiplier mapping (0-7)
     - Text justification (Left, Center, Right, Top, Bottom)
     - Multi-line text support
     - Special character handling
     - Default values
   - SymbolRenderer: TODO
   - ShapeRenderer: TODO

3. Main SVGRenderer Class
   - Manages renderers
   - Handles state transitions
   - Provides high-level interface

## Implementation Status
- Base renderer: Complete
- Wire renderer: Complete with tests
- Text renderer: Complete with tests
- Symbol renderer: Not started
- Shape renderer: Not started
- Logging system: Not started

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