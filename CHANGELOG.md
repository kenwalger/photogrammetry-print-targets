# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- **AVERY 6450 Alignment**: Fine-tuned label positions based on physical sheet measurements
  - Updated margins: Left 25.00mm, Top 11.70mm (measured from physical sheet)
  - Updated spacing: Horizontal 27.45mm, Vertical 28.65mm (measured from physical sheet)
  - Applied 15.0mm vertical offset for optimal alignment
  - Removed calibration reference from AVERY 6450 output (not needed for label sheet workflow)

### Added
- **AVERY 6450 Label Sheet Support**: Native support for AVERY 6450 round label sheets
  - 7 columns × 9 rows = 63 labels per sheet layout
  - Markers positioned at exact label center coordinates
  - Extracted layout specifications from official AVERY template
  - Set as default output format for improved usability
  - Automatic multi-page support for large marker sets
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
  - `--page-size {letter,a4,avery6450}` option for US Letter (215.9x279.4mm), A4 (210x297mm), or AVERY 6450 label sheets
  - Automatically calculates how many markers fit per page
  - Defaults to AVERY 6450 for improved usability
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
  - `--page-size {letter,a4,avery6450}` for page size selection (default: avery6450)
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
- **Default Output Format**: Changed default page size from US Letter to AVERY 6450 label sheets
  - Improves usability for production workflows using standard label sheets
  - Can still use `--page-size letter` or `--page-size a4` for custom layouts
- **PDF Generation**: `generate_combined_pdf()` now supports multi-page output using `PdfPages`
  - Automatically calculates page capacity based on page size and marker dimensions
  - Splits markers across pages when they exceed single-page capacity
  - Each page maintains proper layout with calibration reference
- **New Function**: Added `generate_avery_6450_pdf()` for AVERY 6450-specific layout
  - Positions markers at exact label center coordinates
  - Handles 63 labels per sheet (7×9 grid)
  - Automatic multi-page support
- **Marker Rendering**: `render_marker_to_axes()` now accepts `start_number` parameter for custom numbering
- **SVG Generation**: `generate_individual_svgs()` now accepts `start_number` parameter for file naming
- **Function Signatures**: `draw_calibration_feature()` now accepts calibration parameters as arguments instead of using global constants
- **Code Structure**: All execution logic moved into `main()` function, making the module importable
- **Constants Organization**: Grouped constants into logical sections (Geometric, Default Configuration, AVERY 6450 specifications)

### Fixed
- **PDF Page Dimensions**: Removed `bbox_inches='tight'` parameter from `pdf.savefig()` call
  - Preserves explicit page size dimensions (US Letter/A4) without unpredictable cropping
  - Ensures multi-page PDFs maintain consistent page sizes across all pages
- **Code Duplication**: Eliminated duplicate page capacity calculation logic
  - Created `calculate_page_capacity()` function to centralize page layout calculations
  - Both `generate_combined_pdf()` and `main()` now use shared function
  - Improves maintainability and ensures consistent calculations
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
