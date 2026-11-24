
from app.problems.three_sat import (
    generate_3sat_instance,
    evaluate_clause,
    evaluate_3sat_formula,
    solve_3sat_brute_force,
    validate_3sat_solution
)


# TEST 1: Check 3-SAT generator
def test_generate_3sat_instance():
    data = generate_3sat_instance(3, 4)

    assert data["num_variables"] == 3
    assert len(data["clauses"]) == 4

    for clause in data["clauses"]:
        assert len(clause) == 3


# TEST 2: Check clause evaluation
def test_evaluate_clause():
    clause = [1, -2, 3]
    assignment = [True, False, False]

    result = evaluate_clause(clause, assignment)

    assert result is True


# TEST 3: Check unsatisfied clause
def test_unsatisfied_clause():
    clause = [1, 2, 3]
    assignment = [False, False, False]

    result = evaluate_clause(clause, assignment)

    assert result is False


# TEST 4: Check complete formula
def test_evaluate_3sat_formula():
    clauses = [
        [1, -2, 3],
        [-1, 2, 3]
    ]

    assignment = [True, False, True]

    result = evaluate_3sat_formula(clauses, assignment)

    assert result is True


# TEST 5: Check Brute Force Solver
def test_solve_3sat_brute_force():
    clauses = [
        [1, 2, 3],
        [-1, 2, 3],
        [1, -2, 3]
    ]

    assignment = solve_3sat_brute_force(3, clauses)

    assert assignment is not None
    assert evaluate_3sat_formula(clauses, assignment) is True


# TEST 6: Check unsatisfiable formula
def test_unsatisfiable_formula():
    clauses = [
        [1, 2, 3],
        [-1, 2, 3],
        [1, -2, 3],
        [1, 2, -3],
        [-1, -2, 3],
        [-1, 2, -3],
        [1, -2, -3],
        [-1, -2, -3]
    ]

    assignment = solve_3sat_brute_force(3, clauses)

    assert assignment is None


# TEST 7: Check solution validator
def test_validate_3sat_solution():
    clauses = [
        [1, -2, 3],
        [-1, 2, 3]
    ]

    assignment = [True, False, True]

    is_valid, result = validate_3sat_solution(
        3, clauses, assignment
    )

    assert is_valid is True
    assert result == "All clauses are satisfied"
