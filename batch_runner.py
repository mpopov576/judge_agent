from scenario_generator import generate_scenario, generate_side_a, generate_side_b
from attorney_a import generate_attorney_a
from attorney_b import generate_attorney_b
from judge import judge_case
from result_logger import save_trial
import random

# No random seed because the results are not reproducible anyway (the case would be different)

num_iterations = 200

def run_trial(case_id, word_limit_a, word_limit_b):
    print(f"Starting trial {case_id}...")

    scenario = generate_scenario()

    side_a = generate_side_a(scenario)
    side_b = generate_side_b(scenario)

    statement_a = generate_attorney_a(side_a, word_limit_a)
    statement_b = generate_attorney_b(side_b, word_limit_b)

    result = judge_case(statement_a, statement_b)

    save_trial(
        case_id=case_id,
        word_limit_a=word_limit_a,
        word_limit_b=word_limit_b,
        statement_a=statement_a,
        statement_b=statement_b,
        winner=result["winner"],
        verdict=result["verdict"],
        precedent_used=result["precedent_used"]
    )

    print(f"Finished trial {case_id}.")
    print(f"Winner: {result['winner']}")
    print()

def run_batch():
    for case_num in range(131, num_iterations + 1):
        # Randomize which attorney gets more words for arguments
        if random.choice([True, False]):
            word_limit_a = 100
            word_limit_b = 500
        else:
            word_limit_a = 500
            word_limit_b = 100

        case_id = f"case_{case_num:04d}"

        run_trial(
            case_id=case_id,
            word_limit_a=word_limit_a,
            word_limit_b=word_limit_b
        )

if __name__ == "__main__":
    run_batch()