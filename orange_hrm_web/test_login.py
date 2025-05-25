import time
import os
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from orange_hrm_setup.config import config
from constant import validation_assert, error, input_field
from log_config import setup_logger

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')

chrome_options.add_argument('--disable-dev-shm-usage')
prefs = {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
    "profile.password_manager_leak_detection": False

}


chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=chrome_options)

chrome_options.add_argument("--headless") # Optional for headless mode

driver.maximize_window()
driver.get(config.WEB_URL)
wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))
wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))

user_name = config.USER_NAME
password = config.PASSWORD

logger = setup_logger()

def save_screenshot(filename, use_timestamp=True, folder="screenshorts"):
    os.makedirs(folder, exist_ok=True)

    if use_timestamp:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = "{}_{}.png".format(filename, timestamp)
    else:
        filename = "{}.png".format(filename)

    full_path = folder, filename
    driver.save_screenshot(f"{folder}/{filename}")  # using global driver
    return full_path

def username_input():
    return wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Username']")))


def password_input():
    return wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Password']")))


def login_btn():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Login']")))


def check_blank_username():
    username_variable = wait.until(EC.presence_of_element_located(
        (By.XPATH, "(//span[contains(@class, 'oxd-input-field-error-message') and text()='Required'])[1]")))
    return username_variable


def check_blank_password():
    password_variable = wait.until(EC.presence_of_element_located(
        (By.XPATH, "(//span[contains(@class, 'oxd-input-field-error-message') and text()='Required'])[2]")))
    return password_variable


def check_invalid_creds():
    creds_variable = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class, 'oxd-alert')]//p[text()='Invalid credentials']")
        )
    )
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


class TestOrangeHrmLogin:

    def test_blank_login_field(self):
        login_btn().click()
        assert check_blank_username().text == validation_assert.ENTER_USERNAME
        assert check_blank_password().text == validation_assert.ENTER_PASSWORD
        save_screenshot("blank_creds")
        logger.info("Enter blank username and password check the error message is displayed.")

    def test_invalid_password(self):
        refresh_page()
        time.sleep(1)
        username_input().send_keys(config.USER_NAME)
        password_input().send_keys(input_field.INVALID_PASSWORD)
        login_btn().click()
        time.sleep(1)
        assert check_invalid_creds().text == error.INVALID_CREDS_ERROR_MESSAGE
        save_screenshot("invalid_password")
        logger.info("Enter invalid password and check the error message is displayed.")

    def test_invalid_username(self):
        refresh_page()
        username_input().send_keys(input_field.INVALID_USERNAME)
        password_input().send_keys(config.PASSWORD)
        login_btn().click()
        assert check_invalid_creds().text == error.INVALID_CREDS_ERROR_MESSAGE
        save_screenshot("invalid_username")
        logger.info("Enter invalid username check the error message is displayed.")
        refresh_page()

    def test_invalid_username_password(self):
        refresh_page()
        username_input().send_keys(input_field.INVALID_USERNAME)
        password_input().send_keys(input_field.INVALID_PASSWORD)
        login_btn().click()
        assert check_invalid_creds().text == error.INVALID_CREDS_ERROR_MESSAGE
        save_screenshot("invalid_username_password")
        logger.info("Enter invalid username and password and check the error message is displayed.")
        refresh_page()

    def test_valid_login_flow(self):
        refresh_page()
        username_input().send_keys(config.USER_NAME)
        password_input().send_keys(config.PASSWORD)
        login_btn().click()
        assert check_for_dashboard().text == validation_assert.DASHBOARD
        logger.info("User logged in successfully")

    def test_logout(self):
        refresh_page()
        logout_menu().click()
        time.sleep(1)
        logout_link().click()
        assert login_btn().is_displayed()
        logger.info("Log out is successfully")
        quit_browser()
