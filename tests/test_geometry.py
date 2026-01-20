"""Tests for marker geometry functions."""

import pytest
from matplotlib.patches import Circle, Wedge
from main import get_coded_marker, RING_INNER_MULTIPLIER, RING_OUTER_MULTIPLIER


class TestGetCodedMarker:
    """Test suite for get_coded_marker function."""

    def test_center_dot_present(self):
        """Test that center dot is always present."""
        patches = get_coded_marker(0, 0, 3.0, 8, 1)
        assert len(patches) > 0
        assert any(isinstance(p, Circle) for p in patches)

    def test_center_dot_properties(self):
        """Test center dot has correct properties."""
        patches = get_coded_marker(10.0, 20.0, 3.0, 8, 1)
        circle = next(p for p in patches if isinstance(p, Circle))
        assert circle.center == (10.0, 20.0)
        assert circle.radius == 3.0
        assert circle.get_facecolor()[0] == 0.0  # Black

    def test_ring_segments_count(self):
        """Test that correct number of ring segments are created."""
        code = 0b10101010  # 4 bits set
        patches = get_coded_marker(0, 0, 3.0, 8, code)
        wedges = [p for p in patches if isinstance(p, Wedge)]
        assert len(wedges) == 4

    def test_all_bits_set(self):
        """Test marker with all bits set."""
        bits = 8
        code = 2 ** bits - 1  # All bits set
        patches = get_coded_marker(0, 0, 3.0, bits, code)
        wedges = [p for p in patches if isinstance(p, Wedge)]
        assert len(wedges) == bits

    def test_no_bits_set(self):
        """Test marker with no bits set (only center dot)."""
        patches = get_coded_marker(0, 0, 3.0, 8, 0)
        wedges = [p for p in patches if isinstance(p, Wedge)]
        assert len(wedges) == 0
        circles = [p for p in patches if isinstance(p, Circle)]
        assert len(circles) == 1

    def test_ring_geometry(self):
        """Test that ring segments have correct geometry."""
        dot_radius = 3.0
        patches = get_coded_marker(0, 0, dot_radius, 8, 1)
        wedges = [p for p in patches if isinstance(p, Wedge)]
        
        if wedges:
            wedge = wedges[0]
            expected_inner = dot_radius * RING_INNER_MULTIPLIER
            expected_outer = dot_radius * RING_OUTER_MULTIPLIER
            expected_width = expected_outer - expected_inner
            
            assert wedge.r == expected_outer
            assert wedge.width == expected_width

    def test_ring_angles(self):
        """Test that ring segments have correct angular distribution."""
        bits = 8
        code = 0b11111111  # All bits set
        patches = get_coded_marker(0, 0, 3.0, bits, code)
        wedges = [p for p in patches if isinstance(p, Wedge)]
        
        angle_step = 360.0 / bits
        for i, wedge in enumerate(wedges):
            expected_theta1 = i * angle_step
            expected_theta2 = (i + 1) * angle_step
            assert abs(wedge.theta1 - expected_theta1) < 0.001
            assert abs(wedge.theta2 - expected_theta2) < 0.001

    def test_different_bit_counts(self):
        """Test markers with different bit counts."""
        for bits in [4, 6, 8, 10]:
            code = 1  # First bit set
            patches = get_coded_marker(0, 0, 3.0, bits, code)
            wedges = [p for p in patches if isinstance(p, Wedge)]
            assert len(wedges) == 1

    def test_different_codes(self):
        """Test that different codes produce different patterns."""
        code1_patches = get_coded_marker(0, 0, 3.0, 8, 1)
        code2_patches = get_coded_marker(0, 0, 3.0, 8, 2)
        
        code1_wedges = [p for p in code1_patches if isinstance(p, Wedge)]
        code2_wedges = [p for p in code2_patches if isinstance(p, Wedge)]
        
        # Should have different wedge positions
        assert len(code1_wedges) == 1
        assert len(code2_wedges) == 1
        assert code1_wedges[0].theta1 != code2_wedges[0].theta1

    def test_position_independence(self):
        """Test that marker position doesn't affect geometry."""
        patches1 = get_coded_marker(0, 0, 3.0, 8, 5)
        patches2 = get_coded_marker(100, 200, 3.0, 8, 5)
        
        wedges1 = [p for p in patches1 if isinstance(p, Wedge)]
        wedges2 = [p for p in patches2 if isinstance(p, Wedge)]
        
        assert len(wedges1) == len(wedges2)
        # Geometry should be same, only position differs
        for w1, w2 in zip(wedges1, wedges2):
            assert w1.r == w2.r
            assert w1.width == w2.width
            assert w1.theta1 == w2.theta1
            assert w1.theta2 == w2.theta2

    def test_black_color(self):
        """Test that all patches are black."""
        patches = get_coded_marker(0, 0, 3.0, 8, 0b10101010)
        for patch in patches:
            facecolor = patch.get_facecolor()
            # Black is (0, 0, 0, 1) in RGBA
            assert facecolor[0] == 0.0
            assert facecolor[1] == 0.0
            assert facecolor[2] == 0.0
