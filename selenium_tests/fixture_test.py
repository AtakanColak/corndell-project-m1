from dotenv import find_dotenv, load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from threading import Thread
import pytest

from todo_app.data.trello_service import TrelloService
from todo_app.app import create_app

@pytest.fixture(scope='module')
def trello_service_fix():
    file_path = find_dotenv('../.env.integration')
    load_dotenv(file_path, override=True)
    return TrelloService()

@pytest.fixture(scope='module')
def app_with_temp_board(trello_service_fix):
    board_id = trello_service_fix.create_board('integration_test_board').json()['id']
    trello_service_fix.switch_board(board_id)
    application = create_app(trello_service_fix)
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application
    thread.join(1)
    trello_service_fix.delete_board(board_id).json()

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.headless = True
    with webdriver.Firefox(options = options) as driver:
        yield driver