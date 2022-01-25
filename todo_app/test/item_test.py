from todo_app.data.item import Item, ItemType
from todo_app.data.trello_service import TrelloService

def get_test_items(trello_service: TrelloService):
    return [
        Item.from_trello_card({ 'id' : 1, 'name' : 'Test1', 'idList': trello_service.TODO_LIST_ID}, ItemType.ToDo),
        Item.from_trello_card({ 'id' : 2, 'name' : 'Test2', 'idList': trello_service.DOING_LIST_ID}, ItemType.Doing),
        Item.from_trello_card({ 'id' : 3, 'name' : 'Test3', 'idList': trello_service.DONE_LIST_ID}, ItemType.Done)
    ]