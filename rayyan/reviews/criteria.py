from typing import Any, Dict
from rayyan.paths import REVIEWS_ROUTE


class ReviewCriteria:
    def create_criterion(self, review_id: int, criterion: Dict[str, Any]) -> Dict[str, Any]:
        return self._request(
            "POST", f"{REVIEWS_ROUTE}/{review_id}/criteria", payload={"criterion": criterion}
        )

    def list_criteria(self, review_id: int) -> Dict[str, Any]:
        return self._request("GET", f"{REVIEWS_ROUTE}/{review_id}/criteria")

    def update_criterion(self, review_id: int, criterion_id: int, criterion: Dict[str, Any]) -> Dict[str, Any]:
        return self._request(
            "PUT",
            f"{REVIEWS_ROUTE}/{review_id}/criteria/{criterion_id}",
            payload={"criterion": criterion},
        )

    def delete_criterion(self, review_id: int, criterion_id: int) -> Dict[str, Any]:
        return self._request("DELETE", f"{REVIEWS_ROUTE}/{review_id}/criteria/{criterion_id}")
