
import json


def build_prompt(problem_name, instance):

    problem_name = problem_name.lower()

    instructions = {

        "tsp": """
Solve the Travelling Salesperson Problem.
Find the shortest route visiting every city exactly once
and returning to the starting city.
Return the route as a list of city indices.
Do not repeat the starting city at the end.
""",

        "knapsack": """
Solve the 0/1 Knapsack Problem.
Choose items to maximize total value without exceeding capacity.
Return a binary selection list where 1 means selected
and 0 means not selected.
""",

        "graph_coloring": """
Solve the Graph Coloring Problem.
Assign colors to vertices so that no connected vertices
have the same color.
Use non-negative integers as color labels.
Return a list of colors for all vertices.
""",

        "three_sat": """
Solve the 3-SAT Problem.
Find a Boolean assignment that satisfies every clause.
Return a list containing only true or false values.
""",

        "subset_sum": """
Solve the Subset Sum Problem.
Find a subset whose sum is exactly equal to the target.
Return a binary selection list where 1 means selected
and 0 means not selected.
"""
    }

    if problem_name not in instructions:
        raise ValueError("Unsupported problem name")

    prompt = f"""
You are an expert problem-solving AI.

PROBLEM:
{problem_name.upper()}

INSTRUCTIONS:
{instructions[problem_name]}

INPUT INSTANCE:
{json.dumps(instance, indent=2)}

OUTPUT FORMAT:
Return only valid JSON in this format:

{{
    "solution": [your_answer]
}}

Do not include explanations or Markdown.
"""

    return prompt


if __name__ == "__main__":

    sample_instance = {
        "numbers": [3, 5, 7, 10],
        "target": 15
    }

    prompt = build_prompt("subset_sum", sample_instance)

    print(prompt)
