import os

from lxml import etree


class ParserInfoMod():
    def __init__(self, path):
        if not os.path.isfile(path):
            raise ValueError("File not existe")
        info_mod = etree.parse(path)
        self.__info_mod_root = info_mod.getroot()

    def load_medtada(self):
        dict_metadat = {
            "Name": str,
            "Author": str,
            "Version": str,
            "Description": str,
            "Website": str
        }
        for item in self.__info_mod_root:
            dict_metadat[item.tag] = item.text

        return dict_metadat


class Parse(object):
    def __init__(self,):
        pass
