
import pytest
from unittest.mock import Mock

import app.llm.llm_interface as llm_module


def test_gemini_provider_creation():

    provider = llm_module.GeminiLLMProvider(api_key="test-key")

    assert provider.api_key == "test-key"


def test_gemini_provider_uses_environment_key(monkeypatch):

    monkeypatch.setenv("GEMINI_API_KEY", "env-test-key")

    provider = llm_module.GeminiLLMProvider()

    assert provider.api_key == "env-test-key"


def test_gemini_provider_missing_key(monkeypatch):

    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    with pytest.raises(ValueError):
        llm_module.GeminiLLMProvider()


def test_gemini_provider_empty_prompt():

    provider = llm_module.GeminiLLMProvider(api_key="test-key")

    with pytest.raises(ValueError):
        provider.generate_response("")


def test_gemini_provider_generates_response(monkeypatch):

    fake_response = Mock()

    fake_response.json.return_value = {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {"text": '{"solution": [1, 0, 1]}'}
                    ]
                }
            }
        ]
    }

    monkeypatch.setattr(
        llm_module.requests,
        "post",
        lambda *args, **kwargs: fake_response
    )

    provider = llm_module.GeminiLLMProvider(api_key="test-key")

    result = provider.generate_response("Solve this problem")

    assert result == '{"solution": [1, 0, 1]}'


def test_gemini_provider_uses_correct_model(monkeypatch):

    captured = {}

    def fake_post(url, **kwargs):
        captured["url"] = url

        response = Mock()
        response.json.return_value = {
            "candidates": [
                {
                    "content": {
                        "parts": [{"text": "Test response"}]
                    }
                }
            ]
        }
        return response

    monkeypatch.setattr(llm_module.requests, "post", fake_post)

    provider = llm_module.GeminiLLMProvider(api_key="test-key")

    provider.generate_response("Test prompt")

    assert "gemini-3.5-flash" in captured["url"]


def test_gemini_provider_empty_response(monkeypatch):

    fake_response = Mock()

    fake_response.json.return_value = {
        "candidates": []
    }

    monkeypatch.setattr(
        llm_module.requests,
        "post",
        lambda *args, **kwargs: fake_response
    )

    provider = llm_module.GeminiLLMProvider(api_key="test-key")

    with pytest.raises(ValueError):
        provider.generate_response("Test prompt")

