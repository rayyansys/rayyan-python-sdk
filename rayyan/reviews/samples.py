from typing import Any, Dict, List, Optional
from rayyan.paths import REVIEWS_ROUTE


class ReviewSamples:
    def create_samples(
        self,
        review_id: int,
        samples: List[Dict[str, Any]],
        sort_key: str = "id",
        sort_dir: str = "asc",
        extra: Optional[Dict[str, Any]] = None,
        search: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        payload = {"samples": samples, "sort_key": sort_key, "sort_dir": sort_dir}
        if extra:
            payload["extra"] = extra
        if search:
            payload["search"] = search
        return self._request("POST", f"{REVIEWS_ROUTE}/{review_id}/samples", payload=payload)

    def update_sample(self, review_id: int, sample_id: int, sample: Dict[str, Any]) -> Dict[str, Any]:
        return self._request(
            "PUT", f"{REVIEWS_ROUTE}/{review_id}/samples/{sample_id}", payload={"sample": sample}
        )

    def delete_sample(self, review_id: int, sample_id: int) -> Dict[str, Any]:
        return self._request("DELETE", f"{REVIEWS_ROUTE}/{review_id}/samples/{sample_id}")

    def list_samples(self, review_id: int) -> Dict[str, Any]:
        return self._request("GET", f"{REVIEWS_ROUTE}/{review_id}/samples")
