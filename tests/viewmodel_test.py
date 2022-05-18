import pytest
from todo_app.data.item import Item, ItemType
from todo_app.data.trello_service import TrelloService
from todo_app.data.viewmodel import ViewModel
from tests.item_test import get_test_items
from dotenv import find_dotenv, load_dotenv

@pytest.fixture
def trello_service():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    return TrelloService()

@pytest.fixture
def vm(trello_service: TrelloService):
    return ViewModel(get_test_items(trello_service))

def test_ctor(vm, trello_service):
    items = get_test_items(trello_service)
    assert len(vm.items) == len(items)

def test_todo_items(vm):
    assert len(vm.todo_items) == 1

def test_doing_items(vm):
    assert len(vm.doing_items) == 1

def test_done_items(vm):
    assert len(vm.done_items) == 1