# LTspice to SVG Converter

A tool to convert LTspice schematics to SVG format, preserving the visual layout and making it easy to embed in web pages or documentation.

## Features

- Converts LTspice schematics (.asc files) to SVG format
- Preserves all schematic elements:
  - Wires and connections
  - Circuit symbols with proper orientation and mirroring
  - Net labels and flags
  - IO pins
  - Text elements
- Supports both local and LTspice library symbols
- Customizable output:
  - Adjustable line width
  - Configurable font size
  - Customizable scale factor
  - Optional text rendering control

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
python src/ltspice_to_svg.py your_schematic.asc
```

This will generate `your_schematic.svg` in the same directory as your schematic file.

### Command Line Options

- `--stroke-width`: Width of lines in the SVG (default: 3.0)
- `--dot-size`: Size of junction dots relative to stroke width (default: 1.5)
- `--scale`: Scale factor for coordinates (default: 1.0)
- `--font-size`: Font size in pixels (default: 16.0)
- `--ltspice-lib`: Path to LTspice symbol library (overrides LTSPICE_LIB_PATH)
- `--no-text`: Skip rendering text elements
- `--no-symbol-text`: Skip rendering symbol text elements

Example with options:
```bash
python src/ltspice_to_svg.py your_schematic.asc --stroke-width 2.0 --font-size 14.0 --scale 1.2
```

### Environment Variables

- `LTSPICE_LIB_PATH`: Path to LTspice symbol library

  On macOS:
  ```bash
  export LTSPICE_LIB_PATH="/Users/$USER/Library/Application Support/LTspice/lib/sym"
  ```

  On Windows:
  
  CMD:
  ```cmd
  set LTSPICE_LIB_PATH="C:\Users\%USERNAME%\AppData\Local\LTspice\lib\sym"
  ```
  
  PowerShell:
  ```powershell
  $env:LTSPICE_LIB_PATH="C:\Users\$env:USERNAME\AppData\Local\LTspice\lib\sym"
  ```

  Note: You can also use the `--ltspice-lib` command line option to override this setting.

## Examples

### Basic Schematic
```bash
python src/ltspice_to_svg.py examples/basic_rc.asc
```

### Complex Circuit
```bash
python src/ltspice_to_svg.py examples/opamp_circuit.asc --stroke-width 2.0 --font-size 12.0
```

## Output

The tool generates an SVG file that:
- Maintains the original schematic layout
- Uses standard SVG elements for easy embedding
- Preserves text readability with proper orientation
- Supports high-resolution display

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
