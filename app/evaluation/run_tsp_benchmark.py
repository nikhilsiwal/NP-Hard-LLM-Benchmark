
from app.problems.tsp import (
    generate_tsp_instance,
    solve_tsp_brute_force,
    validate_tsp_solution
)

from app.llm.llm_interface import GeminiLLMProvider
from app.evaluation.benchmark_runner import run_benchmark


def main():

    # Step 1: Generate TSP problem
    cities = generate_tsp_instance(
        num_cities=5,
        seed=42
    )

    instance = {
        "cities": cities
    }

    print("===== TSP BENCHMARK =====")
    print("Cities:", cities)

    # Step 2: Find exact solution
    reference_solution = solve_tsp_brute_force(cities)

    if reference_solution is None:
        print("No reference solution found.")
        return

    optimal_route, optimal_distance = reference_solution

    print("\nExact Solver Route:", optimal_route)
    print("Exact Minimum Distance:", optimal_distance)

    # Step 3: Create validator
    def validator(solution):

        is_valid, details = validate_tsp_solution(
            cities,
            solution
        )

        return is_valid, details if is_valid else None

    # Step 4: Connect Gemini
    provider = GeminiLLMProvider()

    print("\nSending TSP problem to Gemini AI...")

    # Step 5: Run benchmark
    result = run_benchmark(
        problem_name="tsp",
        instance=instance,
        optimal_value=round(optimal_distance, 2),
        objective="min",
        provider=provider,
        validator=validator,
        provider_name="gemini"
    )

    # Step 6: Display result
    print("\n===== GEMINI TSP BENCHMARK RESULT =====")
    print("Gemini Route:", result["solution"])
    print("Valid Route:", result["validity"])
    print("Gemini Distance:", result["validation_result"])
    print("Metrics:", result["metrics"])
    print("Experiment ID:", result["experiment_id"])


if __name__ == "__main__":
    main()
