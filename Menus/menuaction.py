from typing import Union


class MenuActionMenu:
    def __init__(self):
        pass


class MenuActionPlay:
    def __init__(self, level: str):
        self.level: str = level


class MenuActionSelectLevel:
    def __init__(self):
        pass


class MenuActionQuit:
    def __init__(self):
        pass


class MenuActionPlayerSelect:
    def __init__(self):
        pass


class MenuActionCredits:
    def __init__(self):
        pass


MenuAction = Union[MenuActionMenu, MenuActionPlay, MenuActionPlayerSelect, MenuActionSelectLevel, MenuActionQuit,
                   MenuActionCredits]
