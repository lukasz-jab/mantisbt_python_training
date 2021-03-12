from pony.orm import *
from src.fixture.project import Project


class ORMFixture:

    db = Database()

    class ORMProject(db.Entity):
        _table_ = 'mantis_project_table'
        id = PrimaryKey(int, column='id')
        name = Required(str, column='name')
        status = Optional(str, column='status')
        inheritanced = Optional(str, column='inherit_global')
        visibility = Optional(str, column='view_state')
        description = Optional(str, column='description')

    def __init__(self, host, name, user, password):
        self.db.bind('mysql', host=host, database=name, user=user, password=password) #conv=decoders
        self.db.generate_mapping()
        sql_debug(True)

    def convert_projects_to_model(self, projects):
        def convert(project):
            return Project(id=project.id, name=project.name, status=project.status, inheritanced=project.inheritanced,
                           visibility=project.visibility, description=project.description)
        return list(map(convert, projects))

    @db_session
    def get_projects_list(self):
        return self.convert_projects_to_model(list(select(p for p in ORMFixture.ORMProject)))
