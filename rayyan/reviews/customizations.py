from typing import Any, Dict
from rayyan.paths import REVIEWS_ROUTE


class ReviewCustomizations:
    def customize(self, id: int, article_id: int, plan: Dict[str, Any]) -> Dict[str, Any]:
        return self._request(
            "POST",
            f"{REVIEWS_ROUTE}/{id}/customize",
            payload={"article_id": article_id, "plan": plan},
        )

    def bulk_customizations(self, id: int, key: str, value: int, article_ids: str) -> Dict[str, Any]:
        params = {"key": key, "value": value, "article_ids": article_ids}
        return self._request("POST", f"{REVIEWS_ROUTE}/{id}/customize", params=params)

    def get_customizations(self, id: int, params: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("GET", f"{REVIEWS_ROUTE}/{id}/customizations", params=params)