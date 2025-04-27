# Component Relationships

This document provides a visual overview of how the different components in the LTspice to SVG converter relate to each other.

## High-Level Component Diagram

```
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
```

## Detailed Component Relationships

### Parser Layer

```
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
```

### Renderer Layer

```
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
```

## Data Flow Diagram

```
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
```

## Configuration Flow

```
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
```

## Symbol Resolution Process

```
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
```

## Rendering Configuration Hierarchy

```
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
```

## ViewBox Calculation Process

```
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
```

## Inheritance and Class Relationships

```
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
```

These diagrams provide a visual representation of the component relationships in the LTspice to SVG converter. The modular architecture allows for clear separation of concerns, making the codebase maintainable and extensible. 