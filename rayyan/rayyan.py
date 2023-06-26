from rayyan.request import Request
from rayyan.user import User
from rayyan.review import Review
from rayyan.admin import Admin
from rayyan.mendey_connect import MendeleyConnect
from rayyan.paths import BASE_URL


class Rayyan:
    def __init__(self, credentials_file_path: str, base_url: str = BASE_URL):
        self.user = User(self)
        self.review = Review(self)
        self.admin = Admin(self)
        self.mendeley_connect = MendeleyConnect(self)

        self._request = Request(self)
        self._credentials_file_path = credentials_file_path
        self._base_url = base_url
        self._credentials_handler()

    def _credentials_handler(self) -> None:
        _credentials = self._request.get_credentials_from_credentials_file()
        self._access_token = _credentials["access_token"]
        self._refresh_token = _credentials["refresh_token"]
        self._token_type = _credentials["token_type"]
