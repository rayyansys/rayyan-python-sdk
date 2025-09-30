from typing import Any, Dict
from rayyan.paths import MYLIBRARY_ROUTE


class ReviewImporters:
    def import_from_mylibrary_to_review(self, review_id: int, file: Dict[str, Any]) -> Dict[str, Any]:
        return self._request(
            "POST", MYLIBRARY_ROUTE, payload={"review_id": review_id, "file": file}
        )