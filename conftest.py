import json
import os

import pytest
import ftputil
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
def app(request, config):
    global fixture
    browser = request.config.getoption("--browser")
    if fixture is None:
        fixture = Application(browser=browser, config=config)
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


@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))


@pytest.fixture(scope="session", autouse=True)
def server_ftp(request, config):
    install_server_configuration(config["ftp"]["host"], config["ftp"]["username"], config["ftp"]["password"])
    def fin():
        restore_server_configuration(config["ftp"]["host"], config["ftp"]["username"], config["ftp"]["password"])
    request.addfinalizer(fin)


def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_defaults_inc.php.bak"):
            remote.remove("config_defaults_inc.php.bak")
        if remote.path.isfile("config_defaults_inc.php"):
            remote.rename("config_defaults_inc.php", "config_defaults_inc.php.bak")
        remote.upload(os.path.join(os.path.dirname(__file__), "resources/config_defaults_inc.php"), "config_defaults_inc.php")

def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_defaults_inc.php.bak"):
            if remote.path.isfile("config_defaults_inc.php"):
                remote.remove("config_defaults_inc.php")
            remote.rename("config_defaults_inc.php.bak", "config_defaults_inc.php")



def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--target", action="store", default="target.json")
    parser.addoption("--check_ui", action="store_true")
