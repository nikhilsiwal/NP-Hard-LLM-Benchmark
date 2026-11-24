
def main():
    print("=" * 50)
    print("NP-HARD PROBLEM WITH LLM BENCHMARKING")
    print("=" * 50)
    print("Project environment is ready!")
    print("Development will start soon.")



if __name__ == "__main__":

    cities = generate_tsp_instance(5)

    print("Generated Cities:")

    for city in cities:
        print(city)

    route, distance = solve_tsp_brute_force(cities)

    print("\nOptimal Route:", route + [route[0]])
    print("Minimum Distance:", round(distance, 2))

    # Validate the route
    is_valid, result = validate_tsp_solution(cities, route)

    print("\nValidation Result:", is_valid)
    print("Validation Details:", result)
