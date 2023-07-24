from rayyan.request import Request
from rayyan.user import User
from rayyan.paths import BASE_URL


class Rayyan:
    def __init__(self, credentials_file_path: str):
        self.user = User(self)
        self._request = Request(self)
        self._base_url = BASE_URL
        self._request.credentials_file_handler(credentials_file_path)
