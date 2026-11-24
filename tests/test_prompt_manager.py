
import pytest

from app.llm.prompt_manager import build_prompt


# TEST 1
def test_subset_sum_prompt():
    instance = {
        "numbers": [3, 5, 7],
        "target": 10
    }

    prompt = build_prompt("subset_sum", instance)

    assert "SUBSET_SUM" in prompt
    assert "10" in prompt


# TEST 2
def test_tsp_prompt():
    instance = {"cities": [[0, 0], [1, 1]]}

    prompt = build_prompt("tsp", instance)

    assert "TSP" in prompt
    assert "shortest route" in prompt


# TEST 3
def test_knapsack_prompt():
    instance = {
        "items": [{"weight": 2, "value": 5}],
        "capacity": 5
    }

    prompt = build_prompt("knapsack", instance)

    assert "KNAPSACK" in prompt
    assert "capacity" in prompt


# TEST 4
def test_graph_coloring_prompt():
    instance = {
        "vertices": 3,
        "edges": [[0, 1], [1, 2]]
    }

    prompt = build_prompt("graph_coloring", instance)

    assert "GRAPH_COLORING" in prompt
    assert "colors" in prompt


# TEST 5
def test_three_sat_prompt():
    instance = {
        "num_variables": 3,
        "clauses": [[1, -2, 3]]
    }

    prompt = build_prompt("three_sat", instance)

    assert "THREE_SAT" in prompt
    assert "Boolean" in prompt


# TEST 6
def test_prompt_output_format():
    instance = {"numbers": [1, 2], "target": 2}

    prompt = build_prompt("subset_sum", instance)

    assert '"solution"' in prompt
    assert "valid JSON" in prompt


# TEST 7
def test_unsupported_problem():
    with pytest.raises(ValueError):
        build_prompt("unknown_problem", {})
