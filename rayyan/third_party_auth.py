from typing import TYPE_CHECKING, Dict

from .paths import THIRD_PARTY_AUTH
from .conf import MENDELEY

if TYPE_CHECKING:
    from rayyan.rayyan import Rayyan
else:
    Rayyan = None

ALLOWED_PROVIDERS = [MENDELEY]


class ThirdPartyAuth:
    def __init__(self, rayyan: Rayyan, third_party: str):
        self._validate_third_party_name(third_party)
        self.__rayyan__ = rayyan
        self._third_party = third_party

    def _validate_third_party_name(self, third_party: str) -> None:
        if third_party not in ALLOWED_PROVIDERS:
            raise ValueError(
                f"Unsupported third-party provider: {third_party}, make sure to use one from {ALLOWED_PROVIDERS}"
            )

    def get_auth_link(self) -> Dict[str, str]:
        return self.__rayyan__.request.request_handler(
            method="GET", path=f"{THIRD_PARTY_AUTH}/{self._third_party}"
        )

    def get_access_token(self) -> Dict[str, str]:
        return self.__rayyan__.request.request_handler(
            method="GET", path=f"{THIRD_PARTY_AUTH}/{self._third_party}_access_token"
        )

    def get_access_token_from_code(self, code: str = None) -> Dict[str, str]:
        return self.__rayyan__.request.request_handler(
            method="GET",
            path=f"{THIRD_PARTY_AUTH}/{self._third_party}_access_token_from_code",
            params={"code": code},
        )
