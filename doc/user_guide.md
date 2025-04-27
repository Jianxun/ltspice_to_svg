# User Guide

## Installation

### Option 1: Install directly from GitHub (Recommended)

```bash
pip install git+https://github.com/Jianxun/ltspice_to_svg.git
```

After installation, you can use the command-line tool from anywhere:

```bash
ltspice_to_svg your_schematic.asc
```

### Option 2: Clone the repository and install

1. Clone the repository:
```bash
git clone https://github.com/Jianxun/ltspice_to_svg.git
cd ltspice_to_svg
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install as a development package:
```bash
pip install -e .
```

## Basic Usage

After installation, you can use the tool directly from the command line:

```bash
ltspice_to_svg your_schematic.asc
```

If you haven't installed the package, you can use the provided shell script:

```bash
./ltspice_to_svg.sh your_schematic.asc
```

This will generate `your_schematic.svg` in the same directory as your schematic file.

## Command Line Options

The tool supports several command line options to customize the output:

### Basic Options
- `--stroke-width FLOAT`: Width of lines in the SVG (default: 2.0)
- `--dot-size FLOAT`: Size of junction dots relative to stroke width (default: 1.5)
- `--base-font-size FLOAT`: Base font size in pixels (default: 16.0)
- `--margin FLOAT`: Margin around schematic elements as percentage of viewbox (default: 10.0, can be set to 0 for tight fit)
- `--font-family STRING`: Font family for text elements (default: Arial)

### Text Rendering Options
- `--no-text`: Master switch to disable ALL text rendering
- `--no-schematic-comment`: Skip rendering schematic comments
- `--no-spice-directive`: Skip rendering SPICE directives
- `--no-nested-symbol-text`: Skip rendering text inside symbols
- `--no-component-name`: Skip rendering component names (R1, C1, etc.)
- `--no-component-value`: Skip rendering component values (10k, 1uF, etc.)
- `--no-net-label`: Skip rendering net label flags
- `--no-pin-name`: Skip rendering I/O pin text while keeping the pin shapes

### File Options
- `--export-json`: Export intermediate JSON files for debugging
- `--ltspice-lib PATH`: Path to LTspice symbol library (overrides system default)

## Example Usage Scenarios

### Basic Conversion

To convert a schematic with default settings:

```bash
ltspice_to_svg myschematic.asc
```

### Customizing Visual Style

To adjust line thickness and font size:

```bash
ltspice_to_svg myschematic.asc --stroke-width 2.5 --base-font-size 14.0
```

### Tight Fit for Documents

To create an SVG with minimal margins around the circuit:

```bash
ltspice_to_svg myschematic.asc --margin 0.0
```

### Changing Font Family

To use a different font for all text elements:

```bash
ltspice_to_svg myschematic.asc --font-family "Helvetica"
ltspice_to_svg myschematic.asc --font-family "Courier New"  # For monospace text
```

### Clean Circuit Diagram

To create a clean diagram without specific text elements:

```bash
ltspice_to_svg myschematic.asc --no-schematic-comment --no-spice-directive
```

### Bare Schematic 

For documentation with just components and wires (no text at all):

```bash
ltspice_to_svg myschematic.asc --no-text
```

### Keep Component Information but Hide Pin Names

Show component names and values but hide I/O pin text:

```bash
ltspice_to_svg myschematic.asc --no-pin-name
```

## Symbol Library

The tool needs access to LTspice symbol files (.asy) to properly render schematic symbols. By default, it looks for symbols in the following locations:

1. The directory containing the schematic file
2. The LTspice symbol library directory (set via `LTSPICE_LIB_PATH` environment variable)
3. The directory specified by the `--ltspice-lib` command line option

### Setting Symbol Library Path

You can set the symbol library path in several ways:

1. Environment variable:
```bash
export LTSPICE_LIB_PATH=/path/to/ltspice/lib
```

2. Command line option:
```bash
ltspice_to_svg my_circuit.asc --ltspice-lib /path/to/ltspice/lib
```

## Troubleshooting

### Common Issues

#### Missing Symbols
- **Problem**: "Symbol not found: [symbol_name]"
- **Solution**: 
  - Ensure the symbol library path is correctly set
  - Copy the missing symbol files to the same directory as your schematic
  - Use the `--ltspice-lib` option to specify the path to your symbol library

#### Encoding Issues
- **Problem**: "Failed to decode file"
- **Solution**: 
  - Use the included `fix_encoding.py` tool to fix file encoding:
    ```bash
    python tools/fix_encoding.py path/to/problematic/file.asc
    ```
  - This will convert the file to UTF-16LE without BOM, which is the encoding LTspice uses

#### Text Rendering Problems
- **Problem**: Text appears incorrectly positioned or styled
- **Solution**: 
  - Try adjusting the font size with `--base-font-size`
  - Change the font family with `--font-family`
  - Use `--no-text` to confirm if the issue is text-related
  - Check if the schematic has very small or very large text elements

#### Viewbox Issues
- **Problem**: Parts of the circuit are cut off in the SVG
- **Solution**:
  - Increase the margin with `--margin 15.0` or higher
  - Check if your schematic has elements very far from the main circuit

### Debugging

For debugging purposes, you can export intermediate JSON files:

```bash
ltspice_to_svg my_circuit.asc --export-json
```

This will create JSON files in the same directory as your output SVG, containing the parsed data structures that were used to generate the SVG. These files can be helpful for understanding how the tool interprets the LTspice schematic.

## Post-Processing

The SVG files produced by this tool are structured logically with groups for different element types, making them easy to work with in vector graphics editors like Adobe Illustrator or Inkscape. 

Common post-processing tasks:
- Adjust text positioning or font styling
- Add additional annotations or highlights
- Export to other formats like PDF or PNG
- Include in technical documentation 