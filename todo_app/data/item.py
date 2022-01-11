import os

class ItemType:
    Done = 'Done'
    Doing = 'Doing'
    ToDo = 'To Do'

class Item:
    TODO_LIST_ID = os.getenv('TRELLO_LIST_ID')
    DOING_LIST_ID = os.getenv('TRELLO_DOING_LIST')
    DONE_LIST_ID = os.getenv('TRELLO_DONE_LIST')

    def __init__(self, id, name, list_id):
        self.id = id
        self.name = name
        self.list_id = list_id

    @property
    def status(self):
        if self.list_id == self.DONE_LIST_ID:
            return ItemType.Done
        elif self.list_id == self.DOING_LIST_ID:
            return ItemType.Doing
        else:
            return ItemType.ToDo

    @classmethod
    def from_trello_card(cls, card):
        print(card['idList'])
        return cls(card['id'], card['name'], card['idList'])

        