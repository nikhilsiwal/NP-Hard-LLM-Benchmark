

import random
import math
from itertools import permutations


# STEP 1: Generate random cities
def generate_tsp_instance(num_cities=5, seed=42):
    random.seed(seed)

    cities = []

    for i in range(num_cities):
        x = random.randint(0, 100)
        y = random.randint(0, 100)

        cities.append({
            "id": i,
            "x": x,
            "y": y
        })

    return cities


# STEP 2: Calculate distance between two cities
def calculate_distance(city1, city2):
    dx = city1["x"] - city2["x"]
    dy = city1["y"] - city2["y"]

    return math.sqrt(dx**2 + dy**2)


# STEP 3: Calculate total distance of a route
def calculate_tour_distance(cities, route):
    total_distance = 0

    for i in range(len(route)):
        current_city = cities[route[i]]
        next_city = cities[route[(i + 1) % len(route)]]

        total_distance += calculate_distance(
            current_city,
            next_city
        )

    return total_distance


# STEP 4: Find optimal route using Brute Force
def solve_tsp_brute_force(cities):
    n = len(cities)

    if n < 2:
        raise ValueError("At least 2 cities are required")

    best_route = None
    best_distance = float("inf")

    # Fix city 0 as the starting city
    for perm in permutations(range(1, n)):
        route = [0] + list(perm)

        distance = calculate_tour_distance(cities, route)

        if distance < best_distance:
            best_distance = distance
            best_route = route

    return best_route, best_distance


# STEP 5: Validate TSP Solution
def validate_tsp_solution(cities, route):
    n = len(cities)

    # Check route length
    if len(route) != n:
        return False, "Invalid route length"

    # Check city IDs are valid integers
    if any(type(city) is not int or city < 0 or city >= n for city in route):
        return False, "Invalid city ID found"

    # Check duplicate cities
    if len(set(route)) != n:
        return False, "Duplicate cities found"

    # Check all cities are visited
    if set(route) != set(range(n)):
        return False, "Some cities are missing"

    # Calculate total distance
    distance = calculate_tour_distance(cities, route)

    return True, round(distance, 2)


# STEP 6: Run the program
if __name__ == "__main__":

    cities = generate_tsp_instance(5)

    print("Generated Cities:")

    for city in cities:
        print(city)

    # Find optimal route
    route, distance = solve_tsp_brute_force(cities)

    print("\nOptimal Route:", route + [route[0]])
    print("Minimum Distance:", round(distance, 2))

    # Validate the route
    is_valid, result = validate_tsp_solution(cities, route)

    print("\nValidation Result:", is_valid)
    print("Validation Details:", result)


