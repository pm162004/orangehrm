
import pytest
import logging
from log_config import setup_logger

logger = setup_logger()
test_data = [
    ("Alice Johnson", "2025-05-21 10:00"),
    ("Bob Smith", "2025-05-21 11:00"),
    ("Carol Davis", "2025-05-21 14:00"),
]

@pytest.mark.parametrize("candidate_name, interview_time", test_data)
def test_schedule_interview(candidate_name, interview_time):
    logger.info(f"Scheduling interview for {candidate_name} at {interview_time}")
    print(f"Scheduling interview for {candidate_name} at {interview_time}")
    assert candidate_name != ""
    assert interview_time != ""
