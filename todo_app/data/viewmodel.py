from todo_app.data.item import ItemType


class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    def __get_items_of_type(self, itemType: ItemType):
        return [item for item in self._items if item.status == itemType]

    @property
    def todo_items(self):
        return self.__get_items_of_type(ItemType.ToDo)

    @property
    def doing_items(self):
        return self.__get_items_of_type(ItemType.Doing)

    @property
    def done_items(self):
        return self.__get_items_of_type(ItemType.Done)