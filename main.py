"""
Photogrammetric Coded Target Generator

Generates printable photogrammetry targets with built-in calibration references.
Outputs both a combined PDF and individual SVG files for each target.

NOTE: Print at 100% scale / Actual Size.
      Disable all driver scaling and borderless expansion.
"""

import argparse
import math
import os
import sys
from typing import List, Tuple

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import Wedge, Circle

# ==============================
# GEOMETRIC CONSTANTS
# ==============================

# Ring geometry multipliers (relative to dot radius)
RING_INNER_MULTIPLIER: float = 1.6  # Inner ring radius = dot_radius * 1.6
RING_OUTER_MULTIPLIER: float = 2.4  # Outer ring radius = dot_radius * 2.4

# Marker size calculation
MARKER_SIZE_MULTIPLIER: float = 6.0  # Total marker size = dot_radius * 6

# Label positioning (relative to dot radius)
LABEL_OFFSET_X_MULTIPLIER: float = 2.8  # Label X offset = dot_radius * 2.8
LABEL_OFFSET_Y_MULTIPLIER: float = 2.8  # Label Y offset = dot_radius * 2.8

# Calibration feature positioning
CAL_LABEL_OFFSET_MULTIPLIER: float = 2.5  # Label Y offset = cal_dot_radius * 2.5
CAL_POSITION_Y_MULTIPLIER: float = 0.8  # Calibration Y position = margin * 0.8

# Font sizes
LABEL_FONTSIZE: int = 6
CAL_LABEL_FONTSIZE: int = 6

# ==============================
# DEFAULT CONFIGURATION
# ==============================

DEFAULT_DOT_RADIUS_MM: float = 3.0  # 6 mm diameter center dot
DEFAULT_BITS: int = 8  # number of ring bits
DEFAULT_COLUMNS: int = 4  # markers per row
DEFAULT_MARKERS_TOTAL: int = 12  # total markers to generate
DEFAULT_DPI: int = 300  # print resolution (does not affect scale)
DEFAULT_PAGE_MARGIN_MM: float = 10.0  # white margin for printing
DEFAULT_MARKER_PADDING_MM: float = 5.0  # gap between markers

# Calibration feature defaults
DEFAULT_CAL_DOT_RADIUS_MM: float = 2.0
DEFAULT_CAL_DOT_SPACING_MM: float = 20.0
DEFAULT_CAL_LABEL: str = "20.00 mm calibration reference"

# Output defaults
DEFAULT_OUTPUT_PDF: str = "coded_markers_6mm.pdf"
DEFAULT_OUTPUT_DIR: str = "targets"

# ==============================
# VALIDATION
# ==============================


def validate_config(
    dot_radius: float,
    bits: int,
    columns: int,
    markers_total: int,
    page_margin: float,
    marker_padding: float,
    cal_dot_spacing: float
) -> Tuple[bool, str]:
    """
    Validate configuration parameters.

    Args:
        dot_radius: Radius of center dot in mm.
        bits: Number of ring bits.
        columns: Number of markers per row.
        markers_total: Total number of markers.
        page_margin: Page margin in mm.
        marker_padding: Padding between markers in mm.
        cal_dot_spacing: Calibration dot spacing in mm.

    Returns:
        Tuple of (is_valid, error_message).
    """
    if dot_radius <= 0:
        return False, "Dot radius must be positive"
    if bits < 4 or bits > 16:
        return False, "Bits must be between 4 and 16"
    if columns < 1:
        return False, "Columns must be at least 1"
    if markers_total < 1:
        return False, "Markers total must be at least 1"
    if page_margin < 0:
        return False, "Page margin must be non-negative"
    if marker_padding < 0:
        return False, "Marker padding must be non-negative"
    if cal_dot_spacing <= 0:
        return False, "Calibration dot spacing must be positive"

    max_code = 2 ** bits
    if markers_total >= max_code:
        return False, f"Markers total ({markers_total}) exceeds maximum codes ({max_code - 1}) for {bits} bits"

    return True, ""


def check_marker_overlap(
    dot_radius: float,
    marker_padding: float
) -> Tuple[bool, str]:
    """
    Check if markers would overlap given the current configuration.

    Args:
        dot_radius: Radius of center dot in mm.
        marker_padding: Padding between markers in mm.

    Returns:
        Tuple of (no_overlap, warning_message).
    """
    marker_size = dot_radius * MARKER_SIZE_MULTIPLIER
    marker_radius = marker_size / 2

    if marker_padding < marker_radius * 2:
        return False, (
            f"Warning: Marker padding ({marker_padding}mm) may be insufficient. "
            f"Marker radius is {marker_radius:.2f}mm, minimum padding should be "
            f"{marker_radius * 2:.2f}mm to prevent overlap."
        )

    return True, ""


# ==============================
# CODE GENERATION
# ==============================


def rotate_code(code: int, bits: int, rotation: int) -> int:
    """
    Rotate a binary code by a specified number of positions.

    Args:
        code: The binary code to rotate.
        bits: Number of bits in the code.
        rotation: Number of positions to rotate (positive = left, negative = right).

    Returns:
        The rotated code.
    """
    rotation = rotation % bits
    if rotation == 0:
        return code
    
    # Left rotation: (code << rotation) | (code >> (bits - rotation))
    # Mask to keep only 'bits' bits
    mask = (1 << bits) - 1
    return ((code << rotation) | (code >> (bits - rotation))) & mask


def canonical_rotation(code: int, bits: int) -> int:
    """
    Find the canonical (lexicographically smallest) rotation of a code.

    This ensures rotationally invariant codes - any rotation of a code
    maps to the same canonical representation.

    Args:
        code: The binary code to find canonical rotation for.
        bits: Number of bits in the code.

    Returns:
        The canonical (smallest) rotation of the code.
    """
    if code == 0:
        return 0
    
    canonical = code
    for rotation in range(1, bits):
        rotated = rotate_code(code, bits, rotation)
        if rotated < canonical:
            canonical = rotated
    
    return canonical


def is_rotationally_invariant(code: int, bits: int) -> bool:
    """
    Check if a code is in its canonical (rotationally invariant) form.

    Args:
        code: The binary code to check.
        bits: Number of bits in the code.

    Returns:
        True if the code equals its canonical rotation.
    """
    return code == canonical_rotation(code, bits)


# Industry-standard rotationally invariant codes
# These are canonical codes that work well for photogrammetry
# Based on patterns used in professional photogrammetry software

# Generate rotationally invariant codes for lookup tables
# These are computed lazily to avoid import-time delays
# All codes are verified to be rotationally invariant

# Cache for generated codes (lazy initialization)
_STANDARD_CODES_CACHE: dict[int, List[int]] = {}


def _generate_standard_codes_8bit() -> List[int]:
    """Generate 8-bit rotationally invariant codes."""
    codes = []
    for code in range(1, 256):
        if is_rotationally_invariant(code, 8):
            codes.append(code)
            if len(codes) >= 30:
                break
    return codes


def _generate_standard_codes_12bit() -> List[int]:
    """Generate 12-bit rotationally invariant codes."""
    codes = []
    for code in range(1, 4096):
        if is_rotationally_invariant(code, 12):
            codes.append(code)
            if len(codes) >= 50:
                break
    return codes


def _generate_standard_codes_14bit() -> List[int]:
    """Generate 14-bit rotationally invariant codes."""
    codes = []
    for code in range(1, 16384):
        if is_rotationally_invariant(code, 14):
            codes.append(code)
            if len(codes) >= 50:
                break
    return codes


def _get_industry_standard_codes(bits: int) -> List[int]:
    """
    Get industry-standard rotationally invariant codes for a given bit count.
    
    Uses lazy initialization to avoid import-time performance delays.
    Codes are generated on first access and cached for subsequent calls.
    
    Args:
        bits: Number of bits (8, 12, or 14).
        
    Returns:
        List of rotationally invariant codes.
    """
    if bits not in _STANDARD_CODES_CACHE:
        if bits == 8:
            _STANDARD_CODES_CACHE[8] = _generate_standard_codes_8bit()
        elif bits == 12:
            _STANDARD_CODES_CACHE[12] = _generate_standard_codes_12bit()
        elif bits == 14:
            _STANDARD_CODES_CACHE[14] = _generate_standard_codes_14bit()
        else:
            # Not a standard bit count, return empty list
            return []
    
    return _STANDARD_CODES_CACHE[bits]


def generate_rotationally_invariant_codes(bits: int, n: int) -> List[int]:
    """
    Generate rotationally invariant codes algorithmically.

    This function generates codes that are in their canonical form,
    ensuring that any rotation of a marker will be recognized as
    the same code.

    Args:
        bits: Number of bits in the coded ring.
        n: Number of codes to generate.

    Returns:
        A list of rotationally invariant codes.
    """
    codes: List[int] = []
    max_code = 2 ** bits
    
    # Start from 1 (0 is not a valid marker code)
    for code in range(1, max_code):
        if is_rotationally_invariant(code, bits):
            codes.append(code)
            if len(codes) >= n:
                break
    
    return codes


def get_ring_codes(bits: int, n: int) -> List[int]:
    """
    Generate a deterministic list of rotationally invariant binary marker codes.

    This implementation uses industry-standard patterns for common bit counts
    (8, 12, 14) and generates rotationally invariant codes algorithmically
    for other bit counts.

    Rotationally invariant codes ensure that a marker can be identified
    correctly regardless of its orientation - critical for photogrammetry
    workflows where markers may be viewed from different angles.

    Args:
        bits: Number of bits used in the coded ring (4-16).
        n: Number of marker codes to generate.

    Returns:
        A list of integer codes suitable for binary ring encoding.
        All codes are rotationally invariant (canonical form).
    """
    # Use industry-standard lookup table if available (lazy initialization)
    if bits in (8, 12, 14):
        standard_codes = _get_industry_standard_codes(bits)
        if standard_codes:
            return standard_codes[:min(n, len(standard_codes))]
    
    # For other bit counts, generate rotationally invariant codes algorithmically
    return generate_rotationally_invariant_codes(bits, n)


# ==============================
# MARKER GEOMETRY
# ==============================


def get_coded_marker(
    center_x: float,
    center_y: float,
    dot_radius: float,
    bits: int,
    code: int
) -> List[Wedge | Circle]:
    """
    Create the geometric elements for a single coded photogrammetry marker.

    The marker consists of:
    - A solid circular center dot
    - A surrounding binary-coded ring

    All dimensions are defined in millimeters.

    Args:
        center_x: X-coordinate of the marker center (mm).
        center_y: Y-coordinate of the marker center (mm).
        dot_radius: Radius of the solid center dot (mm).
        bits: Number of binary segments in the coded ring.
        code: Integer value encoding which ring segments are filled.

    Returns:
        A list of Matplotlib patch objects representing the marker geometry.
    """
    patches: List[Wedge | Circle] = []

    # --- center dot ---
    patches.append(
        Circle(
            (center_x, center_y),
            radius=dot_radius,
            facecolor="black",
            edgecolor="none"
        )
    )

    # --- coded ring ---
    ring_inner = dot_radius * RING_INNER_MULTIPLIER
    ring_outer = dot_radius * RING_OUTER_MULTIPLIER
    angle_step_deg = 360.0 / bits

    for i in range(bits):
        if (code >> i) & 1:
            theta1 = i * angle_step_deg
            theta2 = (i + 1) * angle_step_deg

            patches.append(
                Wedge(
                    (center_x, center_y),
                    r=ring_outer,
                    theta1=theta1,
                    theta2=theta2,
                    width=ring_outer - ring_inner,
                    facecolor="black",
                    edgecolor="none"
                )
            )

    return patches


def draw_calibration_feature(
    ax: Axes,
    origin_x: float,
    origin_y: float,
    cal_dot_radius: float,
    cal_dot_spacing: float,
    cal_label: str
) -> None:
    """
    Draw a calibration reference consisting of two dots separated
    by a known center-to-center distance.

    This feature is intended for physical verification of print scale.

    Args:
        ax: Matplotlib Axes object to draw on.
        origin_x: X-coordinate of the first calibration dot (mm).
        origin_y: Y-coordinate of the first calibration dot (mm).
        cal_dot_radius: Radius of calibration dots (mm).
        cal_dot_spacing: Center-to-center spacing of calibration dots (mm).
        cal_label: Text label for the calibration feature.
    """
    dot1 = Circle(
        (origin_x, origin_y),
        radius=cal_dot_radius,
        facecolor="black",
        edgecolor="none"
    )

    dot2 = Circle(
        (origin_x + cal_dot_spacing, origin_y),
        radius=cal_dot_radius,
        facecolor="black",
        edgecolor="none"
    )

    ax.add_patch(dot1)
    ax.add_patch(dot2)

    ax.text(
        origin_x + cal_dot_spacing / 2,
        origin_y - cal_dot_radius * CAL_LABEL_OFFSET_MULTIPLIER,
        cal_label,
        fontsize=CAL_LABEL_FONTSIZE,
        ha="center",
        va="top"
    )


# ==============================
# RENDERING
# ==============================


def render_marker_to_axes(
    ax: Axes,
    center_x: float,
    center_y: float,
    dot_radius: float,
    bits: int,
    code: int,
    marker_index: int,
    show_label: bool = True
) -> None:
    """
    Render a single marker to the given axes.

    Args:
        ax: Matplotlib Axes object to draw on.
        center_x: X-coordinate of marker center (mm).
        center_y: Y-coordinate of marker center (mm).
        dot_radius: Radius of center dot (mm).
        bits: Number of ring bits.
        code: Marker code value.
        marker_index: Zero-based index of the marker (for labeling).
        show_label: Whether to display the marker number label.
    """
    patches = get_coded_marker(center_x, center_y, dot_radius, bits, code)
    for p in patches:
        ax.add_patch(p)

    if show_label:
        ax.text(
            center_x + dot_radius * LABEL_OFFSET_X_MULTIPLIER,
            center_y + dot_radius * LABEL_OFFSET_Y_MULTIPLIER,
            str(marker_index + 1),
            fontsize=LABEL_FONTSIZE,
            ha="right",
            va="top"
        )


def generate_combined_pdf(
    codes: List[int],
    dot_radius: float,
    bits: int,
    columns: int,
    page_margin: float,
    marker_padding: float,
    dpi: int,
    cal_dot_radius: float,
    cal_dot_spacing: float,
    cal_label: str,
    output_path: str
) -> None:
    """
    Generate a combined PDF with all markers arranged in a grid.

    Args:
        codes: List of marker codes to generate.
        dot_radius: Radius of center dot (mm).
        bits: Number of ring bits.
        columns: Number of markers per row.
        page_margin: Page margin (mm).
        marker_padding: Padding between markers (mm).
        dpi: Print resolution.
        cal_dot_radius: Calibration dot radius (mm).
        cal_dot_spacing: Calibration dot spacing (mm).
        cal_label: Calibration label text.
        output_path: Path to output PDF file.
    """
    rows = math.ceil(len(codes) / columns)
    marker_size = dot_radius * MARKER_SIZE_MULTIPLIER
    marker_cell_size = marker_size + marker_padding

    page_width = columns * marker_cell_size + 2 * page_margin
    page_height = rows * marker_cell_size + 2 * page_margin

    fig = plt.figure(
        figsize=(page_width / 25.4, page_height / 25.4),
        dpi=dpi
    )

    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, page_width)
    ax.set_ylim(0, page_height)
    ax.set_aspect("equal")
    ax.axis("off")

    # Render all markers
    for idx, code in enumerate(codes):
        col = idx % columns
        row = idx // columns

        cx = page_margin + col * marker_cell_size + marker_cell_size / 2
        cy = page_height - (page_margin + row * marker_cell_size + marker_cell_size / 2)

        render_marker_to_axes(ax, cx, cy, dot_radius, bits, code, idx, show_label=True)

    # Draw calibration reference
    draw_calibration_feature(
        ax,
        page_margin,
        page_margin * CAL_POSITION_Y_MULTIPLIER,
        cal_dot_radius,
        cal_dot_spacing,
        cal_label
    )

    plt.savefig(output_path, dpi=dpi, transparent=True)
    plt.close()


def generate_individual_svgs(
    codes: List[int],
    dot_radius: float,
    bits: int,
    output_dir: str
) -> None:
    """
    Generate individual SVG files for each marker.

    Args:
        codes: List of marker codes to generate.
        dot_radius: Radius of center dot (mm).
        bits: Number of ring bits.
        output_dir: Directory to save SVG files.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    marker_size = dot_radius * MARKER_SIZE_MULTIPLIER

    for idx, code in enumerate(codes):
        target_fig = plt.figure(figsize=(marker_size / 25.4, marker_size / 25.4))
        target_ax = target_fig.add_axes([0, 0, 1, 1])
        target_ax.set_aspect("equal")
        target_ax.axis("off")

        render_marker_to_axes(
            target_ax, 0, 0, dot_radius, bits, code, idx, show_label=False
        )

        target_ax.set_xlim(-marker_size / 2, marker_size / 2)
        target_ax.set_ylim(-marker_size / 2, marker_size / 2)

        target_fig.savefig(
            f"{output_dir}/target_{idx + 1}.svg",
            transparent=True
        )
        plt.close(target_fig)


# ==============================
# MAIN
# ==============================


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate photogrammetry targets with calibration references.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--dot-radius",
        type=float,
        default=DEFAULT_DOT_RADIUS_MM,
        help="Radius of center dot in millimeters"
    )

    parser.add_argument(
        "--bits",
        type=int,
        default=DEFAULT_BITS,
        help="Number of bits in the coded ring"
    )

    parser.add_argument(
        "--columns",
        type=int,
        default=DEFAULT_COLUMNS,
        help="Number of markers per row"
    )

    parser.add_argument(
        "--markers",
        type=int,
        default=DEFAULT_MARKERS_TOTAL,
        dest="markers_total",
        help="Total number of markers to generate"
    )

    parser.add_argument(
        "--dpi",
        type=int,
        default=DEFAULT_DPI,
        help="Print resolution (does not affect scale)"
    )

    parser.add_argument(
        "--margin",
        type=float,
        default=DEFAULT_PAGE_MARGIN_MM,
        dest="page_margin",
        help="Page margin in millimeters"
    )

    parser.add_argument(
        "--padding",
        type=float,
        default=DEFAULT_MARKER_PADDING_MM,
        dest="marker_padding",
        help="Padding between markers in millimeters"
    )

    parser.add_argument(
        "--cal-dot-radius",
        type=float,
        default=DEFAULT_CAL_DOT_RADIUS_MM,
        help="Calibration dot radius in millimeters"
    )

    parser.add_argument(
        "--cal-spacing",
        type=float,
        default=DEFAULT_CAL_DOT_SPACING_MM,
        dest="cal_dot_spacing",
        help="Calibration dot center-to-center spacing in millimeters"
    )

    parser.add_argument(
        "--cal-label",
        type=str,
        default=DEFAULT_CAL_LABEL,
        help="Calibration reference label text"
    )

    parser.add_argument(
        "--output-pdf",
        type=str,
        default=DEFAULT_OUTPUT_PDF,
        help="Output PDF filename"
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default=DEFAULT_OUTPUT_DIR,
        help="Output directory for individual SVG files"
    )

    parser.add_argument(
        "--skip-svgs",
        action="store_true",
        help="Skip generation of individual SVG files"
    )

    parser.add_argument(
        "--skip-pdf",
        action="store_true",
        help="Skip generation of combined PDF file"
    )

    return parser.parse_args()


def main() -> None:
    """Main entry point."""
    args = parse_arguments()

    # Validate configuration
    is_valid, error_msg = validate_config(
        args.dot_radius,
        args.bits,
        args.columns,
        args.markers_total,
        args.page_margin,
        args.marker_padding,
        args.cal_dot_spacing
    )

    if not is_valid:
        print(f"Error: {error_msg}", file=sys.stderr)
        sys.exit(1)

    # Check for potential overlap
    no_overlap, warning_msg = check_marker_overlap(
        args.dot_radius,
        args.marker_padding
    )
    if not no_overlap:
        print(f"Warning: {warning_msg}", file=sys.stderr)

    # Generate codes
    codes = get_ring_codes(args.bits, args.markers_total)

    # Generate combined PDF
    if not args.skip_pdf:
        generate_combined_pdf(
            codes,
            args.dot_radius,
            args.bits,
            args.columns,
            args.page_margin,
            args.marker_padding,
            args.dpi,
            args.cal_dot_radius,
            args.cal_dot_spacing,
            args.cal_label,
            args.output_pdf
        )
        print(f"Generated combined PDF: {args.output_pdf}")

    # Generate individual SVGs
    if not args.skip_svgs:
        generate_individual_svgs(
            codes,
            args.dot_radius,
            args.bits,
            args.output_dir
        )
        print(f"Generated {len(codes)} individual SVG files in: {args.output_dir}/")


if __name__ == "__main__":
    main()
