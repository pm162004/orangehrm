import pytest
import json

def load_candidates_from_json(file_path):
    with open(file_path) as f:
        return json.load(f)

candidates = load_candidates_from_json("./candidate.json")

@pytest.mark.parametrize("candidate", candidates)
def test_schedule_interview(candidate):
    name = candidate["name"]
    time = candidate["interview_time"]
    print(f"Scheduling interview for {name} at {time}")
    assert name != ""
    assert time != ""
