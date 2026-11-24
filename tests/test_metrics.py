
import pytest

from app.evaluation.metrics import (
    calculate_optimality_gap,
    evaluate_metrics
)


# TEST 1
def test_minimization_optimality_gap():
    gap = calculate_optimality_gap(120, 100, "min")

    assert gap == 20.0


# TEST 2
def test_maximization_optimality_gap():
    gap = calculate_optimality_gap(80, 100, "max")

    assert gap == 20.0


# TEST 3
def test_perfect_accuracy():
    result = evaluate_metrics(
        True, 100, 100, "min"
    )

    assert result["accuracy"] == 1.0
    assert result["optimality_gap"] == 0.0


# TEST 4
def test_invalid_solution():
    result = evaluate_metrics(
        False, 120, 100, "min"
    )

    assert result["validity"] is False
    assert result["accuracy"] == 0.0


# TEST 5
def test_metrics_with_latency_and_tokens():
    result = evaluate_metrics(
        True, 100, 100,
        "min", 1.5, 150
    )

    assert result["latency"] == 1.5
    assert result["tokens_used"] == 150


# TEST 6
def test_invalid_objective():
    with pytest.raises(ValueError):
        calculate_optimality_gap(100, 90, "average")


# TEST 7
def test_negative_latency():
    with pytest.raises(ValueError):
        evaluate_metrics(
            True, 100, 100,
            "min", latency=-1
        )
