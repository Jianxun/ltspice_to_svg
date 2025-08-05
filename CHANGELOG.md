# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-01-05

### Added
- **CLI Version Command**: Added `--version` flag to display version information
- **SVG Metadata Enhancement**: Added semantic symbol metadata with custom namespace
  - Custom namespace: `xmlns:s="https://github.com/nturley/netlistsvg"`
  - Symbol type attributes: `s:type="NMOS"`, `s:type="Voltage"`, etc.
  - Symbol dimension attributes: `s:width="64"`, `s:height="128"`
- **Pretty SVG Formatting**: SVG files now include proper indentation for readability
- **Comprehensive Symbol Orientation Testing**: Added test coverage for all 8 orientations (R0, R90, R180, R270, M0, M90, M180, M270)
- **NetlistSVG Compatibility Analysis**: Added documentation for future netlistsvg integration

### Fixed
- **Critical Symbol Rotation Bug**: Fixed incorrect transformation order for mirrored symbols (M90, M270)
  - Now correctly applies mirror first (`scale(-1,1)`), then rotation (`rotate(angle)`)
  - Previous implementation incorrectly rotated first, then mirrored
- **Window Text Rotation Issues**: Fixed text rendering in rotated symbols (R180, R270)
  - Added rotation compensation logic to keep text readable
  - Implemented justification swapping (Left ↔ Right, VTop ↔ VBottom)
  - Applied 180° counter-rotation for affected orientations
- **ViewBox Calculation**: Fixed missing symbols in viewbox bounds calculation
  - Symbols were previously excluded causing elements to appear off-canvas
  - Added `_include_symbols()` method to ViewboxCalculator

### Changed
- **Development Status**: Upgraded from Alpha to Beta status
- **Symbol Renderer Enhancement**: Enhanced `begin_symbol()` method to accept symbol metadata
- **Test Improvements**: Updated test4_symbols to validate all orientation combinations


### Technical Details
- Enhanced `SymbolRenderer.set_transformation()` with correct LTspice transformation order
- Added `TextRenderer` support for additional rotation compensation
- Improved `ViewboxCalculator` to include all positioned elements
- Disabled svgwrite validation for custom attributes compatibility
- Added symbol dimension calculation from actual shape bounds

## [0.1.1] - 2025-05-09

### Added
- Initial release with basic LTspice to SVG conversion
- Support for schematics (.asc) and symbols (.asy)
- Command-line interface with rendering options
- PyPI package distribution
- Basic symbol rendering and text handling

### Features
- Wire and T-junction rendering
- Symbol placement and orientation (partial)
- Text element rendering
- Flag rendering (ground, net labels, I/O pins)
- Configurable stroke width, font size, and margins
- JSON export for debugging

---

**Legend:**
- **Added**: New features
- **Changed**: Changes in existing functionality  
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Vulnerability fixes