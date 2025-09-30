from typing import Any, Dict
from rayyan.paths import REVIEWS_ROUTE


class ReviewAiScreeners:
    def create_ai_screener(self, review_id: int, extra: Dict[str, Any]) -> Dict[str, Any]:
        return self._request(
            "POST", f"{REVIEWS_ROUTE}/{review_id}/ai_screeners", payload={"extra": extra}
        )