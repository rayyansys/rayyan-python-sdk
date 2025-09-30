from typing import Any, Dict, List
from rayyan.paths import REVIEWS_ROUTE


class ReviewQuestions:
    def create_question(self, review_id: int, stage_id: int, question: Dict[str, Any]) -> Dict[str, Any]:
        return self._request(
            "POST",
            f"{REVIEWS_ROUTE}/{review_id}/stages/{stage_id}/questions",
            payload={"question": question},
        )

    def list_questions(self, review_id: int, stage_id: int) -> Dict[str, Any]:
        return self._request("GET", f"{REVIEWS_ROUTE}/{review_id}/stages/{stage_id}/questions")

    def get_question(self, review_id: int, stage_id: int, question_id: int) -> Dict[str, Any]:
        return self._request(
            "GET",
            f"{REVIEWS_ROUTE}/{review_id}/stages/{stage_id}/questions/{question_id}",
        )

    def update_question(self, review_id: int, stage_id: int, question_id: int, question: Dict[str, Any]) -> Dict[str, Any]:
        return self._request(
            "PUT",
            f"{REVIEWS_ROUTE}/{review_id}/stages/{stage_id}/questions/{question_id}",
            payload={"question": question},
        )

    def delete_question(self, review_id: int, stage_id: int, question_id: int) -> Dict[str, Any]:
        return self._request(
            "DELETE",
            f"{REVIEWS_ROUTE}/{review_id}/stages/{stage_id}/questions/{question_id}",
        )
