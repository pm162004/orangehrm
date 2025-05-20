import pytest

# Sample data: (candidate_name, interview_time)
test_data = [
    ("Alice Johnson", "2025-05-21 10:00"),
    ("Bob Smith", "2025-05-21 11:00"),
    ("Carol Davis", "2025-05-21 14:00"),
]

@pytest.mark.parametrize("candidate_name, interview_time", test_data)
def test_schedule_interview(candidate_name, interview_time):
    print(f"Scheduling interview for {candidate_name} at {interview_time}")
    # Your Selenium code here using candidate_name & interview_time
    # e.g. fill forms, click buttons, assert success messages
    assert candidate_name != ""
    assert interview_time != ""
