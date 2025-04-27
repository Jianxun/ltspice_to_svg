# Basic Usage

After installation, you can use the LTspice to SVG converter directly from the command line.

## Simple Conversion

To convert an LTspice schematic to SVG:

```bash
ltspice_to_svg your_schematic.asc
```

This will generate `your_schematic.svg` in the same directory as your schematic file.

## Using the Shell Script

If you haven't installed the package, you can use the provided shell script:

```bash
./ltspice_to_svg.sh your_schematic.asc
```

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

## Symbol Library Configuration

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