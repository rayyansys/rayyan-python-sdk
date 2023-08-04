from .paths import DELETE_USER_ROUTE, REVOKE_TOKEN_ROUTE, USER_INFO_ROUTE
from typing import TYPE_CHECKING, Dict, Union


if TYPE_CHECKING:
    from rayyan.rayyan import Rayyan
else:
    Rayyan = None


class User:
    def __init__(self, rayyan: Rayyan):
        self.__rayyan__ = rayyan

    def get_info(self) -> Dict[str, Union[int, str, Dict[str, str]]]:
        return self.__rayyan__.request.request_handler(
            method="GET", path=USER_INFO_ROUTE
        )

    def delete(self) -> Dict[str, Union[int, str, Dict[str, str]]]:
        return self.__rayyan__.request.request_handler(
            method="DELETE", path=DELETE_USER_ROUTE
        )

    def revoke_token(self) -> Dict[str, Union[int, str, Dict[str, str]]]:
        return self.__rayyan__.request.request_handler(
            method="POST", path=REVOKE_TOKEN_ROUTE
        )
