from typing import Any, Dict, Optional
from rayyan.reviews.filters import ExportFilters, build_query
from rayyan.paths import REVIEWS_ROUTE


class ReviewExports:
    def export(
        self,
        review_id: int,
        export_format: str,
        filters: Optional[ExportFilters] = None,
    ) -> Dict[str, Any]:
        """Export a review in one of the allowed formats: csv, ris, bib, enw.

        `filters` will be converted to query params using `build_query`.
        """

        params: Dict[str, Any] = {}
        if filters:
            for key, value in filters.items():
                if isinstance(value, list):
                    params[key] = value
                else:
                    params[key] = value

        params_list = build_query(params)

        return self._request(
            "GET",
            f"{REVIEWS_ROUTE}/{review_id}/export.{export_format}",
            params=params_list,
        )
