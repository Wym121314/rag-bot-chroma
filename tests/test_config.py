"""
Tests for config module.

Validates configuration structure and completeness.
"""

import pytest
from utils.config import MODEL_OPTIONS, CHINESE_EMBEDDING_MODEL


class TestModelOptions:
    """Test MODEL_OPTIONS configuration."""

    def test_has_providers(self):
        """Should define at least one model provider."""
        assert len(MODEL_OPTIONS) > 0

    def test_all_providers_have_models(self):
        """Each provider should have at least one model."""
        for provider, config in MODEL_OPTIONS.items():
            assert "models" in config, f"{provider} missing 'models' key"
            assert len(config["models"]) > 0, f"{provider} has no models"

    def test_all_providers_have_playground(self):
        """Each provider should have a playground URL."""
        for provider, config in MODEL_OPTIONS.items():
            assert "playground" in config, f"{provider} missing 'playground' key"
            assert config["playground"].startswith("http"), f"{provider} playground is not a URL"

    def test_expected_providers_exist(self):
        """Core providers should be present."""
        expected = ["Groq", "Gemini"]
        for provider in expected:
            assert provider in MODEL_OPTIONS, f"Missing provider: {provider}"

    def test_model_names_are_strings(self):
        """All model names should be non-empty strings."""
        for provider, config in MODEL_OPTIONS.items():
            for model in config["models"]:
                assert isinstance(model, str) and len(model) > 0, (
                    f"Invalid model name in {provider}: {model}"
                )


class TestEmbeddingModel:
    """Test embedding model configuration."""

    def test_chinese_embedding_model_is_string(self):
        """Embedding model name should be a non-empty string."""
        assert isinstance(CHINESE_EMBEDDING_MODEL, str)
        assert len(CHINESE_EMBEDDING_MODEL) > 0

    def test_chinese_embedding_model_format(self):
        """Should follow HuggingFace model format: org/model-name."""
        assert "/" in CHINESE_EMBEDDING_MODEL, "Should be in org/model format"
