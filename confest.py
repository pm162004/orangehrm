import os
from datetime import datetime
import pytest

def pytest_collection_modify_items(session, config, items):
    order = [
        "test_blank_login_field",
        "test_invalid_username_and_password",
        "test_invalid_username",
        "test_invalid_password",
        "test_valid_login_flow",
        "test_logout"
    ]
    item_dict = {item.name: item for item in items}
    ordered_items = [item_dict[name] for name in order if name in item_dict]
    # Add remaining tests at the end if any
    rest = [item for item in items if item not in ordered_items]
    items[:] = ordered_items + rest

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    # Define the path for the report folder
    report_dir = "/home/web-h-028/PycharmProjects/orange_hrm_automation/reports"

    # Create the reports directory if it doesn't exist
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    # Create a timestamp string safe for filenames (no spaces or colons)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Set the path for the HTML report
    config.option.htmlpath = os.path.join(report_dir, f"report_{timestamp}.html")

    # Optional: create self-contained HTML report
    config.option.self_contained_html = True
