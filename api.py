from fastapi import FastAPI, BackgroundTasks
from uuid import uuid4
from scenario_generator import generate_scenario, generate_side_a, generate_side_b
from attorney_a import generate_attorney_a
from attorney_b import generate_attorney_b
from judge import judge_case
from result_logger import save_trial

app = FastAPI()

# In-memory store of job statuses. Lost on restart
jobs = {}

def run_trial_job(job_id: str, word_limit_a: int, word_limit_b: int):
    jobs[job_id]["status"] = "running"

    try:
        scenario = generate_scenario()
        side_a = generate_side_a(scenario)
        side_b = generate_side_b(scenario)

        statement_a = generate_attorney_a(side_a, word_limit_a)
        statement_b = generate_attorney_b(side_b, word_limit_b)

        result = judge_case(statement_a, statement_b)

        save_trial(
            case_id=job_id,
            word_limit_a=word_limit_a,
            word_limit_b=word_limit_b,
            statement_a=statement_a,
            statement_b=statement_b,
            winner=result["winner"],
            verdict=result["verdict"],
            precedent_used=result["precedent_used"]
        )

        jobs[job_id]["status"] = "done"
        jobs[job_id]["result"] = {
            "winner": result["winner"],
            "verdict": result["verdict"],
            "precedent_used": result["precedent_used"],
            "word_limit_a": word_limit_a,
            "word_limit_b": word_limit_b,
            "actual_words_a": len(statement_a.split()),
            "actual_words_b": len(statement_b.split())
        }

    except Exception as e:
            jobs[job_id]["status"] = "failed"
            jobs[job_id]["error"] = str(e)



@app.post("/trials")
def start_trial(background_tasks: BackgroundTasks, word_limit_a: int = 100, word_limit_b: int = 500):
    job_id = str(uuid4())
    jobs[job_id] = {"status": "queued", "result": None}

    background_tasks.add_task( run_trial_job, job_id, word_limit_a, word_limit_b)

    return {"job_id": job_id}

@app.get("/trials/{job_id}")
def get_trial(job_id: str):
    if job_id not in jobs:
        return {"status": "not_found"}

    return jobs[job_id]