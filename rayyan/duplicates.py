from typing import TYPE_CHECKING, Dict

from .paths import REVIEWS_ROUTE


if TYPE_CHECKING:
    from rayyan.rayyan import Rayyan
else:
    Rayyan = None


class Duplicates:
    def __init__(self, rayyan: Rayyan):
        self.__rayyan__ = rayyan

    def get_duplicate(self, id, article_id) -> Dict[str, str]:
        return self.__rayyan__.request.request_handler(
            method="GET", path=f"{REVIEWS_ROUTE}/{id}/duplicates/{article_id}"
        )

    def add_duplicate(self, id) -> Dict[str, str]:
        return self.__rayyan__.request.request_handler(
            method="POST", path=f"{REVIEWS_ROUTE}/{id}/duplicates/"
        )

    def update_duplicate(
        self, id, article_id, duplicate_action: int, isDeletedArticle: bool = False
    ) -> Dict[str, str]:
        return self.__rayyan__.request.request_handler(
            method="PATCH",
            payload={
                "duplicate_action": duplicate_action,
                "isDeletedArticle": isDeletedArticle,
            },
            path=f"{REVIEWS_ROUTE}/{id}/duplicates/{article_id}",
        )
