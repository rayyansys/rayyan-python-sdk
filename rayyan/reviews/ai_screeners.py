from typing import Any, Dict, Optional
from rayyan.paths import REVIEWS_ROUTE


class ReviewAiScreeners:
    def create_ai_screener(
        self,
        review_id: int,
        extra: Dict[str, Any],
        ai_model_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Start an AI screener job on a review.

        `ai_model_name` picks the screener model (e.g. "gpt-4.1-mini"); omit it to
        use the default. The accepted names are `LlmBotsLoader::SUPPORTED_MODELS`
        in rayyan-ruby. Rayyan returns 400 if the model is unsupported, or if the
        `ai_screener_model_change` feature is not enabled for the user.
        """
        payload: Dict[str, Any] = {"extra": extra}
        if ai_model_name is not None:
            payload["ai_model_name"] = ai_model_name
        return self._request(
            "POST", f"{REVIEWS_ROUTE}/{review_id}/ai_screeners", payload=payload
        )