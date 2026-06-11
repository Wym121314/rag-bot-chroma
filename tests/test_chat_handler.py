"""
Tests for chat handler module.

Tests conversation memory formatting and session state logic.
"""

import pytest
from datetime import datetime
from utils.chat_handler import format_chat_history


class TestFormatChatHistory:
    """Test chat history formatting for multi-turn memory."""

    def test_empty_history(self):
        """Empty history should return empty string."""
        result = format_chat_history([])
        assert result == ""

    def test_single_turn(self):
        """Single Q&A turn should be formatted correctly."""
        history = [
            ("续航多少？", "续航606公里", "groq", "llama3", ["manual.pdf"], datetime.now())
        ]
        result = format_chat_history(history)
        assert "用户问：续航多少？" in result
        assert "助手答：续航606公里" in result
        assert "之前的对话记录" in result

    def test_multiple_turns(self):
        """Multiple turns should all appear in output."""
        history = [
            ("续航多少？", "续航606公里", "groq", "llama3", ["m.pdf"], datetime.now()),
            ("电池多大？", "电池75kWh", "groq", "llama3", ["m.pdf"], datetime.now()),
        ]
        result = format_chat_history(history)
        assert "续航多少？" in result
        assert "电池多大？" in result
        assert "606公里" in result
        assert "75kWh" in result

    def test_limits_recent_turns(self):
        """Should only include the last N turns."""
        history = [
            (f"问题{i}", f"回答{i}", "groq", "llama3", ["m.pdf"], datetime.now())
            for i in range(10)
        ]
        result = format_chat_history(history, max_turns=3)
        # Should have the last 3 turns (7, 8, 9)
        assert "问题9" in result
        assert "问题8" in result
        assert "问题7" in result
        assert "问题0" not in result
        assert "问题1" not in result

    def test_custom_max_turns(self):
        """Should respect custom max_turns parameter."""
        history = [
            ("Q1", "A1", "g", "m", ["f"], datetime.now()),
            ("Q2", "A2", "g", "m", ["f"], datetime.now()),
            ("Q3", "A3", "g", "m", ["f"], datetime.now()),
        ]
        result = format_chat_history(history, max_turns=2)
        assert "Q3" in result
        assert "Q2" in result
        assert "Q1" not in result

    def test_returns_string(self):
        """Return type should always be str."""
        history = [("Q", "A", "g", "m", ["f"], datetime.now())]
        assert isinstance(format_chat_history(history), str)
