from typing import Any, Dict
from rayyan.paths import FULLTEXT_ROUTE


class ReviewFulltext:
    def get_fulltext_link(self, id: int) -> Dict[str, Any]:
        return self._request("GET", f"{FULLTEXT_ROUTE}/{id}")