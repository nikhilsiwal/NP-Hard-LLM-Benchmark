"""Run user-supplied TSP, Knapsack, and Graph Coloring instances.

For larger instances, use scalable reference algorithms:
- TSP: nearest-neighbour + 2-opt (heuristic for >9 cities)
- Knapsack: dynamic programming (exact, up to 50 items)
- Graph coloring: DSATUR greedy (heuristic for >8 vertices)

The returned reference_type makes it clear whether the reference is proven optimal.
"""

import math

from app.problems.tsp import (
    solve_tsp_brute_force,
    validate_tsp_solution,
)
from app.problems.knapsack import validate_knapsack_solution
from app.problems.graph_coloring import (
    solve_graph_coloring,
    validate_graph_coloring,
)
from app.llm.llm_interface import GeminiLLMProvider, GroqLLMProvider
from app.evaluation.benchmark_runner import run_benchmark


MAX_CUSTOM_SIZE = 50
MAX_KNAPSACK_CAPACITY = 100_000


def solve_tsp_nearest_neighbor_2opt(cities):
    """Return a good TSP tour using nearest-neighbour construction and 2-opt."""
    n = len(cities)
    if n < 2:
        raise ValueError("At least 2 cities are required")

    def distance(i, j):
        return math.hypot(
            cities[i]["x"] - cities[j]["x"],
            cities[i]["y"] - cities[j]["y"],
        )

    unvisited = set(range(1, n))
    route = [0]
    while unvisited:
        current = route[-1]
        nxt = min(unvisited, key=lambda city: distance(current, city))
        route.append(nxt)
        unvisited.remove(nxt)

    def total_distance(candidate):
        return sum(
            distance(candidate[i], candidate[(i + 1) % n])
            for i in range(n)
        )

    improved = True
    while improved:
        improved = False
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                candidate = route[:i] + route[i:j + 1][::-1] + route[j + 1:]
                if total_distance(candidate) + 1e-12 < total_distance(route):
                    route = candidate
                    improved = True
    return route, total_distance(route)


def solve_knapsack_dynamic_programming(items, capacity):
    """Exact 0/1 knapsack DP with solution reconstruction."""
    n = len(items)
    # dp[i][c] is the best value using the first i items and capacity c.
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i, item in enumerate(items, start=1):
        weight, value = item["weight"], item["value"]
        previous = dp[i - 1]
        current = dp[i]
        for cap in range(capacity + 1):
            current[cap] = previous[cap]
            if weight <= cap:
                current[cap] = max(
                    current[cap],
                    previous[cap - weight] + value,
                )

    selection = [0] * n
    remaining = capacity
    for i in range(n, 0, -1):
        if dp[i][remaining] != dp[i - 1][remaining]:
            selection[i - 1] = 1
            remaining -= items[i - 1]["weight"]

    total_weight = sum(
        item["weight"] for item, chosen in zip(items, selection) if chosen
    )
    return selection, total_weight, dp[n][capacity]


def solve_graph_coloring_dsatur(graph):
    """Greedy DSATUR coloring; valid coloring, not guaranteed minimum."""
    n = graph["num_vertices"]
    adjacency = [set() for _ in range(n)]
    for u, v in graph["edges"]:
        adjacency[u].add(v)
        adjacency[v].add(u)

    colors = [-1] * n
    uncolored = set(range(n))
    while uncolored:
        def priority(vertex):
            neighbor_colors = {
                colors[neighbor]
                for neighbor in adjacency[vertex]
                if colors[neighbor] != -1
            }
            return (len(neighbor_colors), len(adjacency[vertex]), -vertex)

        vertex = max(uncolored, key=priority)
        unavailable = {
            colors[neighbor]
            for neighbor in adjacency[vertex]
            if colors[neighbor] != -1
        }
        color = 0
        while color in unavailable:
            color += 1
        colors[vertex] = color
        uncolored.remove(vertex)

    return colors, len(set(colors))


def validate_custom_instance(problem_name, instance):
    if problem_name == "tsp":
        cities = instance.get("cities")
        if not isinstance(cities, list) or not 2 <= len(cities) <= MAX_CUSTOM_SIZE:
            raise ValueError("TSP supports 2 to 50 cities.")
        for index, city in enumerate(cities):
            if not isinstance(city, dict) or "x" not in city or "y" not in city:
                raise ValueError(f"City {index} must contain numeric x and y coordinates.")
            for coordinate in ("x", "y"):
                value = city[coordinate]
                if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                    raise ValueError(f"City {index} coordinate {coordinate} must be a finite number.")
            city["id"] = index
        return

    if problem_name == "knapsack":
        items = instance.get("items")
        capacity = instance.get("capacity")
        if not isinstance(items, list) or not 1 <= len(items) <= MAX_CUSTOM_SIZE:
            raise ValueError("Knapsack supports 1 to 50 items.")
        if type(capacity) is not int or not 0 <= capacity <= MAX_KNAPSACK_CAPACITY:
            raise ValueError("Capacity must be an integer from 0 to 100000.")
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
        n = instance.get("num_vertices")
        edges = instance.get("edges")
        if type(n) is not int or not 1 <= n <= MAX_CUSTOM_SIZE:
            raise ValueError("Graph Coloring supports 1 to 50 vertices.")
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
    """Compute a reference solution, call one LLM, validate, and persist metrics."""
    validate_custom_instance(problem_name, instance)

    if problem_name == "tsp":
        cities = instance["cities"]
        if len(cities) <= 9:
            reference_solution, reference_value = solve_tsp_brute_force(cities)
            reference_type = "exact"
        else:
            reference_solution, reference_value = solve_tsp_nearest_neighbor_2opt(cities)
            reference_type = "heuristic (nearest-neighbour + 2-opt)"

        objective = "min"

        def validator(solution):
            valid, value = validate_tsp_solution(cities, solution)
            return valid, value if valid else None

    elif problem_name == "knapsack":
        items, capacity = instance["items"], instance["capacity"]
        reference_solution, _, reference_value = solve_knapsack_dynamic_programming(items, capacity)
        reference_type = "exact (dynamic programming)"
        objective = "max"

        def validator(solution):
            valid, details = validate_knapsack_solution(items, capacity, solution)
            return (True, details["total_value"]) if valid else (False, None)

    else:
        if instance["num_vertices"] <= 8:
            reference_solution, reference_value = solve_graph_coloring(instance)
            reference_type = "exact"
        else:
            reference_solution, reference_value = solve_graph_coloring_dsatur(instance)
            reference_type = "heuristic (DSATUR)"
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
        optimal_value=round(reference_value, 2),
        objective=objective,
        provider=provider,
        validator=validator,
        provider_name=provider_name,
    )
    result["exact_solution"] = reference_solution
    result["exact_value"] = reference_value
    result["reference_type"] = reference_type
    return result
