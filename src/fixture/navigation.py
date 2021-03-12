class NavigationHelper():
    def __init__(self, app):
        self.app = app

    def open_projects_board(self):
        wd = self.app.wd
        wd.find_element_by_css_selector("div#sidebar a[href='/mantisbt-2.25.0/manage_overview_page.php']").click()
        wd.find_element_by_css_selector("div.page-content a[href='/mantisbt-2.25.0/manage_proj_page.php']").click()
