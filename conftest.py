import json
import os

import pytest

from src.fixture.application import Application

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
    request.addfinalizer(fixture.destroy)
    return fixture

# @pytest.fixture(scope="session", autouse=True)
# def stop(request):
#     request.addfinalizer(fixture.destroy)
#     return fixture

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--target", action="store", default="target.json")