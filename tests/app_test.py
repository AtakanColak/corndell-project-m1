import os
from tokenize import Name
import pytest
import requests

from todo_app.app import create_app
from tests.viewmodel_test import trello_service

class StubResponse:
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data
        self.ok = True

    def json(self):
        return self.fake_response_data

def get_lists_stub(url, params):
    test_board_id = os.environ.get('TRELLO_BOARD_ID')
    fake_response_data = []
    if url == f'https://api.trello.com/1/boards/{test_board_id}/lists':
        fake_response_data = [{
            'id': '123abc',
            'name': 'To Do',
            'cards': [{
                'id' : 1,
                'name': 'Test1',
                'idList' : 'SumListID'
            }]
        }]
    return StubResponse(fake_response_data)

@pytest.fixture
def client(trello_service):
    test_app = create_app(trello_service)
    with test_app.test_client() as client:
        yield client

def test_index_page(monkeypatch, client):
    monkeypatch.setattr(requests, 'get', get_lists_stub)
    response = client.get('/')
    assert response.status_code == 200