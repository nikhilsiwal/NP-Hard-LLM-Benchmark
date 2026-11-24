
def calculate_optimality_gap(
    llm_value,
    optimal_value,
    objective="min"
):
    if objective not in ["min", "max"]:
        raise ValueError("Objective must be 'min' or 'max'")

    if llm_value is None or optimal_value is None:
        return None

    if optimal_value == 0:
        if llm_value == optimal_value:
            return 0.0
        return None

    if objective == "min":
        gap = ((llm_value - optimal_value) / abs(optimal_value)) * 100

    else:
        gap = ((optimal_value - llm_value) / abs(optimal_value)) * 100

    return round(gap, 2)


def evaluate_metrics(
    is_valid,
    llm_value,
    optimal_value,
    objective="min",
    latency=None,
    tokens_used=None
):
    if type(is_valid) is not bool:
        raise ValueError("is_valid must be True or False")

    if latency is not None and latency < 0:
        raise ValueError("Latency cannot be negative")

    if tokens_used is not None:
        if type(tokens_used) is not int or tokens_used < 0:
            raise ValueError("Tokens must be a non-negative integer")

    if objective not in ["min", "max"]:
        raise ValueError("Invalid objective")

    if not is_valid or llm_value is None or optimal_value is None:
        accuracy = 0.0
        gap = None

    else:
        accuracy = 1.0 if llm_value == optimal_value else 0.0

        gap = calculate_optimality_gap(
            llm_value,
            optimal_value,
            objective
        )

    return {
        "validity": is_valid,
        "accuracy": accuracy,
        "optimality_gap": gap,
        "latency": latency,
        "tokens_used": tokens_used
    }


if __name__ == "__main__":

    metrics = evaluate_metrics(
        is_valid=True,
        llm_value=120,
        optimal_value=100,
        objective="min",
        latency=1.5,
        tokens_used=150
    )

    print("Evaluation Metrics:")
    for key, value in metrics.items():
        print(key, ":", value)
