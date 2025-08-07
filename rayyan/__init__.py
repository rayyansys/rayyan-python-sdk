from rayyan.request import Request
from rayyan.stateless_request import StatelessRequest

from rayyan.paths import BASE_URL


class Rayyan:
    def __init__(self, credentials_file_path: str, url: str = BASE_URL):
        self.request = Request(self)
        self._base_url = url
        self.request._credentials_file_handler(credentials_file_path)


class StatelessRayyan:
    def __init__(self, bearer_token: str, url: str = BASE_URL):
        self._base_url = url
        self.request = StatelessRequest(base_url=url, bearer_token=bearer_token)