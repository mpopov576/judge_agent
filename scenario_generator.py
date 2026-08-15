from local_llm import generate, generate_json
from case_types import get_random_case_type
import json

max_json_retries = 2

def generate_scenario():
    case_type = get_random_case_type()

    instructions = f"""
        Generate a realistic legal dispute.
        
        Case Type:
        {case_type}

        The case must be genuinely balanced: based only on the facts,
        neither side should have an obvious advantage.

        Provide:
        - background
        - parties
        - dispute
        - relevant shared facts

        Do not provide, evidence, claims, or a verdict.
    """

    scenario = generate(instructions)

    return scenario

def generate_side_a(scenario):
    # Creating the information given to Attorney A
    side_a_prompt = f"""
        You are generating the private information given to Attorney A by
        their client.

        The client is NOT a lawyer. Their account should sound like a real
        person explaining what happened to their attorney. It may be messy,
        emotional, incomplete, biased, poorly organized, or use incorrect
        legal terminology.

        Generate:

        1. The client's raw account of what happened.
        2. Evidence the client provides to Attorney A.

        The attorney will later interpret this information and present a
        formal argument to the judge.

        IMPORTANT:
        - Do not write the attorney's argument.
        - Do not make the client's account polished or legally structured.
        - The client may misunderstand parts of the situation.
        - Evidence must be consistent with the scenario.
        - Do not invent facts that contradict the scenario.
        - Evidence should contain both strong and weak pieces.

        Scenario:
        {scenario}
    """
    last_error = None

    for attempt in range(max_json_retries + 1):
        try:
            a_statement = generate_json(side_a_prompt)
            return json.loads(a_statement)
        except json.JSONDecodeError as e:
            last_error = e
            print(f"generate_side_a: failed after {max_json_retries + 1} attempts: {last_error}")

    raise RuntimeError(f"generate_side_a: failed after {max_json_retries + 1} attempts: {last_error}")




def generate_side_b(scenario):
    # Creating the information given to Attorney B
    side_b_prompt = f"""
        You are generating the private information given to Attorney B by
        their client.

        The client is NOT a lawyer. Their account should sound like a real
        person explaining what happened to their attorney. It may be messy,
        emotional, incomplete, biased, poorly organized, or use incorrect
        legal terminology.

        Generate:

        1. The client's raw account of what happened.
        2. Evidence the client provides to Attorney B.

        The attorney will later interpret this information and present a
        formal argument to the judge.

        IMPORTANT:
        - Do not write the attorney's argument.
        - Do not make the client's account polished or legally structured.
        - The client may misunderstand parts of the situation.
        - Evidence must be consistent with the scenario.
        - Do not invent facts that contradict the scenario.
        - Evidence should contain both strong and weak pieces.

        Scenario:
        {scenario}
    """

    last_error = None
    for attempt in range(max_json_retries + 1):
        try:
            b_statement = generate_json(side_b_prompt)
            return json.loads(b_statement)
        except json.JSONDecodeError as e:
            last_error = e
            print(f"generate_side_b: JSON decode failed on attempt {attempt + 1}: {e}")

    raise RuntimeError(f"generate_side_b: failed after {max_json_retries + 1} attempts: {last_error}")