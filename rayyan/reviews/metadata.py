from typing import Any, Dict, Optional
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

    def create_stage(self, review_id: int, name: str, phase: str, type_: str) -> Dict[str, Any]:
        """Create a new stage in a review.

        Args:
            review_id (int): ID of the review.
            name (str): Name of the stage.
            phase (str): Phase of the stage (e.g., "screening", "extraction").
            type_ (str): Type of the stage (e.g., "included", "maybe").

        Returns:
            dict: Stage creation response.
        """
        payload = {
            "stage": {
                "name": name,
                "phase": phase,
                "type": type_
            }
        }
        return self._request("POST", f"{REVIEWS_ROUTE}/{review_id}/stages", payload=payload)

    def import_articles_to_stage(
        self, review_id: int, stage_id: int, extra: Optional[dict] = None
    ) -> Dict[str, Any]:
        """Import articles into a specific stage of a review.

        Args:
            review_id (int): ID of the review.
            stage_id (int): ID of the stage.
            extra (dict, optional): Import options. Can include:
                - {"mode": "included"} or {"mode": "maybe"}
                - {"user_labels": ["label_1", ...]}
        Returns:
            dict: Import response.
        """
        if extra is None:
            extra = {}  # default fallback

        return self._request(
            "POST",
            f"{REVIEWS_ROUTE}/{review_id}/stages/{stage_id}/import",
            payload={"extra": extra}
        )
