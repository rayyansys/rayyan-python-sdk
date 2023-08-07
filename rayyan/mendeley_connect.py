from typing import TYPE_CHECKING, Dict

from .paths import MENDELEY_ROUTE


if TYPE_CHECKING:
    from rayyan.rayyan import Rayyan
else:
    Rayyan = None


class MendeleyConnect:
    def __init__(self, rayyan: Rayyan):
        self.__rayyan__ = rayyan

    def get_mendeley_auth_link(self) -> Dict[str, str]:
        return self.__rayyan__.request.request_handler(
            method="GET", path=f"{MENDELEY_ROUTE}/mendeley"
        )

    def get_mendeley_access_token(self) -> Dict[str, str]:
        return self.__rayyan__.request.request_handler(
            method="GET", path=f"{MENDELEY_ROUTE}/mendeley_access_token"
        )

    def get_mendeley_access_token_from_code(self, code: str = None) -> Dict[str, str]:
        return self.__rayyan__.request.request_handler(
            method="GET",
            path=f"{MENDELEY_ROUTE}/mendeley_access_token_from_code",
            params={"code": code},
        )
