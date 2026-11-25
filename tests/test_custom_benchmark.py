import json
import pytest

import app.evaluation.custom_benchmark as custom
import app.evaluation.benchmark_runner as runner


class FakeProvider:
    def __init__(self, solution):
        self.solution = solution
        self.total_tokens = 10

    def generate_response(self, prompt):
        return json.dumps({"solution": self.solution})


@pytest.mark.parametrize(
    "problem,instance,solution",
    [
        (
            "tsp",
            {"cities": [{"x": 0, "y": 0}, {"x": 3, "y": 4}, {"x": 6, "y": 0}]},
            [0, 1, 2],
        ),
        (
            "knapsack",
            {"items": [{"weight": 2, "value": 30}, {"weight": 4, "value": 50}], "capacity": 4},
            [0, 1],
        ),
        (
            "graph_coloring",
            {"num_vertices": 3, "edges": [[0, 1], [1, 2], [0, 2]]},
            [0, 1, 2],
        ),
    ],
)
def test_custom_benchmark_runs_and_validates(monkeypatch, problem, instance, solution):
    monkeypatch.setattr(custom, "GeminiLLMProvider", lambda: FakeProvider(solution))
    monkeypatch.setattr(runner, "save_experiment", lambda **kwargs: 123)

    result = custom.run_custom_benchmark(problem, instance, "gemini")

    assert result["experiment_id"] == 123
    assert result["validity"] is True
    assert result["exact_solution"] is not None
    assert result["metrics"]["validity"] is True


def test_custom_tsp_accepts_50_cities():
    instance = {"cities": [{"x": i, "y": i * 2} for i in range(50)]}
    custom.validate_custom_instance("tsp", instance)
    assert len(instance["cities"]) == 50


def test_custom_tsp_rejects_more_than_50_cities():
    instance = {"cities": [{"x": i, "y": i} for i in range(51)]}
    with pytest.raises(ValueError, match="2 to 50 cities"):
        custom.validate_custom_instance("tsp", instance)


def test_custom_tsp_uses_heuristic_for_50_cities(monkeypatch):
    cities = [{"x": (i * 17) % 101, "y": (i * 31) % 97} for i in range(50)]
    route, distance = custom.solve_tsp_nearest_neighbor_2opt(cities)
    valid, _ = custom.validate_tsp_solution(cities, route)
    assert valid is True
    assert distance > 0


def test_custom_knapsack_accepts_50_items_and_solves_exactly():
    items = [{"weight": i + 1, "value": (i + 1) * 3} for i in range(50)]
    instance = {"items": items, "capacity": 100}
    custom.validate_custom_instance("knapsack", instance)
    selection, weight, value = custom.solve_knapsack_dynamic_programming(items, 100)
    assert len(selection) == 50
    assert weight <= 100
    assert value > 0


def test_custom_graph_accepts_50_vertices():
    instance = {"num_vertices": 50, "edges": [[i, i + 1] for i in range(49)]}
    custom.validate_custom_instance("graph_coloring", instance)
    coloring, colors_used = custom.solve_graph_coloring_dsatur(instance)
    valid, details = custom.validate_graph_coloring(instance, coloring)
    assert valid is True
    assert details["colors_used"] == colors_used


def test_custom_graph_rejects_more_than_50_vertices():
    instance = {"num_vertices": 51, "edges": []}
    with pytest.raises(ValueError, match="1 to 50 vertices"):
        custom.validate_custom_instance("graph_coloring", instance)


def test_custom_graph_rejects_invalid_edge():
    instance = {"num_vertices": 3, "edges": [[0, 3]]}
    with pytest.raises(ValueError, match="Invalid edge"):
        custom.validate_custom_instance("graph_coloring", instance)
