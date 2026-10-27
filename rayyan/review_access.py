from typing import Optional, Union

from .paths import REVIEWS_ROUTE

from rayyan.types import RayyanProtocol as Rayyan



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
        user_reason: Optional[str] = None,
    ) -> Union[dict, str]:
        """Invite users to a review. Returns "" on success; raises HTTPError if rejected.

        `user_reason` is included in the invitation email sent to every invitee.
        """
        payload = {
            "role_id": role_id,
            "user_emails": user_emails,
        }
        if user_reason is not None:
            payload["user_reason"] = user_reason
        return self.__rayyan__.request.request_handler(
            method="POST",
            path=f"{REVIEWS_ROUTE}/{id}/invite",
            payload=payload,
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
