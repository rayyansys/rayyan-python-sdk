import json
from typing import TYPE_CHECKING, Dict, Union
from requests import request
from requests.models import Response
from rayyan.conf import CREDENTIAL_KEYS
from rayyan.errors import InvalidCredentialsError, RefreshTokenExpiredError
from rayyan.paths import REFRESH_TOKEN_ROUTE

if TYPE_CHECKING:
    from rayyan.rayyan import Rayyan
else:
    Rayyan = None


class Request:
    """
    The `Request` class handles HTTP requests with authorization and error
    handling, including refreshing access tokens and validating credentials data.
    """

    is_refreshed: bool = False

    def __init__(self, rayyan: Rayyan):
        self.rayyan = rayyan

    def response_handler(
        self,
        response: Response,
        method: str,
        path: str,
        headers: Dict[str, str],
        payload: Union[Dict[str, str], str] = {},
    ) -> Dict[str, Union[int, str, Dict[str, str]]]:
        data = {}
        try:
            data = response.json()
        except Exception:
            data = {}

        code: int = response.status_code

        if code >= 200 and code <= 299:
            return data

        elif response.status_code == 401 and not self.is_refreshed:
            self.refresh_credentials()
            return self.request_handler(method, path, headers, payload)

        response.raise_for_status()
        reason = response.reason
        response_body: Dict[str, Union[int, str, Dict[str, str]]] = {
            "code": code,
            "message": reason,
            "data": data,
        }
        if data.get("error"):
            response_body["error"] = data["error"][0]

        return response_body

    def request_handler(
        self,
        method: str,
        path: str,
        headers: Dict[str, str] = {},
        payload: Union[Dict[str, str], str] = {},
        params: Dict[str, str] = {},
    ) -> Dict[str, Union[int, str, Dict[str, str]]]:
        """
        This is a Python function that handles HTTP requests with various parameters and returns a
        dictionary of the response.
        """
        headers[
            "Authorization"
        ] = f"{self.rayyan._token_type} {self.rayyan._access_token}"
        if method == "POST":
            headers["Content-Type"] = "application/json"
            payload = json.dumps(payload)

        response = request(
            method=method,
            url=f"{self.rayyan._base_url}{path}",
            headers=headers,
            params=params,
            data=payload,
        )

        return self.response_handler(response, method, path, headers, payload)

    def get_credentials_from_credentials_file(self) -> Dict[str, str]:
        """
        This function reads and returns credentials data from a JSON file after validating it.
        """
        with open(self.rayyan._credentials_file_path) as credentials_file:
            credentials = json.load(credentials_file)
            return self.validate_credentials_data(credentials)

    def validate_credentials_data(self, data: Dict[str, str]) -> Dict[str, str]:
        """
        This function validates if a dictionary contains all the required keys for credentials data and
        raises an error if any key is missing.
        """
        if missed_keys := tuple(set(CREDENTIAL_KEYS) - set(data.keys())):
            raise InvalidCredentialsError(
                f"The data provided in credentials file missing key(s): {missed_keys}"
            )
        return data

    def refresh_token_request_handler(self) -> Dict[str, Union[int, str]]:
        """
        This function sends a request to refresh an access token using a refresh token and returns the
        response data.
        """
        payload: Dict[str, str] = {
            "grant_type": "refresh_token",
            "refresh_token": self.rayyan._refresh_token,
        }

        response = request(
            method="POST",
            url=f"{self.rayyan._base_url}{REFRESH_TOKEN_ROUTE}",
            data=payload,
        )

        code = response.status_code

        if code == 401:
            raise RefreshTokenExpiredError(
                "Refresh token expired, please update the credentials file and try again."
            )

        data: Dict[str, Union[int, str]] = response.json()

        return data

    def refresh_credentials(self) -> None:
        """
        This function refreshes the access token by calling an API and updating the access and refresh
        tokens in a credentials file.
        """
        new_credentials: Dict[
            str, Union[int, str]
        ] = self.refresh_token_request_handler()

        self.rayyan._access_token = str(new_credentials["access_token"])
        self.rayyan._refresh_token = str(new_credentials["refresh_token"])
        self.rayyan._token_type = str(new_credentials["token_type"])

        with open(self.rayyan._credentials_file_path, "w") as credentials_file:
            json.dump(new_credentials, credentials_file)

        self.is_refreshed = True
