"""Run user-supplied TSP, Knapsack, and Graph Coloring instances."""

from app.problems.tsp import solve_tsp_brute_force, validate_tsp_solution
from app.problems.knapsack import (
    solve_knapsack_brute_force,
    validate_knapsack_solution,
)
from app.problems.graph_coloring import (
    solve_graph_coloring,
    validate_graph_coloring,
)
from app.llm.llm_interface import GeminiLLMProvider, GroqLLMProvider
from app.evaluation.benchmark_runner import run_benchmark


def validate_custom_instance(problem_name, instance):
    if problem_name == "tsp":
        cities = instance["cities"]
        if not isinstance(cities, list) or not 2 <= len(cities) <= 9:
            raise ValueError("TSP needs 2 to 9 cities for exact brute-force comparison.")
        for index, city in enumerate(cities):
            if not isinstance(city, dict) or "x" not in city or "y" not in city:
                raise ValueError(f"City {index} must contain numeric x and y coordinates.")
            if not isinstance(city["x"], (int, float)) or not isinstance(city["y"], (int, float)):
                raise ValueError(f"City {index} coordinates must be numbers.")
            city["id"] = index
        return

    if problem_name == "knapsack":
        items = instance["items"]
        capacity = instance["capacity"]
        if not isinstance(items, list) or not 1 <= len(items) <= 18:
            raise ValueError("Knapsack needs 1 to 18 items for exact brute-force comparison.")
        if type(capacity) is not int or capacity < 0:
            raise ValueError("Capacity must be a non-negative integer.")
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                raise ValueError(f"Item {index} must be an object.")
            if type(item.get("weight")) is not int or item["weight"] < 0:
                raise ValueError(f"Item {index} weight must be a non-negative integer.")
            if type(item.get("value")) is not int or item["value"] < 0:
                raise ValueError(f"Item {index} value must be a non-negative integer.")
            item["id"] = index
        return

    if problem_name == "graph_coloring":
        n = instance["num_vertices"]
        edges = instance["edges"]
        if type(n) is not int or not 1 <= n <= 8:
            raise ValueError("Graph Coloring supports 1 to 8 vertices for exact comparison.")
        if not isinstance(edges, list):
            raise ValueError("Edges must be a list of [u, v] pairs.")
        normalized = []
        for edge in edges:
            if not isinstance(edge, (list, tuple)) or len(edge) != 2:
                raise ValueError("Each edge must look like [0, 1].")
            u, v = edge
            if type(u) is not int or type(v) is not int or not (0 <= u < n and 0 <= v < n) or u == v:
                raise ValueError(f"Invalid edge: {edge}")
            normalized.append([min(u, v), max(u, v)])
        if len({tuple(edge) for edge in normalized}) != len(normalized):
            raise ValueError("Duplicate edges are not allowed.")
        instance["edges"] = [tuple(edge) for edge in normalized]
        return

    raise ValueError("Unsupported custom problem.")


def run_custom_benchmark(problem_name, instance, provider_name):
    """Compute exact reference, call one LLM, validate, and persist metrics."""
    validate_custom_instance(problem_name, instance)

    if problem_name == "tsp":
        cities = instance["cities"]
        exact_route, exact_value = solve_tsp_brute_force(cities)
        optimal_solution = exact_route
        objective = "min"

        def validator(solution):
            valid, value = validate_tsp_solution(cities, solution)
            return valid, value if valid else None

    elif problem_name == "knapsack":
        items, capacity = instance["items"], instance["capacity"]
        optimal_solution, _, exact_value = solve_knapsack_brute_force(items, capacity)
        if optimal_solution is None:
            optimal_solution = [0] * len(items)
            exact_value = 0
        objective = "max"

        def validator(solution):
            valid, details = validate_knapsack_solution(items, capacity, solution)
            return (True, details["total_value"]) if valid else (False, None)

    else:
        exact_coloring, exact_value = solve_graph_coloring(instance)
        optimal_solution = exact_coloring
        objective = "min"

        def validator(solution):
            valid, details = validate_graph_coloring(instance, solution)
            return (True, details["colors_used"]) if valid else (False, None)

    if provider_name == "gemini":
        provider = GeminiLLMProvider()
    elif provider_name == "groq":
        provider = GroqLLMProvider()
    else:
        raise ValueError("Provider must be gemini or groq.")

    result = run_benchmark(
        problem_name=problem_name,
        instance=instance,
        optimal_value=round(exact_value, 2),
        objective=objective,
        provider=provider,
        validator=validator,
        provider_name=provider_name,
    )
    result["exact_solution"] = optimal_solution
    result["exact_value"] = exact_value
    return result
