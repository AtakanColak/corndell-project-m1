import os

class ItemType:
    Done = 'Done'
    Doing = 'Doing'
    ToDo = 'To Do'

class Item:
    def __init__(self, id, name, list_id, status: ItemType):
        self.id = id
        self.name = name
        self.list_id = list_id
        self.status = status

    @classmethod
    def from_trello_card(cls, card, item_type: ItemType):
        return cls(card['id'], card['name'], card['idList'], item_type)

        