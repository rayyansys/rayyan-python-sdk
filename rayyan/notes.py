from typing import TYPE_CHECKING

from .paths import REVIEWS_ROUTE


if TYPE_CHECKING:
    from rayyan.rayyan import Rayyan
else:
    Rayyan = None


class Notes:
    def __init__(self, rayyan: Rayyan):
        self.__rayyan__ = rayyan

    def create_note(self, review_id: int, article_id: int, text: str) -> dict:
        return self.__rayyan__.request.request_handler(
            method="POST",
            path=f"{REVIEWS_ROUTE}/{review_id}/articles/{article_id}/notes",
            payload={"text": text},
        )

    def update_note(
        self, review_id: int, article_id: int, note_id: int, text: str
    ) -> dict:
        return self.__rayyan__.request.request_handler(
            method="PUT",
            path=f"{REVIEWS_ROUTE}/{review_id}/articles/{article_id}/notes/{note_id}",
            payload={"text": text},
        )

    def delete_note(self, review_id: int, article_id: int, note_id: int) -> dict:
        return self.__rayyan__.request.request_handler(
            method="DELETE",
            path=f"{REVIEWS_ROUTE}/{review_id}/articles/{article_id}/notes/{note_id}",
        )
