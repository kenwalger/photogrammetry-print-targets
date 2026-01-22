#!/usr/bin/env python3
"""
Development tool to analyze AVERY 6450 PDF template and extract layout specifications.

This script was used to extract the exact label positions and spacing from the
official AVERY 6450 template PDF. The extracted values are now hardcoded in main.py.

Usage:
    python tools/analyze_avery_template.py
"""

import sys

def analyze_pdf_template(pdf_path: str) -> None:
    """Analyze PDF template to extract layout information."""
    try:
        from pypdf import PdfReader
        reader = PdfReader(pdf_path)
        page = reader.pages[0]
        
        # Get page dimensions (in points, convert to mm)
        mediabox = page.mediabox
        width_pt = float(mediabox.width)
        height_pt = float(mediabox.height)
        
        # Convert points to mm (1 point = 0.352778 mm)
        width_mm = width_pt * 0.352778
        height_mm = height_pt * 0.352778
        
        print(f"Page Dimensions:")
        print(f"  Width: {width_mm:.2f} mm ({width_pt:.2f} points)")
        print(f"  Height: {height_mm:.2f} mm ({height_pt:.2f} points)")
        print(f"  Width: {width_mm/25.4:.2f} inches")
        print(f"  Height: {height_mm/25.4:.2f} inches")
        
        # Try to extract any annotations or form fields that might indicate label positions
        label_positions = []
        
        if '/Annots' in page:
            annots = page['/Annots']
            print(f"\nFound {len(annots)} annotations")
            for i, annot in enumerate(annots):
                obj = annot.get_object()
                if '/Rect' in obj:
                    rect = obj['/Rect']
                    # Convert rect to mm (rect is in points: [x0, y0, x1, y1])
                    x0_pt, y0_pt, x1_pt, y1_pt = [float(r) for r in rect]
                    center_x_pt = (x0_pt + x1_pt) / 2
                    center_y_pt = (y0_pt + y1_pt) / 2
                    center_x_mm = center_x_pt * 0.352778
                    center_y_mm = (height_pt - center_y_pt) * 0.352778  # Flip Y coordinate
                    label_positions.append((center_x_mm, center_y_mm))
                    if i < 5:  # Show first 5
                        print(f"  Annotation {i+1}: center at ({center_x_mm:.2f}, {center_y_mm:.2f}) mm")
        
        # Check for form fields
        if '/AcroForm' in reader.trailer:
            print("\nFound AcroForm in document")
        
        # Analyze content stream for circles (label outlines)
        try:
            content = page['/Contents'].get_object()
            if hasattr(content, 'get_data'):
                stream_data = content.get_data()
                print(f"\nContent stream size: {len(stream_data)} bytes")
                
                # Look for circle/ellipse commands - PDF uses 'c' (curveto) or arc commands
                # AVERY templates often use circles for label guides
                # Try to find patterns that might indicate label positions
                import re
                # Look for coordinate patterns - PDF uses various commands
                # Try multiple patterns to find circle centers
                patterns = [
                    rb'(\d+\.?\d*)\s+(\d+\.?\d*)\s+[cm]',  # curveto/moveto
                    rb'(\d+\.?\d*)\s+(\d+\.?\d*)\s+(\d+\.?\d*)\s+(\d+\.?\d*)\s+(\d+\.?\d*)\s+(\d+\.?\d*)\s+c',  # bezier curves
                ]
                
                all_points = []
                for pattern in patterns:
                    matches = re.findall(pattern, stream_data)
                    for match in matches:
                        try:
                            if len(match) == 2:
                                x_pt = float(match[0])
                                y_pt = float(match[1])
                            elif len(match) == 6:
                                # Bezier curve - use control points
                                x_pt = float(match[4])
                                y_pt = float(match[5])
                            else:
                                continue
                            x_mm = x_pt * 0.352778
                            y_mm = (height_pt - y_pt) * 0.352778
                            all_points.append((x_mm, y_mm))
                        except:
                            continue
                
                if all_points:
                    print(f"  Found {len(all_points)} coordinate points")
                    # Find unique positions (round to nearest 0.1mm to group similar positions)
                    unique_positions = {}
                    for x, y in all_points:
                        x_rounded = round(x * 10) / 10
                        y_rounded = round(y * 10) / 10
                        key = (x_rounded, y_rounded)
                        if key not in unique_positions:
                            unique_positions[key] = (x, y)
                    
                    # Filter to likely label centers (should be in a grid pattern)
                    # Look for positions that appear multiple times or are at regular intervals
                    label_candidates = []
                    for pos in unique_positions.values():
                        # Label centers are likely between 10-200mm from edges
                        if 10 < pos[0] < 200 and 10 < pos[1] < 270:
                            label_candidates.append(pos)
                    
                    # Sort and group by rows (similar Y values)
                    label_candidates.sort(key=lambda p: (-p[1], p[0]))  # Top to bottom, left to right
                    
                    print(f"  Found {len(label_candidates)} candidate label positions")
                    if len(label_candidates) >= 3:
                        print(f"  First 3 positions:")
                        for i, (x, y) in enumerate(label_candidates[:3]):
                            print(f"    Label {i+1}: ({x:.2f}, {y:.2f}) mm")
                        
                        # Calculate spacing
                        if len(label_candidates) >= 2:
                            # Group by row
                            rows = {}
                            for x, y in label_candidates:
                                y_row = round(y / 5) * 5
                                if y_row not in rows:
                                    rows[y_row] = []
                                rows[y_row].append((x, y))
                            
                            # Find horizontal spacing
                            for y_key, row_positions in sorted(rows.items(), reverse=True):
                                if len(row_positions) >= 2:
                                    row_positions.sort(key=lambda p: p[0])
                                    h_spacing = row_positions[1][0] - row_positions[0][0]
                                    print(f"  Horizontal spacing: {h_spacing:.2f} mm")
                                    print(f"  Columns: {len(row_positions)}")
                                    break
                            
                            # Find vertical spacing
                            if len(rows) >= 2:
                                y_values = sorted(rows.keys(), reverse=True)
                                v_spacing = y_values[0] - y_values[1]
                                print(f"  Vertical spacing: {v_spacing:.2f} mm")
                                print(f"  Rows: {len(rows)}")
                                
                                # Calculate margins
                                all_x = [p[0] for row in rows.values() for p in row]
                                all_y = [p[1] for row in rows.values() for p in row]
                                left_margin = min(all_x)
                                top_margin = height_mm - max(all_y)
                                print(f"  Left margin (to first label center): {left_margin:.2f} mm")
                                print(f"  Top margin (to first label center): {top_margin:.2f} mm")
                                
                                # Store the actual positions
                                label_positions = label_candidates
        except Exception as e:
            print(f"  Could not analyze content stream: {e}")
        
        # If we found label positions, calculate spacing
        if len(label_positions) >= 2:
            print(f"\nFound {len(label_positions)} label positions")
            # Sort by Y (top to bottom), then X (left to right)
            label_positions.sort(key=lambda p: (-p[1], p[0]))
            
            # Calculate horizontal spacing (between columns)
            if len(label_positions) >= 2:
                # Find positions in same row (similar Y values)
                row_groups = {}
                for x, y in label_positions:
                    y_rounded = round(y / 5) * 5  # Group by ~5mm
                    if y_rounded not in row_groups:
                        row_groups[y_rounded] = []
                    row_groups[y_rounded].append((x, y))
                
                # Find first row with multiple labels
                for y_key, positions in row_groups.items():
                    if len(positions) >= 2:
                        positions.sort(key=lambda p: p[0])
                        h_spacing = positions[1][0] - positions[0][0]
                        print(f"  Horizontal spacing: {h_spacing:.2f} mm")
                        break
                
                # Calculate vertical spacing (between rows)
                if len(row_groups) >= 2:
                    y_values = sorted(row_groups.keys(), reverse=True)
                    v_spacing = y_values[0] - y_values[1]
                    print(f"  Vertical spacing: {v_spacing:.2f} mm")
                
                # Find margins
                min_x = min(p[0] for p in label_positions)
                max_y = max(p[1] for p in label_positions)
                left_margin = min_x
                top_margin = height_mm - max_y
                print(f"  Left margin (to first label center): {left_margin:.2f} mm")
                print(f"  Top margin (to first label center): {top_margin:.2f} mm")
        
        return width_mm, height_mm
        
    except ImportError as e:
        print(f"Import error: {e}", file=sys.stderr)
        print("Trying alternative import...", file=sys.stderr)
        try:
            import pypdf
            reader = pypdf.PdfReader(pdf_path)
            page = reader.pages[0]
            mediabox = page.mediabox
            width_pt = float(mediabox.width)
            height_pt = float(mediabox.height)
            width_mm = width_pt * 0.352778
            height_mm = height_pt * 0.352778
            print(f"Page Dimensions:")
            print(f"  Width: {width_mm:.2f} mm ({width_pt:.2f} points)")
            print(f"  Height: {height_mm:.2f} mm ({height_pt:.2f} points)")
            return width_mm, height_mm
        except Exception as e2:
            print(f"Error: {e2}", file=sys.stderr)
            return None, None
    except Exception as e:
        print(f"Error analyzing PDF: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    # Path relative to project root
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    pdf_path = os.path.join(project_root, "Avery6450_Templates", "Avery6450RoundLabels.pdf")
    analyze_pdf_template(pdf_path)
