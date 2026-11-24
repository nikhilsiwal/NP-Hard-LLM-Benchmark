
import random
from itertools import product


# STEP 1: Generate Knapsack instance
def generate_knapsack_instance(num_items=5, capacity=15, seed=42):
    random.seed(seed)

    items = []

    for i in range(num_items):
        weight = random.randint(1, 10)
        value = random.randint(10, 100)

        items.append({
            "id": i,
            "weight": weight,
            "value": value
        })

    return {
        "capacity": capacity,
        "items": items
    }


# STEP 2: Calculate total weight and value
def calculate_knapsack_result(items, selection):
    total_weight = 0
    total_value = 0

    for i in range(len(items)):
        if selection[i] == 1:
            total_weight += items[i]["weight"]
            total_value += items[i]["value"]

    return total_weight, total_value


# STEP 3: Find optimal solution using Brute Force
def solve_knapsack_brute_force(items, capacity):
    n = len(items)

    best_selection = None
    best_value = 0
    best_weight = 0

    # Generate all possible 0/1 selections
    for selection in product([0, 1], repeat=n):

        weight, value = calculate_knapsack_result(
            items, selection
        )

        if weight <= capacity and value > best_value:
            best_selection = list(selection)
            best_value = value
            best_weight = weight

    return best_selection, best_weight, best_value


# STEP 4: Validate Knapsack solution
def validate_knapsack_solution(items, capacity, selection):
    n = len(items)

    if len(selection) != n:
        return False, "Invalid selection length"

    if any(type(x) is not int or x not in (0, 1) for x in selection):
        return False, "Selection must contain only 0 and 1"

    weight, value = calculate_knapsack_result(items, selection)

    if weight > capacity:
        return False, "Knapsack capacity exceeded"

    return True, {
        "total_weight": weight,
        "total_value": value
    }


# STEP 5: Run the program
if __name__ == "__main__":

    data = generate_knapsack_instance(
        num_items=5,
        capacity=15
    )

    items = data["items"]
    capacity = data["capacity"]

    print("Knapsack Capacity:", capacity)

    print("\nGenerated Items:")

    for item in items:
        print(item)

    selection, weight, value = solve_knapsack_brute_force(
        items, capacity
    )

    print("\nOptimal Selection:", selection)
    print("Total Weight:", weight)
    print("Maximum Value:", value)

    is_valid, result = validate_knapsack_solution(
        items, capacity, selection
    )

    print("\nValidation Result:", is_valid)
    print("Validation Details:", result)
