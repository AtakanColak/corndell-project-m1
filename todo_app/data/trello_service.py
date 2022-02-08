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
        self.TODO_LIST_ID = os.getenv('TRELLO_LIST_ID')
        self.DOING_LIST_ID = os.getenv('TRELLO_DOING_LIST')
        self.DONE_LIST_ID = os.getenv('TRELLO_DONE_LIST')
        pprint.pprint(vars(self))

    def get_items_of_list(self, list_id, list_status, append_target) -> None:
        params = { 'key' : self.key, 'token' : self.token}
        resp = requests.get(f"{self.url}/1/lists/{list_id}/cards", params=params)
        print(resp.json())
        for card in resp.json():
            append_target.append(Item.from_trello_card(card, list_status))

    def get_items(self) -> list:
        items = []
        self.get_items_of_list(self.TODO_LIST_ID, ItemType.ToDo, items)
        self.get_items_of_list(self.DOING_LIST_ID, ItemType.Doing, items)
        self.get_items_of_list(self.DONE_LIST_ID, ItemType.Done, items)
        return items

    def add_item(self, name) -> requests.Response:
        params = {'key': self.key, 'token' : self.token, 'name' : name, 'idList' : Item.TODO_LIST_ID}
        return requests.post(f'{self.url}/1/cards', params=params)

    def complete_item(self, id, list_id) -> requests.Response:
        next_list_id = Item.DOING_LIST_ID
        if list_id == Item.DOING_LIST_ID:
            next_list_id = Item.DONE_LIST_ID
        params = { 'key' : self.key, 'token' : self.token, 'idList': next_list_id }
        return requests.put(f'{self.url}/1/cards/{id}', params=params)