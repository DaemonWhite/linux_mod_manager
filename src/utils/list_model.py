from gi.repository import GObject, Gio


class ListRowModel(GObject.Object, Gio.ListModel):
    __gtype_name__ = 'ListRowModel'

    def __init__(self):
        super().__init__()
        self.row = []

    def __iter__(self):
        return iter(self.row)

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
        self.items_changed(len(self.row) - 1, False, True)

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
                self.row.pop(i)
                self.items_changed(i, True, False)

    def remove_row_by_name(self, name):
        for i, roww in enumerate(self.row):
            if roww.get_title() == name:
                self.items_changed(i, True, False)
                self.row.pop(i)
                break


def give_item_list_row(list_item):
    return list_item
