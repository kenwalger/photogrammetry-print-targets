"""Tests for rendering functions."""

import os
import tempfile
import shutil
from pathlib import Path

import pytest
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from main import (
    render_marker_to_axes,
    generate_combined_pdf,
    generate_individual_svgs,
    draw_calibration_feature
)


class TestRenderMarkerToAxes:
    """Test suite for render_marker_to_axes function."""

    def test_marker_rendered(self):
        """Test that marker is rendered to axes."""
        fig, ax = plt.subplots()
        ax.set_xlim(-20, 20)
        ax.set_ylim(-20, 20)
        
        render_marker_to_axes(ax, 0, 0, 3.0, 8, 1, 0, show_label=True)
        
        # Check that patches were added
        assert len(ax.patches) > 0
        plt.close(fig)

    def test_label_rendered(self):
        """Test that label is rendered when show_label=True."""
        fig, ax = plt.subplots()
        ax.set_xlim(-20, 20)
        ax.set_ylim(-20, 20)
        
        render_marker_to_axes(ax, 0, 0, 3.0, 8, 1, 5, show_label=True)
        
        # Check that text was added
        assert len(ax.texts) > 0
        assert any("6" in str(t.get_text()) for t in ax.texts)  # Index 5 -> label "6"
        plt.close(fig)

    def test_no_label_when_disabled(self):
        """Test that label is not rendered when show_label=False."""
        fig, ax = plt.subplots()
        ax.set_xlim(-20, 20)
        ax.set_ylim(-20, 20)
        
        render_marker_to_axes(ax, 0, 0, 3.0, 8, 1, 0, show_label=False)
        
        # Check that no text was added
        assert len(ax.texts) == 0
        plt.close(fig)

    def test_multiple_markers(self):
        """Test rendering multiple markers."""
        fig, ax = plt.subplots()
        ax.set_xlim(-50, 50)
        ax.set_ylim(-50, 50)
        
        for i in range(3):
            render_marker_to_axes(ax, i * 10, 0, 3.0, 8, i + 1, i, show_label=True)
        
        assert len(ax.patches) >= 3
        assert len(ax.texts) == 3
        plt.close(fig)


class TestDrawCalibrationFeature:
    """Test suite for draw_calibration_feature function."""

    def test_calibration_dots_rendered(self):
        """Test that calibration dots are rendered."""
        fig, ax = plt.subplots()
        ax.set_xlim(-10, 50)
        ax.set_ylim(-10, 10)
        
        draw_calibration_feature(ax, 0, 0, 2.0, 20.0, "Test label")
        
        # Should have 2 circles
        circles = [p for p in ax.patches if hasattr(p, 'radius')]
        assert len(circles) == 2
        plt.close(fig)

    def test_calibration_label_rendered(self):
        """Test that calibration label is rendered."""
        fig, ax = plt.subplots()
        ax.set_xlim(-10, 50)
        ax.set_ylim(-10, 10)
        
        draw_calibration_feature(ax, 0, 0, 2.0, 20.0, "Test label")
        
        # Should have label text
        assert len(ax.texts) > 0
        assert any("Test label" in str(t.get_text()) for t in ax.texts)
        plt.close(fig)

    def test_calibration_spacing(self):
        """Test that calibration dots have correct spacing."""
        fig, ax = plt.subplots()
        ax.set_xlim(-10, 50)
        ax.set_ylim(-10, 10)
        
        spacing = 20.0
        draw_calibration_feature(ax, 10.0, 5.0, 2.0, spacing, "Test")
        
        circles = [p for p in ax.patches if hasattr(p, 'center')]
        assert len(circles) == 2
        
        # Check spacing
        centers = [c.center for c in circles]
        x_coords = [c[0] for c in centers]
        assert abs(max(x_coords) - min(x_coords) - spacing) < 0.001
        plt.close(fig)


class TestGenerateCombinedPdf:
    """Test suite for generate_combined_pdf function."""

    def test_pdf_generated(self):
        """Test that PDF file is created."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test_output.pdf")
            codes = [1, 2, 3]
            
            generate_combined_pdf(
                codes=codes,
                dot_radius=3.0,
                bits=8,
                columns=2,
                page_margin=10.0,
                marker_padding=5.0,
                dpi=150,  # Lower DPI for faster tests
                cal_dot_radius=2.0,
                cal_dot_spacing=20.0,
                cal_label="Test",
                output_path=output_path
            )
            
            assert os.path.exists(output_path)
            assert os.path.getsize(output_path) > 0

    def test_pdf_with_different_configs(self):
        """Test PDF generation with different configurations."""
        with tempfile.TemporaryDirectory() as tmpdir:
            for columns in [2, 4, 6]:
                output_path = os.path.join(tmpdir, f"test_{columns}.pdf")
                codes = list(range(1, 13))
                
                generate_combined_pdf(
                    codes=codes,
                    dot_radius=3.0,
                    bits=8,
                    columns=columns,
                    page_margin=10.0,
                    marker_padding=5.0,
                    dpi=150,
                    cal_dot_radius=2.0,
                    cal_dot_spacing=20.0,
                    cal_label="Test",
                    output_path=output_path
                )
                
                assert os.path.exists(output_path)


class TestGenerateIndividualSvgs:
    """Test suite for generate_individual_svgs function."""

    def test_svgs_generated(self):
        """Test that SVG files are created."""
        with tempfile.TemporaryDirectory() as tmpdir:
            codes = [1, 2, 3]
            
            generate_individual_svgs(
                codes=codes,
                dot_radius=3.0,
                bits=8,
                output_dir=tmpdir
            )
            
            # Check that files were created
            for i, code in enumerate(codes):
                svg_path = os.path.join(tmpdir, f"target_{i + 1}.svg")
                assert os.path.exists(svg_path)
                assert os.path.getsize(svg_path) > 0

    def test_svg_naming(self):
        """Test that SVG files have correct naming."""
        with tempfile.TemporaryDirectory() as tmpdir:
            codes = [1, 2, 3, 4, 5]
            
            generate_individual_svgs(
                codes=codes,
                dot_radius=3.0,
                bits=8,
                output_dir=tmpdir
            )
            
            # Check naming sequence
            for i in range(len(codes)):
                expected_name = f"target_{i + 1}.svg"
                svg_path = os.path.join(tmpdir, expected_name)
                assert os.path.exists(svg_path)

    def test_directory_creation(self):
        """Test that output directory is created if it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            new_dir = os.path.join(tmpdir, "new_targets")
            codes = [1, 2]
            
            generate_individual_svgs(
                codes=codes,
                dot_radius=3.0,
                bits=8,
                output_dir=new_dir
            )
            
            assert os.path.exists(new_dir)
            assert os.path.isdir(new_dir)

    def test_multiple_svgs(self):
        """Test generation of multiple SVG files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            codes = list(range(1, 13))
            
            generate_individual_svgs(
                codes=codes,
                dot_radius=3.0,
                bits=8,
                output_dir=tmpdir
            )
            
            # Count SVG files
            svg_files = [f for f in os.listdir(tmpdir) if f.endswith('.svg')]
            assert len(svg_files) == len(codes)
