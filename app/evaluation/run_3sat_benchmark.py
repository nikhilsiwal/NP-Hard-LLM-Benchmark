
from app.problems.three_sat import (
    generate_3sat_instance,
    solve_3sat_brute_force,
    validate_3sat_solution
)

from app.llm.llm_interface import GeminiLLMProvider
from app.evaluation.benchmark_runner import run_benchmark


def main():

    # Step 1: Generate 3-SAT problem
    instance = generate_3sat_instance(
        num_variables=3,
        num_clauses=4,
        seed=42
    )

    num_variables = instance["num_variables"]
    clauses = instance["clauses"]

    print("===== 3-SAT BENCHMARK =====")
    print("Number of Variables:", num_variables)
    print("Clauses:", clauses)

    # Step 2: Find exact solution
    reference_solution = solve_3sat_brute_force(
        num_variables,
        clauses
    )

    if reference_solution is None:
        print("Formula is unsatisfiable.")
        return

    print("\nExact Solver Assignment:", reference_solution)

    # Step 3: Create validator
    def validator(solution):

        is_valid, details = validate_3sat_solution(
            num_variables,
            clauses,
            solution
        )

        if is_valid:
            return True, 1

        return False, None

    # Step 4: Connect Gemini
    provider = GeminiLLMProvider()

    print("\nSending 3-SAT problem to Gemini AI...")

    # Step 5: Run benchmark
    result = run_benchmark(
        problem_name="three_sat",
        instance=instance,
        optimal_value=1,
        objective="max",
        provider=provider,
        validator=validator,
        provider_name="gemini"
    )

    # Step 6: Display result
    print("\n===== GEMINI 3-SAT BENCHMARK RESULT =====")
    print("Gemini Assignment:", result["solution"])
    print("Valid Assignment:", result["validity"])
    print("Validation Details:", result["validation_result"])
    print("Metrics:", result["metrics"])
    print("Experiment ID:", result["experiment_id"])


if __name__ == "__main__":
    main()
