from typing import Any, Dict, Optional
from rayyan.types import RayyanProtocol as Rayyan
from rayyan.paths import REVIEWS_ROUTE


class ReviewBase:
    """Base class providing a thin wrapper around the Rayyan request handler.

    This is intended to be mixed into other classes that implement feature
    groups (samples, questions, results, etc.).
    """

    def __init__(self, rayyan: Rayyan):
        self._rayyan = rayyan

    def _request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        return self._rayyan.request.request_handler(method=method, path=path, **kwargs)

    # basic review-level methods
    def get_all(self) -> Dict[str, Any]:
        return self._request("GET", REVIEWS_ROUTE)

    def get(self, id: int) -> Dict[str, Any]:
        return self._request("GET", f"{REVIEWS_ROUTE}/{id}")

    def create(self, review: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", REVIEWS_ROUTE, payload={"review": review})
