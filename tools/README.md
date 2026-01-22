# Development Tools

This directory contains development and analysis tools used during the project.

## analyze_avery_template.py

Script used to analyze the official AVERY 6450 PDF template and extract layout specifications.

**Purpose**: Extract exact label positions, spacing, and margins from the AVERY 6450 template PDF.

**Usage**:
```bash
python tools/analyze_avery_template.py
```

**Output**: Prints page dimensions, label positions, spacing calculations, and margin information extracted from the template.

**Note**: The extracted values are now hardcoded in `main.py` as AVERY 6450 constants. This script is kept for reference and potential future template analysis.
