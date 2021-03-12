from src.model.project import Project


class ProjectHelper():
    def __init__(self, app):
        self.app = app

    def create_project(self, project):
        wd = self.app.wd
        wd.find_element_by_css_selector("form[action='manage_proj_create_page.php']").click()
        wd.find_element_by_css_selector("form#manage-project-create-form input#project-name").send_keys(project.name)
        wd.find_element_by_css_selector("form#manage-project-create-form textarea#project-description").send_keys(
            project.description)
        wd.find_element_by_css_selector("form#manage-project-create-form input[type=submit]").click()

    def get_projects_list(self):
        wd = self.app.wd
        self.app.navigation.open_projects_board()
        projects = []
        web_el_projects = wd.find_elements_by_css_selector("div.col-md-12.col-xs-12 div.widget-body tbody tr td a")
        for project in web_el_projects:
            projects.append(Project(name=project.text, id=project.get_attribute("href")[70:]))
        return projects

    def delete_project(self, project):
        wd = self.app.wd
        wd.find_element_by_css_selector("a[href='manage_proj_edit_page.php?project_id=%s']" % project.id).click()
        wd.find_element_by_css_selector("form#project-delete-form input[type=submit]").click()
        wd.find_element_by_css_selector("form.center input[type=submit]").click()
