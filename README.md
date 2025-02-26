# LTspice to SVG Converter

A Python tool to convert LTspice schematics (.asc files) into SVG format. The tool preserves the visual appearance of the schematic while making it web-friendly and scalable.

## Features

- Converts LTspice schematics (.asc) to SVG format
- Handles wires, symbols, text elements, and flags
- Supports symbol rotation and mirroring
- Maintains text readability (instance names and labels remain upright)
- Detects and marks T-junctions with dots
- Configurable stroke width and font size
- Optional JSON export for debugging
- Supports both UTF-16 and UTF-8 encoded files
- Handles built-in symbols (GND, etc.)
- Option to disable text rendering

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ltspice_to_svg.git
cd ltspice_to_svg
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Basic usage:
```bash
python src/ltspice_to_svg.py schematic.asc
```

This will create `schematic.svg` in the same directory as the input file.

### Command Line Options

- `--stroke-width FLOAT`: Set line width (default: 3.0)
- `--dot-size FLOAT`: Set T-junction dot size relative to stroke width (default: 1.5)
- `--scale FLOAT`: Scale factor for coordinates (default: 1.0)
- `--font-size FLOAT`: Font size in pixels (default: 16.0)
- `--export-json`: Export intermediate JSON files for debugging
- `--ltspice-lib PATH`: Path to LTspice symbol library (overrides LTSPICE_LIB_PATH)
- `--no-text`: Skip rendering text elements

### Environment Variables

- `LTSPICE_LIB_PATH`: Path to LTspice symbol library directory

### Examples

Convert with custom stroke width and font size:
```bash
python src/ltspice_to_svg.py schematic.asc --stroke-width 2.0 --font-size 20.0
```

Convert without text elements:
```bash
python src/ltspice_to_svg.py schematic.asc --no-text
```

Export debug data:
```bash
python src/ltspice_to_svg.py schematic.asc --export-json
```

## Supported Features

### Schematic Elements
- Wires with configurable stroke width
- Symbol drawings (lines, circles, rectangles, arcs)
- Text elements with proper alignment and sizing
- Instance names that remain upright regardless of symbol rotation
- T-junction dots
- Ground symbols and flags

### Symbol Transformations
- Rotation (0°, 90°, 180°, 270°)
- Mirroring
- Text position adjustment for mirrored symbols

### Text Formatting
- Multiple font sizes (8 levels)
- Text alignment (Left, Center, Right, Top, Bottom)
- Upright text regardless of symbol rotation
- Optional text rendering

## Contributing

See [Development Guide](doc/development.md) for implementation details and contribution guidelines.

## License

[MIT License](LICENSE)
