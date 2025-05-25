import subprocess

file_order = [
    "orange_hrm_web/test_login.py",
    "orange_hrm_web/test_add_new_candidate.py",
    "orange_hrm_web/test_search_and_validate_candidate.py",
    "orange_hrm_web/test_logout.py",
]

for file in file_order:
    result = subprocess.run(["pytest", file])
    if result.returncode != 0:
        print(f"Test failed: {file}")
        break
