from dataclasses import dataclass


@dataclass
class Dependencies:
    plugin: str
    active: str


class Base(object):

    def __init__(self,):
        self.__childs = []

    @property
    def get_childs(self):
        self.__childs.copy()

    def set_child(self, child):
        self.__childs.append(child)


class Flag(Base):
    def __init__(self, name, value, operator):
        pass


class Flags(Base):
    def __init__(self):
        self.__flags = {}

    def append_flags(self, flag):
        self.__flags[flag.name] = flag


class ModuleDendecies(Base):
    def __init__(self, plugin: str, operator: str):
        super().__init__()
        self.PLUGIN = plugin
        self.OPERATOR = operator
        self.dependencies = []

    def dependacies(self, dependencie):
        self.Dependencies.append(dependencie)


class Option(Base):

    def __init__(self,):
        super().__init__()


class Options(Base):
    def __init__(self):
        super().__init__()
        self.__options = []

    def add_option(self, option: Option):
        self.__options.append(option)


# group name and type
class Group(Base):

    def __init__(self, name, tipe):
        super().__init__()
        self.NAME = name
        self.TIPE = tipe


# groups order
class Groups(Base):
    def __init__(self, order):
        super().__init__()
        self.ORDER = order
        self.__groups

    def append(self, group: Group):
        self.__groups.append(group)


# installStep order > name
class Page(Base):

    def __init__(self, name, order):
        super().__init__()
        self.NAME = name
        self.__groups

    def __len__(self):
        return len(self.__groups)

    def add_group(self, group: Group):
        self.__groups.append(group)
