Testing Strategy
===============

This document outlines the testing strategy and coverage for the LTspice to SVG converter.

Test Structure
-------------

The test suite is organized into several categories:

.. code-block:: none

    tests/
    ├── unit_tests/                # Unit tests for individual components
    │   ├── test_rendering_config.py
    │   ├── test_viewbox_calculator.py
    │   ├── test_flag_renderer/
    │   ├── test_shape_renderer/
    │   ├── test_symbol_renderer/
    │   ├── test_text_renderers/
    │   └── test_wire_renderer/
    │
    └── integration/              # Integration and end-to-end tests
        ├── test_ltspice_to_svg/
        └── test_svg_renderer/

Test Categories
--------------

Unit Tests
~~~~~~~~~~

Unit tests focus on testing individual components in isolation, verifying that each component works correctly on its own.

**RenderingConfig Tests**

Tests for the configuration object that controls rendering options:

* Option validation
* Default values
* Option getters and setters
* Configuration inheritance

**ViewboxCalculator Tests**

Tests for the component that calculates the SVG viewbox:

* Bounds calculation
* Margin application
* Coordinate transformation
* Edge case handling (empty input, single point, etc.)

**Flag Renderer Tests**

Tests for the flag renderer component:

* Ground flag rendering
* Net label flag rendering
* IO pin rendering
* Flag orientation and positioning

**Shape Renderer Tests**

Tests for shape rendering:

* Line rendering
* Rectangle rendering
* Circle rendering
* Arc rendering
* Coordinate transformations

**Symbol Renderer Tests**

Tests for symbol rendering:

* Symbol definition parsing
* Symbol instance rendering
* Rotation and mirroring
* Component attributes

**Text Renderer Tests**

Tests for text rendering:

* Text positioning
* Alignment options
* Font size calculations
* Text rotation and mirroring

**Wire Renderer Tests**

Tests for wire rendering:

* Wire connections
* Line style options
* Junction detection
* T-junction handling

Integration Tests
~~~~~~~~~~~~~~~~

Integration tests verify that components work correctly together and that end-to-end processing flows function properly.

**LTspice to SVG Tests**

End-to-end tests that exercise the main conversion pipeline:

* Command-line argument handling
* File loading and parsing
* SVG generation
* File output

**SVG Renderer Tests**

Integration tests for the SVG renderer:

* Complete schematic rendering
* Symbol library interaction
* Text and shape coordination
* Viewbox calculation

Test Fixtures and Helpers
------------------------

The test suite includes several fixtures and helper functions to facilitate testing:

**Cleanup Fixture**

A pytest fixture that cleans up test result directories:

.. code-block:: python

    @pytest.fixture(autouse=True, scope="session")
    def cleanup_results_dirs():
        """Clean up all results directories before running tests."""
        results_dirs = get_results_dirs()
        for results_dir in results_dirs:
            if os.path.exists(results_dir):
                shutil.rmtree(results_dir)
            os.makedirs(results_dir)
        yield

**Mock File Objects**

Fixtures to mock file I/O operations:

* Mock symbol files
* Mock schematic files
* Mock configuration files

Test Data Management
------------------

Test data organization:

* Input files (.asc, .asy) stored with test modules
* Expected output stored in reference files
* Results stored in `results` directories
* Comparison between expected and actual results

Test Execution
-------------

Running Tests
~~~~~~~~~~~~

.. code-block:: bash

    # Run all tests
    python -m pytest tests/

    # Run only unit tests
    python -m pytest tests/unit_tests/

    # Run only integration tests
    python -m pytest tests/integration/

    # Run tests with coverage report
    python -m pytest --cov=src tests/

    # Run tests for specific component
    python -m pytest tests/unit_tests/test_flag_renderer/

Continuous Integration
--------------------

The project uses continuous integration to ensure code quality:

* Automated test runs on each commit
* Code coverage reporting
* Integration with GitHub Actions
* Status badges for build and coverage

Test Coverage Strategy
--------------------

The testing approach aims to achieve comprehensive coverage:

* Unit tests for each component function
* Integration tests for component interactions
* Full end-to-end tests for main workflows
* Testing of error conditions and edge cases
* Performance testing for large schematics

Visual Testing
-----------

For visual components, testing includes:

* SVG output verification
* Element positioning checks
* Style application validation
* Pixel-perfect comparison of SVG outputs

Future Test Improvements
---------------------

Planned enhancements to testing:

* Automated visual regression testing
* Performance benchmarking
* Fuzz testing for robustness
* More extensive edge case coverage
* Improved mocking for faster test execution 