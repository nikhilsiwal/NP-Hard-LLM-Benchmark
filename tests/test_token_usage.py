
from app.evaluation import benchmark_runner


class FakeLLMProvider:

    total_tokens = 155

    def generate_response(self, prompt):
        return '{"solution": [1, 0, 1]}'


def test_benchmark_runner_saves_token_usage(monkeypatch):

    saved_data = {}

    monkeypatch.setattr(
        benchmark_runner,
        "build_prompt",
        lambda problem_name, instance: "Test prompt"
    )

    monkeypatch.setattr(
        benchmark_runner,
        "parse_llm_response",
        lambda response: [1, 0, 1]
    )

    def fake_save_experiment(
        problem_name,
        provider,
        solution,
        metrics
    ):
        saved_data["metrics"] = metrics
        return 999

    monkeypatch.setattr(
        benchmark_runner,
        "save_experiment",
        fake_save_experiment
    )

    provider = FakeLLMProvider()

    result = benchmark_runner.run_benchmark(
        problem_name="subset_sum",
        instance={"numbers": [1, 2, 3], "target": 4},
        optimal_value=10,
        objective="max",
        provider=provider,
        validator=lambda solution: (True, 10),
        provider_name="test"
    )

    assert result["metrics"]["tokens_used"] == 155
    assert saved_data["metrics"]["tokens_used"] == 155
    assert result["experiment_id"] == 999


def test_benchmark_runner_supports_provider_without_token_data(monkeypatch):

    class BasicProvider:

        def generate_response(self, prompt):
            return '{"solution": [1, 0, 1]}'

    monkeypatch.setattr(
        benchmark_runner,
        "build_prompt",
        lambda problem_name, instance: "Test prompt"
    )

    monkeypatch.setattr(
        benchmark_runner,
        "parse_llm_response",
        lambda response: [1, 0, 1]
    )

    monkeypatch.setattr(
        benchmark_runner,
        "save_experiment",
        lambda **kwargs: 1000
    )

    result = benchmark_runner.run_benchmark(
        problem_name="subset_sum",
        instance={"numbers": [1, 2, 3], "target": 4},
        optimal_value=10,
        objective="max",
        provider=BasicProvider(),
        validator=lambda solution: (True, 10)
    )

    assert result["metrics"]["tokens_used"] is None
