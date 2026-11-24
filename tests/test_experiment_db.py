
import pytest

from app.database.experiment_db import (
    initialize_database,
    save_experiment,
    get_all_experiments
)


@pytest.fixture
def database_path(tmp_path):
    return str(tmp_path / "test_experiments.db")


# TEST 1
def test_initialize_database(database_path):
    initialize_database(database_path)

    import os
    assert os.path.exists(database_path)


# TEST 2
def test_save_experiment(database_path):
    metrics = {
        "validity": True,
        "accuracy": 1.0,
        "optimality_gap": 0.0,
        "latency": 1.5,
        "tokens_used": 150
    }

    experiment_id = save_experiment(
        "subset_sum",
        "mock",
        [1, 0, 1],
        metrics,
        database_path
    )

    assert experiment_id == 1


# TEST 3
def test_get_all_experiments(database_path):
    metrics = {
        "validity": True,
        "accuracy": 1.0,
        "optimality_gap": 0.0,
        "latency": 1.5,
        "tokens_used": 100
    }

    save_experiment(
        "tsp", "mock", [0, 1, 2], metrics, database_path
    )

    experiments = get_all_experiments(database_path)

    assert len(experiments) == 1


# TEST 4
def test_saved_solution(database_path):
    metrics = {
        "validity": True,
        "accuracy": 1.0,
        "optimality_gap": 0.0,
        "latency": 1.0,
        "tokens_used": 50
    }

    save_experiment(
        "subset_sum", "mock", [1, 0, 1], metrics, database_path
    )

    experiments = get_all_experiments(database_path)

    assert experiments[0]["solution"] == [1, 0, 1]


# TEST 5
def test_saved_provider(database_path):
    metrics = {
        "validity": True,
        "accuracy": 1.0,
        "optimality_gap": 0.0,
        "latency": 1.0,
        "tokens_used": 50
    }

    save_experiment(
        "tsp", "gemini", [0, 1, 2], metrics, database_path
    )

    experiments = get_all_experiments(database_path)

    assert experiments[0]["provider"] == "gemini"


# TEST 6
def test_multiple_experiments(database_path):
    metrics = {
        "validity": True,
        "accuracy": 1.0,
        "optimality_gap": 0.0,
        "latency": 1.0,
        "tokens_used": 50
    }

    save_experiment("tsp", "mock", [0, 1], metrics, database_path)
    save_experiment("knapsack", "mock", [1, 0], metrics, database_path)

    experiments = get_all_experiments(database_path)

    assert len(experiments) == 2


# TEST 7
def test_empty_database(database_path):
    experiments = get_all_experiments(database_path)

    assert experiments == []
