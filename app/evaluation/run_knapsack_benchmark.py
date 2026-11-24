
from app.problems.knapsack import (
    generate_knapsack_instance,
    solve_knapsack_brute_force,
    validate_knapsack_solution
)

from app.llm.llm_interface import GeminiLLMProvider
from app.evaluation.benchmark_runner import run_benchmark


def main():

    # Step 1: Generate Knapsack problem
    instance = generate_knapsack_instance(
        num_items=5,
        capacity=15,
        seed=42
    )

    items = instance["items"]
    capacity = instance["capacity"]

    print("===== KNAPSACK BENCHMARK =====")
    print("Capacity:", capacity)
    print("Items:", items)

    # Step 2: Find exact solution
    optimal_selection, optimal_weight, optimal_value = (
        solve_knapsack_brute_force(items, capacity)
    )

    print("\nExact Solver Selection:", optimal_selection)
    print("Exact Total Weight:", optimal_weight)
    print("Exact Maximum Value:", optimal_value)

    # Step 3: Create validator
    def validator(solution):

        is_valid, details = validate_knapsack_solution(
            items,
            capacity,
            solution
        )

        if is_valid:
            return True, details["total_value"]

        return False, None

    # Step 4: Connect Gemini
    provider = GeminiLLMProvider()

    print("\nSending Knapsack problem to Gemini AI...")

    # Step 5: Run benchmark
    result = run_benchmark(
        problem_name="knapsack",
        instance=instance,
        optimal_value=optimal_value,
        objective="max",
        provider=provider,
        validator=validator,
        provider_name="gemini"
    )

    # Step 6: Display result
    print("\n===== GEMINI KNAPSACK BENCHMARK RESULT =====")
    print("Gemini Selection:", result["solution"])
    print("Valid Solution:", result["validity"])
    print("Gemini Value:", result["validation_result"])
    print("Metrics:", result["metrics"])
    print("Experiment ID:", result["experiment_id"])


if __name__ == "__main__":
    main()
