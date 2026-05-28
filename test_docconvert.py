#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for DocConvert-CLI."""

import os
import tempfile
import pytest
from pathlib import Path

from docconvert import (
    FormatDetector,
    EncodingDetector,
    ConversionConfig,
    DocumentConverter,
)


class TestFormatDetector:
    """Tests for FormatDetector class."""
    
    def test_detect_from_extension_markdown(self):
        assert FormatDetector.detect_from_extension("test.md") == "markdown"
        assert FormatDetector.detect_from_extension("test.markdown") == "markdown"
        assert FormatDetector.detect_from_extension("test.mkd") == "markdown"
    
    def test_detect_from_extension_html(self):
        assert FormatDetector.detect_from_extension("test.html") == "html"
        assert FormatDetector.detect_from_extension("test.htm") == "html"
    
    def test_detect_from_extension_pdf(self):
        assert FormatDetector.detect_from_extension("test.pdf") == "pdf"
    
    def test_detect_from_extension_docx(self):
        assert FormatDetector.detect_from_extension("test.docx") == "docx"
        assert FormatDetector.detect_from_extension("test.doc") == "docx"
    
    def test_detect_from_extension_txt(self):
        assert FormatDetector.detect_from_extension("test.txt") == "txt"
    
    def test_detect_from_content_html(self):
        content = "<!DOCTYPE html><html><body>Test</body></html>"
        assert FormatDetector.detect_from_content(content) == "html"
    
    def test_detect_from_content_markdown(self):
        content = "# Heading\n\nThis is **bold** text."
        assert FormatDetector.detect_from_content(content) == "markdown"
    
    def test_detect_from_content_unknown(self):
        content = "Just plain text without any specific markers."
        assert FormatDetector.detect_from_content(content) is None


class TestEncodingDetector:
    """Tests for EncodingDetector class."""
    
    def test_detect_utf8(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Hello, World! 你好，世界！")
            temp_path = f.name
        
        try:
            encoding = EncodingDetector.detect(temp_path)
            assert encoding in ['utf-8', 'utf-8-sig']
        finally:
            os.unlink(temp_path)
    
    def test_detect_with_fallback(self):
        # Create a file with binary content
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.bin', delete=False) as f:
            f.write(b'\x80\x81\x82\x83')
            temp_path = f.name
        
        try:
            encoding = EncodingDetector.detect(temp_path)
            # Should fallback to one of the supported encodings
            assert encoding in ['utf-8', 'latin-1', 'cp1252']
        finally:
            os.unlink(temp_path)


class TestDocumentConverter:
    """Tests for DocumentConverter class."""
    
    def test_generate_output_path(self):
        config = ConversionConfig(output_format='html')
        converter = DocumentConverter(config)
        
        output_path = converter._generate_output_path("test.md", "html")
        assert output_path.endswith(".html")
        assert "test" in output_path
    
    def test_generate_output_path_with_output_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ConversionConfig(output_format='html', output_dir=tmpdir)
            converter = DocumentConverter(config)
            
            output_path = converter._generate_output_path("test.md", "html")
            assert output_path.startswith(tmpdir)
            assert output_path.endswith("test.html")
    
    def test_md_to_html_conversion(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "input.md")
            output_path = os.path.join(tmpdir, "output.html")
            
            with open(input_path, 'w', encoding='utf-8') as f:
                f.write("# Hello World\n\nThis is a test.")
            
            config = ConversionConfig(output_format='html')
            converter = DocumentConverter(config)
            
            success = converter.convert(input_path, output_path)
            assert success
            assert os.path.exists(output_path)
            
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
                assert "Hello World" in content
                assert "<!DOCTYPE html>" in content
    
    def test_html_to_md_conversion(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "input.html")
            output_path = os.path.join(tmpdir, "output.md")
            
            with open(input_path, 'w', encoding='utf-8') as f:
                f.write("<h1>Hello World</h1><p>This is a test.</p>")
            
            config = ConversionConfig(output_format='markdown')
            converter = DocumentConverter(config)
            
            success = converter.convert(input_path, output_path)
            assert success
            assert os.path.exists(output_path)
            
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
                assert "Hello World" in content
    
    def test_txt_to_md_conversion(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "input.txt")
            output_path = os.path.join(tmpdir, "output.md")
            
            with open(input_path, 'w', encoding='utf-8') as f:
                f.write("Hello World\n\nThis is a test.")
            
            config = ConversionConfig(output_format='markdown')
            converter = DocumentConverter(config)
            
            success = converter.convert(input_path, output_path)
            assert success
            assert os.path.exists(output_path)
    
    def test_same_format_copy(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "input.md")
            output_path = os.path.join(tmpdir, "output.md")
            
            with open(input_path, 'w', encoding='utf-8') as f:
                f.write("# Test")
            
            config = ConversionConfig(output_format='markdown')
            converter = DocumentConverter(config)
            
            success = converter.convert(input_path, output_path)
            assert success
            assert os.path.exists(output_path)
            
            with open(output_path, 'r', encoding='utf-8') as f:
                assert f.read() == "# Test"


class TestConversionConfig:
    """Tests for ConversionConfig dataclass."""
    
    def test_default_values(self):
        config = ConversionConfig()
        assert config.input_format is None
        assert config.output_format is None
        assert config.output_dir is None
        assert config.template is None
        assert config.encoding == "utf-8"
        assert config.preserve_metadata is True
        assert config.verbose is False
    
    def test_custom_values(self):
        config = ConversionConfig(
            input_format="markdown",
            output_format="html",
            output_dir="/tmp/output",
            encoding="gbk",
            verbose=True
        )
        assert config.input_format == "markdown"
        assert config.output_format == "html"
        assert config.output_dir == "/tmp/output"
        assert config.encoding == "gbk"
        assert config.verbose is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
