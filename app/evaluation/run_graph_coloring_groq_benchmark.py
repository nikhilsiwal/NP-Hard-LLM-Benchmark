
from app.problems.graph_coloring import (
    generate_graph_instance,
    solve_graph_coloring,
    validate_graph_coloring
)

from app.llm.llm_interface import GroqLLMProvider
from app.evaluation.benchmark_runner import run_benchmark


def main():

    # Step 1: Generate graph
    instance = generate_graph_instance(
        num_vertices=5,
        seed=42
    )

    print("===== GROQ GRAPH COLORING BENCHMARK =====")
    print("Number of Vertices:", instance["num_vertices"])
    print("Graph Edges:", instance["edges"])

    # Step 2: Find exact solution
    optimal_coloring, optimal_colors = solve_graph_coloring(
        instance
    )

    print("\nExact Solver Coloring:", optimal_coloring)
    print("Minimum Colors Required:", optimal_colors)

    # Step 3: Create validator
    def validator(solution):

        is_valid, details = validate_graph_coloring(
            instance,
            solution
        )

        if is_valid:
            return True, details["colors_used"]

        return False, None

    # Step 4: Connect Groq
    provider = GroqLLMProvider(
        model="openai/gpt-oss-120b"
    )

    print("\nSending Graph Coloring problem to Groq AI...")

    # Step 5: Run benchmark
    result = run_benchmark(
        problem_name="graph_coloring",
        instance=instance,
        optimal_value=optimal_colors,
        objective="min",
        provider=provider,
        validator=validator,
        provider_name="groq"
    )

    # Step 6: Display result
    print("\n===== GROQ GRAPH COLORING RESULT =====")
    print("Groq Coloring:", result["solution"])
    print("Valid Coloring:", result["validity"])
    print("Colors Used:", result["validation_result"])
    print("Metrics:", result["metrics"])
    print("Experiment ID:", result["experiment_id"])


if __name__ == "__main__":
    main()
