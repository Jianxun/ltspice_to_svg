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

## Technical Details
- The project uses Python 3.12.9
- Testing framework: pytest
- SVG rendering is handled by the SVGRenderer class
- Wire and T-junction detection is implemented in the WireRenderer class
- Shape rendering is implemented in the ShapeRenderer class
- Symbol rendering is implemented in the SymbolRenderer class
- Rendering features:
  - Line styles: solid, dashed, dotted, dash-dot, dash-dot-dot
  - Shape types: lines, rectangles, circles/ellipses, arcs
  - Stroke width customization
  - Proper viewBox calculation for all shapes
  - Arc rendering with correct angle handling and direction
  - Symbol group creation and transformation
  - Symbol shape and text rendering

## Project Structure
```
.
├── src/
│   ├── generators/
│   │   └── svg_renderer.py
│   ├── parsers/
│   │   └── asc_parser.py
│   └── renderers/
│       ├── wire_renderer.py
│       ├── shape_renderer.py
│       └── symbol_renderer.py
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
│           └── test4_symbols/
│               ├── test4_symbols.asc
│               ├── test_symbols.py
│               └── results/
│                   ├── test4_symbols.svg
│                   └── test4_symbols.json
└── context/
    ├── memory.md
    └── todo.md
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

### Next Task: Test4 (Symbols)
- Need to implement symbol rendering tests
- Will need to handle:
  - Symbol transformations (rotation, position)
  - Symbol shape rendering
  - Symbol text rendering
  - Symbol group creation
  - Symbol data handling

### Dependencies
- SVG path command format: `M start_x start_y A rx ry x-axis-rotation large-arc sweep end_x end_y`
- Using svgwrite library for SVG generation
- pytest for testing