from typing import Any, Dict, Optional
from rayyan.paths import REVIEWS_ROUTE


class ReviewArticles:
    def copy(self, id: int, review: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", f"{REVIEWS_ROUTE}/{id}/copy", payload={"review": review})

    def results(self, id: int, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        params = params or {}
        return self._request("GET", f"{REVIEWS_ROUTE}/{id}/results", params=params)

    def list_articles_with_fulltext(self, review_id: int) -> Dict[str, Any]:
        return self.results(id=review_id, params={"extra[fulltext_types][]": "pr"})

    def get_fulltext_link(self, id: int) -> Dict[str, Any]:
        # NOTE: moved to fulltext module, but keep as convenience wrapper
        from rayyan.paths import FULLTEXT_ROUTE

        return self._request("GET", f"{FULLTEXT_ROUTE}/{id}")

    def articles(self, id: int, start: Optional[int] = None, length: Optional[int] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if start is not None:
            params["start"] = start
        if length is not None:
            params["length"] = length
        return self._request("GET", f"{REVIEWS_ROUTE}/{id}/articles", params=params)

    def facets(self, id: int, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        params = params or {}
        return self._request("GET", f"{REVIEWS_ROUTE}/{id}/facets", params=params)

    def inclusion_counts(self, id: int, user_id: int = 0) -> Dict[str, Any]:
        return self._request("GET", f"{REVIEWS_ROUTE}/{id}/inclusion_counts", params={"user_id": user_id})
