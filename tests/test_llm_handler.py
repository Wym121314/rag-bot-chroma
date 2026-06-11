"""
Tests for LLM handler module.

Tests chain construction logic by mocking LLM providers.
No real API calls are made.
"""

import pytest
from unittest.mock import patch, MagicMock
from utils.llm_handler import get_llm_chain, CAR_MANUAL_SYSTEM_PROMPT, CAR_MANUAL_USER_PROMPT


class TestPromptTemplates:
    """Test prompt template content."""

    def test_system_prompt_has_rules(self):
        """System prompt should contain key behavioral rules."""
        assert "文档内容回答" in CAR_MANUAL_SYSTEM_PROMPT
        assert "来源" in CAR_MANUAL_SYSTEM_PROMPT  # Source citation
        assert "未提及" in CAR_MANUAL_SYSTEM_PROMPT  # "Not mentioned" fallback

    def test_user_prompt_has_placeholders(self):
        """User prompt should have {context} and {input} placeholders."""
        assert "{context}" in CAR_MANUAL_USER_PROMPT
        assert "{input}" in CAR_MANUAL_USER_PROMPT

    def test_system_prompt_is_chinese(self):
        """System prompt should be in Chinese (car manual domain)."""
        assert "汽车" in CAR_MANUAL_SYSTEM_PROMPT or "顾问" in CAR_MANUAL_SYSTEM_PROMPT


class TestGetLlmChain:
    """Test LLM chain construction."""

    def test_returns_none_without_model(self):
        """Should return None when no model is specified."""
        mock_vs = MagicMock()
        result = get_llm_chain("groq", None, mock_vs)
        assert result is None

    def test_returns_none_for_unknown_provider(self):
        """Should return None for unsupported provider."""
        mock_vs = MagicMock()
        result = get_llm_chain("unknown_provider", "some-model", mock_vs)
        assert result is None

    @patch("utils.llm_handler.ChatGroq")
    def test_groq_chain_created(self, mock_groq):
        """Should create a chain for Groq provider."""
        mock_vs = MagicMock()
        result = get_llm_chain("groq", "llama3-70b-8192", mock_vs)
        assert result is not None
        mock_groq.assert_called_once()

    @patch("utils.llm_handler.ChatGoogleGenerativeAI")
    def test_gemini_chain_created(self, mock_gemini):
        """Should create a chain for Gemini provider."""
        mock_vs = MagicMock()
        result = get_llm_chain("gemini", "gemini-2.0-flash", mock_vs)
        assert result is not None
        mock_gemini.assert_called_once()

    @patch("utils.llm_handler.ChatOpenAI")
    def test_deepseek_chain_created(self, mock_openai):
        """Should create a chain for DeepSeek provider."""
        mock_vs = MagicMock()
        result = get_llm_chain("deepseek", "deepseek-chat", mock_vs)
        assert result is not None
        mock_openai.assert_called_once()

    @patch("utils.llm_handler.ChatGroq")
    def test_groq_uses_zero_temperature(self, mock_groq):
        """LLM should use temperature=0 for factual answers."""
        mock_vs = MagicMock()
        get_llm_chain("groq", "llama3-70b-8192", mock_vs)
        call_kwargs = mock_groq.call_args
        assert call_kwargs.kwargs.get("temperature") == 0 or call_kwargs[1].get("temperature") == 0

    @patch("utils.llm_handler.ChatGroq")
    def test_retriever_k_is_five(self, mock_groq):
        """Retriever should fetch top 5 documents."""
        mock_vs = MagicMock()
        get_llm_chain("groq", "llama3-70b-8192", mock_vs)
        mock_vs.as_retriever.assert_called_once()
        call_kwargs = mock_vs.as_retriever.call_args
        assert call_kwargs.kwargs.get("search_kwargs", {}).get("k") == 5
