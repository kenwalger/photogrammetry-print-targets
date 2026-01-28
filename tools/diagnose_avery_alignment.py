#!/usr/bin/env python3
"""
Diagnostic tool to help identify AVERY 6450 alignment issues.

This script generates a test PDF with measurement guides to help determine
the exact label positions on your physical AVERY 6450 label sheets.

Usage:
    python tools/diagnose_avery_alignment.py

Instructions:
1. Print the generated PDF at 100% scale (no scaling, no fit-to-page)
2. Place it on top of an AVERY 6450 label sheet
3. Measure the following and provide the values:
   - Distance from left edge of page to center of first (leftmost) label
   - Distance from top edge of page to center of first (top) label
   - Horizontal spacing between label centers (measure several to average)
   - Vertical spacing between label centers (measure several to average)
   - Any consistent horizontal or vertical offset you observe
"""

import sys
import os

# Add parent directory to path to import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Circle
import matplotlib.patches as mpatches

# Import constants from main
from main import (
    PAGE_SIZE_AVERY_6450,
    AVERY_6450_COLUMNS,
    AVERY_6450_ROWS,
    AVERY_6450_LEFT_MARGIN_MM,
    AVERY_6450_TOP_MARGIN_MM,
    AVERY_6450_HORIZONTAL_SPACING_MM,
    AVERY_6450_VERTICAL_SPACING_MM,
)


def generate_diagnostic_pdf(output_path: str = "avery_6450_alignment_diagnostic.pdf") -> None:
    """Generate a diagnostic PDF with measurement guides."""
    
    fig = plt.figure(
        figsize=(PAGE_SIZE_AVERY_6450[0] / 25.4, PAGE_SIZE_AVERY_6450[1] / 25.4),
        dpi=300
    )
    
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, PAGE_SIZE_AVERY_6450[0])
    ax.set_ylim(0, PAGE_SIZE_AVERY_6450[1])
    ax.set_aspect("equal")
    
    # Draw page border
    border = mpatches.Rectangle(
        (0, 0), PAGE_SIZE_AVERY_6450[0], PAGE_SIZE_AVERY_6450[1],
        linewidth=2, edgecolor='black', facecolor='none'
    )
    ax.add_patch(border)
    
    # Draw current label center positions
    for row in range(AVERY_6450_ROWS):
        y_from_top = AVERY_6450_TOP_MARGIN_MM + row * AVERY_6450_VERTICAL_SPACING_MM
        y_from_bottom = PAGE_SIZE_AVERY_6450[1] - y_from_top
        
        for col in range(AVERY_6450_COLUMNS):
            x = AVERY_6450_LEFT_MARGIN_MM + col * AVERY_6450_HORIZONTAL_SPACING_MM
            
            # Draw crosshair at label center
            ax.plot([x - 5, x + 5], [y_from_bottom, y_from_bottom], 
                   'r-', linewidth=0.5, alpha=0.7)
            ax.plot([x, x], [y_from_bottom - 5, y_from_bottom + 5], 
                   'r-', linewidth=0.5, alpha=0.7)
            
            # Draw circle representing label (25.4mm diameter = 12.7mm radius)
            circle = Circle((x, y_from_bottom), 12.7, 
                          linewidth=1, edgecolor='red', facecolor='none', 
                          linestyle='--', alpha=0.5)
            ax.add_patch(circle)
            
            # Label with coordinates
            label_text = f"({col+1},{row+1})\n{x:.2f},{y_from_bottom:.2f}"
            ax.text(x, y_from_bottom - 18, label_text, 
                   fontsize=6, ha='center', va='top',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    # Draw measurement guides from page edges
    # Left edge to first column
    ax.annotate('', xy=(AVERY_6450_LEFT_MARGIN_MM, PAGE_SIZE_AVERY_6450[1] - AVERY_6450_TOP_MARGIN_MM),
                xytext=(0, PAGE_SIZE_AVERY_6450[1] - AVERY_6450_TOP_MARGIN_MM),
                arrowprops=dict(arrowstyle='<->', color='blue', lw=1))
    ax.text(AVERY_6450_LEFT_MARGIN_MM / 2, PAGE_SIZE_AVERY_6450[1] - AVERY_6450_TOP_MARGIN_MM + 3,
           f'Left margin:\n{AVERY_6450_LEFT_MARGIN_MM:.2f}mm',
           fontsize=8, ha='center', color='blue',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.8))
    
    # Top edge to first row
    ax.annotate('', xy=(AVERY_6450_LEFT_MARGIN_MM, PAGE_SIZE_AVERY_6450[1] - AVERY_6450_TOP_MARGIN_MM),
                xytext=(AVERY_6450_LEFT_MARGIN_MM, PAGE_SIZE_AVERY_6450[1]),
                arrowprops=dict(arrowstyle='<->', color='blue', lw=1))
    ax.text(AVERY_6450_LEFT_MARGIN_MM + 8, PAGE_SIZE_AVERY_6450[1] - AVERY_6450_TOP_MARGIN_MM / 2,
           f'Top margin:\n{AVERY_6450_TOP_MARGIN_MM:.2f}mm',
           fontsize=8, ha='left', color='blue',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.8))
    
    # Horizontal spacing between first two columns
    first_y = PAGE_SIZE_AVERY_6450[1] - AVERY_6450_TOP_MARGIN_MM
    ax.annotate('', xy=(AVERY_6450_LEFT_MARGIN_MM + AVERY_6450_HORIZONTAL_SPACING_MM, first_y),
                xytext=(AVERY_6450_LEFT_MARGIN_MM, first_y),
                arrowprops=dict(arrowstyle='<->', color='green', lw=1))
    ax.text(AVERY_6450_LEFT_MARGIN_MM + AVERY_6450_HORIZONTAL_SPACING_MM / 2, first_y + 3,
           f'Horizontal spacing:\n{AVERY_6450_HORIZONTAL_SPACING_MM:.2f}mm',
           fontsize=8, ha='center', color='green',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.8))
    
    # Vertical spacing between first two rows
    first_x = AVERY_6450_LEFT_MARGIN_MM
    second_y = PAGE_SIZE_AVERY_6450[1] - (AVERY_6450_TOP_MARGIN_MM + AVERY_6450_VERTICAL_SPACING_MM)
    ax.annotate('', xy=(first_x, second_y),
                xytext=(first_x, first_y),
                arrowprops=dict(arrowstyle='<->', color='green', lw=1))
    ax.text(first_x + 8, (first_y + second_y) / 2,
           f'Vertical spacing:\n{AVERY_6450_VERTICAL_SPACING_MM:.2f}mm',
           fontsize=8, ha='left', color='green',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.8))
    
    # Add instructions
    instructions = (
        "AVERY 6450 Alignment Diagnostic\n"
        "===============================\n\n"
        "Current Settings:\n"
        f"  Left margin: {AVERY_6450_LEFT_MARGIN_MM:.2f} mm\n"
        f"  Top margin: {AVERY_6450_TOP_MARGIN_MM:.2f} mm\n"
        f"  Horizontal spacing: {AVERY_6450_HORIZONTAL_SPACING_MM:.2f} mm\n"
        f"  Vertical spacing: {AVERY_6450_VERTICAL_SPACING_MM:.2f} mm\n\n"
        "Instructions:\n"
        "1. Print this PDF at 100% scale (no scaling)\n"
        "2. Place on top of AVERY 6450 label sheet\n"
        "3. Measure actual label positions\n"
        "4. Report any offsets or spacing differences"
    )
    
    ax.text(PAGE_SIZE_AVERY_6450[0] - 5, 5, instructions,
           fontsize=7, ha='right', va='bottom',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9))
    
    # Save PDF
    with PdfPages(output_path) as pdf:
        pdf.savefig(fig, transparent=False)
    
    plt.close(fig)
    print(f"Diagnostic PDF generated: {output_path}")
    print("\nPlease print this PDF and measure the actual label positions on your AVERY 6450 sheet.")


if __name__ == "__main__":
    generate_diagnostic_pdf()
