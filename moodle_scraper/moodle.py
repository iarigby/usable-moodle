import os
import pickle
from pathlib import Path

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


class CredentialsNotFound(Exception):
    pass


def log_in(driver, cookies_file: Path):
    driver.delete_all_cookies()
    cookies = pickle.load(open(cookies_file, "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get("http://moodle.univie.ac.at/")

    try:
        log_in_section = driver.find_element(By.ID, "loginpage_grid")
    except NoSuchElementException:
        return

    log_in_button = log_in_section.find_element(By.TAG_NAME, "button")
    log_in_button.click()

    moodle_username, moodle_password = os.environ.get('MOODLE_USERNAME'), os.environ.get('MOODLE_PASSWORD')
    if not (moodle_username or moodle_password):
        raise CredentialsNotFound()
    driver.find_element(By.ID, "userid").send_keys(moodle_username)
    driver.find_element(By.ID, "password").send_keys(moodle_password)
    driver.find_element(By.ID, "_shib_idp_donotcache").click()
    driver.find_element(By.NAME, "_eventId_proceed").click()

    pickle.dump(driver.get_cookies(), open(cookies_file, "wb"))

