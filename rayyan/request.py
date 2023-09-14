import json
from typing import TYPE_CHECKING, Dict, Union
from requests import request
import requests
from requests.models import Response
from requests import Request as RequestModel
from requests import Session
from rayyan.conf import CREDENTIAL_KEYS
from rayyan.errors import InvalidCredentialsError, RefreshTokenExpiredError
from rayyan.paths import REFRESH_TOKEN_ROUTE
from requests import PreparedRequest
from requests_toolbelt.multipart.encoder import MultipartEncoder


if TYPE_CHECKING:
    from rayyan.rayyan import Rayyan

else:
    Rayyan = None


class Request:
    """
    The `Request` class handles HTTP requests with authorization and error
    handling, including refreshing access tokens and validating credentials data.
    """

    def __init__(self, rayyan: Rayyan):
        self.rayyan = rayyan

    def _response_handler(
        self, response: Response, session: Session, prepared_request: PreparedRequest
    ) -> Dict[str, Union[int, str, Dict[str, str]]]:
        if response.status_code == 401:
            self._refresh_credentials()
            prepared_request.headers["Authorization"] = f"Bearer {self._access_token}"
            response = session.send(prepared_request)
                    
        if 'application/json' in response.headers.get('Content-Type', ''):
            data = response.json()
        else:
            data = response.text

        code: int = response.status_code
        if code >= 200 and code <= 299:
            return data

        response.raise_for_status()
        reason = response.reason
        response_body: Dict[str, Union[int, str, Dict[str, str]]] = {
            "code": code,
            "message": reason,
            "data": data,
        }

        return response_body

    def request_handler(
        self,
        path: str,
        files: list = None,
        method: str = "GET",
        headers: Dict[str, str] = {},
        payload: Dict[str, Union[int, str, Dict[str, str]]] = None,
        params: Dict[str, str] = {},
        body_type: str = "json",
    ) -> Dict[str, Union[int, str, Dict[str, str]]]:
        """
        This is a Python function that handles HTTP requests with various parameters and returns a
        dictionary of the response.
        """
        headers["Authorization"] = f"bearer {self._access_token}"
        headers["Accept"] = "application/json"
        dumped_payload = payload
        if body_type == "json" and payload is not None:
            headers["Content-Type"] = "application/json"
            dumped_payload = json.dumps(payload)

        session = Session()
        request = RequestModel(
            method=method,
            url=f"{self.rayyan._base_url}{path}",
            headers=headers,
            params=params,
            data=dumped_payload,
            files=files,
        )
        prepared_request = session.prepare_request(request)
        response = session.send(prepared_request)
        return self._response_handler(response, session, prepared_request)
    
    def file_uploader(
        self,
        url: str,
        headers: Dict[str, str] = {},
        params: Dict[str, str] = {},
    ) -> Dict[str, Union[int, str, Dict[str, str]]]:
        
        multipart_data = MultipartEncoder(
            fields=params
        )
        headers['Content-Type'] = multipart_data.content_type
        response = requests.post(url, data=multipart_data, headers=headers)
        
        code: int = response.status_code
        if code >= 200 and code <= 299:
            return response.text

        response.raise_for_status()
        reason = response.reason
        response_body: Dict[str, Union[int, str, Dict[str, str]]] = {
            "code": code,
            "message": reason,
            "data": response.text,
        }

        return response_body
    
    def _get_credentials_from_credentials_file(self) -> Dict[str, str]:
        """
        This function reads and returns credentials data from a JSON file after validating it.
        """
        with open(self._credentials_file_path) as credentials_file:
            credentials = json.load(credentials_file)
            return self._validate_credentials_data(credentials)

    def _validate_credentials_data(self, data: Dict[str, str]) -> Dict[str, str]:
        """
        This function validates if a dictionary contains all the required keys for credentials data and
        raises an error if any key is missing.
        """
        if missed_keys := tuple(set(CREDENTIAL_KEYS) - set(data.keys())):
            raise InvalidCredentialsError(
                f"The data provided in credentials file missing key(s): {missed_keys}"
            )
        return data

    def _refresh_token_request_handler(self) -> Dict[str, Union[int, str]]:
        """
        This function sends a request to refresh an access token using a refresh token and returns the
        response data.
        """
        payload: Dict[str, str] = {
            "grant_type": "refresh_token",
            "refresh_token": self._refresh_token,
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

    def _refresh_credentials(self) -> None:
        """
        This function refreshes the access token by calling an API and updating the access and refresh
        tokens in a credentials file.
        """
        new_credentials: Dict[
            str, Union[int, str]
        ] = self._refresh_token_request_handler()

        self._access_token = str(new_credentials["access_token"])
        self._refresh_token = str(new_credentials["refresh_token"])

        with open(self._credentials_file_path, "w") as credentials_file:
            json.dump(new_credentials, credentials_file)

    def _credentials_file_handler(self, file_path: str) -> None:
        self._credentials_file_path = file_path
        _credentials = self._get_credentials_from_credentials_file()
        self._access_token = _credentials["access_token"]
        self._refresh_token = _credentials["refresh_token"]
