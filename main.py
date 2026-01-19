import math
import os
from typing import List

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import Wedge, Circle

# NOTE:
# Print at 100% scale / Actual Size.
# Disable all driver scaling and borderless expansion.

# ==============================
# CONFIGURATION (ARCHIVAL SAFE)
# ==============================

DOT_RADIUS_MM: float = 3.0        # 6 mm diameter center dot
BITS: int = 8                     # number of ring bits
COLUMNS: int = 4                  # markers per row
MARKERS_TOTAL: int = 12           # total markers to generate
DPI: int = 300                    # print resolution (does not affect scale)
PAGE_MARGIN_MM: float = 10.0      # white margin for printing
MARKER_PADDING_MM: float = 5.0    # 5mm gap between markers

# ==============================
# CALIBRATION FEATURE
# ==============================

CAL_DOT_RADIUS_MM: float = 2.0
CAL_DOT_SPACING_MM: float = 20.0
CAL_LABEL: str = "20.00 mm calibration reference"

# ==============================
# CODE GENERATION (PLACEHOLDER)
# ==============================

def get_ring_codes(bits: int, n: int) -> List[int]:
    """
    Generate a deterministic list of binary marker codes.

    This is a placeholder implementation intended to be replaced with
    a MATLAB-equivalent ring-code generator if exact compatibility is required.

    Args:
        bits: Number of bits used in the coded ring.
        n: Number of marker codes to generate.

    Returns:
        A list of integer codes suitable for binary ring encoding.
    """
    max_code = 2 ** bits
    return list(range(1, min(n + 1, max_code)))

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
    ring_inner = dot_radius * 1.6
    ring_outer = dot_radius * 2.4
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

def draw_calibration_feature(ax: Axes, origin_x: float, origin_y: float) -> None:
    """
    Draw a calibration reference consisting of two dots separated
    by a known center-to-center distance.

    This feature is intended for physical verification of print scale.

    Args:
        ax: Matplotlib Axes object to draw on.
        origin_x: X-coordinate of the first calibration dot (mm).
        origin_y: Y-coordinate of the first calibration dot (mm).
    """
    dot1 = Circle(
        (origin_x, origin_y),
        radius=CAL_DOT_RADIUS_MM,
        facecolor="black",
        edgecolor="none"
    )

    dot2 = Circle(
        (origin_x + CAL_DOT_SPACING_MM, origin_y),
        radius=CAL_DOT_RADIUS_MM,
        facecolor="black",
        edgecolor="none"
    )

    ax.add_patch(dot1)
    ax.add_patch(dot2)

    ax.text(
        origin_x + CAL_DOT_SPACING_MM / 2,
        origin_y - CAL_DOT_RADIUS_MM * 2.5,
        CAL_LABEL,
        fontsize=6,
        ha="center",
        va="top"
    )

# ==============================
# LAYOUT & RENDERING
# ==============================

codes = get_ring_codes(BITS, MARKERS_TOTAL)
rows = math.ceil(len(codes) / COLUMNS)

MARKER_SIZE_MM = DOT_RADIUS_MM * 6
MARKER_CELL_SIZE = MARKER_SIZE_MM + MARKER_PADDING_MM

page_width = COLUMNS * MARKER_CELL_SIZE + 2 * PAGE_MARGIN_MM
page_height = rows * MARKER_CELL_SIZE + 2 * PAGE_MARGIN_MM

fig = plt.figure(
    figsize=(page_width / 25.4, page_height / 25.4),
    dpi=DPI
)

ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, page_width)
ax.set_ylim(0, page_height)
ax.set_aspect("equal")
ax.axis("off")

for idx, code in enumerate(codes):
    col = idx % COLUMNS
    row = idx // COLUMNS

    cx = PAGE_MARGIN_MM + col * MARKER_CELL_SIZE + MARKER_CELL_SIZE / 2
    cy = page_height - (
        PAGE_MARGIN_MM + row * MARKER_CELL_SIZE + MARKER_CELL_SIZE / 2
    )

    patches = get_coded_marker(cx, cy, DOT_RADIUS_MM, BITS, code)
    for p in patches:
        ax.add_patch(p)

    ax.text(
        cx + DOT_RADIUS_MM * 2.8,
        cy + DOT_RADIUS_MM * 2.8,
        str(idx + 1),
        fontsize=6,
        ha="right",
        va="top"
    )

# Draw calibration reference once per page
draw_calibration_feature(
    ax,
    PAGE_MARGIN_MM,
    PAGE_MARGIN_MM * 0.8
)

# ==============================
# EXPORT (1:1 SCALE)
# ==============================

plt.savefig(
    "coded_markers_6mm.pdf",
    dpi=DPI,
    transparent=True
)
plt.close()


# ==============================
# Create directory if it doesn't exist
# ==============================

output_dir = "targets"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Inside your loop, save individual SVGs for the "Targets" folder
for idx, code in enumerate(codes):
    # (Existing coordinate logic...)

    # Create a small temp figure for the individual SVG
    target_fig = plt.figure(figsize=(MARKER_SIZE_MM / 25.4, MARKER_SIZE_MM / 25.4))
    target_ax = target_fig.add_axes([0, 0, 1, 1])
    target_ax.set_aspect("equal")
    target_ax.axis("off")

    # Add patches to the individual file
    target_patches = get_coded_marker(0, 0, DOT_RADIUS_MM, BITS, code)
    for p in target_patches:
        target_ax.add_patch(p)

    target_ax.set_xlim(-MARKER_SIZE_MM / 2, MARKER_SIZE_MM / 2)
    target_ax.set_ylim(-MARKER_SIZE_MM / 2, MARKER_SIZE_MM / 2)

    target_fig.savefig(f"{output_dir}/target_{idx + 1}.svg", transparent=True)
    plt.close(target_fig)