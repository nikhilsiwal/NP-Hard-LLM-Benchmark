
import time

from app.llm.prompt_manager import build_prompt
from app.llm.response_parser import parse_llm_response
from app.evaluation.metrics import evaluate_metrics
from app.database.experiment_db import save_experiment


def run_benchmark(
    problem_name,
    instance,
    optimal_value,
    objective,
    provider,
    validator,
    provider_name="mock"
):

    # Step 1: Generate prompt
    prompt = build_prompt(problem_name, instance)

    # Step 2: Get LLM response
    start_time = time.time()

    response = provider.generate_response(prompt)

    latency = time.time() - start_time

    # Step 3: Read token usage if provider supports it
    tokens_used = getattr(provider, "total_tokens", None)

    # Step 4: Parse response
    solution = parse_llm_response(response)

    # Step 5: Validate solution
    is_valid, validation_result = validator(solution)

    # Step 6: Calculate metrics
    llm_value = validation_result if is_valid else None

    metrics = evaluate_metrics(
        is_valid=is_valid,
        llm_value=llm_value,
        optimal_value=optimal_value,
        objective=objective,
        latency=round(latency, 4),
        tokens_used=tokens_used
    )

    # Step 7: Save experiment
    experiment_id = save_experiment(
        problem_name=problem_name,
        provider=provider_name,
        solution=solution,
        metrics=metrics
    )

    return {
        "experiment_id": experiment_id,
        "problem_name": problem_name,
        "solution": solution,
        "validity": is_valid,
        "validation_result": validation_result,
        "metrics": metrics
    }
