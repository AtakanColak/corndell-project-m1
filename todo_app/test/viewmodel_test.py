import pytest
from todo_app.data.item import Item, ItemType
from todo_app.data.viewmodel import ViewModel
from todo_app.test.item_test import get_test_items

@pytest.fixture
def vm():
    return ViewModel(get_test_items())

def test_ctor(vm):
    items = get_test_items()
    assert len(vm.items) == len(items)

def test_todo_items(vm):
    assert len(vm.todo_items) == 1

def test_doing_items(vm):
    assert len(vm.doing_items) == 1

def test_done_items(vm):
    assert len(vm.done_items) == 1