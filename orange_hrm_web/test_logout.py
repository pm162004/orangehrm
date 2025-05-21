import logging
import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from orange_hrm_setup.config import config
from constant import validation_assert, error,input_field
from log_config import setup_logger




logger = setup_logger()



# Setup driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # Optional for headless mode
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(config.WEB_URL)

# driver.implicitly_wait(10)
wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))
wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))

user_name = config.USER_NAME
password = config.PASSWORD

# Elements
def username_input():
    return wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Username']")))

def password_input():
    return wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Password']")))

def login_btn():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Login']")))


def check_blank_username():
    username_variable = wait.until(EC.presence_of_element_located((By.XPATH, "(//span[@class='oxd-text oxd-text--span oxd-input-field-error-message oxd-input-group__message'][normalize-space()='Required'])[1]")))
    return username_variable


def check_blank_password():
    password_variable = wait.until(EC.presence_of_element_located((By.XPATH, "(//span[@class='oxd-text oxd-text--span oxd-input-field-error-message oxd-input-group__message'][normalize-space()='Required'])[2]")))
    return password_variable

def check_invalid_creds():
    creds_variable = wait.until(EC.presence_of_element_located((By.XPATH, "//p[@class='oxd-text oxd-text--p oxd-alert-content-text']")))
    return creds_variable

def check_for_dashboard():
    return wait.until(EC.presence_of_element_located((By.XPATH, "//h6[normalize-space()='Dashboard']")))

def logout_menu():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='oxd-userdropdown-tab']")))

def logout_link():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Logout']")))

def refresh_page():
    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))
    wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
    time.sleep(1)
    return driver.refresh()

def quit_browser():
    time.sleep(1)
    return driver.quit()

# Test Cases
@pytest.mark.order(1)
class TestOrangeHrmLoOut:

    @pytest.mark.order(1)
    def test_valid_login_flow(self):
        refresh_page()
        username_input().send_keys(user_name)
        password_input().send_keys(password)
        login_btn().click()
        assert check_for_dashboard().text == validation_assert.dashboard
        logger.info("User logged in successfully")

    @pytest.mark.order(2)
    def test_logout(self):
        refresh_page()
        logout_menu().click()
        time.sleep(1)
        logout_link().click()
        assert login_btn().is_displayed()
        logger.info("Log out is successfully")
        quit_browser()