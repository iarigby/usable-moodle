import os
import pickle
from pathlib import Path
from time import sleep

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CredentialsNotFound(Exception):
    pass


def log_in(driver, cookies_file: Path):
    driver.delete_all_cookies()
    try:
        cookies = pickle.load(open(cookies_file, "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
    except FileNotFoundError:
        pass

    driver.get("http://moodle.univie.ac.at/")
    sleep(1)
    try:
        log_in_section = driver.find_element(By.ID, "loginpage_grid")
    except NoSuchElementException:
        return

    log_in_button = log_in_section.find_element(By.TAG_NAME, "button")
    log_in_button.click()
    sleep(1)

    moodle_username, moodle_password = os.environ.get('MOODLE_USERNAME'), os.environ.get('MOODLE_PASSWORD')
    if not (moodle_username or moodle_password):
        raise CredentialsNotFound()
    driver.find_element(By.ID, "userid").send_keys(moodle_username)
    driver.find_element(By.ID, "password").send_keys(moodle_password)
    driver.find_element(By.ID, "_shib_idp_donotcache").click()
    driver.find_element(By.NAME, "_eventId_proceed").click()

    pickle.dump(driver.get_cookies(), open(cookies_file, "wb"))


def navigate_to_course(driver, course_name):
    driver.get("https://moodle.univie.ac.at/my/courses.php")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "coursename")))
    course_links = driver.find_elements(By.CLASS_NAME, "coursename")
    course_link_elem = next(e for e in course_links if course_name in e.accessible_name)
    course_link = course_link_elem.get_attribute('href')
    driver.get(course_link)


def navigate_to_activity_by_name(driver, activity_name: str):
    activity_items = driver.find_elements(By.CLASS_NAME, "activity-item")
    activity_item = next(e for e in activity_items if e.get_attribute('data-activityname') == activity_name)
    activity_url = activity_item.find_element(By.TAG_NAME, 'a').get_attribute('href')
    driver.get(activity_url)
