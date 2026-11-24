
from app.problems.knapsack import (
    generate_knapsack_instance,
    calculate_knapsack_result,
    solve_knapsack_brute_force,
    validate_knapsack_solution
)


# TEST 1: Check item generator
def test_generate_knapsack_instance():
    data = generate_knapsack_instance(5, 15)

    assert len(data["items"]) == 5
    assert data["capacity"] == 15


# TEST 2: Check weight and value calculation
def test_calculate_knapsack_result():
    items = [
        {"id": 0, "weight": 2, "value": 10},
        {"id": 1, "weight": 3, "value": 20}
    ]

    selection = [1, 1]

    weight, value = calculate_knapsack_result(items, selection)

    assert weight == 5
    assert value == 30


# TEST 3: Check Brute Force Solver
def test_solve_knapsack_brute_force():
    items = [
        {"id": 0, "weight": 2, "value": 10},
        {"id": 1, "weight": 3, "value": 20},
        {"id": 2, "weight": 4, "value": 30}
    ]

    selection, weight, value = solve_knapsack_brute_force(items, 5)

    assert selection == [0, 0, 1]
    assert weight == 4
    assert value == 30


# TEST 4: Check valid solution
def test_validate_valid_solution():
    items = [
        {"id": 0, "weight": 2, "value": 10},
        {"id": 1, "weight": 3, "value": 20}
    ]

    selection = [1, 1]

    is_valid, result = validate_knapsack_solution(
        items, 5, selection
    )

    assert is_valid is True
    assert result["total_weight"] == 5
    assert result["total_value"] == 30


# TEST 5: Check invalid selection length
def test_validate_invalid_length():
    items = [
        {"id": 0, "weight": 2, "value": 10},
        {"id": 1, "weight": 3, "value": 20}
    ]

    selection = [1]

    is_valid, result = validate_knapsack_solution(
        items, 5, selection
    )

    assert is_valid is False


# TEST 6: Check capacity exceeded
def test_validate_capacity_exceeded():
    items = [
        {"id": 0, "weight": 4, "value": 10},
        {"id": 1, "weight": 5, "value": 20}
    ]

    selection = [1, 1]

    is_valid, result = validate_knapsack_solution(
        items, 7, selection
    )

    assert is_valid is False
    assert result == "Knapsack capacity exceeded"


# TEST 7: Check invalid selection values
def test_validate_invalid_selection():
    items = [
        {"id": 0, "weight": 2, "value": 10},
        {"id": 1, "weight": 3, "value": 20}
    ]

    selection = [1, 2]

    is_valid, result = validate_knapsack_solution(
        items, 5, selection
    )

    assert is_valid is False

