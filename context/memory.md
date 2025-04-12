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

## Technical Details
- The project uses Python 3.12.9
- Testing framework: pytest
- SVG rendering is handled by the SVGRenderer class
- Wire and T-junction detection is implemented in the WireRenderer class

## Project Structure
```
.
├── src/
│   ├── generators/
│   │   └── svg_renderer.py
│   ├── parsers/
│   │   └── asc_parser.py
│   └── renderers/
│       └── wire_renderer.py
├── tests/
│   └── integration/
│       └── test_svg_renderer/
│           └── test1_wires_and_tjunctions/
│               ├── test1_wires_and_tjunctions.asc
│               ├── test1_wires_and_tjunctions.py
│               └── results/
│                   ├── test1_wires_and_tjunctions.svg
│                   └── test1_wires_and_tjunctions.json
└── context/
    ├── memory.md
    └── todo.md
```

## Lessons Learned
1. T-junction detection requires careful consideration of both direct and indirect connections
2. Visual debugging is important for verifying T-junction detection
3. Using appropriate dot size multipliers improves visibility of T-junctions
4. Assertions should be added to verify expected counts of detected elements