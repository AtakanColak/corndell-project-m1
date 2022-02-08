import os
from dotenv import find_dotenv, load_dotenv
import pytest

from todo_app.app import create_app

class StubResponse:
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data
        
    def json(self):
        return self.fake_response_data

def get_lists_stub(url, params):
    test_board_id = os.environ.get('TRELLO_BOARD_ID')
    fake_response_data = None
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
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    test_app = create_app()
    with test_app.test_client() as client:
        yield client

def test_index_page(client):
    response = client.get('/')