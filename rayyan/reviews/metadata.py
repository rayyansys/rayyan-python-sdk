from typing import Any, Dict
from rayyan.paths import REVIEWS_ROUTE


class ReviewMetadata:
    def list_stages(self, review_id: int) -> Dict[str, Any]:
        return self.facets(id=review_id, params={"facets[stages]": "1"})

    def calculate_ratings(self, id: int) -> Dict[str, Any]:
        return self._request("POST", f"{REVIEWS_ROUTE}/{id}/calculate_ratings")

    def archive(self, id: int) -> Dict[str, Any]:
        return self._request("POST", f"{REVIEWS_ROUTE}/{id}/archive")

    def unarchive(self, id: int) -> Dict[str, Any]:
        return self._request("POST", f"{REVIEWS_ROUTE}/{id}/unarchive")

    def blind(self, id: int) -> Dict[str, Any]:
        return self._request("POST", f"{REVIEWS_ROUTE}/{id}/blind")
