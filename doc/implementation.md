# Implementation Details

This document provides detailed implementation information for the LTspice to SVG converter.

## Configuration

### SVG Generator Configuration
Key configuration parameters in SVGGenerator:
- `stroke_width`: Line thickness (default: 1.0)
- `dot_size_multiplier`: Size of junction dots (default: 0.75)
- `scale`: Coordinate scaling factor (default: 0.1)
- `font_size`: Base font size (default: 22.0)
- `text_centering_compensation`: Text alignment adjustment (default: 0.35)
- `net_label_distance`: Distance of net labels from origin (default: 8)
- `no_text`: Skip rendering all text elements
- `no_symbol_text`: Skip rendering symbol text elements only
- `size_multipliers`: Font size scaling factors

### Text Rendering Options
- `no_text`: Completely disable text rendering
  - Useful for debugging shape rendering
  - Improves performance for large schematics
- `no_symbol_text`: Disable only symbol text rendering
  - Keeps net labels and other text
  - Useful for focusing on component connections

## Shape Rendering

### Line Styles

All shapes in the SVG output use round line caps (`stroke-linecap="round"`) for consistent appearance:
- Solid lines use round caps for better visual quality
- Dotted lines (style code 2) use round caps to create proper dots
- Dashed lines (style code 1) use round caps for consistent ends

For dotted/dashed styles:
- Dots are created using a very small dash length (0.1) followed by a gap (2)
- Dashes use a length of 4 times the stroke width
- Gaps between elements are 2 times the stroke width

Example style codes:
```
0: solid
1: dash (4,2)
2: dot (0.1,2)
3: dash dot (4,2,0.1,2)
4: dash dot dot (4,2,0.1,2,0.1,2)
```

Implementation details:
- Rectangles with styles use SVG path elements to ensure proper line caps
- Circles and ellipses with styles use the stroke-linecap attribute
- Arcs with styles use SVG path elements with proper line caps

## Text Rendering

### Text Transformation
- Text positions are transformed according to symbol rotation and mirroring:
  1. Apply mirroring (if any)
  2. Apply rotation (0°, 90°, 180°, 270°)
  3. Apply final translation to symbol position
- Vertical text (VTop/VBottom) is handled by:
  1. Creating a separate text group
  2. Rotating text 90° around its anchor point
  3. Converting VTop/VBottom to Top/Bottom for standard alignment

### Text Style Resolution
- WINDOW entries in symbol files define text positioning and styling
- Two main types of WINDOW entries:
  - WINDOW 0: Instance name text settings
  - WINDOW 3: Value text settings
- Text rendering rules:
  1. Instance names (WINDOW 0):
     - Always rendered if present in symbol
     - Uses WINDOW override from schematic if available
     - Falls back to WINDOW default from symbol file
     - Uses default position if no WINDOW settings found
  2. Values (WINDOW 3):
     - Only rendered if WINDOW 3 exists in symbol file or schematic override
     - Uses WINDOW override from schematic if available
     - Falls back to WINDOW default from symbol file
     - No default rendering if WINDOW 3 is not defined

## Flag and IO Pin Handling

### Flag Orientation Rules
- Wire directions are calculated using a 90-degree grid system:
  - 0°: Left (negative X)
  - 90°: Up (negative Y)
  - 180°: Right (positive X)
  - 270°: Down (positive Y)
- Flag orientation rules:
  1. Single wire connection:
     - Flag points in the same direction as the wire
  2. Two opposite wires:
     - Vertical wires (90° or 270°): Flag points right (180°)
     - Horizontal wires (0° or 180°): Flag points down (270°)
  3. Default cases:
     - No connected wires: Points left (0°)
     - Non-opposite wire pairs: Points left (0°)
     - More than two wires: Points left (0°)

### Implementation Considerations
- Wire direction calculation uses atan2 for angle computation
- Angles are normalized to the 90-degree grid system
- Flag orientation ensures consistent rendering across the schematic
- Special handling for ground flags and IO pins to maintain visual consistency

## Debug Features

Debug features can be enabled through SVGGenerator:
- `export_json`: Exports debug data to JSON file
- Debug data includes:
  - Wires
  - Symbols
  - Texts
  - Flags
  - IO pins
  - Shapes
  - Symbol data
  - T-junctions

## Scale Factor

The default scale factor (0.1) may make shapes too small to be visible. Use a larger scale factor (e.g. 1.0) if shapes appear too small:

```bash
python ./src/ltspice_to_svg.py input.asc --scale 1.0
```

## File Encoding

### LTspice File Encoding

LTspice uses different encoding schemes for its schematic files (.asc) based on content:

1. **ASCII Encoding**
   - Used for schematics containing only ASCII characters
   - Example: Simple schematics with basic components and text
   - Most common for new schematics without special characters

2. **UTF-16LE without BOM**
   - Used when special characters are present (e.g., µ, Ω, °)
   - No Byte Order Mark (BOM) at the start of the file
   - Example: Schematics with component values using micro (µ) or ohm (Ω) symbols

### Implementation Guidelines

When working with LTspice files programmatically:

1. **Reading Files**
   ```python
   # Try ASCII first (for simple schematics)
   try:
       with open('file.asc', 'r', encoding='ascii') as f:
           text = f.read()
   except UnicodeError:
       # If ASCII fails, try UTF-16LE
       with open('file.asc', 'rb') as f:
           content = f.read()
           # Skip BOM if present
           if content.startswith(b'\xff\xfe'):
               content = content[2:]
           text = content.decode('utf-16')
   ```

2. **Writing Files**
   ```python
   # Always use UTF-16LE without BOM for compatibility
   with open('file.asc', 'wb') as f:
       f.write(text.encode('utf-16le'))
   ```

### Important Notes

- Never add a BOM to LTspice files as it prevents LTspice from opening them correctly
- The encoding choice is automatic based on content, not on how the file was created
- When in doubt, use UTF-16LE without BOM to ensure compatibility
- This applies to both .asc (schematic) and .asy (symbol) files

### Encoding Normalization Tool

If a file becomes corrupted due to improper encoding handling, use the `tools/normalize_encoding.py` script to fix it:

```bash
./tools/normalize_encoding.py <file_path>
```

The tool will:
1. Analyze the file's current encoding
2. Create a backup (.bak) before making changes
3. Normalize to UTF-16LE without BOM if needed
4. Report all changes made

Common scenarios where normalization is needed:
- Files with UTF-16LE BOM that can't be opened in LTspice
- ASCII files containing special characters (µ, Ω, etc.)
- Files corrupted by different text editors
- Files copied from different systems/platforms

Safety features:
- Only modifies files that need normalization
- Creates backups before changes
- Only works on .asc and .asy files
- Provides clear feedback about actions taken 