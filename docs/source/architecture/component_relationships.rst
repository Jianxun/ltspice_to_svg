Component Relationships
=====================

This document provides a visual overview of how the different components in the LTspice to SVG converter relate to each other.

High-Level Component Diagram
---------------------------

.. code-block:: none

    +-------------------+     +-------------------+     +-------------------+
    |                   |     |                   |     |                   |
    |  Command Line     |     |  RenderingConfig  |     |  File System      |
    |  Interface        +---->|  (Configuration)  |     |  Access           |
    |                   |     |                   |     |                   |
    +--------+----------+     +---------+---------+     +--------+----------+
             |                          |                        |
             v                          v                        v
    +-------------------+     +-------------------+     +-------------------+
    |                   |     |                   |     |                   |
    |  LTspice_to_SVG   +---->|  SVG Generator   |     |  Symbol Library   |
    |  (Main Module)    |     |  (Coordinator)   +---->|  (Symbol Storage) |
    |                   |     |                   |     |                   |
    +--------+----------+     +---------+---------+     +-------------------+
             |                          |
             |                          |
             v                          v
    +-------------------+     +-------------------+
    |                   |     |                   |
    |  Parsers          |     |  Renderers        |
    |  (Data Extraction)|     |  (SVG Generation) |
    |                   |     |                   |
    +--------+----------+     +---------+---------+
             |                          |
             v                          v
    +-------------------+     +-------------------+
    |  - ASC Parser     |     |  - SVG Renderer   |
    |  - ASY Parser     |     |  - Wire Renderer  |
    |  - Shape Parser   |     |  - Text Renderer  |
    |                   |     |  - Flag Renderer  |
    +-------------------+     +-------------------+

Detailed Component Relationships
-------------------------------

Parser Layer
~~~~~~~~~~~

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

The Parser Layer consists of specialized parsers for different file types and content:

* **Schematic Parser**: Coordinates the overall parsing process
* **ASC Parser**: Handles LTspice schematic (.asc) files
* **ASY Parser**: Handles LTspice symbol (.asy) files
* **Shape Parser**: Processes geometric shapes from both file types

Renderer Layer
~~~~~~~~~~~~~

.. code-block:: none

                       +-------------------+
                       |                   |
                       |  SVG Renderer     |
                       |  (Base Renderer)  |
                       +--------+----------+
                                |
                                | Delegates to specialized renderers
                                v
        +-------------------+   |   +-------------------+   +-------------------+
        |                   |   |   |                   |   |                   |
        |  Symbol Renderer  |<--+-->|  Wire Renderer    |<--+-->  Text Renderer |
        |                   |   |   |                   |   |   |               |
        +-------------------+   |   +-------------------+   |   +---------------+
                                |                           |
        +-------------------+   |   +-------------------+   |
        |                   |   |   |                   |   |
        |  Shape Renderer   |<--+-->|  Flag Renderer    |<--+
        |                   |       |                   |
        +-------------------+       +-------------------+

The Renderer Layer consists of specialized renderers for different content types:

* **SVG Renderer**: Main coordinator for rendering process
* **Symbol Renderer**: Renders symbol components
* **Wire Renderer**: Renders wires and connections
* **Text Renderer**: Handles text elements
* **Shape Renderer**: Renders geometric shapes
* **Flag Renderer**: Renders flags and annotations

Data Flow Diagram
---------------

.. code-block:: none

     +-------------+     +--------------+     +----------------+     +---------------+
     |             |     |              |     |                |     |               |
     | LTspice ASC +---->| ASC Parser   +---->| Internal Data  +---->| SVG Renderer  |
     | File        |     |              |     | Structure      |     |               |
     |             |     |              |     |                |     |               |
     +-------------+     +--------------+     +----------------+     +------+--------+
                                |                                           |
                                v                                           v
     +-------------+     +--------------+                           +---------------+
     |             |     |              |                           |               |
     | LTspice ASY +---->| ASY Parser   |                          | SVG Output    |
     | Files       |     |              |                          | File          |
     |             |     |              |                          |               |
     +-------------+     +--------------+                          +---------------+

The data flows through the system in a structured manner:

1. Input files (.asc and .asy) are read
2. Parsers extract structured data
3. Data is processed into internal representation
4. Renderers generate SVG output

Configuration Flow
----------------

.. code-block:: none

                     +-------------------+
                     |                   |
                     | Command Line Args |
                     |                   |
                     +--------+----------+
                              |
                              v
     +-------------------+    |    +-------------------+
     |                   |    |    |                   |
     | Default           +----+--->| RenderingConfig   |
     | Configuration     |         | Object            |
     |                   |         |                   |
     +-------------------+         +--------+----------+
                                            |
                                            | Consumed by
                                            v
     +-------------------+    +-------------------+    +-------------------+
     |                   |    |                   |    |                   |
     | SVG Renderer      |<---+ ViewboxCalculator |<---+ Symbol Renderer   |
     |                   |    |                   |    |                   |
     +-------------------+    +-------------------+    +-------------------+
            ^                                                  ^
            |                                                  |
            |     +-------------------+    +-------------------+
            |     |                   |    |                   |
            +-----+ Text Renderer     |    | Flag Renderer     +----+
                  |                   |<---+                   |
                  +-------------------+    +-------------------+

The configuration system provides a central way to customize the rendering process:

1. Command line arguments are processed
2. Default configuration is applied where not specified
3. RenderingConfig object is created
4. Configuration is consumed by all renderers

Symbol Resolution Process
-----------------------

.. code-block:: none

     +-------------+     +--------------+     +----------------+     +---------------+
     |             |     |              |     | Symbol Library |     |               |
     | Component   +---->| Find Symbol  +---->| Search Paths:  +---->| Symbol        |
     | in Schematic|     | by Name      |     | 1. Local Dir   |     | Definition    |
     |             |     |              |     | 2. LTSPICE_LIB |     | (.asy file)   |
     +-------------+     +--------------+     | 3. --ltspice-lib     +------+--------+
                                              +----------------+            |
                                                                            v
                                                                     +---------------+
                                                                     |               |
                                                                     | Render Symbol |
                                                                     | with proper   |
                                                                     | transformation|
                                                                     +---------------+

Symbol resolution follows a systematic process:

1. Component reference is found in schematic
2. Symbol name is extracted
3. Symbol definition is searched in several locations
4. Symbol definition is parsed
5. Symbol is rendered with appropriate transformation

Rendering Configuration Hierarchy
-------------------------------

.. code-block:: none

     +------------------+
     |                  |
     | RenderingConfig  | (Central configuration store)
     |                  |
     +--------+---------+
              |
              | Configures
              v
     +------------------+
     |                  |
     | BaseRenderer     | (Common rendering functionality)
     |                  |
     +--------+---------+
              |
              | Inherited by
              v
    +-------------------+        +-------------------+
    |                   |        |                   |
    | SVGRenderer       +-------->TextRenderer       |
    | (Main coordinator)|        |(Text handling)    |
    |                   |        |                   |
    +--------+----------+        +-------------------+
             |
             | Uses
             v
    +-------------------+        +-------------------+
    |                   |        |                   |
    | SymbolRenderer    +-------->FlagRenderer       |
    | (Symbol handling) |        |(Flag handling)    |
    |                   |        |                   |
    +-------------------+        +-------------------+

The rendering configuration follows a hierarchical structure:

1. RenderingConfig object stores all configuration parameters
2. BaseRenderer provides common functionality with configuration
3. Specialized renderers inherit from BaseRenderer
4. SVGRenderer coordinates other renderers

ViewBox Calculation Process
-------------------------

.. code-block:: none

     +-------------+     +--------------+     +----------------+     +---------------+
     |             |     |              |     |                |     |               |
     | Parsed      +---->| ViewBox      +---->| Apply Margin   +---->| Final SVG     |
     | Elements    |     | Calculator   |     | from Config    |     | ViewBox       |
     |             |     |              |     |                |     |               |
     +------+------+     +--------------+     +----------------+     +---------------+
            |
            | Types of Elements
            v
     +-------------+     +--------------+     +----------------+
     | - Wires     |     | - Symbols    |     | - Text Elements|
     | - Junctions |     | - Components |     | - Flags        |
     | - IO Pins   |     | - Shapes     |     | - Net Labels   |
     +-------------+     +--------------+     +----------------+

The ViewBox calculation process ensures all elements fit within the SVG:

1. All parsed elements are collected
2. Bounds are calculated for each element
3. Overall bounds are determined
4. Margin is applied based on configuration
5. Final SVG viewBox is established

Inheritance and Class Relationships
---------------------------------

.. code-block:: none

                       BaseRenderer
                             |
                             | Inherits
                             v
                +-------------------------+
                |                         |
       SVGRenderer                  TextRenderer
                |                         |
                | Uses                    | Used by
                v                         |
       +------------------+               |
       |                  |               |
       | SymbolRenderer   |               |
       +------------------+               |
                |                         |
                | Uses                    |
                v                         |
       +------------------+               |
       |                  |               |
       | FlagRenderer     +---------------+
       +------------------+

The class inheritance structure provides a clean separation of concerns:

* **BaseRenderer**: Provides common functionality for all renderers
* **SVGRenderer**: Coordinates the overall rendering process
* **TextRenderer**: Specialized for text handling
* **SymbolRenderer**: Specialized for symbol rendering
* **FlagRenderer**: Specialized for flag rendering

These diagrams provide a visual representation of the component relationships in the LTspice to SVG converter. The modular architecture allows for clear separation of concerns, making the codebase maintainable and extensible. 