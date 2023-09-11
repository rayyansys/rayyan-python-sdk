from typing import TYPE_CHECKING

from .paths import REVIEWS_ROUTE


if TYPE_CHECKING:
    from rayyan.rayyan import Rayyan
else:
    Rayyan = None


class ReviewAccess:
    def __init__(self, rayyan: Rayyan):
        self.__rayyan__ = rayyan

    def delete_access(self, id: int, user_id: int) -> dict:
        return self.__rayyan__.request.request_handler(
            method="POST",
            path=f"{REVIEWS_ROUTE}/{id}/delete_review_access",
            params={"user_id": user_id},
        )

    def update_access(self, id: int, role_id: int, user_emails: list) -> dict:
        return self.__rayyan__.request.request_handler(
            method="POST",
            path=f"{REVIEWS_ROUTE}/{id}/update_review_access",
            payload={"role_id": role_id, "user_emails": user_emails},
        )

    def invite(
        self,
        id: int,
        role_id: int,
        user_emails: list,
        user_reason: str,
    ) -> dict:
        return self.__rayyan__.request.request_handler(
            method="POST",
            path=f"{REVIEWS_ROUTE}/{id}/invite",
            payload={
                "role_id": role_id,
                "user_emails": user_emails,
                "user_reason": user_reason,
            },
        )

    def revoke(
        self,
        id: int,
        user_id: int,
    ) -> dict:
        return self.__rayyan__.request.request_handler(
            method="POST",
            path=f"{REVIEWS_ROUTE}/{id}/revoke",
            params={"user_id": user_id},
        )

    def restore(
        self,
        id: int,
        user_id: int,
    ) -> dict:
        return self.__rayyan__.request.request_handler(
            method="POST",
            path=f"{REVIEWS_ROUTE}/{id}/restore",
            params={
                "user_id": user_id,
            },
        )
