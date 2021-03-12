from src.model.project import Project


def test_projects_ui_with_db(app, admin, orm_db, check_ui):
    if check_ui:
        def clean(project):
            return Project(id=project.id, name=project.name.replace(" ", ""))

        db_projects = map(clean, orm_db.get_projects_list())

        app.session.login(admin["username"], admin["password"])
        app.navigation.open_projects_board()
        ui_projects = map(clean, app.project.get_projects_list())

        assert str(sorted(db_projects, key=Project.id_or_max)) == str(sorted(ui_projects, key=Project.id_or_max))
    else:
        print()
        print("Test: test_projects_ui_with_db DISABLED, --check_ui option not added")
