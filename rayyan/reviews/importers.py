from typing import Any, Dict
from rayyan.paths import MYLIBRARY_ROUTE


class ReviewImporters:
    def import_from_mylibrary_to_review(self, review_id: int, file: Dict[str, Any]) -> Dict[str, Any]:
        return self._request(
            "POST", MYLIBRARY_ROUTE, payload={"review_id": review_id, "file": file}
        )

    def import_pdf_to_review_article(
        self, review_id: int, article_id: int, file: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Import a specific PDF from My Library into a review article.

        Args:
            review_id (int): ID of the review.
            article_id (int): ID of the article within the review to attach the PDF to.
            file (dict): File metadata with PDF info, e.g.:
                {
                    "key": "example.pdf",
                    "size": 204800,
                    "metadata": {
                        "metadata_signature": "bea0cb45...",
                        "titles": ["Example Study Title"],
                        "type": "pdf"
                    }
                }

        Returns:
            dict: API response confirming successful import or containing errors.
        """
        payload = {
            "review_id": review_id,
            "article_id": article_id,
            "file": file
        }

        return self._request("POST", f"{MYLIBRARY_ROUTE}", payload=payload)
