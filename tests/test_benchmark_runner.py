
import app.evaluation.benchmark_runner as runner


class FakeLLMProvider:

    def generate_response(self, prompt):
        return '{"solution": [1, 0, 1, 0]}'


def setup_runner(monkeypatch, validator, provider_name="mock"):

    saved_data = {}

    def fake_save_experiment(**kwargs):
        saved_data.update(kwargs)
        return 42

    monkeypatch.setattr(
        runner,
        "save_experiment",
        fake_save_experiment
    )

    result = runner.run_benchmark(
        problem_name="subset_sum",
        instance={
            "numbers": [3, 5, 7, 10],
            "target": 10
        },
        optimal_value=10,
        objective="max",
        provider=FakeLLMProvider(),
        validator=validator,
        provider_name=provider_name
    )

    return result, saved_data


def test_benchmark_returns_result(monkeypatch):

    result, _ = setup_runner(
        monkeypatch,
        lambda solution: (True, 10)
    )

    assert isinstance(result, dict)


def test_benchmark_returns_solution(monkeypatch):

    result, _ = setup_runner(
        monkeypatch,
        lambda solution: (True, 10)
    )

    assert result["solution"] == [1, 0, 1, 0]


def test_benchmark_valid_solution(monkeypatch):

    result, _ = setup_runner(
        monkeypatch,
        lambda solution: (True, 10)
    )

    assert result["validity"] is True


def test_benchmark_invalid_solution(monkeypatch):

    result, _ = setup_runner(
        monkeypatch,
        lambda solution: (False, "Invalid solution")
    )

    assert result["validity"] is False


def test_benchmark_saves_experiment(monkeypatch):

    result, saved_data = setup_runner(
        monkeypatch,
        lambda solution: (True, 10)
    )

    assert result["experiment_id"] == 42
    assert saved_data["problem_name"] == "subset_sum"


def test_benchmark_uses_provider_name(monkeypatch):

    _, saved_data = setup_runner(
        monkeypatch,
        lambda solution: (True, 10),
        provider_name="test_provider"
    )

    assert saved_data["provider"] == "test_provider"


def test_benchmark_calculates_metrics(monkeypatch):

    result, _ = setup_runner(
        monkeypatch,
        lambda solution: (True, 10)
    )

    assert result["metrics"]["accuracy"] == 1.0
    assert result["metrics"]["optimality_gap"] == 0.0
