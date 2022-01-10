import requests
import os

from todo_app.data.item import Item

url = "https://api.trello.com"
id = os.getenv('TRELLO_BOARD_ID')
key = os.getenv('TRELLO_KEY')
token = os.getenv('TRELLO_TOKEN')

def get_items_of_list(list_name, append_target):
    params = { 'key' : key, 'token' : token}
    resp = requests.get(f"{url}/1/lists/{list_name}/cards", params=params)
    for card in resp.json():
        append_target.append(Item.from_trello_card(card))

def get_items():
    items = []
    get_items_of_list(Item.TODO_LIST_ID, items)
    get_items_of_list(Item.DOING_LIST_ID, items)
    get_items_of_list(Item.DONE_LIST_ID, items)
    return items

def add_item(name):
    params = {'key': key, 'token' : token, 'name' : name, 'idList' : Item.TODO_LIST_ID}
    return requests.post(f'{url}/1/cards', params=params)

def complete_item(id, list_id):
    next_list_id = Item.DOING_LIST_ID
    if list_id == Item.DOING_LIST_ID:
        next_list_id = Item.DONE_LIST_ID
    params = { 'key' : key, 'token' : token, 'idList': next_list_id }
    return requests.put(f'{url}/1/cards/{id}', params=params)