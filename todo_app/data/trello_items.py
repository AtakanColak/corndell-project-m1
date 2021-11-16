import requests
import os

from todo_app.data.item import Item

url = "https://api.trello.com"
id = os.getenv('TRELLO_BOARD_ID')
key = os.getenv('TRELLO_KEY')
token = os.getenv('TRELLO_TOKEN')
list_id = os.getenv('TRELLO_LIST_ID')
done_list_id = os.getenv('TRELLO_DONE_LIST')

def get_items():
    params = { 'key' : key, 'token' : token}
    resp = requests.get(f"{url}/1/lists/{list_id}/cards", params=params)
    items = []
    for card in resp.json():
        items.append(Item.from_trello_card(card))
    return items

def add_item(name):
    params = {'key': key, 'token' : token, 'name' : name, 'idList' : list_id}
    return requests.post(f'{url}/1/cards', params=params)

def complete_item(id):
    params = { 'key' : key, 'token' : token, 'idList': done_list_id}
    return requests.put(f'{url}/1/cards/{id}', params=params)