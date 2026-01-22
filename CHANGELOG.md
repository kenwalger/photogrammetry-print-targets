# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Multi-Page PDF Support**: Automatic pagination for large marker sets
  - Automatically splits markers across multiple pages when they don't fit on one page
  - Uses standard page sizes (US Letter or A4) with automatic layout calculation
  - Each page includes calibration reference
  - Supports generating hundreds of markers across multiple pages
- **Starting Number Option**: Custom numbering ranges for markers
  - `--start-number` CLI option to set starting marker number
  - Useful for generating different ranges (e.g., markers 100-120)
  - Applies to both PDF labels and SVG file naming
- **Page Size Selection**: Configurable page sizes
  - `--page-size {letter,a4}` option for US Letter (215.9x279.4mm) or A4 (210x297mm)
  - Automatically calculates how many markers fit per page
  - Defaults to US Letter for compatibility
- **Rotationally Invariant Codes**: Professional-grade code generation for photogrammetry
  - Industry-standard lookup tables for 8-bit, 12-bit, and 14-bit targets (lazy initialization)
  - Algorithmic generation for other bit counts (4-16 bits)
  - Canonical rotation ensures markers are identified correctly regardless of orientation
  - Replaces placeholder sequential code generator with production-ready implementation
  - Performance optimization: codes generated on-demand to avoid import-time delays
- **Comprehensive Test Suite**: Full test coverage for all major components
  - Unit tests for validation functions (`test_validation.py`) - 18 tests
  - Unit tests for code generation (`test_code_generation.py`) - 10 tests
  - Unit tests for marker geometry (`test_geometry.py`) - 12 tests
  - Integration tests for rendering functions (`test_rendering.py`) - 12 tests
  - Integration tests for CLI interface (`test_cli.py`) - 11 tests
  - pytest configuration with 80% coverage target
  - **Test Results**: 64 tests passing, 99.34% code coverage, 1.56s execution time
- **CLI Interface**: Full command-line argument parsing for all configuration parameters
  - `--dot-radius`, `--bits`, `--columns`, `--markers` for marker configuration
  - `--start-number` for custom marker numbering ranges
  - `--margin`, `--padding`, `--dpi` for layout configuration
  - `--page-size {letter,a4}` for page size selection
  - `--cal-dot-radius`, `--cal-spacing`, `--cal-label` for calibration feature
  - `--output-pdf`, `--output-dir` for output configuration
  - `--skip-svgs`, `--skip-pdf` for selective output generation
- **Input Validation**: Comprehensive validation of configuration parameters
  - Parameter range checking (bits: 4-16, positive values, etc.)
  - Code limit validation (marker count vs available codes)
  - Overlap detection with warning messages
- **Code Organization**: Improved structure and maintainability
  - Execution guard (`if __name__ == "__main__":`) for importability
  - Refactored duplicate marker rendering logic into reusable `render_marker_to_axes()` function
  - Separated concerns: `generate_combined_pdf()` and `generate_individual_svgs()` functions
  - Extracted all magic numbers to named constants with documentation
- **Documentation**: Enhanced documentation
  - Updated README.md with CLI usage examples and feature descriptions
  - Updated ROADMAP.md to reflect completed Phase 2 items
  - Added CHANGELOG.md for change tracking

### Changed
- **PDF Generation**: `generate_combined_pdf()` now supports multi-page output using `PdfPages`
  - Automatically calculates page capacity based on page size and marker dimensions
  - Splits markers across pages when they exceed single-page capacity
  - Each page maintains proper layout with calibration reference
- **Marker Rendering**: `render_marker_to_axes()` now accepts `start_number` parameter for custom numbering
- **SVG Generation**: `generate_individual_svgs()` now accepts `start_number` parameter for file naming
- **Function Signatures**: `draw_calibration_feature()` now accepts calibration parameters as arguments instead of using global constants
- **Code Structure**: All execution logic moved into `main()` function, making the module importable
- **Constants Organization**: Grouped constants into logical sections (Geometric, Default Configuration)
- **Default Padding**: Increased default marker padding from 5.0mm to 7.5mm for better spacing

### Fixed
- **Code Duplication**: Eliminated duplicate marker rendering code between PDF and SVG generation
- **Magic Numbers**: Replaced all hardcoded multipliers and offsets with named constants
  - Ring geometry: `RING_INNER_MULTIPLIER`, `RING_OUTER_MULTIPLIER`
  - Marker sizing: `MARKER_SIZE_MULTIPLIER`
  - Label positioning: `LABEL_OFFSET_X_MULTIPLIER`, `LABEL_OFFSET_Y_MULTIPLIER`
  - Calibration positioning: `CAL_LABEL_OFFSET_MULTIPLIER`, `CAL_POSITION_Y_MULTIPLIER`
- **stderr Reference**: Fixed inconsistent stderr reference (`os.sys.stderr` -> `sys.stderr`)

### Technical Details
- All functions are now pure and testable (no side effects from module-level execution)
- Type hints maintained throughout
- Backward compatible: default behavior unchanged when run without arguments
- Error handling: Validation errors exit with appropriate error codes and messages
- Warning system: Overlap detection provides helpful guidance without failing

## [1.0.0] - Initial Release

### Added
- Mathematically precise coded targets using circular arc (Wedge) geometry
- 8-bit coded ring system
- 6 mm solid center dots
- Sheet-level calibration reference (20.00 mm)
- Combined PDF output
- Individual SVG file generation
- Millimeter-based geometry throughout
- Print verification documentation
