import json
from typing import Any, Dict, List, Optional, Union
from rayyan.paths import REVIEWS_ROUTE

# Customization keys for exclusion reasons are namespaced with this prefix.
EXCLUSION_REASON_PREFIX = "__EXR__"

# Value used to remove a customization (label/reason) from an article.
REMOVE_VALUE = -1

# Template for a stage-level customization "scope", built from a stage ID.
STAGE_SCOPE_TEMPLATE = "__SYSTEM__STAGE__{stage_id}"


def stage_scope(stage_id: Any) -> str:
    """Build a stage-level customization scope from its stage ID."""
    return STAGE_SCOPE_TEMPLATE.format(stage_id=stage_id)


def stage_question_answer_key(stage_id: Any, question_id: Any) -> str:
    """Build a data-extraction question's answer_key (scope) from its IDs."""
    return f"{stage_scope(stage_id)}__QUESTION__{question_id}"


class ReviewCustomizations:
    def customize(
        self,
        id: int,
        article_id: int,
        plan: Dict[str, Any],
        scope: Optional[str] = None,
        allow_string_value: Optional[bool] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"article_id": article_id, "plan": plan}
        if scope is not None:
            payload["scope"] = scope
        if allow_string_value is not None:
            payload["allow_string_value"] = allow_string_value
        return self._request(
            "POST",
            f"{REVIEWS_ROUTE}/{id}/customize",
            payload=payload,
        )

    def answer_question(
        self,
        id: int,
        article_id: int,
        stage_id: Any,
        question_id: Any,
        answer: Union[str, Dict[str, Any], List[Union[str, Dict[str, Any]]]],
        key: str = "included",
        allow_string_value: bool = True,
    ) -> Dict[str, Any]:
        """Answer a data-extraction question for a single article.

        The question is identified by its ``stage_id`` and ``question_id``, from
        which the customization ``scope`` (the question's answer_key) is built.
        ``answer`` is the value (or list of values) to record; it is encoded into
        the ``plan`` payload the API expects, i.e.
        ``{key: '[{"text": <value>}, ...]'}``.

        An answer may also be a dict answer item (e.g. ``{"text": ..., "source_excerpt":
        ..., "pages": [...]}``) to store the supporting evidence with the text; dicts are
        sent as given. This replaces the question's existing answers for the article.
        """
        answers = answer if isinstance(answer, (list, tuple)) else [answer]
        items = [{"text": a} if isinstance(a, str) else dict(a) for a in answers]
        plan = {key: json.dumps(items)}
        return self.customize(
            id=id,
            article_id=article_id,
            plan=plan,
            scope=stage_question_answer_key(stage_id, question_id),
            allow_string_value=allow_string_value,
        )

    def bulk_customizations(
        self,
        id: int,
        key: str,
        value: int,
        article_ids: Union[str, List[Any]],
        stage_id: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """Apply a customization (e.g. a screening decision) to many articles at once.

        ``article_ids`` may be a list/tuple of IDs or an already comma-separated
        string; it is normalized to the comma-separated string the API expects.
        For screening decisions, ``key`` is typically ``"included"`` and ``value``
        is ``1`` (include), ``0`` (maybe) or ``-1`` (exclude).

        When ``stage_id`` is given, the customization is scoped to that stage (so
        the decision is recorded for the stage rather than at the review level).

        The parameters are sent in the JSON request body, so the number of
        article IDs is not limited by the URL length.
        """
        if isinstance(article_ids, (list, tuple)):
            article_ids = ", ".join(str(article_id) for article_id in article_ids)
        payload: Dict[str, Any] = {"key": key, "value": value, "article_ids": article_ids}
        if stage_id is not None:
            payload["scope"] = stage_scope(stage_id)
        return self._request("POST", f"{REVIEWS_ROUTE}/{id}/customize", payload=payload)

    def _set_customization(
        self,
        id: int,
        article_ids: Union[str, List[Any]],
        key: str,
        value: int,
    ) -> Dict[str, Any]:
        """Add or remove a keyed customization (label/reason) on articles.

        Both directions use the bulk endpoint (``{article_ids, key, value}``) in a
        single request: the API deletes the customization when ``value`` is
        ``REMOVE_VALUE`` (-1) and inserts it otherwise.
        """
        return self.bulk_customizations(
            id=id,
            key=key,
            value=value,
            article_ids=article_ids,
        )

    def set_label(
        self,
        id: int,
        article_ids: Union[str, List[Any]],
        label: str,
        value: int = 1,
    ) -> Dict[str, Any]:
        """Add or remove a label on one or more articles.

        ``label`` is the label name, used as the customization ``key``. ``value``
        is ``1`` to add the label and ``-1`` to remove it. ``article_ids`` may be
        a list/tuple of IDs or an already comma-separated string.
        """
        return self._set_customization(
            id=id,
            article_ids=article_ids,
            key=label,
            value=value,
        )

    def set_reason(
        self,
        id: int,
        article_ids: Union[str, List[Any]],
        reason: str,
        value: int = 1,
    ) -> Dict[str, Any]:
        """Add or remove an exclusion reason on one or more articles.

        ``reason`` is the reason text; it is namespaced with
        ``EXCLUSION_REASON_PREFIX`` to form the customization ``key``. ``value``
        is ``1`` to add the reason and ``-1`` to remove it. ``article_ids`` may be
        a list/tuple of IDs or an already comma-separated string.
        """
        return self._set_customization(
            id=id,
            article_ids=article_ids,
            key=f"{EXCLUSION_REASON_PREFIX}{reason}",
            value=value,
        )

    def get_customizations(self, id: int, params: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("GET", f"{REVIEWS_ROUTE}/{id}/customizations", params=params)
