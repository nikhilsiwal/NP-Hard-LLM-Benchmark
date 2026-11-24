
import random
from itertools import product


# STEP 1: Generate a random 3-SAT instance
def generate_3sat_instance(num_variables=3, num_clauses=4, seed=42):
    random.seed(seed)

    clauses = []

    for _ in range(num_clauses):
        variables = random.sample(
            range(1, num_variables + 1), 3
        )

        clause = []

        for variable in variables:
            # Positive number means variable
            # Negative number means NOT variable
            literal = variable * random.choice([-1, 1])
            clause.append(literal)

        clauses.append(clause)

    return {
        "num_variables": num_variables,
        "clauses": clauses
    }


# STEP 2: Evaluate one clause
def evaluate_clause(clause, assignment):
    for literal in clause:
        variable = abs(literal)

        value = assignment[variable - 1]

        if literal < 0:
            value = not value

        if value:
            return True

    return False


# STEP 3: Evaluate complete 3-SAT formula
def evaluate_3sat_formula(clauses, assignment):
    for clause in clauses:
        if not evaluate_clause(clause, assignment):
            return False

    return True


# STEP 4: Find solution using Brute Force
def solve_3sat_brute_force(num_variables, clauses):
    # Generate all True/False combinations
    for assignment in product([False, True], repeat=num_variables):

        if evaluate_3sat_formula(clauses, assignment):
            return list(assignment)

    return None


# STEP 5: Validate 3-SAT solution
def validate_3sat_solution(num_variables, clauses, assignment):

    if assignment is None:
        return False, "No satisfying assignment found"

    if len(assignment) != num_variables:
        return False, "Invalid assignment length"

    if any(type(value) is not bool for value in assignment):
        return False, "Assignment must contain only True or False"

    if not evaluate_3sat_formula(clauses, assignment):
        return False, "Some clauses are not satisfied"

    return True, "All clauses are satisfied"


# STEP 6: Run the program
if __name__ == "__main__":

    data = generate_3sat_instance(
        num_variables=3,
        num_clauses=4
    )

    num_variables = data["num_variables"]
    clauses = data["clauses"]

    print("Number of Variables:", num_variables)

    print("\nGenerated Clauses:")

    for clause in clauses:
        print(clause)

    # Find satisfying assignment
    assignment = solve_3sat_brute_force(
        num_variables, clauses
    )

    print("\nSatisfying Assignment:", assignment)

    # Validate solution
    is_valid, result = validate_3sat_solution(
        num_variables, clauses, assignment
    )

    print("\nValidation Result:", is_valid)
    print("Validation Details:", result)
