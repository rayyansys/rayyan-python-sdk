from typing import Dict

from .paths import REVIEWS_ROUTE


from rayyan.types import RayyanProtocol as Rayyan


class Duplicates:
    def __init__(self, rayyan: Rayyan):
        self.__rayyan__ = rayyan

    def get_duplicate(self, id, article_id) -> Dict[str, str]:
        return self._request(
            method="GET", path=f"{REVIEWS_ROUTE}/{id}/duplicates/{article_id}"
        )

    def add_duplicate(self, id) -> Dict[str, str]:
        return self._request(
            method="POST", path=f"{REVIEWS_ROUTE}/{id}/duplicates/"
        )

    def update_duplicate(
        self, id, article_id, duplicate_action: int, isDeletedArticle: bool = False
    ) -> Dict[str, str]:
        return self._request(
            method="PATCH",
            payload={
                "duplicate_action": duplicate_action,
                "isDeletedArticle": isDeletedArticle,
            },
            path=f"{REVIEWS_ROUTE}/{id}/duplicates/{article_id}",
        )
