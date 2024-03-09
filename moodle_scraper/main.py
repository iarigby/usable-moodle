from pathlib import Path

from selenium import webdriver
from dotenv import load_dotenv
import moodle

load_dotenv()

cookies_file = Path(__file__).parent.parent / "cookies.pkl"

driver = webdriver.Firefox()

driver.get("http://moodle.univie.ac.at/")
try:
    moodle.log_in(driver, cookies_file)
except moodle.CredentialsNotFound:
    print("Environment variable for moodle credentials not defined")
    driver.close()
    exit(1)

driver.close()

