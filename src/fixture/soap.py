from suds.client import Client
from suds import WebFault

from src.model.project import Project


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client("http://127.0.0.1/mantisbt-2.25.0/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_projects_list(self, username, password):
        client = Client("http://127.0.0.1/mantisbt-2.25.0/api/soap/mantisconnect.php?wsdl")
        try:
            mc_projects = client.service.mc_projects_get_user_accessible(username, password)
            return list(map(lambda p: Project(id = p.id, name = p.name), mc_projects))
        except WebFault as wb:
            wb.__str__()

