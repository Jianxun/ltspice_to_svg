# LTspice to SVG Converter

A tool to convert LTspice schematic files (.asc) and symbol files (.asy) to SVG format.

## Overview

This tool converts LTspice schematic and symbol files to SVG format, preserving:
- Component symbols and their connections
- Text labels and net names
- Wire styles (solid, dashed, dotted)
- Component rotations and mirroring
- Text orientations and alignments

## Project Structure

```
src/
├── generators/           # SVG generation components
│   ├── svg_generator.py  # Main SVG generation coordinator
│   ├── shape_renderer.py # Shape rendering (wires, lines, circles, etc.)
│   ├── text_renderer.py  # Text element rendering
│   ├── flag_renderer.py  # Flag rendering
│   ├── io_pin_renderer.py # IO pin rendering
│   ├── symbol_renderer.py # Symbol rendering
│   └── net_label_renderer.py # Net label rendering
├── parsers/             # LTspice file parsing components
│   ├── asc_parser.py    # Schematic (.asc) file parser
│   ├── asy_parser.py    # Symbol (.asy) file parser
│   └── shape_parser.py  # Shape element parser
└── ltspice_to_svg.py    # Main entry point
```

## Documentation

- [Development Guide](development.md) - Development guidelines and workflow
- [Architecture](architecture.md) - Detailed architecture and component design
- [Implementation](implementation.md) - Implementation details and technical notes
- [Testing](testing.md) - Test strategies and coverage
- [Lessons Learned](lessons.md) - Project-specific lessons and best practices

## Usage

Basic usage:
```bash
python ./src/ltspice_to_svg.py input.asc --scale 1.0
```

Options:
- `--scale`: Coordinate scaling factor (default: 0.1)
- `--output`: Output SVG file path (default: input.svg)
- `--export-json`: Export debug data to JSON file
- `--no-text`: Skip rendering all text elements
- `--no-symbol-text`: Skip rendering symbol text elements only

## Environment Setup

Set the LTspice symbol library path:
```bash
export LTSPICE_LIB_PATH="/Users/$USER/Library/Application Support/LTspice/lib/sym"
```

## Development

See the [Development Guide](development.md) for setup and contribution guidelines.

## Testing

See the [Testing Guide](testing.md) for test strategies and coverage information. 