# Photogrammetric Coded Target Generator

This repository contains a small, self-contained Python script for generating
printable photogrammetry targets with a built-in calibration reference.

The output is a **1:1 scale PDF** intended for physical printing and use in
photogrammetric capture workflows.

---

## Features

- Mathematically precise coded targets using circular arc (Wedge) geometry
- **Rotationally invariant codes** - markers can be identified correctly regardless of orientation
- Industry-standard code patterns for 8-bit, 12-bit, and 14-bit targets
- **AVERY 6450 label sheet support** - native support for AVERY 6450 round labels (7×9 grid, 63 labels per sheet)
- **Multi-page PDF support** - automatically splits large marker sets across multiple pages
- **Starting number option** - generate markers with custom numbering ranges
- Configurable page sizes (AVERY 6450 default, US Letter, or A4)
- Configurable bit count (4-16 bits) for coded rings
- 6 mm solid center dots (design-space, configurable)
- Explicit millimeter-based geometry
- Sheet-level calibration reference (20.00 mm, configurable)
- Print-verifiable output (PDF and individual SVGs)
- Command-line interface for full configuration control
- Input validation and overlap detection
- No surface contact or adhesive requirements
- Sub-pixel centroid optimization for high-angle gantry capture

---

## Requirements

- Python 3.9+
- matplotlib>=3.7
- numpy>=1.23
- pytest>=7.4.0 (for testing)
- pytest-cov>=4.1.0 (for test coverage)

Minimal dependencies are intentional. pytest is only needed for development/testing.

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Usage

### Basic Usage

Generate targets with default settings:

```bash
python main.py
```

This creates:
- `coded_markers_6mm.pdf` - Combined PDF with all markers (AVERY 6450 layout by default)
- `targets/target_1.svg` through `targets/target_N.svg` - Individual marker files

**Note**: By default, the script generates output optimized for AVERY 6450 round label sheets (7 columns × 9 rows = 63 labels per sheet). Use `--page-size letter` or `--page-size a4` for custom layouts.

### Command-Line Options

The script supports extensive configuration via command-line arguments:

```bash
python main.py --help
```

**Marker Configuration:**
- `--dot-radius FLOAT` - Radius of center dot in millimeters (default: 3.0)
- `--bits INT` - Number of bits in the coded ring (default: 8, range: 4-16)
- `--columns INT` - Number of markers per row (default: 4)
- `--markers INT` - Total number of markers to generate (default: 12)
- `--start-number INT` - Starting number for marker labels and file naming (default: 1)

**Layout Configuration:**
- `--margin FLOAT` - Page margin in millimeters (default: 10.0)
- `--padding FLOAT` - Padding between markers in millimeters (default: 5.0)
- `--dpi INT` - Print resolution (default: 300, does not affect scale)

**Calibration Feature:**
- `--cal-dot-radius FLOAT` - Calibration dot radius in millimeters (default: 2.0)
- `--cal-spacing FLOAT` - Calibration dot center-to-center spacing in millimeters (default: 20.0)
- `--cal-label STRING` - Calibration reference label text (default: "20.00 mm calibration reference")

**Output Configuration:**
- `--output-pdf STRING` - Output PDF filename (default: "coded_markers_6mm.pdf")
- `--output-dir STRING` - Output directory for individual SVG files (default: "targets")
- `--skip-svgs` - Skip generation of individual SVG files
- `--skip-pdf` - Skip generation of combined PDF file
- `--page-size {letter,a4,avery6450}` - Page size: 'avery6450' (AVERY 6450 label sheet, 7×9 grid, default), 'letter' (US Letter, 215.9x279.4mm), or 'a4' (210x297mm)

### Example: Custom Configuration

Generate 16 markers with 10-bit coding in a 5-column layout:

```bash
python main.py --bits 10 --markers 16 --columns 5 --output-pdf targets_10bit.pdf
```

Generate 75 markers (automatically splits across multiple pages):

```bash
python main.py --markers 75 --columns 5
```

Generate markers starting from number 100:

```bash
python main.py --markers 20 --start-number 100
```

Generate markers on A4 paper:

```bash
python main.py --page-size a4 --markers 50
```

Generate markers for AVERY 6450 label sheets (default):

```bash
python main.py --markers 63
```

Generate markers for custom layout (US Letter with custom columns):

```bash
python main.py --page-size letter --columns 5 --markers 20
```

Generate only the combined PDF (skip individual SVGs):

```bash
python main.py --skip-svgs
```

Generate only individual SVGs (skip combined PDF):

```bash
python main.py --skip-pdf
```

---

## Validation

The script includes built-in validation:

- **Configuration validation**: Checks parameter ranges and logical constraints
- **Overlap detection**: Warns if marker padding may be insufficient
- **Code limit checking**: Ensures requested marker count doesn't exceed available codes

Example validation output:

```
Warning: Marker padding (2.0mm) may be insufficient. Marker radius is 9.00mm, 
minimum padding should be 18.00mm to prevent overlap.
```

---

## Code Structure

The script is organized into clear functional sections:

- **Geometric Constants**: Named constants for all magic numbers
- **Validation**: Input validation and overlap detection
- **Code Generation**: Deterministic marker code generation
- **Marker Geometry**: Core geometric calculations
- **Rendering**: Separate functions for PDF and SVG generation
- **CLI Interface**: Command-line argument parsing

The code is importable and testable - all functionality is accessible via functions
rather than executing at module level.

---

## Printing Guidelines

See [PRINTING_TARGETS.md](PRINTING_TARGETS.md) for detailed printing instructions,
tolerance specifications, and verification procedures.

**Critical:** Always print at **100% scale / Actual Size**. Disable all driver
scaling and borderless expansion.

---

## Development

### Running Tests

The project includes a comprehensive test suite using pytest. To run tests:

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests (use python -m pytest to ensure venv Python is used)
python -m pytest

# Or if using python3 explicitly
python3 -m pytest

# Run with coverage report
python -m pytest --cov=main --cov-report=html

# Run specific test file
python -m pytest tests/test_validation.py

# Run with verbose output
python -m pytest -v
```

**Note:** Use `python -m pytest` instead of just `pytest` to ensure the virtual environment's Python interpreter is used.

The test suite includes:
- **Unit tests** for validation functions (`test_validation.py`) - 18 tests
- **Unit tests** for code generation (`test_code_generation.py`) - 10 tests
- **Unit tests** for marker geometry (`test_geometry.py`) - 12 tests
- **Integration tests** for rendering functions (`test_rendering.py`) - 12 tests
- **Integration tests** for CLI interface (`test_cli.py`) - 11 tests

**Test Results:**
- 64 tests total, all passing
- 99.34% code coverage (exceeds 80% target)
- Fast execution: ~1.5 seconds for full test suite

### Code Quality

- All magic numbers extracted to named constants
- Functions are pure and testable
- Clear separation of concerns (generation vs rendering)
- Comprehensive input validation
- Type hints throughout

---

## License

See [LICENSE](LICENSE) for details.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.
