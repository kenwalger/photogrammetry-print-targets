# Photogrammetric Coded Target Generator

This repository contains a small, self-contained Python script for generating
printable photogrammetry targets with a built-in calibration reference.

The output is a **1:1 scale PDF** intended for physical printing and use in
photogrammetric capture workflows.

---

## Features

- Mathematically precise coded targets using circular arc (Wedge) geometry
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

Minimal dependencies are intentional.

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
- `coded_markers_6mm.pdf` - Combined PDF with all markers
- `targets/target_1.svg` through `targets/target_N.svg` - Individual marker files

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

### Example: Custom Configuration

Generate 16 markers with 10-bit coding in a 5-column layout:

```bash
python main.py --bits 10 --markers 16 --columns 5 --output-pdf targets_10bit.pdf
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

After PR review, a test suite will be added. The code structure is designed to
facilitate unit testing of individual functions.

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
