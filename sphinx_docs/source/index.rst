.. LTspice to SVG Converter documentation master file, created by
   sphinx-quickstart on Sat Apr 26 21:57:05 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

LTspice to SVG Converter
=======================

A tool to convert LTspice circuit schematics (.asc) and symbols (.asy) into SVG format.

Features
--------

* Converts LTspice schematics (.asc) to SVG format
* Converts LTspice symbol files (.asy) to SVG format
* Handles symbol transformations (rotation, mirroring)
* Configurable rendering options (stroke width, font size, etc.)
* Control over text rendering (component names, values, etc.)
* Supports UTF-16LE encoding used by LTspice
* Generates professional-looking, publication-ready circuit diagrams

.. toctree::
   :maxdepth: 2
   :caption: User Guide:

   user_guide/installation
   user_guide/basic_usage
   user_guide/command_line_options
   user_guide/tutorials
   user_guide/troubleshooting

.. toctree::
   :maxdepth: 2
   :caption: Architecture:

   architecture/overview
   architecture/component_relationships
   architecture/parsers
   architecture/renderers
   architecture/configuration

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   api/main
   api/parsers
   api/renderers
   api/utils

.. toctree::
   :maxdepth: 2
   :caption: Development:

   development/setup
   development/contributing
   development/testing
   development/releasing

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

