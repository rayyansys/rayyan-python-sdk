from rayyan.request import Request
from rayyan.user import User
from rayyan.third_party_auth import ThirdPartyAuth
from rayyan.review import Review
from rayyan.paths import BASE_URL


class Rayyan:
    def __init__(self, credentials_file_path: str, url: str = BASE_URL):
        self.user = User(self)
        self.third_party_auth = ThirdPartyAuth(self)
        self.review = Review(self)
        self.request = Request(self)
        self._base_url = url
        self.request._credentials_file_handler(credentials_file_path)
