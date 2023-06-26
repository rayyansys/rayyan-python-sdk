from typing import TYPE_CHECKING, Dict, Optional

from .paths import DELETE_USER_ROUTE, REVOKE_TOKEN_ROUTE, USER_INFO_ROUTE


if TYPE_CHECKING:
    from rayyan.rayyan import Rayyan
else:
    Rayyan = None


class User:
    def __init__(self, rayyan: Rayyan):
        self.__rayyan__ = rayyan

    def get_info(self) -> Dict[str, str]:
        return self.__rayyan__._request.request_handler(
            method="GET", path=USER_INFO_ROUTE
        )

    def delete(self) -> Dict[str, str]:
        return self.__rayyan__._request.request_handler(
            method="DELETE", path=DELETE_USER_ROUTE
        )

    def revoke_token(self) -> Dict[str, str]:
        return self.__rayyan__._request.request_handler(
            method="POST", path=REVOKE_TOKEN_ROUTE
        )
