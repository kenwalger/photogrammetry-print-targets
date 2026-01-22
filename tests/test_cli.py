"""Tests for CLI interface and integration."""

import os
import sys
import tempfile
from io import StringIO
from unittest.mock import patch

import pytest

from main import main, parse_arguments


class TestParseArguments:
    """Test suite for parse_arguments function."""

    def test_default_arguments(self):
        """Test that default arguments are correct."""
        with patch('sys.argv', ['main.py']):
            args = parse_arguments()
            assert args.dot_radius == 3.0
            assert args.bits == 8
            assert args.columns == 4
            assert args.markers_total == 12
            assert args.dpi == 300
            assert args.page_margin == 10.0
            assert args.marker_padding == 5.0

    def test_custom_arguments(self):
        """Test parsing custom arguments."""
        with patch('sys.argv', [
            'main.py',
            '--dot-radius', '5.0',
            '--bits', '10',
            '--columns', '6',
            '--markers', '20',
            '--dpi', '150',
            '--margin', '15.0',
            '--padding', '8.0'
        ]):
            args = parse_arguments()
            assert args.dot_radius == 5.0
            assert args.bits == 10
            assert args.columns == 6
            assert args.markers_total == 20
            assert args.dpi == 150
            assert args.page_margin == 15.0
            assert args.marker_padding == 8.0

    def test_output_options(self):
        """Test output-related arguments."""
        with patch('sys.argv', [
            'main.py',
            '--output-pdf', 'custom.pdf',
            '--output-dir', 'custom_dir',
            '--skip-svgs'
        ]):
            args = parse_arguments()
            assert args.output_pdf == 'custom.pdf'
            assert args.output_dir == 'custom_dir'
            assert args.skip_svgs is True
            assert args.skip_pdf is False

    def test_skip_options(self):
        """Test skip flags."""
        with patch('sys.argv', ['main.py', '--skip-pdf']):
            args = parse_arguments()
            assert args.skip_pdf is True
            assert args.skip_svgs is False

    def test_calibration_arguments(self):
        """Test calibration feature arguments."""
        with patch('sys.argv', [
            'main.py',
            '--cal-dot-radius', '3.0',
            '--cal-spacing', '25.0',
            '--cal-label', 'Custom label'
        ]):
            args = parse_arguments()
            assert args.cal_dot_radius == 3.0
            assert args.cal_dot_spacing == 25.0
            assert args.cal_label == 'Custom label'


class TestMainIntegration:
    """Integration tests for main function."""

    def test_main_with_defaults(self):
        """Test main function with default arguments (AVERY 6450)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('sys.argv', [
                'main.py',
                '--output-pdf', os.path.join(tmpdir, 'test.pdf'),
                '--output-dir', os.path.join(tmpdir, 'targets'),
                '--dpi', '150'  # Lower DPI for faster tests
            ]):
                # Capture stdout
                with patch('sys.stdout', new=StringIO()) as fake_out:
                    main()
                    output = fake_out.getvalue()
                    assert 'Generated AVERY 6450 PDF' in output
                    assert 'Generated' in output and 'individual SVG files' in output

    def test_main_skip_pdf(self):
        """Test main function skipping PDF generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('sys.argv', [
                'main.py',
                '--skip-pdf',
                '--output-dir', os.path.join(tmpdir, 'targets'),
                '--dpi', '150'
            ]):
                with patch('sys.stdout', new=StringIO()) as fake_out:
                    main()
                    output = fake_out.getvalue()
                    assert 'Generated combined PDF' not in output
                    assert 'individual SVG files' in output

    def test_main_skip_svgs(self):
        """Test main function skipping SVG generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('sys.argv', [
                'main.py',
                '--skip-svgs',
                '--output-pdf', os.path.join(tmpdir, 'test.pdf'),
                '--dpi', '150'
            ]):
                with patch('sys.stdout', new=StringIO()) as fake_out:
                    main()
                    output = fake_out.getvalue()
                    assert 'Generated AVERY 6450 PDF' in output
                    assert 'individual SVG files' not in output

    def test_main_validation_error(self):
        """Test main function with invalid configuration."""
        with patch('sys.argv', [
            'main.py',
            '--bits', '3',  # Invalid: too low
            '--output-pdf', '/tmp/test.pdf',
            '--output-dir', '/tmp/targets'
        ]):
            with patch('sys.stderr', new=StringIO()) as fake_err:
                with pytest.raises(SystemExit):
                    main()
                error_output = fake_err.getvalue()
                assert 'Error' in error_output

    def test_main_overlap_warning(self):
        """Test main function with overlap warning."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('sys.argv', [
                'main.py',
                '--dot-radius', '10.0',
                '--padding', '2.0',  # Insufficient padding
                '--output-pdf', os.path.join(tmpdir, 'test.pdf'),
                '--output-dir', os.path.join(tmpdir, 'targets'),
                '--dpi', '150'
            ]):
                with patch('sys.stderr', new=StringIO()) as fake_err:
                    with patch('sys.stdout', new=StringIO()):
                        main()
                        warning_output = fake_err.getvalue()
                        assert 'Warning' in warning_output
                        assert 'insufficient' in warning_output.lower()

    def test_main_creates_output_files(self):
        """Test that main function actually creates output files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            pdf_path = os.path.join(tmpdir, 'test.pdf')
            svg_dir = os.path.join(tmpdir, 'targets')
            
            with patch('sys.argv', [
                'main.py',
                '--markers', '3',  # Small number for faster test
                '--output-pdf', pdf_path,
                '--output-dir', svg_dir,
                '--dpi', '150'
            ]):
                with patch('sys.stdout', new=StringIO()):
                    main()
                    
                    # Check PDF was created
                    assert os.path.exists(pdf_path)
                    
                    # Check SVGs were created
                    assert os.path.exists(svg_dir)
                    svg_files = [f for f in os.listdir(svg_dir) if f.endswith('.svg')]
                    assert len(svg_files) == 3
