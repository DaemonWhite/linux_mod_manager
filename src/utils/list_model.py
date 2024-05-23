from gi.repository import GObject, Gio
from custom_widget.check_row import CheckRow


class GObjectSelected(GObject.Object):
    __gtype_name__ = 'GObjectSelected'

    def __init__(self, objectt: object):
        super().__init__()
        self.__object = objectt

    @property
    def object(self):
        return self.__object


class ListSingleSelectModel(GObject.Object, Gio.ListModel):
    __gtype_name__ = 'ListSingleSelectModel'

    def __init__(self, groups: list):
        super().__init__()


class ListMultipleSelectModel(GObject.Object, Gio.ListModel):
    __gtype_name__ = 'ListMultipleSelectModel'

    def __init__(self, groups: list):
        super().__init__()
        self.groups = []
        for group in groups:
            self.groups.append(GObjectSelected(group))
        print("coucou")

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        print("ok")
        if self.index < len(self.groups):
            result = self.groups[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration

    def enable(self, name: str, value: bool):
        for group in self.groups:
            if group.object.name == name:
                group.object.enable = value
                return value

    def do_get_item(self, index):
        print("call -> ", self.groups[index])
        return self.groups[index]

    def do_get_n_items(self):
        return len(self.groups)

    def do_get_item_type(self):
        return GObjectSelected


class ListRowModel(GObject.Object, Gio.ListModel):
    __gtype_name__ = 'ListRowModel'

    def __init__(self):
        super().__init__()
        self.row = []

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.row):
            result = self.row[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration

    def do_get_item(self, index):
        return self.row[index]

    def do_get_item_by_name(self, name):
        row_return = None

        for roww in self.row:
            if roww.get_title() == name:
                row_return = roww
                break

        return row_return

    def do_get_n_items(self):
        return len(self.row)

    def append_row(self, row):
        self.row.append(row)
        index = len(self.row) - 1
        self.items_changed(index, False, True)

    def clear(self):
        for _ in self.row:
            self.items_changed(0, True, False)

        self.row.clear()

    def remove_row(self, index):
        for roww in self.row:
            print(roww.get_title())
        self.items_changed(index, True, False)
        self.row.pop(index)
        for roww in self.row:
            print(roww.get_title())

    def remove_row_by_row(self, by_row):
        for i, roww in enumerate(self.row):
            if roww == by_row:
                self.items_changed(i, True, False)
                self.row.pop(i)

    def remove_row_by_name(self, name):
        for i, roww in enumerate(self.row):
            if roww.get_title() == name:
                self.items_changed(i, True, False)
                self.row.pop(i)
                break


def give_item_list_row(list_item):
    return list_item
