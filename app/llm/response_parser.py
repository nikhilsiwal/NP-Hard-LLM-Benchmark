
import json
import re


def parse_llm_response(response):

    if not isinstance(response, str):
        raise ValueError("Response must be a string")

    response = response.strip()

    if not response:
        raise ValueError("Response is empty")

    # Remove Markdown code block if present
    response = re.sub(r"^```(?:json)?\s*", "", response)
    response = re.sub(r"\s*```$", "", response)

    try:
        data = json.loads(response)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON response")

    if not isinstance(data, dict):
        raise ValueError("Response must be a JSON object")

    if "solution" not in data:
        raise ValueError("Solution field not found")

    solution = data["solution"]

    if not isinstance(solution, list):
        raise ValueError("Solution must be a list")

    return solution


if __name__ == "__main__":

    sample_response = """
    {
        "solution": [1, 0, 1, 0]
    }
    """

    result = parse_llm_response(sample_response)

    print("LLM Response:", sample_response)
    print("Extracted Solution:", result)
