from typing import TYPE_CHECKING

from .paths import REVIEWS_ROUTE


if TYPE_CHECKING:
    from rayyan.rayyan import Rayyan
else:
    Rayyan = None


class Highlight:
    def __init__(self, rayyan: Rayyan):
        self.__rayyan__ = rayyan

    def create_highlight(self, id: int, category_id: int, keyword: str) -> dict:
        return self.__rayyan__.request.request_handler(
            method="POST",
            path=f"{REVIEWS_ROUTE}/{id}/highlights",
            payload={"keyword": keyword, "category": category_id},
        )

    def delete_highlight(self, id: int, category_id: int, keyword: str) -> dict:
        return self.__rayyan__.request.request_handler(
            method="DELETE",
            path=f"{REVIEWS_ROUTE}/{id}/highlight",
            payload={"id": keyword, "category": category_id},
        )
