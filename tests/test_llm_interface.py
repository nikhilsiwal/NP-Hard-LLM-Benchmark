
import pytest

from app.llm.llm_interface import (
    LLMProvider,
    MockLLMProvider
)


# TEST 1
def test_mock_provider_creation():
    provider = MockLLMProvider()

    assert isinstance(provider, MockLLMProvider)


# TEST 2
def test_mock_provider_is_llm_provider():
    provider = MockLLMProvider()

    assert isinstance(provider, LLMProvider)


# TEST 3
def test_generate_response():
    provider = MockLLMProvider()

    response = provider.generate_response("Solve TSP")

    assert isinstance(response, str)


# TEST 4
def test_response_contains_solution():
    provider = MockLLMProvider()

    response = provider.generate_response("Solve problem")

    assert '"solution"' in response


# TEST 5
def test_response_is_valid_json():
    import json

    provider = MockLLMProvider()

    response = provider.generate_response("Solve problem")
    data = json.loads(response)

    assert "solution" in data


# TEST 6
def test_empty_prompt():
    provider = MockLLMProvider()

    with pytest.raises(ValueError):
        provider.generate_response("")


# TEST 7
def test_abstract_provider_cannot_be_created():
    with pytest.raises(TypeError):
        LLMProvider()
