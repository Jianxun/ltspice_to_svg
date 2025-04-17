# User Guide

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

## Basic Usage

The tool can be used from the command line to convert LTspice schematics to SVG format:

```bash
python -m src.ltspice_to_svg path/to/your/schematic.asc
```

This will create an SVG file in the same directory as your schematic file.

## Command Line Options

The tool supports several command line options to customize the output:

```bash
python -m src.ltspice_to_svg path/to/schematic.asc [options]
```

### Available Options:

- `--stroke-width FLOAT`: Set the width of lines in the SVG (default: 3.0)
- `--dot-size FLOAT`: Set the size of junction dots relative to stroke width (default: 1.5)
- `--scale FLOAT`: Set the scale factor for coordinates (default: 1.0)
- `--font-size FLOAT`: Set the font size in pixels (default: 16.0)
- `--export-json`: Export intermediate JSON files for debugging
- `--ltspice-lib PATH`: Set the path to LTspice symbol library
- `--no-text`: Skip rendering text elements

### Examples:

1. Basic conversion:
```bash
python -m src.ltspice_to_svg my_circuit.asc
```

2. Custom stroke width and font size:
```bash
python -m src.ltspice_to_svg my_circuit.asc --stroke-width 2.0 --font-size 12.0
```

3. Export JSON for debugging:
```bash
python -m src.ltspice_to_svg my_circuit.asc --export-json
```

4. Skip text rendering:
```bash
python -m src.ltspice_to_svg my_circuit.asc --no-text
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
python -m src.ltspice_to_svg my_circuit.asc --ltspice-lib /path/to/ltspice/lib
```

## Troubleshooting

### Common Issues

1. **Missing Symbols**
   - Error: "Symbol not found: [symbol_name]"
   - Solution: Ensure the symbol library path is correctly set

2. **Encoding Issues**
   - Error: "Failed to decode file"
   - Solution: Use the `fix_encoding.py` tool to fix file encoding

3. **Text Rendering Problems**
   - Issue: Text appears incorrectly positioned or rotated
   - Solution: Try adjusting the font size or scale

### Debugging

For debugging purposes, you can:

1. Export intermediate JSON files:
```bash
python -m src.ltspice_to_svg my_circuit.asc --export-json
```

2. Check the generated JSON files in the `output` directory

3. Use the `--no-text` option to isolate rendering issues

## Best Practices

1. **File Organization**
   - Keep schematic files and their associated symbol files in the same directory
   - Use a consistent symbol library path

2. **Symbol Design**
   - Ensure symbols are properly defined in .asy files
   - Use standard pin names and positions

3. **Text Elements**
   - Use clear, concise labels
   - Avoid overlapping text elements

4. **Performance**
   - For large schematics, consider using the `--no-text` option first
   - Adjust scale and stroke width for optimal rendering 