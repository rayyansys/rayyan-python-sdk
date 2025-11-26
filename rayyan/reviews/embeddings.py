from typing import Any, Dict
from rayyan.paths import REVIEWS_ROUTE


class ReviewEmbeddings:
    def get_embedding_token(self, review_id: int) -> Dict[str, Any]:
        """
        Retrieve the embedding token for a review.
        """
        return self._request("GET", f"{REVIEWS_ROUTE}/{review_id}/embeddings")
