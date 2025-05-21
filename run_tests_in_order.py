import subprocess

file_order = [
    "test_01_login.py",
    "test_02_add_new_candidate.py",
    "test_03_search_and_validate_candidate.py",
    "test_04_logout.py",
]

for file in file_order:
    result = subprocess.run(["pytest", file])
    if result.returncode != 0:
        print(f"Test failed: {file}")
        break
