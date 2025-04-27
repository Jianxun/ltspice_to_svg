Architecture Overview
====================

System Design
------------

The LTspice to SVG converter is a Python-based tool that converts LTspice schematic files (.asc) to SVG format. The system follows a modular architecture with clear separation of concerns between parsing and rendering components.

Core Components
~~~~~~~~~~~~~~

.. image:: ../_static/architecture_overview.png
   :alt: Architecture Overview Diagram
   :align: center

1. **Main Module** (``ltspice_to_svg.py``)
    * Entry point for the application
    * Handles command-line arguments and configuration
    * Coordinates the parsing and rendering process

2. **Parsers** (``src/parsers/``)
    * ``schematic_parser.py``: Main parser that coordinates the parsing process
    * ``asc_parser.py``: Parses LTspice schematic files (.asc)
    * ``asy_parser.py``: Parses LTspice symbol files (.asy)
    * ``shape_parser.py``: Handles parsing of geometric shapes

3. **Renderers** (``src/renderers/``)
    * ``svg_renderer.py``: Main renderer that coordinates the SVG generation
    * ``symbol_renderer.py``: Renders schematic symbols
    * ``text_renderer.py``: Handles text rendering
    * ``wire_renderer.py``: Renders wires and connections
    * ``shape_renderer.py``: Renders geometric shapes
    * ``flag_renderer.py``: Renders schematic flags and annotations
    * ``base_renderer.py``: Base class for all renderers

Data Flow
~~~~~~~~

.. image:: ../_static/data_flow.png
   :alt: Data Flow Diagram
   :align: center

1. **Input Processing**
    * LTspice schematic file (.asc) is read
    * Symbol files (.asy) are loaded as needed
    * Text encoding is handled appropriately (UTF-16LE)

2. **Parsing**
    * Schematic elements are parsed into an intermediate representation
    * Symbols are parsed and stored in a symbol library
    * Geometric shapes and text are extracted

3. **Rendering**
    * SVG document is created
    * Elements are rendered in appropriate order:
        1. Wires and connections
        2. Symbols
        3. Text
        4. Shapes
        5. Flags and annotations

Configuration
------------

The system supports various configuration options:

.. code-block:: python

    # Example configuration through RenderingConfig
    config = RenderingConfig(
        stroke_width=2.0,               # Line thickness
        dot_size_multiplier=1.5,        # Size of junction dots 
        base_font_size=16.0,            # Base font size
        viewbox_margin=10.0,            # Margin around the schematic as percentage
        font_family="Arial",            # Font family for text elements
        no_schematic_comment=False,     # Skip rendering schematic comments
        no_spice_directive=False,       # Skip rendering SPICE directives
        no_nested_symbol_text=False,    # Skip rendering text inside symbols
        no_component_name=False,        # Skip rendering component names
        no_component_value=False,       # Skip rendering component values
        no_net_label=False,             # Skip rendering net label flags
        no_pin_name=False               # Skip rendering I/O pin text
    )

Key Parameters:

* ``stroke_width``: Line thickness
* ``dot_size_multiplier``: Size of junction dots 
* ``base_font_size``: Base font size
* ``viewbox_margin``: Margin around the schematic as percentage
* ``font_family``: Font family for text elements
* Text rendering options to selectively turn off certain text elements
* Debug features (``export_json``) for troubleshooting

Error Handling
-------------

The system includes robust error handling:

* File encoding issues are handled gracefully
* Missing symbol files are reported with clear error messages
* Invalid schematic elements are logged for troubleshooting
* SVG rendering errors are caught and reported with context

Coordinate System
----------------

.. image:: ../_static/coordinate_system.png
   :alt: Coordinate System Diagram
   :align: center

* LTspice uses a coordinate system where:
    * Origin is at the center of the schematic
    * Y-axis points upward
    * Units are in LTspice grid points
* SVG coordinates are transformed as needed
* Viewbox is automatically calculated to fit all elements with configurable margin

Symbol Transformations
---------------------

LTspice symbols can be rotated and mirrored. The converter handles these transformations:

**Rotation Types**

* R0: No rotation
* R90: 90 degrees clockwise
* R180: 180 degrees
* R270: 270 degrees clockwise

**Mirroring**

* M0: Mirror across Y-axis, no rotation
* M90: Mirror across Y-axis, then rotate 90 degrees
* M180: Mirror across Y-axis, then rotate 180 degrees
* M270: Mirror across Y-axis, then rotate 270 degrees

Text Handling
------------

The converter includes sophisticated text handling capabilities:

**Font Sizes**

Font sizes are determined by a multiplier index (0-7):

* 0: 0.625x base size
* 1: 1.0x base size
* 2: 1.5x base size (default)
* 3: 2.0x base size
* 4: 2.5x base size
* 5: 3.5x base size
* 6: 5.0x base size
* 7: 7.0x base size

**Text Alignment Options**

* Left: Left-aligned, vertically centered
* Center: Horizontally and vertically centered
* Right: Right-aligned, vertically centered
* Top: Top-aligned, horizontally centered
* Bottom: Bottom-aligned, horizontally centered
* VTop: Vertically oriented, top-aligned
* VBottom: Vertically oriented, bottom-aligned

WINDOW Line Handling
-------------------

**In Symbol Files (.asy)**

* Define default text rendering rules for component attributes
* WINDOW 0: Default position/style for component name (e.g., "R1", "M1")
* WINDOW 3: Default position/style for component value (e.g., "1k", "10u")
* Part of symbol's template/definition

**In Schematic Files (.asc)**

* Follow SYMBOL lines to override default text rendering
* Customize text position/style for specific component instances
* If no override provided, use defaults from symbol definition

**Format**

.. code-block:: none

    WINDOW <type> <x> <y> <justification> [size_multiplier]

* ``type``: 0 (name) or 3 (value)
* ``x, y``: Relative coordinates from symbol origin
* ``justification``: Text alignment (Left, Right, Center, Top, Bottom, VTop, VBottom)
* ``size_multiplier``: Optional font size index (0-7)

T-Junction Detection
------------------

The system automatically detects and represents T-junctions:

* Identifies points where 3 or more wires meet
* Excludes symbol terminal points
* Verifies wire directions to avoid false positives
* Adds dots with size relative to stroke width 