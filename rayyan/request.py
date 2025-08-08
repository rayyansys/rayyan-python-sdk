import json
from typing import Dict, Union, Optional, Callable
from requests import Session, request
from requests.models import Response
from requests_toolbelt.multipart.encoder import MultipartEncoder

from rayyan.conf import CREDENTIAL_KEYS
from rayyan.errors import InvalidCredentialsError, RefreshTokenExpiredError
from rayyan.paths import REFRESH_TOKEN_ROUTE
from rayyan.types import RayyanProtocol as Rayyan


class BaseRequest:
    """
    Base request handling logic, shared by stateful and stateless variants.
    Implements common error handling, token refresh, and request preparation.
    """

    def __init__(self, rayyan: Rayyan, allow_refresh: bool = True):
        self.rayyan = rayyan
        self._allow_refresh = allow_refresh

    def _prepare_request(
        self,
        path: str,
        method: str,
        headers: Optional[Dict[str, str]],
        payload: Optional[dict],
        params: Optional[Dict[str, str]],
        files: Optional[list],
        body_type: str,
    ):
        headers = headers or {}
        params = params or {}
        headers["Authorization"] = f"Bearer {self._access_token}"
        headers["Accept"] = "application/json"

        if body_type == "json" and payload is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(payload)
        else:
            data = payload

        req_url = f"{self.rayyan._base_url}{path}"
        return req_url, method, headers, params, data, files

    def _handle_response(
        self, response: Response, retry_callable: Optional[Callable] = None
    ) -> Union[dict, str]:
        if response.status_code == 401 and retry_callable:
            if self._allow_refresh:
                self._refresh_credentials()
            return retry_callable()

        if "application/json" in response.headers.get("Content-Type", ""):
            data = response.json()
        else:
            data = response.text

        if 200 <= response.status_code <= 299:
            return data

        response.raise_for_status()

    def _validate_credentials_data(self, data: Dict[str, str]) -> Dict[str, str]:
        if missing := tuple(set(CREDENTIAL_KEYS) - set(data.keys())):
            raise InvalidCredentialsError(
                f"Missing credential key(s): {missing}"
            )
        return data

    def _get_credentials_from_file(self) -> Dict[str, str]:
        with open(self._credentials_file_path) as f:
            credentials = json.load(f)
            return self._validate_credentials_data(credentials)

    def _refresh_token_request(self) -> Dict[str, Union[int, str]]:
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self._refresh_token,
        }
        resp = request(
            method="POST",
            url=f"{self.rayyan._base_url}{REFRESH_TOKEN_ROUTE}",
            data=payload,
        )
        if resp.status_code == 401:
            raise RefreshTokenExpiredError(
                "Refresh token expired, please update the credentials file."
            )
        return resp.json()

    def _refresh_credentials(self) -> None:
        new_creds = self._refresh_token_request()
        self._access_token = str(new_creds["access_token"])
        self._refresh_token = str(new_creds["refresh_token"])
        with open(self._credentials_file_path, "w") as f:
            json.dump(new_creds, f)

    def _load_credentials(self, file_path: str) -> None:
        self._credentials_file_path = file_path
        creds = self._get_credentials_from_file()
        self._access_token = creds["access_token"]
        self._refresh_token = creds["refresh_token"]

    def file_uploader(
        self,
        url: str,
        params: Dict[str, str] = {},
        headers: Dict[str, str] = {},
    ) -> Union[dict, str]:
        multipart_data = MultipartEncoder(fields=params)
        headers["Content-Type"] = multipart_data.content_type
        resp = request("POST", url, data=multipart_data, headers=headers)
        return self._handle_response(resp)


class StatefulRequest(BaseRequest):
    """Efficient, persistent session for multiple requests."""

    def __init__(self, rayyan: Rayyan, credentials_file_path: str = None):
        super().__init__(rayyan, allow_refresh=True)
        self.session = Session()
        self._load_credentials(credentials_file_path)

    def request_handler(
        self,
        path: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        payload: Optional[dict] = None,
        params: Optional[Dict[str, str]] = None,
        files: Optional[list] = None,
        body_type: str = "json",
    ):
        req_url, method, headers, params, data, files = self._prepare_request(
            path, method, headers, payload, params, files, body_type
        )

        def retry():
            return self.session.request(
                method, req_url, headers=headers, params=params, data=data, files=files
            )

        resp = self.session.request(
            method, req_url, headers=headers, params=params, data=data, files=files
        )
        return self._handle_response(resp, retry_callable=retry)

    def close(self):
        self.session.close()


class StatelessRequest(BaseRequest):
    """Lightweight, no persistent session."""

    def __init__(self, rayyan: Rayyan, bearer_token: str = None):
        super().__init__(rayyan, allow_refresh=False)
        self._access_token = bearer_token
        self._refresh_token = None

    def request_handler(
        self,
        path: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        payload: Optional[dict] = None,
        params: Optional[Dict[str, str]] = None,
        files: Optional[list] = None,
        body_type: str = "json",
    ):
        req_url, method, headers, params, data, files = self._prepare_request(
            path, method, headers, payload, params, files, body_type
        )

        def retry():
            return request(
                method, req_url, headers=headers, params=params, data=data, files=files
            )

        resp = request(
            method, req_url, headers=headers, params=params, data=data, files=files
        )
        return self._handle_response(resp, retry_callable=retry)
