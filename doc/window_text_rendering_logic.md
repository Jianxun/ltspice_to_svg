# Window Text Rendering Logic

## Overview
Window text is a special type of text used to render symbol properties (e.g., symbol name, value) in LTspice schematics. Unlike standard symbol text, window text values can vary between different instances of the same symbol.

## Data Structure

### Window Definition in Symbols
Windows are defined in the `symbols.{symbol_name}.windows` dictionary with property IDs as keys:
```json
"windows": {
  "0": {  // Name window
    "x": 24,
    "y": 16,
    "justification": "Left",
    "size_multiplier": 2
  },
  "3": {  // Value window
    "x": 24,
    "y": 96,
    "justification": "Left",
    "size_multiplier": 2
  }
}
```

Each window has the following properties:
- Key: Property ID (e.g., "0", "3")
  - `0`: Symbol name
  - `3`: Symbol value
- Value: Window properties
  - `x`, `y`: Default coordinates for text placement
  - `justification`: Text alignment (e.g., "Left", "VBottom", "VTop")
  - `size_multiplier`: Controls text size

### Window Overrides in Schematic
Overrides are specified in `schematic.symbols[].window_overrides` with the same structure:
```json
"window_overrides": {
  "0": {
    "x": -32,
    "y": 56,
    "justification": "VBottom",
    "size_multiplier": 2
  },
  "3": {
    "x": 32,
    "y": 56,
    "justification": "VTop",
    "size_multiplier": 2
  }
}
```

## Rendering Logic

1. For each symbol instance:
   - Get the base symbol definition from `symbols.{symbol_name}`
   - For each property ID in the symbol's `windows` dictionary:
     a. Check if the instance has a corresponding property value
     b. If no property value exists, skip this window
     c. If property exists:
        - Use the window's default properties (x, y, justification, size_multiplier)
        - Check for overrides in `window_overrides` for this property_id
        - If overrides exist, use them instead of defaults
        - Render the text using the symbol text rendering logic with the final properties

## Special Considerations

1. **Text Values**:
   - Window text values come from the symbol instance properties, not from the symbol definition
   - If a property is missing, the window should not be rendered

2. **Text Justification**:
   - Support both horizontal and vertical text justifications
   - Common justifications:
     - Horizontal: "Left", "Center", "Right"
     - Vertical: "VBottom", "VTop"

3. **Size Control**:
   - Size is controlled by `size_multiplier` in both window definition and overrides
   - When overridden, use the override's `size_multiplier` value
   - Convert size_multiplier to appropriate text scaling factor

4. **Transformations**:
   - Window text should respect the symbol's transformation (rotation, mirroring)
   - Apply the same transformation rules as regular symbol text

5. **Property IDs**:
   - `0`: Symbol name (e.g., "V1", "M1")
   - `3`: Symbol value (e.g., "5V", "1k")

## Implementation Notes

1. **Property Resolution**:
   - First check for property value in the symbol instance
   - If missing, skip window rendering
   - If present, proceed with coordinate and justification resolution

2. **Coordinate Resolution**:
   - Use default coordinates from window definition
   - Apply overrides if present in window_overrides
   - Final coordinates should be relative to symbol position

3. **Justification Resolution**:
   - Use default justification from window definition
   - Apply override justification if present
   - Handle both horizontal and vertical justifications

4. **Size Resolution**:
   - Use default size_multiplier from window definition
   - If overridden, use the size_multiplier value from window_overrides
   - Convert size_multiplier to appropriate text scaling factor 