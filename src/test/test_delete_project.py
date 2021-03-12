import random

from src.model.project import Project


def test_delete_project(app, admin, orm_db, check_ui):
    app.session.login(admin["username"], admin["password"])
    app.navigation.open_projects_board()
    old_projects = orm_db.get_projects_list()
    project = random.choice(old_projects)
    app.project.delete_project(project)
    new_projects = orm_db.get_projects_list()
    old_projects.remove(project)
    if not check_ui:
        app.session.logout()

    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)

    if check_ui:
        def clean(project):
            return Project(id=project.id, name=project.name.replace(" ", ""))
        db_projects = map(clean, orm_db.get_projects_list())
        app.navigation.open_projects_board()
        ui_projects = map(clean, app.project.get_projects_list())

        assert str(sorted(db_projects, key=Project.id_or_max)) == str(sorted(ui_projects, key=Project.id_or_max))
        app.session.logout()