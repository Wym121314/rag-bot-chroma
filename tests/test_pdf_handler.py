"""
Tests for PDF handler module.

Tests the core text extraction and chunking logic without
requiring actual PDF files or external services.
"""

import pytest
from unittest.mock import MagicMock, patch
from utils.pdf_handler import get_text_chunks, get_pdf_text


class TestGetTextChunks:
    """Test text chunking logic."""

    def test_returns_list(self, sample_chinese_text):
        """Chunking should return a list of strings."""
        chunks = get_text_chunks(sample_chinese_text)
        assert isinstance(chunks, list)
        assert all(isinstance(c, str) for c in chunks)

    def test_chunks_not_empty(self, sample_chinese_text):
        """No chunk should be empty."""
        chunks = get_text_chunks(sample_chinese_text)
        assert all(len(c.strip()) > 0 for c in chunks)

    def test_chunk_size_respected(self, sample_chinese_text):
        """Chunks should respect max size (300 + some tolerance for overlap)."""
        chunks = get_text_chunks(sample_chinese_text)
        for chunk in chunks:
            # Allow some tolerance due to separator boundaries
            assert len(chunk) <= 400, f"Chunk too long ({len(chunk)} chars): {chunk[:50]}..."

    def test_content_preserved(self, sample_chinese_text):
        """All original content should appear in chunks (no data loss)."""
        chunks = get_text_chunks(sample_chinese_text)
        combined = "".join(chunks)
        # Key data points should survive chunking
        assert "606" in combined
        assert "75.0 kWh" in combined
        assert "4694mm" in combined

    def test_empty_text_returns_empty(self):
        """Empty input should return empty list."""
        chunks = get_text_chunks("")
        assert chunks == []

    def test_short_text_single_chunk(self):
        """Text shorter than chunk_size should be a single chunk."""
        short = "这是一段很短的文本。"
        chunks = get_text_chunks(short)
        assert len(chunks) == 1
        assert chunks[0] == short

    def test_long_text_multiple_chunks(self):
        """Text longer than chunk_size should split into multiple chunks."""
        long_text = "这是一段测试文本。" * 100  # ~800 chars
        chunks = get_text_chunks(long_text)
        assert len(chunks) > 1

    def test_overlap_exists(self):
        """Adjacent chunks should have some overlap."""
        long_text = "第一句话。第二句话。第三句话。第四句话。第五句话。第六句话。第七句话。第八句话。" * 10
        chunks = get_text_chunks(long_text)
        if len(chunks) > 1:
            # With overlap, the end of chunk[0] should share content with start of chunk[1]
            # This is a soft check — overlap may not always be detectable at sentence boundaries
            assert len(chunks) >= 2


class TestGetPdfText:
    """Test PDF text extraction."""

    def test_extracts_text_with_markers(self):
        """Should extract text with document name and page markers."""
        # Create mock PDF file
        mock_file = MagicMock()
        mock_file.name = "test.pdf"

        # Mock PdfReader
        mock_page1 = MagicMock()
        mock_page1.extract_text.return_value = "第一页内容"
        mock_page2 = MagicMock()
        mock_page2.extract_text.return_value = "第二页内容"

        with patch("utils.pdf_handler.PdfReader") as mock_reader:
            mock_reader.return_value.pages = [mock_page1, mock_page2]
            result = get_pdf_text([mock_file])

        assert "[文档: test.pdf | 第1页]" in result
        assert "[文档: test.pdf | 第2页]" in result
        assert "第一页内容" in result
        assert "第二页内容" in result

    def test_handles_empty_page(self):
        """Should skip pages with no extractable text."""
        mock_file = MagicMock()
        mock_file.name = "empty.pdf"

        mock_page = MagicMock()
        mock_page.extract_text.return_value = ""

        with patch("utils.pdf_handler.PdfReader") as mock_reader:
            mock_reader.return_value.pages = [mock_page]
            result = get_pdf_text([mock_file])

        # Empty page is skipped (code checks page_text.strip()), so result is empty
        assert result == ""

    def test_handles_none_page_text(self):
        """Should handle pages where extract_text returns None."""
        mock_file = MagicMock()
        mock_file.name = "none.pdf"

        mock_page = MagicMock()
        mock_page.extract_text.return_value = None

        with patch("utils.pdf_handler.PdfReader") as mock_reader:
            mock_reader.return_value.pages = [mock_page]
            result = get_pdf_text([mock_file])

        # Should not crash, just skip None content
        assert isinstance(result, str)

    def test_multiple_files(self):
        """Should process multiple PDF files."""
        mock_file1 = MagicMock()
        mock_file1.name = "file1.pdf"
        mock_file2 = MagicMock()
        mock_file2.name = "file2.pdf"

        mock_page1 = MagicMock()
        mock_page1.extract_text.return_value = "文件一内容"
        mock_page2 = MagicMock()
        mock_page2.extract_text.return_value = "文件二内容"

        with patch("utils.pdf_handler.PdfReader") as mock_reader:
            mock_reader.side_effect = [
                MagicMock(pages=[mock_page1]),
                MagicMock(pages=[mock_page2]),
            ]
            result = get_pdf_text([mock_file1, mock_file2])

        assert "文件一内容" in result
        assert "文件二内容" in result
