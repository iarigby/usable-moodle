from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver
from selenium.webdriver import Firefox


class WebDriver(Firefox):
    def __init__(self):
        super().__init__()

    def navigate_to_link(self, header_name: str):
        print()
        # self.find_element(By.)
