from selenium import webdriver

from src.fixture.james import JamesHelper
from src.fixture.navigation import NavigationHelper
from src.fixture.project import ProjectHelper
from src.fixture.session import SessionHelper


class Application:

    def __init__(self, browser, config):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        else:
            raise ValueError("Unrecognized browser")

        self.wd.implicitly_wait(3)
        self.wd.maximize_window()
        self.config = config
        self.base_url = config["web"]["baseUrl"]
        self.session = SessionHelper(self)
        self.navigation = NavigationHelper(self)
        self.project = ProjectHelper(self)
        self.james = JamesHelper(self)

    def open_home(self):
        wd = self.wd
        wd.get(self.base_url)

    def destroy(self):
        self.wd.quit()
