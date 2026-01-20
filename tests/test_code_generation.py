"""Tests for code generation functions."""

import pytest
from main import get_ring_codes


class TestGetRingCodes:
    """Test suite for get_ring_codes function."""

    def test_basic_generation(self):
        """Test basic code generation."""
        codes = get_ring_codes(bits=8, n=5)
        assert len(codes) == 5
        assert codes == [1, 2, 3, 4, 5]

    def test_sequential_codes(self):
        """Test that codes are sequential starting from 1."""
        codes = get_ring_codes(bits=8, n=10)
        assert codes == list(range(1, 11))

    def test_max_codes_limit(self):
        """Test that codes don't exceed maximum for bit count."""
        codes = get_ring_codes(bits=4, n=20)  # Only 15 codes available (1-15)
        assert len(codes) == 15
        assert codes == list(range(1, 16))
        assert max(codes) < 2 ** 4

    def test_exact_max_codes(self):
        """Test requesting exactly the maximum number of codes."""
        bits = 4
        max_codes = 2 ** bits - 1  # 15 codes (1-15)
        codes = get_ring_codes(bits=bits, n=max_codes)
        assert len(codes) == max_codes
        assert codes == list(range(1, max_codes + 1))

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
        assert codes == list(range(1, 101))

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
