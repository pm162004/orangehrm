import os
import logging
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from log_config import setup_logger

# Initialize logger
logger = setup_logger()




# ---------- Test Ordering ----------
def pytest_collection_modify_items(session, config, items):
    # Define the desired file order
    file_order = [
        "test_01_login.py",
        "test_02_add_new_candidate.py",
        "test_03_search_and_validate_candidate.py",
        "test_04_logout.py",
    ]

    # Sort items by the index of their file in file_order
    def file_index(item):
        for idx, filename in enumerate(file_order):
            if filename in item.nodeid:
                return idx
        return len(file_order)  # Files not listed come last

    # Now sort items in-place by file order
    items.sort(key=file_index)
    order = [
        "test_01_login.py::TestOrangeHrmLogin::test_blank_login_field",
        "test_01_login.py::TestOrangeHrmLogin::test_invalid_username",
        "test_01_login.py::TestOrangeHrmLogin::test_invalid_password",
        "test_01_login.py::TestOrangeHrmLogin::test_invalid_username_password",
        "test_01_login.py::TestOrangeHrmLogin::test_valid_login_flow",
        "test_add_candidate.py::TestOrangeHrmCandidate::test_click_add_candidate_btn",
        "test_add_candidate.py::TestOrangeHrmCandidate::test_blank_validations",
        "test_add_candidate.py::TestOrangeHrmCandidate::test_add_new_candidate",
        "test_search_candidate.py::TestOrangeHrmCandidate::test_click_add_candidate_btn",
        "test_search_candidate.py::TestOrangeHrmCandidate::test_search_candidate",
        "test_04_logout.py::TestOrangeHrmLogout::test_logout",
    ]

    item_dict = {item.nodeid: item for item in items}
    ordered_items = [item_dict[name] for name in order if name in item_dict]
    rest = [item for item in items if item not in ordered_items]
    items[:] = ordered_items + rest

    logger.info(f"Test order applied. Ordered: {len(ordered_items)}; Remaining: {len(rest)}")


# ---------- HTML Reporting ----------
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    report_dir = os.path.join(os.path.dirname(__file__), "reports")
    os.makedirs(report_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = os.path.join(report_dir, f"report_{timestamp}.html")
    config.option.htmlpath = report_path
    config.option.self_contained_html = True

    logger.info(f"HTML report will be saved to: {report_path}")

