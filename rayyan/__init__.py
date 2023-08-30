from rayyan.request import Request
from rayyan.paths import BASE_URL


class Rayyan:
    def __init__(self, credentials_file_path: str, url: str = BASE_URL):
        self.request = Request(self)
        self._base_url = url
        self.request._credentials_file_handler(credentials_file_path)
