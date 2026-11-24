
from app.problems.graph_coloring import (
    generate_graph_instance,
    is_valid_coloring,
    solve_graph_coloring,
    validate_graph_coloring
)


# TEST 1: Check graph generator
def test_generate_graph_instance():
    graph = generate_graph_instance(5)

    assert graph["num_vertices"] == 5
    assert isinstance(graph["edges"], list)


# TEST 2: Check valid coloring
def test_valid_coloring():
    graph = {
        "num_vertices": 3,
        "edges": [(0, 1), (1, 2)]
    }

    coloring = [0, 1, 0]

    assert is_valid_coloring(graph, coloring) is True


# TEST 3: Check invalid coloring
def test_invalid_coloring():
    graph = {
        "num_vertices": 3,
        "edges": [(0, 1), (1, 2)]
    }

    coloring = [0, 0, 1]

    assert is_valid_coloring(graph, coloring) is False


# TEST 4: Check Brute Force Solver
def test_solve_graph_coloring():
    graph = {
        "num_vertices": 3,
        "edges": [(0, 1), (1, 2), (0, 2)]
    }

    coloring, num_colors = solve_graph_coloring(graph)

    assert num_colors == 3
    assert is_valid_coloring(graph, coloring) is True


# TEST 5: Check valid solution validator
def test_validate_valid_coloring():
    graph = {
        "num_vertices": 3,
        "edges": [(0, 1), (1, 2)]
    }

    coloring = [0, 1, 0]

    is_valid, result = validate_graph_coloring(graph, coloring)

    assert is_valid is True
    assert result["colors_used"] == 2


# TEST 6: Check invalid solution validator
def test_validate_invalid_coloring():
    graph = {
        "num_vertices": 3,
        "edges": [(0, 1), (1, 2)]
    }

    coloring = [0, 0, 1]

    is_valid, result = validate_graph_coloring(graph, coloring)

    assert is_valid is False


# TEST 7: Check incorrect coloring length
def test_validate_invalid_length():
    graph = {
        "num_vertices": 3,
        "edges": [(0, 1), (1, 2)]
    }

    coloring = [0, 1]

    is_valid, result = validate_graph_coloring(graph, coloring)

    assert is_valid is False
