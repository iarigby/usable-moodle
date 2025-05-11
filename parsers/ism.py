from webdriver.webdriver import WebDriver
from selenium.webdriver.common.by import By


course_name = 'Information Security Management'


def get_schedule(driver: WebDriver, moodle):
    moodle.navigate_to_activity_by_name(driver, 'Schedule')
    main_section = driver.find_element(By.ID, "region-main")
    schedule_paragraph = main_section.find_element(By.TAG_NAME, "p")
    schedule_entries = schedule_paragraph.text.split("\n")
    for entry in schedule_entries:
        [date_str, description] = entry.split(" ", 1)
        day, month, year = date_str.split(".")


steps = [get_schedule]

