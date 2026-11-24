
from app.problems.subset_sum import (
    generate_subset_sum_instance,
    calculate_subset_sum,
    solve_subset_sum_brute_force,
    validate_subset_sum_solution
)


# TEST 1
def test_generate_subset_sum_instance():
    data = generate_subset_sum_instance(6)

    assert len(data["numbers"]) == 6
    assert data["target"] > 0


# TEST 2
def test_calculate_subset_sum():
    numbers = [3, 5, 7]
    selection = [1, 0, 1]

    assert calculate_subset_sum(numbers, selection) == 10


# TEST 3
def test_solve_subset_sum():
    numbers = [3, 5, 7, 10]
    target = 15

    selection = solve_subset_sum_brute_force(numbers, target)

    assert selection is not None
    assert calculate_subset_sum(numbers, selection) == target


# TEST 4
def test_no_solution():
    numbers = [2, 4, 6]
    target = 5

    selection = solve_subset_sum_brute_force(numbers, target)

    assert selection is None


# TEST 5
def test_validate_valid_solution():
    numbers = [3, 5, 7]
    target = 10
    selection = [1, 0, 1]

    is_valid, result = validate_subset_sum_solution(
        numbers, target, selection
    )

    assert is_valid is True
    assert result == 10


# TEST 6
def test_validate_invalid_sum():
    numbers = [3, 5, 7]
    target = 15
    selection = [1, 0, 0]

    is_valid, result = validate_subset_sum_solution(
        numbers, target, selection
    )

    assert is_valid is False


# TEST 7
def test_validate_invalid_length():
    numbers = [3, 5, 7]
    target = 10
    selection = [1, 0]

    is_valid, result = validate_subset_sum_solution(
        numbers, target, selection
    )

    assert is_valid is False
