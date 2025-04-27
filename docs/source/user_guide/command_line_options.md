# Command Line Options

The LTspice to SVG converter provides several command line options to customize the output. These options allow you to control the appearance of the generated SVG file and which elements are included.

## Basic Options

- `--stroke-width FLOAT`: Width of lines in the SVG (default: 2.0)
- `--dot-size FLOAT`: Size of junction dots relative to stroke width (default: 1.5)
- `--base-font-size FLOAT`: Base font size in pixels (default: 16.0)
- `--margin FLOAT`: Margin around schematic elements as percentage of viewbox (default: 10.0, can be set to 0 for tight fit)
- `--font-family STRING`: Font family for text elements (default: Arial)

## Text Rendering Options

- `--no-text`: Master switch to disable ALL text rendering
- `--no-schematic-comment`: Skip rendering schematic comments
- `--no-spice-directive`: Skip rendering SPICE directives
- `--no-nested-symbol-text`: Skip rendering text inside symbols
- `--no-component-name`: Skip rendering component names (R1, C1, etc.)
- `--no-component-value`: Skip rendering component values (10k, 1uF, etc.)
- `--no-net-label`: Skip rendering net label flags
- `--no-pin-name`: Skip rendering I/O pin text while keeping the pin shapes

## File Options

- `--export-json`: Export intermediate JSON files for debugging
- `--ltspice-lib PATH`: Path to LTspice symbol library (overrides system default)

## Getting Help

To see all available options with their descriptions:

```bash
ltspice_to_svg --help
```

## Option Combinations

Many of the options can be combined to achieve the desired output. For example:

```bash
ltspice_to_svg myschematic.asc --stroke-width 2.5 --base-font-size 14.0 --no-schematic-comment --font-family "Helvetica"
```

This command will:
- Convert `myschematic.asc` to SVG
- Set the stroke width to 2.5
- Set the base font size to 14.0
- Skip rendering schematic comments
- Use Helvetica as the font family for all text elements 