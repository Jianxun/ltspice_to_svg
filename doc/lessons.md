# Project-Specific Lessons

This document contains project-specific lessons learned during development. These lessons are particularly relevant to the LTspice to SVG converter project.

## File Handling

### LTspice File Encoding
- LTspice files (.asc and .asy) must be saved in UTF-16LE encoding without BOM (Byte Order Mark)
- When editing these files as plaintext:
  1. Read with proper UTF-16 handling
  2. Make modifications
  3. Write back in UTF-16LE without BOM
- Example Python code:
  ```python
  # Reading
  with open('file.asc', 'rb') as f:
      content = f.read()
  text = content.decode('utf-16')
  
  # Writing
  with open('file.asc', 'w', encoding='utf-16le') as f:
      f.write(modified_text)
  ```

## SVG Rendering

### Text Orientation
- For IO pin text orientation in SVG, use the formula: text_rotation = (90 - pin_orientation) % 360
  - This ensures text is always vertical relative to the pin's orientation
  - Example: When pin is at 0° (horizontal), text is at 90° (vertical)
  - Example: When pin is at 270°, text is at 180° relative to pin (still vertical)

### SVG Text Transform Inspection
When inspecting SVG text orientation:
1. Look for nested transform groups (<g>) that contain the text element
2. Check transforms in order from outer to inner group:
   - Main group usually has translation and pin rotation: `transform="translate(x,y) rotate(pin_angle)"`
   - Text group may have additional rotation: `transform="rotate(text_angle)"`
3. Final text orientation is the combination of all rotations:
   - If text has no rotation group, it inherits parent group's rotation
   - If text has its own rotation group, add that rotation to parent's
4. Example:
   ```xml
   <g transform="translate(-512,352) rotate(0)">
       <!-- No text rotation group = text will be horizontal -->
       <text ...>BUS04</text>
   </g>
   ```

### Line Styles
- Always use round line caps (`stroke-linecap="round"`) for all SVG shapes in this project:
  - This ensures consistent appearance across different shape types (lines, circles, rectangles, arcs)
  - Especially important for dotted/dashed lines where round caps create proper dots
  - Example SVG style:
    ```xml
    <path stroke-linecap="round" stroke-dasharray="0.1,2" .../>  <!-- For dotted lines -->
    <line stroke-linecap="round" .../>  <!-- For solid lines -->
    ```

## Environment Setup
- Always set the environment variable `LTSPICE_LIB_PATH` to the path of the LTspice symbol library:
  ```bash
  export LTSPICE_LIB_PATH="/Users/$USER/Library/Application Support/LTspice/lib/sym"
  ``` 