
from app.problems.subset_sum import (
    generate_subset_sum_instance,
    solve_subset_sum_brute_force,
    validate_subset_sum_solution
)

from app.llm.llm_interface import GeminiLLMProvider
from app.evaluation.benchmark_runner import run_benchmark


def main():

    # Step 1: Generate problem
    instance = generate_subset_sum_instance(
        num_numbers=6,
        seed=42
    )

    # Extract actual values from dictionary
    numbers = instance["numbers"]
    target = instance["target"]

    print("===== SUBSET SUM BENCHMARK =====")
    print("Numbers:", numbers)
    print("Target:", target)

    # Step 2: Find exact solution
    reference_solution = solve_subset_sum_brute_force(
        numbers,
        target
    )

    if reference_solution is None:
        print("No reference solution found.")
        return

    print("\nExact Solver Solution:", reference_solution)

    # Step 3: Create validator
    def validator(solution):

        is_valid, details = validate_subset_sum_solution(
            numbers,
            target,
            solution
        )

        return is_valid, 1 if is_valid else details

    # Step 4: Connect Gemini
    provider = GeminiLLMProvider()

    print("\nSending problem to Gemini AI...")

    # Step 5: Run benchmark
    result = run_benchmark(
        problem_name="subset_sum",
        instance=instance,
        optimal_value=1,
        objective="max",
        provider=provider,
        validator=validator,
        provider_name="gemini"
    )

    # Step 6: Display result
    print("\n===== GEMINI BENCHMARK RESULT =====")
    print("Gemini Solution:", result["solution"])
    print("Valid Solution:", result["validity"])
    print("Validation Details:", result["validation_result"])
    print("Metrics:", result["metrics"])
    print("Experiment ID:", result["experiment_id"])


if __name__ == "__main__":
    main()
