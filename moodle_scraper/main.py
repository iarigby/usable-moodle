from pathlib import Path

from selenium import webdriver
from dotenv import load_dotenv
import moodle
from parsers import ase, ism
from webdriver.webdriver import WebDriver

load_dotenv()

cookies_file = Path(__file__).parent.parent / "cookies.pkl"

driver = WebDriver()

driver.get("http://moodle.univie.ac.at/")

parsers = [ase, ism]

try:
    moodle.log_in(driver, cookies_file)
    for parser in parsers:
        for step_fn in parser.steps:
            moodle.navigate_to_course(driver, parser.course_name)
            step_fn(driver, moodle)
except moodle.CredentialsNotFound:
    print("Environment variable for moodle credentials not defined")
    driver.close()
    exit(1)

driver.close()

