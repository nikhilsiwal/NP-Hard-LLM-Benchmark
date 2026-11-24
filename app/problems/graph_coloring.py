
import random
from itertools import product


# STEP 1: Generate a random graph
def generate_graph_instance(num_vertices=5, seed=42):
    random.seed(seed)

    edges = []

    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):

            # Randomly decide whether an edge exists
            if random.random() < 0.4:
                edges.append((i, j))

    return {
        "num_vertices": num_vertices,
        "edges": edges
    }


# STEP 2: Check whether a coloring is valid
def is_valid_coloring(graph, coloring):
    edges = graph["edges"]

    for u, v in edges:
        if coloring[u] == coloring[v]:
            return False

    return True


# STEP 3: Find minimum coloring using Brute Force
def solve_graph_coloring(graph):
    n = graph["num_vertices"]

    if n < 1:
        raise ValueError("Graph must have at least one vertex")

    # Try increasing number of colors
    for num_colors in range(1, n + 1):

        # Generate all possible color assignments
        for coloring in product(range(num_colors), repeat=n):

            if is_valid_coloring(graph, coloring):
                return list(coloring), num_colors

    return None, None


# STEP 4: Validate graph coloring solution
def validate_graph_coloring(graph, coloring):
    n = graph["num_vertices"]

    # Check coloring length
    if len(coloring) != n:
        return False, "Invalid coloring length"

    # Check color values
    if any(type(color) is not int or color < 0 for color in coloring):
        return False, "Invalid color value"

    # Check whether connected vertices have different colors
    if not is_valid_coloring(graph, coloring):
        return False, "Adjacent vertices have the same color"

    num_colors = len(set(coloring))

    return True, {
        "colors_used": num_colors,
        "coloring": coloring
    }


# STEP 5: Run the program
if __name__ == "__main__":

    graph = generate_graph_instance(
        num_vertices=5,
        seed=42
    )

    print("Number of Vertices:", graph["num_vertices"])
    print("\nGraph Edges:")

    for edge in graph["edges"]:
        print(edge)

    # Find minimum coloring
    coloring, num_colors = solve_graph_coloring(graph)

    print("\nOptimal Coloring:", coloring)
    print("Minimum Colors Required:", num_colors)

    # Validate the solution
    is_valid, result = validate_graph_coloring(
        graph, coloring
    )

    print("\nValidation Result:", is_valid)
    print("Validation Details:", result)
