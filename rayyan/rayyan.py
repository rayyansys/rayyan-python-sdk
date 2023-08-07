from rayyan.request import Request
from rayyan.user import User
from rayyan.mendeley_connect import MendeleyConnect
from rayyan.paths import BASE_URL


class Rayyan:
    def __init__(self, credentials_file_path: str, url: str = BASE_URL):
        self.user = User(self)
        self.mendeley_connect = MendeleyConnect(self)
        self.request = Request(self)
        self._base_url = url
        self.request._credentials_file_handler(credentials_file_path)
