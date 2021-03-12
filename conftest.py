import json
import os

import pytest

from src.fixture.application import Application
from src.fixture.orm import ORMFixture

fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as f:
            target = json.load(f)
    return target


@pytest.fixture
def app(request):
    global fixture
    browser = request.config.getoption("--browser")
    web_config = load_config(request.config.getoption("--target"))["web"]
    if fixture is None:
        fixture = Application(browser=browser, base_url=web_config["baseUrl"])
    return fixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.destroy()

    request.addfinalizer(fin)
    return fixture


@pytest.fixture(scope="session")
def admin(request):
    admin_config = load_config(request.config.getoption("--target"))["webadmin"]
    admin_login = {
        "username": admin_config["login"],
        "password": admin_config["password"]
    }
    return admin_login


@pytest.fixture(scope="session")
def user(request):
    user_config = load_config(request.config.getoption("--target"))["user"]
    user_login = {
        "username": user_config["login"],
        "password": user_config["password"]
    }
    return user_login


@pytest.fixture()
def check_ui(request):
    return request.config.getoption("--check_ui")

@pytest.fixture(scope="session")
def orm_db(request):
    orm_config = load_config(request.config.getoption("--target"))["db"]
    orm_fixture = ORMFixture(host=orm_config["host"], name=orm_config["name"],
                             user=orm_config["user"], password=orm_config["password"])
    return orm_fixture



def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--target", action="store", default="target.json")
    parser.addoption("--check_ui", action="store_true")