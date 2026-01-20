"""Tests for validation functions."""

import pytest
from main import validate_config, check_marker_overlap


class TestValidateConfig:
    """Test suite for validate_config function."""

    def test_valid_config(self):
        """Test that valid configuration passes validation."""
        is_valid, error_msg = validate_config(
            dot_radius=3.0,
            bits=8,
            columns=4,
            markers_total=12,
            page_margin=10.0,
            marker_padding=5.0,
            cal_dot_spacing=20.0
        )
        assert is_valid is True
        assert error_msg == ""

    def test_negative_dot_radius(self):
        """Test that negative dot radius is rejected."""
        is_valid, error_msg = validate_config(
            dot_radius=-1.0,
            bits=8,
            columns=4,
            markers_total=12,
            page_margin=10.0,
            marker_padding=5.0,
            cal_dot_spacing=20.0
        )
        assert is_valid is False
        assert "positive" in error_msg.lower()

    def test_zero_dot_radius(self):
        """Test that zero dot radius is rejected."""
        is_valid, error_msg = validate_config(
            dot_radius=0.0,
            bits=8,
            columns=4,
            markers_total=12,
            page_margin=10.0,
            marker_padding=5.0,
            cal_dot_spacing=20.0
        )
        assert is_valid is False
        assert "positive" in error_msg.lower()

    def test_bits_too_low(self):
        """Test that bits < 4 is rejected."""
        is_valid, error_msg = validate_config(
            dot_radius=3.0,
            bits=3,
            columns=4,
            markers_total=12,
            page_margin=10.0,
            marker_padding=5.0,
            cal_dot_spacing=20.0
        )
        assert is_valid is False
        assert "between 4 and 16" in error_msg

    def test_bits_too_high(self):
        """Test that bits > 16 is rejected."""
        is_valid, error_msg = validate_config(
            dot_radius=3.0,
            bits=17,
            columns=4,
            markers_total=12,
            page_margin=10.0,
            marker_padding=5.0,
            cal_dot_spacing=20.0
        )
        assert is_valid is False
        assert "between 4 and 16" in error_msg

    def test_zero_columns(self):
        """Test that zero columns is rejected."""
        is_valid, error_msg = validate_config(
            dot_radius=3.0,
            bits=8,
            columns=0,
            markers_total=12,
            page_margin=10.0,
            marker_padding=5.0,
            cal_dot_spacing=20.0
        )
        assert is_valid is False
        assert "at least 1" in error_msg

    def test_zero_markers(self):
        """Test that zero markers is rejected."""
        is_valid, error_msg = validate_config(
            dot_radius=3.0,
            bits=8,
            columns=4,
            markers_total=0,
            page_margin=10.0,
            marker_padding=5.0,
            cal_dot_spacing=20.0
        )
        assert is_valid is False
        assert "at least 1" in error_msg

    def test_negative_margin(self):
        """Test that negative margin is rejected."""
        is_valid, error_msg = validate_config(
            dot_radius=3.0,
            bits=8,
            columns=4,
            markers_total=12,
            page_margin=-1.0,
            marker_padding=5.0,
            cal_dot_spacing=20.0
        )
        assert is_valid is False
        assert "non-negative" in error_msg.lower()

    def test_negative_padding(self):
        """Test that negative padding is rejected."""
        is_valid, error_msg = validate_config(
            dot_radius=3.0,
            bits=8,
            columns=4,
            markers_total=12,
            page_margin=10.0,
            marker_padding=-1.0,
            cal_dot_spacing=20.0
        )
        assert is_valid is False
        assert "non-negative" in error_msg.lower()

    def test_zero_cal_spacing(self):
        """Test that zero calibration spacing is rejected."""
        is_valid, error_msg = validate_config(
            dot_radius=3.0,
            bits=8,
            columns=4,
            markers_total=12,
            page_margin=10.0,
            marker_padding=5.0,
            cal_dot_spacing=0.0
        )
        assert is_valid is False
        assert "positive" in error_msg.lower()

    def test_markers_exceed_code_limit(self):
        """Test that requesting more markers than available codes is rejected."""
        is_valid, error_msg = validate_config(
            dot_radius=3.0,
            bits=4,  # Only 15 codes available (1-15)
            columns=4,
            markers_total=16,  # Too many!
            page_margin=10.0,
            marker_padding=5.0,
            cal_dot_spacing=20.0
        )
        assert is_valid is False
        assert "exceeds maximum codes" in error_msg

    def test_markers_at_code_limit(self):
        """Test that requesting exactly the maximum codes is valid."""
        is_valid, error_msg = validate_config(
            dot_radius=3.0,
            bits=4,  # 15 codes available (1-15)
            columns=4,
            markers_total=15,  # Exactly the limit
            page_margin=10.0,
            marker_padding=5.0,
            cal_dot_spacing=20.0
        )
        assert is_valid is True
        assert error_msg == ""

    def test_edge_case_bits_4(self):
        """Test minimum valid bits value."""
        is_valid, error_msg = validate_config(
            dot_radius=3.0,
            bits=4,
            columns=4,
            markers_total=10,
            page_margin=10.0,
            marker_padding=5.0,
            cal_dot_spacing=20.0
        )
        assert is_valid is True

    def test_edge_case_bits_16(self):
        """Test maximum valid bits value."""
        is_valid, error_msg = validate_config(
            dot_radius=3.0,
            bits=16,
            columns=4,
            markers_total=100,
            page_margin=10.0,
            marker_padding=5.0,
            cal_dot_spacing=20.0
        )
        assert is_valid is True


class TestCheckMarkerOverlap:
    """Test suite for check_marker_overlap function."""

    def test_sufficient_padding(self):
        """Test that sufficient padding passes overlap check."""
        no_overlap, warning_msg = check_marker_overlap(
            dot_radius=3.0,
            marker_padding=20.0
        )
        assert no_overlap is True
        assert warning_msg == ""

    def test_insufficient_padding(self):
        """Test that insufficient padding triggers warning."""
        no_overlap, warning_msg = check_marker_overlap(
            dot_radius=3.0,
            marker_padding=2.0  # Too small
        )
        assert no_overlap is False
        assert "insufficient" in warning_msg.lower()
        assert "padding" in warning_msg.lower()

    def test_exact_minimum_padding(self):
        """Test that exact minimum padding passes."""
        dot_radius = 3.0
        marker_size = dot_radius * 6.0  # MARKER_SIZE_MULTIPLIER
        marker_radius = marker_size / 2
        min_padding = marker_radius * 2

        no_overlap, warning_msg = check_marker_overlap(
            dot_radius=dot_radius,
            marker_padding=min_padding
        )
        assert no_overlap is True
        assert warning_msg == ""

    def test_large_dot_radius(self):
        """Test overlap detection with larger dot radius."""
        no_overlap, warning_msg = check_marker_overlap(
            dot_radius=10.0,
            marker_padding=5.0  # Definitely insufficient
        )
        assert no_overlap is False
        assert "insufficient" in warning_msg.lower()

    def test_zero_padding(self):
        """Test that zero padding triggers warning."""
        no_overlap, warning_msg = check_marker_overlap(
            dot_radius=3.0,
            marker_padding=0.0
        )
        assert no_overlap is False
        assert "insufficient" in warning_msg.lower()
