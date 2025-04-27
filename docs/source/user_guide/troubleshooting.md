# Troubleshooting

This section covers common issues that you may encounter when using the LTspice to SVG converter and provides solutions.

## Common Issues

### Missing Symbols

**Problem**: 
You receive an error message like "Symbol not found: [symbol_name]"

**Solution**: 
- Ensure the symbol library path is correctly set
- Copy the missing symbol files to the same directory as your schematic
- Use the `--ltspice-lib` option to specify the path to your symbol library

### Encoding Issues

**Problem**: 
You receive an error message like "Failed to decode file"

**Solution**: 
- Use the included `fix_encoding.py` tool to fix file encoding:
  ```bash
  python tools/fix_encoding.py path/to/problematic/file.asc
  ```
- This will convert the file to UTF-16LE without BOM, which is the encoding LTspice uses

### Text Rendering Problems

**Problem**: 
Text appears incorrectly positioned or styled in the SVG output

**Solution**: 
- Try adjusting the font size with `--base-font-size`
- Change the font family with `--font-family`
- Use `--no-text` to confirm if the issue is text-related
- Check if the schematic has very small or very large text elements

### Viewbox Issues

**Problem**: 
Parts of the circuit are cut off in the SVG output

**Solution**:
- Increase the margin with `--margin 15.0` or higher
- Check if your schematic has elements very far from the main circuit

## Debugging

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

## Getting Help

If the solutions above don't resolve your issue:

1. Check if there's an existing issue on GitHub that matches your problem
2. Open a new issue with:
   - A detailed description of the problem
   - The command you used
   - The error message (if any)
   - The LTspice file (if possible)
   - The version of the tool you're using 