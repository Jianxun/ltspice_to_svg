Parser Architecture
==================

The parsing system in LTspice to SVG is designed to handle the specific file formats used by LTspice: schematic files (.asc) and symbol files (.asy). The parsing subsystem is modular and follows a clean separation of concerns.

Parser Hierarchy
---------------

.. code-block:: none

                        +-------------------+
                        |                   |
                        |  Schematic Parser |
                        |                   |
                        +--------+----------+
                                 |
                                 | Coordinates parsing of
                                 v
         +-------------------+   |   +-------------------+   +-------------------+
         |                   |   |   |                   |   |                   |
         |  ASC Parser       |<--+-->|  ASY Parser       |-->|  Shape Parser     |
         |  (Schematics)     |       |  (Symbols)        |   |  (Geometry)       |
         |                   |       |                   |   |                   |
         +-------------------+       +-------------------+   +-------------------+

Schematic Parser (``schematic_parser.py``)
----------------------------------------

The Schematic Parser is the main entry point for parsing LTspice files. It coordinates the overall parsing process and delegates to specialized parsers.

Key Responsibilities:
~~~~~~~~~~~~~~~~~~~~

* Orchestrate the parsing process
* Manage file loading and encoding detection
* Coordinate between ASC and ASY parsers
* Create and populate the internal data structures
* Export parsed data for debugging (JSON)

ASC Parser (``asc_parser.py``)
----------------------------

The ASC Parser is specialized for parsing LTspice schematic files (.asc).

Key Responsibilities:
~~~~~~~~~~~~~~~~~~~~

* Parse schematic file (.asc) content
* Extract wires, components, symbols, and text elements
* Process component instances
* Handle flag and IO pin definitions
* Extract net labels and connections

File Format:
~~~~~~~~~~~

LTspice schematic files follow a text-based format with specific line types:

* ``WIRE``: Wire definition with coordinates
* ``SYMBOL``: Component instance with symbol reference
* ``TEXT``: Text element with coordinates and content
* ``FLAG``: Net label or connection point
* ``IOPIN``: Input/output pin definition
* ``WINDOW``: Text positioning and styling

Example ASC content:

.. code-block:: none

    SHEET 1 880 680
    WIRE 128 176 80 176
    WIRE 288 176 192 176
    SYMBOL res 208 160 R90
    WINDOW 0 0 56 VBottom 2
    WINDOW 3 32 56 VTop 2
    SYMATTR InstName R1
    SYMATTR Value 1k
    TEXT -24 248 Left 2 !.tran 1

ASY Parser (``asy_parser.py``)
----------------------------

The ASY Parser is specialized for parsing LTspice symbol files (.asy).

Key Responsibilities:
~~~~~~~~~~~~~~~~~~~~

* Parse symbol definition files (.asy)
* Extract symbol shapes (lines, rectangles, circles)
* Handle pin definitions and connection points
* Process default text positions (WINDOW)
* Extract attributes like PREFIX

File Format:
~~~~~~~~~~~

LTspice symbol files also follow a text-based format:

* ``LINE``: Line shape with coordinates
* ``RECTANGLE``: Rectangle shape with coordinates
* ``CIRCLE``: Circle shape with center and radius
* ``PIN``: Pin definition with coordinates and direction
* ``WINDOW``: Default text positioning for component name/value
* ``SYMATTR``: Symbol attribute like PREFIX

Example ASY content:

.. code-block:: none

    Version 4
    SymbolType CELL
    LINE Normal 0 96 0 88
    LINE Normal 0 16 0 24
    LINE Normal 16 80 -16 64
    LINE Normal 16 48 16 80
    RECTANGLE Normal 16 88 -16 24
    WINDOW 0 8 0 Left 2
    WINDOW 3 8 112 Left 2
    SYMATTR Prefix R
    SYMATTR Description Resistor
    PIN 0 16 NONE 0
    PIN 0 96 NONE 0

Shape Parser (``shape_parser.py``)
--------------------------------

The Shape Parser handles geometric shapes found in both ASC and ASY files.

Key Responsibilities:
~~~~~~~~~~~~~~~~~~~~

* Parse shape elements (lines, rectangles, circles)
* Handle coordinates and dimensions
* Process style attributes (line width, fill)
* Extract transformations (rotation, mirroring)

File Encoding Handling
---------------------

LTspice files typically use UTF-16LE encoding. The parser system includes built-in handling for:

* Auto-detection of file encoding
* Fallback strategies for different encoding formats
* Conversion to consistent internal representation
* Tools to fix encoding issues (``fix_encoding.py``)

Parsing Process
-------------

1. **File Loading**:
   - Load the schematic file
   - Detect and handle encoding
   - Read content line by line

2. **Schematic Parsing**:
   - Identify line types (WIRE, SYMBOL, etc.)
   - Parse each line according to its type
   - Build internal data structures

3. **Symbol Resolution**:
   - For each SYMBOL found in schematic:
     - Look for corresponding .asy file
     - Parse symbol definition
     - Store in symbol library

4. **Geometric Shape Extraction**:
   - Extract all shapes from schematic and symbols
   - Process coordinates and transformations
   - Create internal shape representations

5. **Output**:
   - Create a structured representation of all elements
   - Organize data for rendering system
   - Optionally export data as JSON for debugging

Internal Data Structures
----------------------

The parsing system creates a hierarchical data structure:

* Schematic: Top-level container
  * Wires: List of wire definitions with coordinates
  * Symbols: List of component instances with:
    * Symbol name
    * Position
    * Transformation (rotation, mirroring)
    * Attributes (name, value)
  * Texts: List of text elements with:
    * Content
    * Position
    * Style
  * Flags: List of net labels and connection points
  * IO Pins: List of input/output pin definitions

Example Usage
-----------

.. code-block:: python

    from src.parsers.schematic_parser import SchematicParser
    
    # Create parser instance
    parser = SchematicParser("path/to/schematic.asc")
    
    # Parse the schematic and related symbols
    data = parser.parse()
    
    # Access the parsed data
    schematic = data['schematic']
    symbols = data['symbols']
    
    # Export as JSON for debugging
    parser.export_json("output.json") 