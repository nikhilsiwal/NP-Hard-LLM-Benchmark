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


def test_custom_tsp_rejects_too_many_cities():
    instance = {"cities": [{"x": i, "y": i} for i in range(10)]}
    with pytest.raises(ValueError, match="2 to 9 cities"):
        custom.validate_custom_instance("tsp", instance)


def test_custom_graph_rejects_invalid_edge():
    instance = {"num_vertices": 3, "edges": [[0, 3]]}
    with pytest.raises(ValueError, match="Invalid edge"):
        custom.validate_custom_instance("graph_coloring", instance)
