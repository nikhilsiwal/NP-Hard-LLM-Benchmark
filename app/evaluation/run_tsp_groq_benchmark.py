
from app.problems.tsp import (
    generate_tsp_instance,
    solve_tsp_brute_force,
    validate_tsp_solution
)

from app.llm.llm_interface import GroqLLMProvider
from app.evaluation.benchmark_runner import run_benchmark


def calculate_distance(cities, route):
    total = 0

    for i in range(len(route)):
        current_city = cities[route[i]]
        next_city = cities[route[(i + 1) % len(route)]]

        dx = current_city["x"] - next_city["x"]
        dy = current_city["y"] - next_city["y"]

        total += (dx ** 2 + dy ** 2) ** 0.5

    return total


def two_opt(cities, route):
    best_route = route[:]
    best_distance = calculate_distance(cities, best_route)

    improved = True

    while improved:
        improved = False

        for i in range(1, len(best_route) - 1):
            for j in range(i + 1, len(best_route)):

                new_route = best_route[:]
                new_route[i:j + 1] = reversed(
                    new_route[i:j + 1]
                )

                new_distance = calculate_distance(
                    cities,
                    new_route
                )

                if new_distance < best_distance - 1e-9:
                    best_route = new_route
                    best_distance = new_distance
                    improved = True

    return best_route, best_distance


def main():

    cities = generate_tsp_instance(
        num_cities=5,
        seed=42
    )

    instance = {"cities": cities}

    print("===== GROQ TSP BENCHMARK =====")
    print("Cities:", cities)

    reference_solution = solve_tsp_brute_force(cities)

    if reference_solution is None:
        print("No reference solution found.")
        return

    optimal_route, optimal_distance = reference_solution

    print("\nExact Solver Route:", optimal_route)
    print("Exact Minimum Distance:", optimal_distance)

    def validator(solution):
        is_valid, details = validate_tsp_solution(
            cities,
            solution
        )

        return is_valid, details if is_valid else None

    provider = GroqLLMProvider(
        model="openai/gpt-oss-120b"
    )

    print("\nSending TSP problem to Groq AI...")

    result = run_benchmark(
        problem_name="tsp",
        instance=instance,
        optimal_value=round(optimal_distance, 2),
        objective="min",
        provider=provider,
        validator=validator,
        provider_name="groq"
    )

    print("\n===== RAW GROQ RESULT =====")
    print("Groq Route:", result["solution"])
    print("Valid Route:", result["validity"])
    print("Groq Distance:", result["validation_result"])
    print("Metrics:", result["metrics"])
    print("Experiment ID:", result["experiment_id"])

    if result["validity"]:

        optimized_route, optimized_distance = two_opt(
            cities,
            result["solution"]
        )

        gap = (
            (optimized_distance - optimal_distance)
            / optimal_distance
        ) * 100

        print("\n===== AFTER 2-OPT OPTIMIZATION =====")
        print("Optimized Route:", optimized_route)
        print("Optimized Distance:", round(optimized_distance, 4))
        print("Optimality Gap:", round(gap, 4), "%")
        print(
            "Matches Exact Optimum:",
            abs(optimized_distance - optimal_distance) < 1e-6
        )


if __name__ == "__main__":
    main()
