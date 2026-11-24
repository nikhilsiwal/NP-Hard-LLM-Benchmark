
import pytest
from unittest.mock import Mock

import app.llm.llm_interface as llm_module


def create_fake_response(response_text, usage=None):

    fake_response = Mock()

    response_data = {
        "choices": [
            {
                "message": {
                    "content": response_text
                }
            }
        ]
    }

    if usage is not None:
        response_data["usage"] = usage

    fake_response.json.return_value = response_data

    return fake_response


def test_groq_provider_creation():

    provider = llm_module.GroqLLMProvider(
        api_key="test-key"
    )

    assert provider.api_key == "test-key"


def test_groq_provider_uses_environment_key(monkeypatch):

    monkeypatch.setenv("GROQ_API_KEY", "env-test-key")

    provider = llm_module.GroqLLMProvider()

    assert provider.api_key == "env-test-key"


def test_groq_provider_missing_key(monkeypatch):

    monkeypatch.delenv("GROQ_API_KEY", raising=False)

    with pytest.raises(ValueError):
        llm_module.GroqLLMProvider()


def test_groq_provider_empty_prompt():

    provider = llm_module.GroqLLMProvider(
        api_key="test-key"
    )

    with pytest.raises(ValueError):
        provider.generate_response("")


def test_groq_provider_generates_response(monkeypatch):

    fake_response = create_fake_response(
        '{"solution": [1, 0, 1]}'
    )

    monkeypatch.setattr(
        llm_module.requests,
        "post",
        lambda *args, **kwargs: fake_response
    )

    provider = llm_module.GroqLLMProvider(
        api_key="test-key"
    )

    result = provider.generate_response("Solve this problem")

    assert result == '{"solution": [1, 0, 1]}'


def test_groq_provider_uses_correct_model(monkeypatch):

    captured = {}

    def fake_post(url, **kwargs):

        captured["url"] = url
        captured["data"] = kwargs["json"]

        return create_fake_response("Test response")

    monkeypatch.setattr(
        llm_module.requests,
        "post",
        fake_post
    )

    provider = llm_module.GroqLLMProvider(
        api_key="test-key",
        model="openai/gpt-oss-120b"
    )

    provider.generate_response("Test prompt")

    assert "api.groq.com" in captured["url"]
    assert captured["data"]["model"] == "openai/gpt-oss-120b"


def test_groq_provider_extracts_token_usage(monkeypatch):

    fake_response = create_fake_response(
        '{"solution": [1, 0, 1]}',
        {
            "prompt_tokens": 100,
            "completion_tokens": 50,
            "total_tokens": 150
        }
    )

    monkeypatch.setattr(
        llm_module.requests,
        "post",
        lambda *args, **kwargs: fake_response
    )

    provider = llm_module.GroqLLMProvider(
        api_key="test-key"
    )

    provider.generate_response("Solve this problem")

    assert provider.prompt_tokens == 100
    assert provider.completion_tokens == 50
    assert provider.total_tokens == 150


def test_groq_provider_calculates_total_tokens(monkeypatch):

    fake_response = create_fake_response(
        "Test response",
        {
            "prompt_tokens": 100,
            "completion_tokens": 50
        }
    )

    monkeypatch.setattr(
        llm_module.requests,
        "post",
        lambda *args, **kwargs: fake_response
    )

    provider = llm_module.GroqLLMProvider(
        api_key="test-key"
    )

    provider.generate_response("Test prompt")

    assert provider.total_tokens == 150


def test_groq_provider_handles_missing_token_usage(monkeypatch):

    fake_response = create_fake_response("Test response")

    monkeypatch.setattr(
        llm_module.requests,
        "post",
        lambda *args, **kwargs: fake_response
    )

    provider = llm_module.GroqLLMProvider(
        api_key="test-key"
    )

    provider.generate_response("Test prompt")

    assert provider.prompt_tokens is None
    assert provider.completion_tokens is None
    assert provider.total_tokens is None
