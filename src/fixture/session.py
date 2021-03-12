class SessionHelper:
    def __init__(self, app):
        self.app = app

    def login(self, username, password):
        wd = self.app.wd
        self.app.open_home()
        wd.find_element_by_css_selector("input[name=username]").send_keys(username)
        wd.find_element_by_css_selector("input[type=submit]").click()
        wd.find_element_by_css_selector("input[name=password]").send_keys(password)
        wd.find_element_by_css_selector("input[type=submit]").click()

    def logout(self):
        wd = self.app.wd
        logout_container = wd.find_element_by_css_selector("div#navbar a.dropdown-toggle span.user-info")
        logout_container.click()
        logout_container.find_element_by_xpath("//a[contains(@href, '/mantisbt-2.25.0/logout_page.php')]").click()

    def is_logged_in_as(self, username):
        wd = self.app.wd
        return self.get_logged_user() == username

    def get_logged_user(self):
        wd = self.app.wd
        return wd.find_element_by_css_selector("span.user-info")
