from http import HTTPStatus
import pprint
import requests
import os

from todo_app.data.item import Item, ItemType

class TrelloService:
    def __init__(self) -> None:
        self.url = "https://api.trello.com"
        self.id = os.getenv('TRELLO_BOARD_ID')
        self.key = os.getenv('TRELLO_KEY')
        self.token = os.getenv('TRELLO_TOKEN')
        self.load_lists()
        pprint.pprint(vars(self))

    def get_items_of_list(self, list_id, list_status, append_target) -> None:
        params = { 'key' : self.key, 'token' : self.token}
        resp = requests.get(f"{self.url}/1/lists/{list_id}/cards", params=params)
        if resp.ok == False:
            raise resp.text
        for card in resp.json():
            append_target.append(Item.from_trello_card(card, list_status))

    def get_items(self) -> list:
        items = []
        self.get_items_of_list(self.TODO_LIST_ID, ItemType.ToDo, items)
        self.get_items_of_list(self.DOING_LIST_ID, ItemType.Doing, items)
        self.get_items_of_list(self.DONE_LIST_ID, ItemType.Done, items)
        return items

    def add_item(self, name) -> requests.Response:
        params = {'key': self.key, 'token' : self.token, 'name' : name, 'idList' : self.TODO_LIST_ID}
        return requests.post(f'{self.url}/1/cards', params=params)

    def delete_item(self, name) -> requests.Response:
        items = self.get_items()
        for item in items:
            if item.name == name:
                params = {'key': self.key, 'token' : self.token }
                return requests.delete(f'{self.url}/1/cards/{item.id}', params=params)
        fake_resp = requests.Response()
        fake_resp.status_code = HTTPStatus.OK
        return fake_resp

    def complete_item(self, id, list_id) -> requests.Response:
        next_list_id = self.DOING_LIST_ID
        if list_id == self.DOING_LIST_ID:
            next_list_id = self.DONE_LIST_ID
        params = { 'key' : self.key, 'token' : self.token, 'idList': next_list_id }
        return requests.put(f'{self.url}/1/cards/{id}', params=params)

    def switch_board(self, id) -> None:
        self.id = id
        self.load_lists()

    def create_board(self, name) -> requests.Response:
        params = {'key': self.key, 'token' : self.token, 'name' : name}
        return requests.post(f'{self.url}/1/boards', params = params)

    def delete_board(self, id) -> requests.Response:
        params = {'key': self.key, 'token' : self.token}
        return requests.delete(f'{self.url}/1/boards/{id}', params = params)

    def load_lists(self) -> None:
        """Loads To-Do, Doing and Done lists within the current board"""
        params = {'key': self.key, 'token' : self.token, 'id' : self.id}
        resp = requests.get(f'{self.url}/1/boards/{self.id}/lists', params = params)
        if resp.ok == False:
            self.TODO_LIST_ID = ''
            self.DOING_LIST_ID = ''
            self.DONE_LIST_ID = ''
            return
        for list in resp.json():
            name = list['name']
            if name == ItemType.ToDo:
                self.TODO_LIST_ID = list['id']
            elif name == ItemType.Doing:
                self.DOING_LIST_ID = list['id']
            elif name == ItemType.Done:
                self.DONE_LIST_ID = list['id']