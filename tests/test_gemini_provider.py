
import pytest
from unittest.mock import Mock

import app.llm.llm_interface as llm_module


def create_fake_response(response_text, usage_metadata=None):

    fake_response = Mock()

    response_data = {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {"text": response_text}
                    ]
                }
            }
        ]
    }

    if usage_metadata is not None:
        response_data["usageMetadata"] = usage_metadata

    fake_response.json.return_value = response_data

    return fake_response


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

    fake_response = create_fake_response(
        '{"solution": [1, 0, 1]}'
    )

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

        return create_fake_response("Test response")

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


def test_gemini_provider_extracts_token_usage(monkeypatch):

    fake_response = create_fake_response(
        '{"solution": [1, 0, 1]}',
        {
            "promptTokenCount": 100,
            "candidatesTokenCount": 50,
            "totalTokenCount": 150
        }
    )

    monkeypatch.setattr(
        llm_module.requests,
        "post",
        lambda *args, **kwargs: fake_response
    )

    provider = llm_module.GeminiLLMProvider(api_key="test-key")

    provider.generate_response("Solve this problem")

    assert provider.prompt_tokens == 100
    assert provider.completion_tokens == 50
    assert provider.total_tokens == 150


def test_gemini_provider_handles_missing_token_usage(monkeypatch):

    fake_response = create_fake_response(
        '{"solution": [1, 0, 1]}'
    )

    monkeypatch.setattr(
        llm_module.requests,
        "post",
        lambda *args, **kwargs: fake_response
    )

    provider = llm_module.GeminiLLMProvider(api_key="test-key")

    provider.generate_response("Solve this problem")

    assert provider.prompt_tokens is None
    assert provider.completion_tokens is None
    assert provider.total_tokens is None
