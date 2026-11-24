
import random
from itertools import product


def generate_subset_sum_instance(num_numbers=6, seed=42):
    random.seed(seed)

    numbers = random.sample(range(1, 30), num_numbers)

    # Generate a target using a random subset
    selection = [
        random.choice([0, 1])
        for _ in range(num_numbers)
    ]

    if sum(selection) == 0:
        selection[0] = 1

    target = sum(
        numbers[i] * selection[i]
        for i in range(num_numbers)
    )

    return {
        "numbers": numbers,
        "target": target
    }


def calculate_subset_sum(numbers, selection):
    total = 0

    for i in range(len(numbers)):
        if selection[i] == 1:
            total += numbers[i]

    return total


def solve_subset_sum_brute_force(numbers, target):
    n = len(numbers)

    for selection in product([0, 1], repeat=n):
        total = calculate_subset_sum(numbers, selection)

        if total == target:
            return list(selection)

    return None


def validate_subset_sum_solution(numbers, target, selection):

    if selection is None:
        return False, "No solution found"

    if len(selection) != len(numbers):
        return False, "Invalid selection length"

    if any(value not in [0, 1] or type(value) is not int
           for value in selection):
        return False, "Selection must contain only 0 or 1"

    total = calculate_subset_sum(numbers, selection)

    if total != target:
        return False, "Subset sum does not match target"

    return True, total


if __name__ == "__main__":

    data = generate_subset_sum_instance()

    numbers = data["numbers"]
    target = data["target"]

    print("Numbers:", numbers)
    print("Target:", target)

    selection = solve_subset_sum_brute_force(numbers, target)

    print("\nSelection:", selection)

    if selection is not None:
        selected_numbers = [
            numbers[i]
            for i in range(len(numbers))
            if selection[i] == 1
        ]
        print("Selected Numbers:", selected_numbers)

    is_valid, result = validate_subset_sum_solution(
        numbers, target, selection
    )

    print("\nValidation Result:", is_valid)
    print("Validation Details:", result)
