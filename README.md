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

On macOS:
```bash
export LTSPICE_LIB_PATH="/Users/$USER/Library/Application Support/LTspice/lib/sym"
```

On Windows:

CMD:
```cmd
set LTSPICE_LIB_PATH="C:\Users\%USERNAME%\AppData\Local\LTspice\lib\sym"
```
Power Shell:
```powershell
$env:LTSPICE_LIB_PATH="C:\Users\$env:USERNAME\AppData\Local\LTspice\lib\sym"
```

### Examples

Convert with custom stroke width and font size:
```bash
python src/ltspice_to_svg.py ./schematics/miller_ota.asc --stroke-width 2.0 --font-size 20.0
```

Convert without text elements:
```bash
python src/ltspice_to_svg.py ./schematics/miller_ota.asc --no-text
```

Export debug data:
```bash
python src/ltspice_to_svg.py ./schematics/miller_ota.asc --export-json
```

## Supported Features

### Schematic Elements
- Wires with configurable stroke width
- Symbol drawings (lines, circles, rectangles, arcs)
- Text elements with proper alignment and sizing
- Instance names that remain upright regardless of symbol rotation
- T-junction dots
- Ground flags with V-shaped symbol (no text)
- Net labels and IO pins with proper orientation

### Symbol Transformations
- Rotation (0°, 90°, 180°, 270°)
- Mirroring
- Text position adjustment for mirrored symbols
- Proper flag orientation based on connected wires

### Text Formatting
- Multiple font sizes with semantic defaults:
  - Instance names: 1.5x base size
  - Node numbers: 0.625x base size
  - Symbol-specific text: 1.0x base size
- Text alignment (Left, Center, Right, Top, Bottom)
- Proper text positioning based on symbol attributes
- Automatic fallback positions for missing text entries
- Optional text rendering with --no-text flag
- Configurable text centering compensation
- Configurable net label distance from origin

## Contributing

See [Development Guide](doc/development.md) for implementation details and contribution guidelines.

## License

[MIT License](LICENSE)
