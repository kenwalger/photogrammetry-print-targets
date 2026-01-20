"""Tests for code generation functions."""

import pytest
from main import (
    get_ring_codes,
    rotate_code,
    canonical_rotation,
    is_rotationally_invariant,
    generate_rotationally_invariant_codes
)


class TestGetRingCodes:
    """Test suite for get_ring_codes function."""

    def test_basic_generation(self):
        """Test basic code generation."""
        codes = get_ring_codes(bits=8, n=5)
        assert len(codes) == 5
        # Codes should be rotationally invariant (not sequential)
        assert codes[0] == 1  # First code is always 1
        assert all(code > 0 for code in codes)

    def test_rotationally_invariant_codes(self):
        """Test that generated codes are rotationally invariant."""
        codes = get_ring_codes(bits=8, n=10)
        # All codes should be in canonical form
        for code in codes:
            assert is_rotationally_invariant(code, 8)

    def test_max_codes_limit(self):
        """Test that codes don't exceed maximum for bit count."""
        codes = get_ring_codes(bits=4, n=20)
        # Should return available rotationally invariant codes
        assert len(codes) <= 20
        assert all(code < 2 ** 4 for code in codes)
        assert all(is_rotationally_invariant(code, 4) for code in codes)

    def test_industry_standard_8bit(self):
        """Test that 8-bit codes use industry standard patterns."""
        codes = get_ring_codes(bits=8, n=30)
        # Should use industry standard codes (generated, not hardcoded)
        assert len(codes) == 30
        assert codes[0] == 1  # First code is always 1
        # All should be rotationally invariant
        for code in codes:
            assert is_rotationally_invariant(code, 8), \
                f"Code {code} (0b{code:08b}) is not rotationally invariant"

    def test_single_code(self):
        """Test generating a single code."""
        codes = get_ring_codes(bits=8, n=1)
        assert len(codes) == 1
        assert codes == [1]

    def test_different_bit_counts(self):
        """Test code generation with different bit counts."""
        for bits in [4, 6, 8, 10, 12]:
            codes = get_ring_codes(bits=bits, n=5)
            assert len(codes) == 5
            assert all(1 <= code < 2 ** bits for code in codes)

    def test_large_bit_count(self):
        """Test code generation with large bit count."""
        codes = get_ring_codes(bits=16, n=100)
        assert len(codes) == 100
        # All codes should be rotationally invariant
        for code in codes:
            assert is_rotationally_invariant(code, 16)
            assert 1 <= code < 2 ** 16

    def test_codes_never_zero(self):
        """Test that codes never include zero."""
        for bits in [4, 8, 12]:
            codes = get_ring_codes(bits=bits, n=50)
            assert 0 not in codes
            assert all(code > 0 for code in codes)

    def test_deterministic_output(self):
        """Test that function produces deterministic output."""
        codes1 = get_ring_codes(bits=8, n=10)
        codes2 = get_ring_codes(bits=8, n=10)
        assert codes1 == codes2

    def test_all_codes_unique(self):
        """Test that all generated codes are unique."""
        codes = get_ring_codes(bits=8, n=50)
        assert len(codes) == len(set(codes))

    def test_rotational_invariance_property(self):
        """Test that rotated codes map to the same canonical code."""
        codes = get_ring_codes(bits=8, n=10)
        for code in codes:
            canonical = canonical_rotation(code, 8)
            # Rotate the code and verify it maps to same canonical
            for rotation in range(1, 8):
                rotated = rotate_code(code, 8, rotation)
                rotated_canonical = canonical_rotation(rotated, 8)
                assert rotated_canonical == canonical, \
                    f"Code {code} rotated {rotation} should map to {canonical}, got {rotated_canonical}"


class TestRotationalInvariance:
    """Test suite for rotational invariance functions."""

    def test_rotate_code(self):
        """Test code rotation."""
        # 8-bit code: 0b00000001 (1) rotated left by 1 = 0b00000010 (2)
        assert rotate_code(1, 8, 1) == 2
        # Rotated by 8 (full rotation) should be same
        assert rotate_code(1, 8, 8) == 1
        # Rotated by 4 (half rotation) for 8 bits
        assert rotate_code(0b00001111, 8, 4) == 0b11110000

    def test_canonical_rotation(self):
        """Test canonical rotation finding."""
        # Code 2 (0b00000010) should canonicalize to 1 (0b00000001)
        assert canonical_rotation(2, 8) == 1
        # Code 4 (0b00000100) should canonicalize to 1
        assert canonical_rotation(4, 8) == 1
        # Code 3 (0b00000011) is already canonical
        assert canonical_rotation(3, 8) == 3

    def test_is_rotationally_invariant(self):
        """Test rotationally invariant check."""
        # Code 1 is canonical
        assert is_rotationally_invariant(1, 8) is True
        # Code 2 is not canonical (rotates to 1)
        assert is_rotationally_invariant(2, 8) is False
        # Code 3 is canonical
        assert is_rotationally_invariant(3, 8) is True
        # Code 0 is canonical (but not a valid marker)
        assert is_rotationally_invariant(0, 8) is True

    def test_generate_rotationally_invariant_codes(self):
        """Test algorithmic generation of rotationally invariant codes."""
        codes = generate_rotationally_invariant_codes(bits=8, n=10)
        assert len(codes) == 10
        # All should be rotationally invariant
        for code in codes:
            assert is_rotationally_invariant(code, 8)
        # Should start with 1
        assert codes[0] == 1
