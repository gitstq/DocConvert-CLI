#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DocConvert-CLI: A lightweight, cross-platform document format conversion tool.

This tool provides seamless conversion between popular document formats including
Markdown, HTML, PDF, DOCX, and TXT with zero configuration required.

Author: DocConvert Team
License: MIT
Version: 1.0.0
"""

import os
import sys
import re
import glob
import json
import codecs
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

# Document processing libraries
try:
    import markdown
    from markdown.extensions import fenced_code, tables, toc
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

try:
    from docx import Document
    from docx.shared import Pt, Inches, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

try:
    import pypandoc
    PYPANDOC_AVAILABLE = True
except ImportError:
    PYPANDOC_AVAILABLE = False


console = Console()


@dataclass
class ConversionConfig:
    """Configuration for document conversion."""
    input_format: Optional[str] = None
    output_format: Optional[str] = None
    output_dir: Optional[str] = None
    template: Optional[str] = None
    encoding: str = "utf-8"
    preserve_metadata: bool = True
    verbose: bool = False


class FormatDetector:
    """Detects document format from file content and extension."""
    
    FORMAT_SIGNATURES = {
        'html': [r'<\s*html', r'<\s*!DOCTYPE\s+html', r'<\s*head', r'<\s*body'],
        'markdown': [r'^#{1,6}\s', r'\[.*?\]\(.*?\)', r'\*\*.*?\*\*', r'`.*?`', r'```'],
        'json': [r'^\s*\{', r'^\s*\['],
    }
    
    EXTENSION_MAP = {
        '.md': 'markdown',
        '.markdown': 'markdown',
        '.mkd': 'markdown',
        '.html': 'html',
        '.htm': 'html',
        '.pdf': 'pdf',
        '.docx': 'docx',
        '.doc': 'docx',
        '.txt': 'txt',
        '.text': 'txt',
        '.json': 'json',
        '.xml': 'xml',
    }
    
    @classmethod
    def detect_from_extension(cls, filepath: str) -> Optional[str]:
        """Detect format from file extension."""
        ext = Path(filepath).suffix.lower()
        return cls.EXTENSION_MAP.get(ext)
    
    @classmethod
    def detect_from_content(cls, content: str) -> Optional[str]:
        """Detect format from file content."""
        for fmt, patterns in cls.FORMAT_SIGNATURES.items():
            for pattern in patterns:
                if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                    return fmt
        return None
    
    @classmethod
    def detect(cls, filepath: str) -> Optional[str]:
        """Detect format using multiple methods."""
        # Try extension first
        fmt = cls.detect_from_extension(filepath)
        if fmt:
            return fmt
        
        # Try content detection
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(4096)  # Read first 4KB
                return cls.detect_from_content(content)
        except Exception:
            pass
        
        return None


class EncodingDetector:
    """Detects file encoding."""
    
    @staticmethod
    def detect(filepath: str) -> str:
        """Detect file encoding using various methods."""
        # Try common encodings
        encodings = ['utf-8', 'utf-8-sig', 'gbk', 'gb2312', 'latin-1', 'cp1252']
        
        for encoding in encodings:
            try:
                with open(filepath, 'r', encoding=encoding) as f:
                    f.read()
                return encoding
            except (UnicodeDecodeError, UnicodeError):
                continue
        
        return 'utf-8'  # Default fallback


class DocumentConverter:
    """Main document conversion engine."""
    
    SUPPORTED_FORMATS = ['markdown', 'md', 'html', 'pdf', 'docx', 'doc', 'txt', 'text']
    
    def __init__(self, config: ConversionConfig):
        self.config = config
        self.stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'skipped': 0
        }
    
    def convert(self, input_path: str, output_path: Optional[str] = None) -> bool:
        """Convert a single document."""
        try:
            # Detect input format
            input_format = self.config.input_format or FormatDetector.detect(input_path)
            if not input_format:
                console.print(f"[red]❌ Could not detect format for: {input_path}[/red]")
                self.stats['failed'] += 1
                return False
            
            input_format = input_format.lower()
            
            # Determine output format
            output_format = self.config.output_format
            if not output_format and output_path:
                output_format = FormatDetector.detect_from_extension(output_path)
            if not output_format:
                console.print(f"[red]❌ Output format not specified[/red]")
                self.stats['failed'] += 1
                return False
            
            output_format = output_format.lower()
            
            # Normalize format names
            if input_format in ['md', 'mkd']:
                input_format = 'markdown'
            if output_format in ['md', 'mkd']:
                output_format = 'markdown'
            
            # Generate output path if not provided
            if not output_path:
                output_path = self._generate_output_path(input_path, output_format)
            
            # Ensure output directory exists
            output_dir = os.path.dirname(output_path) or '.'
            os.makedirs(output_dir, exist_ok=True)
            
            # Perform conversion
            success = self._perform_conversion(input_path, output_path, input_format, output_format)
            
            if success:
                self.stats['success'] += 1
                console.print(f"[green]✓[/green] Converted: [cyan]{input_path}[/cyan] → [green]{output_path}[/green]")
            else:
                self.stats['failed'] += 1
            
            return success
            
        except Exception as e:
            console.print(f"[red]❌ Error converting {input_path}: {str(e)}[/red]")
            self.stats['failed'] += 1
            return False
    
    def _generate_output_path(self, input_path: str, output_format: str) -> str:
        """Generate output file path."""
        input_path_obj = Path(input_path)
        
        # Determine extension
        ext_map = {
            'markdown': '.md',
            'md': '.md',
            'html': '.html',
            'pdf': '.pdf',
            'docx': '.docx',
            'doc': '.docx',
            'txt': '.txt',
            'text': '.txt',
        }
        ext = ext_map.get(output_format, f'.{output_format}')
        
        # Use configured output directory or same directory as input
        if self.config.output_dir:
            output_dir = Path(self.config.output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
        else:
            output_dir = input_path_obj.parent
        
        output_name = input_path_obj.stem + ext
        return str(output_dir / output_name)
    
    def _perform_conversion(self, input_path: str, output_path: str, 
                           input_format: str, output_format: str) -> bool:
        """Perform the actual conversion."""
        
        # Same format - just copy
        if input_format == output_format:
            import shutil
            shutil.copy2(input_path, output_path)
            return True
        
        # Read input file
        encoding = EncodingDetector.detect(input_path)
        
        try:
            with open(input_path, 'r', encoding=encoding, errors='ignore') as f:
                content = f.read()
        except Exception as e:
            console.print(f"[red]❌ Error reading file: {e}[/red]")
            return False
        
        # Route to specific converter
        conversion_key = f"{input_format}_to_{output_format}"
        
        converters = {
            'markdown_to_html': self._md_to_html,
            'md_to_html': self._md_to_html,
            'html_to_markdown': self._html_to_md,
            'html_to_md': self._html_to_md,
            'markdown_to_txt': self._md_to_txt,
            'md_to_txt': self._md_to_txt,
            'html_to_txt': self._html_to_txt,
            'txt_to_markdown': self._txt_to_md,
            'txt_to_md': self._txt_to_md,
            'txt_to_html': self._txt_to_html,
        }
        
        converter = converters.get(conversion_key)
        
        if converter:
            return converter(content, output_path)
        
        # Try using pypandoc for other conversions
        if PYPANDOC_AVAILABLE:
            return self._pandoc_convert(input_path, output_path, input_format, output_format)
        
        console.print(f"[yellow]⚠ Conversion from {input_format} to {output_format} not yet supported[/yellow]")
        return False
    
    def _md_to_html(self, content: str, output_path: str) -> bool:
        """Convert Markdown to HTML."""
        if MARKDOWN_AVAILABLE:
            extensions = ['fenced_code', 'tables', 'toc', 'nl2br']
            html_content = markdown.markdown(content, extensions=extensions)
            
            # Wrap in basic HTML template
            full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Converted Document</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
               max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
        pre {{ background: #f4f4f4; padding: 10px; border-radius: 4px; overflow-x: auto; }}
        code {{ background: #f4f4f4; padding: 2px 4px; border-radius: 3px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background: #f4f4f4; }}
        blockquote {{ border-left: 4px solid #ddd; margin: 0; padding-left: 16px; color: #666; }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
        else:
            # Fallback: simple conversion
            full_html = self._simple_md_to_html(content)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_html)
        return True
    
    def _simple_md_to_html(self, content: str) -> str:
        """Simple Markdown to HTML conversion (fallback)."""
        html = content
        # Headers
        html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        # Bold and italic
        html = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', html)
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
        # Code
        html = re.sub(r'`(.*?)`', r'<code>\1</code>', html)
        # Links
        html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)
        # Paragraphs
        html = '<p>' + html.replace('\n\n', '</p><p>') + '</p>'
        html = html.replace('\n', '<br>')
        
        return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head><body>{html}</body></html>"""
    
    def _html_to_md(self, content: str, output_path: str) -> bool:
        """Convert HTML to Markdown."""
        if BS4_AVAILABLE:
            soup = BeautifulSoup(content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Convert to markdown-like format
            md_content = self._soup_to_md(soup)
        else:
            # Fallback: strip tags
            md_content = re.sub(r'<[^>]+>', '', content)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        return True
    
    def _soup_to_md(self, soup: BeautifulSoup) -> str:
        """Convert BeautifulSoup object to Markdown."""
        md_parts = []
        
        for elem in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'pre', 'code', 'a', 'ul', 'ol', 'li', 'blockquote']):
            text = elem.get_text(strip=True)
            if not text:
                continue
            
            if elem.name == 'h1':
                md_parts.append(f"# {text}\n")
            elif elem.name == 'h2':
                md_parts.append(f"## {text}\n")
            elif elem.name == 'h3':
                md_parts.append(f"### {text}\n")
            elif elem.name == 'p':
                md_parts.append(f"{text}\n")
            elif elem.name == 'pre':
                md_parts.append(f"```\n{text}\n```\n")
            elif elem.name == 'code':
                md_parts.append(f"`{text}`")
            elif elem.name == 'a':
                href = elem.get('href', '')
                md_parts.append(f"[{text}]({href})")
            elif elem.name == 'blockquote':
                md_parts.append(f"> {text}\n")
        
        return '\n'.join(md_parts)
    
    def _md_to_txt(self, content: str, output_path: str) -> bool:
        """Convert Markdown to plain text."""
        # Remove markdown syntax
        text = content
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # Links
        text = re.sub(r'[#*`~]', '', text)  # Formatting chars
        text = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'[Image: \1]', text)  # Images
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        return True
    
    def _html_to_txt(self, content: str, output_path: str) -> bool:
        """Convert HTML to plain text."""
        if BS4_AVAILABLE:
            soup = BeautifulSoup(content, 'html.parser')
            # Remove script and style
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text(separator='\n', strip=True)
        else:
            text = re.sub(r'<[^>]+>', ' ', content)
            text = re.sub(r'\s+', ' ', text).strip()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        return True
    
    def _txt_to_md(self, content: str, output_path: str) -> bool:
        """Convert plain text to Markdown (wrap paragraphs)."""
        paragraphs = content.split('\n\n')
        md_content = '\n\n'.join(p.strip() for p in paragraphs if p.strip())
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        return True
    
    def _txt_to_html(self, content: str, output_path: str) -> bool:
        """Convert plain text to HTML."""
        paragraphs = content.split('\n\n')
        html_paragraphs = ''.join(f'<p>{p.strip()}</p>' for p in paragraphs if p.strip())
        
        html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head><body>{html_paragraphs}</body></html>"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    
    def _pandoc_convert(self, input_path: str, output_path: str, 
                       input_format: str, output_format: str) -> bool:
        """Use pypandoc for conversion."""
        try:
            # Map format names
            format_map = {
                'markdown': 'markdown',
                'md': 'markdown',
                'html': 'html',
                'pdf': 'pdf',
                'docx': 'docx',
                'doc': 'docx',
                'txt': 'plain',
            }
            
            input_fmt = format_map.get(input_format, input_format)
            output_fmt = format_map.get(output_format, output_format)
            
            pypandoc.convert_file(input_path, output_fmt, format=input_fmt, 
                                 outputfile=output_path)
            return True
        except Exception as e:
            if self.config.verbose:
                console.print(f"[yellow]⚠ Pandoc conversion failed: {e}[/yellow]")
            return False
    
    def batch_convert(self, pattern: str, output_format: str) -> None:
        """Convert multiple files matching a pattern."""
        files = glob.glob(pattern, recursive=True)
        
        if not files:
            console.print(f"[yellow]⚠ No files found matching: {pattern}[/yellow]")
            return
        
        self.stats['total'] = len(files)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            task = progress.add_task(f"Converting to {output_format}...", total=len(files))
            
            for filepath in files:
                if os.path.isfile(filepath):
                    self.config.output_format = output_format
                    self.convert(filepath)
                progress.advance(task)
        
        self._print_stats()
    
    def _print_stats(self) -> None:
        """Print conversion statistics."""
        table = Table(title="Conversion Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Count", style="green")
        
        table.add_row("Total Files", str(self.stats['total']))
        table.add_row("✓ Successful", str(self.stats['success']), style="green")
        table.add_row("✗ Failed", str(self.stats['failed']), style="red" if self.stats['failed'] > 0 else "green")
        table.add_row("○ Skipped", str(self.stats['skipped']), style="yellow")
        
        console.print(table)


@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, help='Show version information')
@click.pass_context
def cli(ctx, version):
    """DocConvert-CLI: Lightweight document format conversion tool.
    
    Examples:
        docconvert convert input.md --to html
        docconvert convert input.html --to markdown --output output.md
        docconvert batch "*.md" --to html
    """
    if version:
        console.print("[bold cyan]DocConvert-CLI[/bold cyan] v1.0.0")
        console.print("A lightweight document format conversion tool")
        return
    
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())


@cli.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--to', '-t', 'output_format', help='Output format (md, html, pdf, docx, txt)')
@click.option('--output', '-o', 'output_path', help='Output file path')
@click.option('--output-dir', '-d', help='Output directory')
@click.option('--encoding', '-e', default='utf-8', help='File encoding')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def convert(input_path, output_format, output_path, output_dir, encoding, verbose):
    """Convert a single document."""
    config = ConversionConfig(
        output_format=output_format,
        output_dir=output_dir,
        encoding=encoding,
        verbose=verbose
    )
    
    converter = DocumentConverter(config)
    success = converter.convert(input_path, output_path)
    
    sys.exit(0 if success else 1)


@cli.command()
@click.argument('pattern')
@click.option('--to', '-t', 'output_format', required=True, help='Output format')
@click.option('--output-dir', '-d', help='Output directory')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def batch(pattern, output_format, output_dir, verbose):
    """Convert multiple documents matching a pattern."""
    config = ConversionConfig(
        output_dir=output_dir,
        verbose=verbose
    )
    
    converter = DocumentConverter(config)
    converter.batch_convert(pattern, output_format)


@cli.command()
def formats():
    """List supported formats and their availability."""
    table = Table(title="Supported Formats")
    table.add_column("Format", style="cyan")
    table.add_column("Extensions", style="yellow")
    table.add_column("Status", style="green")
    
    formats_info = [
        ("Markdown", ".md, .markdown, .mkd", "✓ Native"),
        ("HTML", ".html, .htm", "✓ Native"),
        ("Plain Text", ".txt, .text", "✓ Native"),
        ("PDF", ".pdf", "⚠ Pandoc required" if not PYMUPDF_AVAILABLE else "✓ Native"),
        ("Word", ".docx, .doc", "⚠ Pandoc required" if not DOCX_AVAILABLE else "✓ Native"),
    ]
    
    for fmt, ext, status in formats_info:
        table.add_row(fmt, ext, status)
    
    console.print(table)
    
    # Print library status
    console.print("\n[bold]Optional Dependencies:[/bold]")
    libs = [
        ("pypandoc", PYPANDOC_AVAILABLE, "Extended format support"),
        ("python-docx", DOCX_AVAILABLE, "Word document support"),
        ("pymupdf", PYMUPDF_AVAILABLE, "PDF processing"),
        ("beautifulsoup4", BS4_AVAILABLE, "HTML parsing"),
        ("markdown", MARKDOWN_AVAILABLE, "Markdown processing"),
    ]
    
    for lib, available, desc in libs:
        status = "[green]✓[/green]" if available else "[red]✗[/red]"
        console.print(f"  {status} {lib}: {desc}")


@cli.command()
@click.argument('filepath', type=click.Path(exists=True))
def detect(filepath):
    """Detect the format of a document."""
    detected_format = FormatDetector.detect(filepath)
    encoding = EncodingDetector.detect(filepath)
    
    table = Table(title=f"File Analysis: {filepath}")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="yellow")
    
    table.add_row("Detected Format", detected_format or "Unknown")
    table.add_row("File Encoding", encoding)
    table.add_row("File Size", f"{os.path.getsize(filepath):,} bytes")
    
    console.print(table)


if __name__ == '__main__':
    cli()
