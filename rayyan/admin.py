from typing import TYPE_CHECKING, Dict, Optional

from .paths import REVIEWS_ROUTE


if TYPE_CHECKING:
    from rayyan.rayyan import Rayyan
else:
    Rayyan = None


class FullTexts:
    def __init__(self, rayyan: Rayyan):
        self.__rayyan__ = rayyan




class Search:
    def __init__(self, rayyan: Rayyan):
        self.__rayyan__ = rayyan




class Reviews:
    def __init__(self, rayyan: Rayyan):
        self.__rayyan__ = rayyan




class Teams:
    def __init__(self, rayyan: Rayyan):
        self.__rayyan__ = rayyan




class Admin:
    def __init__(self, rayyan: Rayyan):
        self.__rayyan__ = rayyan
        self.full_text = FullTexts(rayyan)
        self.search = Search(rayyan)
        self.reviews = Reviews(rayyan)
        self.teams = Teams(rayyan)
