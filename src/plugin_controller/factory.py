from gi.repository import GObject


class Game(GObject.Object):
    key = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READWRITE,
        default=""
    )
    plugin = GObject.Property(
        type=object,
        nick="Value",
        blurb="Value",
        flags=GObject.ParamFlags.READWRITE,
    )
