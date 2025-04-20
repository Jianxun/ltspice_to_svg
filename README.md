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

4. Alternatively, install directly from GitHub:
```bash
pip install git+https://github.com/yourusername/ltspice_to_svg.git
```

## Usage

There are several ways to run the tool:

### 1. Using the shell script (recommended)

```bash
./ltspice_to_svg.sh your_schematic.asc
```

This will generate `your_schematic.svg` in the same directory as your schematic file.

### 2. Setting PYTHONPATH manually

```bash
PYTHONPATH=$PYTHONPATH:$(pwd) python src/ltspice_to_svg.py your_schematic.asc
```

### 3. Installing as a package

```bash
pip install -e .
ltspice_to_svg your_schematic.asc
```

### Command Line Options

- `--stroke-width`: Width of lines in the SVG (default: 2.0)
- `--dot-size`: Size of junction dots relative to stroke width (default: 1.5)
- `--base-font-size`: Base font size in pixels (default: 16.0)
- `--export-json`: Export intermediate JSON files for debugging
- `--ltspice-lib`: Path to LTspice symbol library (overrides system default)
- `--no-text`: Master switch to disable ALL text rendering (equivalent to enabling all other text options)
- `--no-schematic-comment`: Skip rendering schematic comments
- `--no-spice-directive`: Skip rendering SPICE directives
- `--no-nested-symbol-text`: Skip rendering nested symbol text
- `--no-component-name`: Skip rendering component names
- `--no-component-value`: Skip rendering component values
- `--no-net-label`: Skip rendering net label flags
- `--no-pin-name`: Skip rendering I/O pin text while keeping the pin shapes

Example with options:
```bash
./ltspice_to_svg.sh ./schematics/miller_ota.asc --stroke-width 3.0 --no-component-value
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

### Circuit Without Text
```bash
python src/ltspice_to_svg.py examples/opamp_circuit.asc --no-text
```

### Circuit With Custom Styling
```bash
python src/ltspice_to_svg.py examples/opamp_circuit.asc --stroke-width 1.5 --base-font-size 14.0
```

### Circuit Without Net Labels
```bash
python src/ltspice_to_svg.py examples/opamp_circuit.asc --no-net-label --no-pin-name
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
