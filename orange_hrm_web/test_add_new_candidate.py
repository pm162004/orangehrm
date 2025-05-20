import logging
import os
import time
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

# Screenshot directory
screenshot_dir = "../screenshorts"
os.makedirs(screenshot_dir, exist_ok=True)

# Elements for login
def username_input():
    return wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Username']")))

def password_input():
    return wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Password']")))

def login_btn():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Login']")))

def check_for_dashboard():
    return wait.until(EC.presence_of_element_located((By.XPATH, "//h6[normalize-space()='Dashboard']")))

def logout_menu():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='oxd-userdropdown-tab']")))

def logout_link():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Logout']")))

def refresh_page():
    driver.refresh()
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(1)

def quit_browser():
    time.sleep(1)
    driver.quit()

def click_menu_recruitment():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Recruitment']")))

def click_candidates_tab():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'viewCandidates')]")))

def add_candidate_btn():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Add']")))

def candidate_firstname_blank_error():
    return wait.until(EC.presence_of_element_located((By.XPATH, "(//span[@class='oxd-text oxd-text--span oxd-input-field-error-message oxd-input-group__message'][normalize-space()='Required'])[1]")))

def candidate_lastname_blank_error():
    return wait.until(EC.presence_of_element_located((By.XPATH, "(//span[@class='oxd-text oxd-text--span oxd-input-field-error-message oxd-input-group__message'][normalize-space()='Required'])[2]")))

def candidate_email_blank_error():
    return wait.until(EC.presence_of_element_located((By.XPATH, "(//span[@class='oxd-text oxd-text--span oxd-input-field-error-message oxd-input-group__message'][normalize-space()='Required'])[3]")))

def candidate_email_invalid_error():
    return wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='oxd-text oxd-text--span oxd-input-field-error-message oxd-input-group__message']")))
def candidate_first_name_input():
    return wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='firstName']")))

def candidate_middle_name_input():
    return wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='middleName']")))
def candidate_last_name_input():
    return wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='lastName']")))

def candidate_email_input():
    return wait.until(EC.presence_of_element_located((By.XPATH, "(//input[@placeholder='Type here'])[1]")))

def candidate_phone_input():
    return wait.until(EC.presence_of_element_located((By.XPATH, "(//input[@placeholder='Type here'])[2]")))
def vacancy_dropdown():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='oxd-select-text--after']")))

def vacancy_option(vacancy_text):
    return wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[@role='listbox']//span[text()='{vacancy_text}']")))

def resume_upload_input():
    return wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))

def save_btn():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']")))

def click_candidates_table_rows():
    return wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='oxd-table-body']//div[@role='row']")))

def candidate_in_table(name):
    return wait.until(EC.presence_of_element_located(
        (By.XPATH, f"//div[@class='oxd-table-body']//div[contains(@role, 'row')]//div[contains(text(), '{name}')]")
    ))


# Test class
class TestOrangeHrmCandidate:

    def test_valid_login_flow(self):
        refresh_page()
        username_input().send_keys(user_name)
        password_input().send_keys(password)
        login_btn().click()
        assert check_for_dashboard().text == validation_assert.dashboard
        logger.info("User logged in successfully")

    def test_click_add_candidate_btn(self):
        click_menu_recruitment().click()
        logger.info("Navigated to Recruitment > Candidates page")
        add_candidate_btn().click()
        logger.info("Clicked Add Candidate button")

        driver.refresh()

    def test_blank_validations(self):
        save_btn().click()

        assert candidate_firstname_blank_error().text == validation_assert.ENTER_FIRST_NAME
        assert candidate_lastname_blank_error().text == validation_assert.ENTER_LAST_NAME
        assert candidate_email_blank_error().text == validation_assert.ENTER_EMAIL
        logger.info("Blank validations are displayed")


    def test_add_new_candidate(self):

        candidate_first_name_input().send_keys(input_field.FIRST_NAME)
        firstname = candidate_first_name_input().get_attribute("value")
        candidate_middle_name_input().send_keys(input_field.MIDDLE_NAME)
        candidate_last_name_input().send_keys(input_field.LAST_NAME)

        vacancy_dropdown().click()
        vacancy_option(input_field.VACANCY_OPTION).click()
        candidate_email_input().send_keys(input_field.INVALID_EMAIL)
        assert candidate_email_invalid_error().text == error.INVALID_EMAIL_ERROR_MESSAGE
        candidate_email_input().send_keys(input_field.EMAIL)
        logger.info("Entered candidate name and email")
        logger.info("Selected vacancy: Software Engineer")
        candidate_phone_input().send_keys(input_field.PHONE_NUMBER)
        resume_path = "/home/web-h-028/PycharmProjects/orange_hrm_automation/resume/candidate_resume.pdf"
        resume_upload_input().send_keys(resume_path)
        logger.info("Uploaded resume")

        save_btn().click()
        logger.info("Clicked Save button")


        assert candidate_in_table(firstname).is_displayed()
        logger.info("Candidate 'John' successfully added and visible in the candidates table")

        # Take screenshot of the candidates list with new entry
        driver.save_screenshot(os.path.join(screenshot_dir, "candidate_added.png"))

        # Logout and quit
        logout_menu().click()
        time.sleep(1)
        logout_link().click()
        logger.info("Logged out successfully")
        quit_browser()
