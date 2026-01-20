# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **CLI Interface**: Full command-line argument parsing for all configuration parameters
  - `--dot-radius`, `--bits`, `--columns`, `--markers` for marker configuration
  - `--margin`, `--padding`, `--dpi` for layout configuration
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
- **Function Signatures**: `draw_calibration_feature()` now accepts calibration parameters as arguments instead of using global constants
- **Code Structure**: All execution logic moved into `main()` function, making the module importable
- **Constants Organization**: Grouped constants into logical sections (Geometric, Default Configuration)

### Fixed
- **Code Duplication**: Eliminated duplicate marker rendering code between PDF and SVG generation
- **Magic Numbers**: Replaced all hardcoded multipliers and offsets with named constants
  - Ring geometry: `RING_INNER_MULTIPLIER`, `RING_OUTER_MULTIPLIER`
  - Marker sizing: `MARKER_SIZE_MULTIPLIER`
  - Label positioning: `LABEL_OFFSET_X_MULTIPLIER`, `LABEL_OFFSET_Y_MULTIPLIER`
  - Calibration positioning: `CAL_LABEL_OFFSET_MULTIPLIER`, `CAL_POSITION_Y_MULTIPLIER`

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
