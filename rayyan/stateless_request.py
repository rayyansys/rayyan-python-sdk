import json
from typing import Dict, Optional, Union
import requests


class StatelessRequest:
    """
    Stateless HTTP request handler that uses a Bearer token passed at initialization.
    Suitable for ephemeral, multi-user, or serverless environments.
    """

    def __init__(self, base_url: str, bearer_token: str):
        self._base_url = base_url.rstrip("/")
        self._bearer_token = bearer_token

    def request_handler(
        self,
        path: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        payload: Optional[Union[Dict, str]] = None,
        params: Optional[Dict[str, str]] = None,
        body_type: str = "json",
        files: Optional[Dict[str, tuple]] = None,
        timeout: int = 10,
    ) -> Dict[str, Union[int, str, Dict[str, str]]]:
        """
        Generic HTTP request handler.

        Args:
            path: Endpoint path (e.g. "/reviews")
            method: HTTP method (GET, POST, etc.)
            headers: Extra headers to include
            payload: Dict or string payload (used for body)
            params: Query params
            body_type: One of "json", "form", "raw"
            files: For multipart/form-data uploads
            timeout: Request timeout in seconds

        Returns:
            Parsed JSON or structured error dict
        """

        url = f"{self._base_url}{path}"
        headers = headers.copy() if headers else {}
        headers["Authorization"] = f"Bearer {self._bearer_token}"
        headers["Accept"] = "application/json"

        data = None
        json_data = None

        if files:
            # When files are used, requests will automatically handle multipart
            pass
        elif body_type == "json" and isinstance(payload, dict):
            headers["Content-Type"] = "application/json"
            json_data = payload
        elif body_type == "form" and isinstance(payload, dict):
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            data = payload
        elif body_type == "raw" and isinstance(payload, str):
            headers["Content-Type"] = "text/plain"
            data = payload

        try:
            response = requests.request(
                method=method.upper(),
                url=url,
                headers=headers,
                params=params,
                data=data,
                json=json_data,
                files=files,
                timeout=timeout,
            )
        except requests.RequestException as e:
            return {
                "code": 0,
                "message": "Request error",
                "data": str(e),
            }

        content_type = response.headers.get("Content-Type", "")
        try:
            if "application/json" in content_type:
                result = response.json()
            else:
                result = response.text
        except ValueError:
            result = response.text

        if 200 <= response.status_code <= 299:
            return result if isinstance(result, dict) else {"data": result}

        return {
            "code": response.status_code,
            "message": response.reason,
            "data": result,
        }
