from typing import Protocol

from rayyan.paths import BASE_URL
from rayyan.request import StatefulRequest, StatelessRequest, BaseRequest


class RayyanProtocol(Protocol):
    request: BaseRequest


class Rayyan:
    def __init__(self, credentials_file_path: str, url: str = BASE_URL):
        self.request = StatefulRequest(self, credentials_file_path=credentials_file_path)
        self._base_url = url


class StatelessRayyan:
    def __init__(self, bearer_token: str, url: str = BASE_URL):
        self._base_url = url
        self.request = StatelessRequest(self, bearer_token=bearer_token)
