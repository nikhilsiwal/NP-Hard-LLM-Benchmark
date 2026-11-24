
import pytest

from app.problems.tsp import (
    generate_tsp_instance,
    calculate_distance,
    calculate_tour_distance,
    solve_tsp_brute_force,
    validate_tsp_solution
)


# TEST 1: Check city generator
def test_generate_tsp_instance():
    cities = generate_tsp_instance(5)

    assert len(cities) == 5


# TEST 2: Check distance calculation
def test_calculate_distance():
    city1 = {"id": 0, "x": 0, "y": 0}
    city2 = {"id": 1, "x": 3, "y": 4}

    distance = calculate_distance(city1, city2)

    assert distance == 5.0


# TEST 3: Check total tour distance
def test_calculate_tour_distance():
    cities = [
        {"id": 0, "x": 0, "y": 0},
        {"id": 1, "x": 3, "y": 0},
        {"id": 2, "x": 3, "y": 4}
    ]

    route = [0, 1, 2]

    distance = calculate_tour_distance(cities, route)

    assert distance == 12.0


# TEST 4: Check Brute Force Solver
def test_solve_tsp_brute_force():
    cities = generate_tsp_instance(5)

    route, distance = solve_tsp_brute_force(cities)

    assert len(route) == 5
    assert len(set(route)) == 5
    assert distance > 0


# TEST 5: Check valid route
def test_validate_valid_route():
    cities = generate_tsp_instance(5)

    route = [0, 1, 2, 3, 4]

    is_valid, result = validate_tsp_solution(cities, route)

    assert is_valid is True
    assert isinstance(result, float)


# TEST 6: Check duplicate city
def test_validate_duplicate_route():
    cities = generate_tsp_instance(5)

    route = [0, 1, 1, 3, 4]

    is_valid, result = validate_tsp_solution(cities, route)

    assert is_valid is False
    assert result == "Duplicate cities found"


# TEST 7: Check incomplete route
def test_validate_incomplete_route():
    cities = generate_tsp_instance(5)

    route = [0, 1, 2, 3]

    is_valid, result = validate_tsp_solution(cities, route)

    assert is_valid is False
    assert result == "Invalid route length"
