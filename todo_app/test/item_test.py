from todo_app.data.item import Item

def get_test_items():
    return [
        Item.from_trello_card({ 'id' : 1, 'name' : 'Test1', 'idList': Item.TODO_LIST_ID}),
        Item.from_trello_card({ 'id' : 2, 'name' : 'Test2', 'idList': Item.DOING_LIST_ID}),
        Item.from_trello_card({ 'id' : 3, 'name' : 'Test3', 'idList': Item.DONE_LIST_ID})
    ]