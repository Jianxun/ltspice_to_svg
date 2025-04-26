# API Documentation

## Main Module

### `convert_schematic(asc_file, stroke_width=3.0, dot_size_multiplier=1.5, scale=1.0, font_size=16.0, export_json=False, no_text=False)`

Converts an LTspice schematic to SVG format.

#### Parameters:
- `asc_file` (str): Path to the .asc schematic file
- `stroke_width` (float): Width of lines in the SVG (default: 3.0)
- `dot_size_multiplier` (float): Size of junction dots relative to stroke width (default: 1.5)
- `scale` (float): Scale factor for coordinates (default: 1.0)
- `font_size` (float): Font size in pixels (default: 16.0)
- `export_json` (bool): Whether to export intermediate JSON files for debugging (default: False)
- `no_text` (bool): Whether to skip rendering text elements (default: False)

## Parsers

### `SchematicParser`

Main parser class that coordinates the parsing process.

#### Methods:
- `__init__(asc_file)`: Initialize parser with schematic file path
- `parse()`: Parse the schematic and return structured data
- `export_json(output_file)`: Export parsed data to JSON file

### `ASCParser`

Parser for LTspice schematic files (.asc).

#### Methods:
- `parse(file_path)`: Parse the ASC file and return schematic data
- `_parse_line(line)`: Parse a single line from the ASC file
- `_parse_wire(line)`: Parse wire definition
- `_parse_symbol(line)`: Parse symbol definition
- `_parse_text(line)`: Parse text element
- `_parse_shape(line)`: Parse geometric shape

### `ASYParser`

Parser for LTspice symbol files (.asy).

#### Methods:
- `parse(file_path)`: Parse the ASY file and return symbol data
- `_parse_line(line)`: Parse a single line from the ASY file
- `_parse_pin(line)`: Parse pin definition
- `_parse_shape(line)`: Parse symbol shape

## Renderers

### `SVGRenderer`

Main renderer class that coordinates SVG generation.

#### Methods:
- `__init__()`: Initialize the renderer
- `load_schematic(schematic_data, symbol_data)`: Load schematic and symbol data
- `create_drawing(output_file)`: Create SVG drawing
- `set_stroke_width(width)`: Set stroke width for lines
- `set_base_font_size(size)`: Set base font size
- `render_wires(dot_size_multiplier)`: Render wires and connections
- `render_symbols()`: Render schematic symbols
- `render_texts()`: Render text elements
- `render_shapes()`: Render geometric shapes
- `render_flags()`: Render schematic flags
- `save()`: Save the SVG file

### `SymbolRenderer`

Renderer for schematic symbols.

#### Methods:
- `render(symbol_data, position, rotation)`: Render a symbol
- `_render_pin(pin_data)`: Render a pin
- `_render_shape(shape_data)`: Render a symbol shape

### `TextRenderer`

Renderer for text elements.

#### Methods:
- `render(text_data, position, rotation)`: Render text
- `_get_text_style(text_data)`: Get text style properties
- `_get_text_position(text_data)`: Calculate text position

### `WireRenderer`

Renderer for wires and connections.

#### Methods:
- `render(wire_data, dot_size_multiplier)`: Render a wire
- `_render_junction(position, size)`: Render a wire junction

### `ShapeRenderer`

Renderer for geometric shapes.

#### Methods:
- `render(shape_data)`: Render a shape
- `_render_line(shape_data)`: Render a line
- `_render_rectangle(shape_data)`: Render a rectangle
- `_render_circle(shape_data)`: Render a circle
- `_render_arc(shape_data)`: Render an arc

### `FlagRenderer`

Renderer for schematic flags and annotations.

#### Methods:
- `render(flag_data)`: Render a flag
- `_get_flag_style(flag_data)`: Get flag style properties
- `_render_flag_text(flag_data)`: Render flag text 