
import pytest

from app.llm.response_parser import parse_llm_response


# TEST 1
def test_valid_json_response():
    response = '{"solution": [1, 0, 1, 0]}'

    result = parse_llm_response(response)

    assert result == [1, 0, 1, 0]


# TEST 2
def test_json_code_block():
    response = """
    ```json
    {
        "solution": [1, 1, 0]
    }
    ```
    """

    result = parse_llm_response(response)

    assert result == [1, 1, 0]


# TEST 3
def test_response_with_spaces():
    response = '   {"solution": [0, 1, 0]}   '

    result = parse_llm_response(response)

    assert result == [0, 1, 0]


# TEST 4
def test_empty_response():
    with pytest.raises(ValueError):
        parse_llm_response("")


# TEST 5
def test_invalid_json():
    response = '{"solution": [1, 0, 1]'

    with pytest.raises(ValueError):
        parse_llm_response(response)


# TEST 6
def test_missing_solution_field():
    response = '{"answer": [1, 0, 1]}'

    with pytest.raises(ValueError):
        parse_llm_response(response)


# TEST 7
def test_solution_not_list():
    response = '{"solution": "1, 0, 1"}'

    with pytest.raises(ValueError):
        parse_llm_response(response)

