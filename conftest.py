import pytest
import json
import ftputil
import os.path
from fixture.application import Application


fixture=None # глобальная переменная
target=None  # глобальная переменная

def load_config(file):
    global target  # глобальная переменная

    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),file)
        with open(config_file) as f:
            target=json.load(f)

    return target

@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))

@pytest.fixture
def app(request,config): # ,version='1.0'
    global fixture  # глобальная переменная
    browser = request.config.getoption("--browser")
    #web_config=load_config(request.config.getoption("--target"))['web']
    #web = config['web']
   #webadmin = config['webadmin']

    if fixture is None or not fixture.is_valid():

       #fixture = Application(browser=browser,base_url=web_config['baseUrl'])
       fixture = Application(browser=browser, config=config)

    #fixture.session.ensure_login(username=web_config['username'], password=web_config['password'])
    #fixture.session.ensure_login(username=webadmin['username'], password=webadmin['password'])

    return fixture

@pytest.fixture(scope="session",autouse=True)
def configure_server(request,config):
    install_server_configuration(config['ftp']['host'],config['ftp']['username'],config['ftp']['password'])
    def fin():
        restore_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    request.addfinalizer(fin)

def install_server_configuration(host,username,password):
    with ftputil.FTPHost(host,username,password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            remote.remove("config_inc.php.bak")
        if remote.path.isfile("config_inc.php"):
            remote.rename("config_inc.php","config_inc.php.bak")
        remote.upload(os.path.join(os.path.dirname(__file__),"resources/config_inc.php"),"config_inc.php")

def restore_server_configuration(host,username,password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            if remote.path.isfile("config_inc.php"):
                remote.remove("config_inc.php")
            remote.rename("config_inc.php.bak", "config_inc.php")

@pytest.fixture(scope="session",autouse=True)
def stop(request):
   def fin():
      fixture.session.ensure_logout()
      fixture.destroy()
   request.addfinalizer(fin)


def pytest_addoption(parser):
    parser.addoption("--browser",action="store",default="firefox")
    parser.addoption("--target", action="store", default="target.json")


