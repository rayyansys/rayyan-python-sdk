from typing import TYPE_CHECKING, Dict, Any, List, Literal, Optional, TypedDict
import json

from .paths import REVIEWS_ROUTE


if TYPE_CHECKING:
    from rayyan.rayyan import Rayyan
else:
    Rayyan = None





class ExportFilters(TypedDict, total=False):
    author_format: Literal["lf", "fl"]
    include_abstracts: int
    include_decisions: int
    include_labels: int
    include_exclusion_reasons: int
    include_user_notes: int
    include_fulltexts: int
    include_questions: int
    article_ids: List[int]
    mode: str
    searches: List[int]
    highlights_1: List[str]
    highlights_2: List[str]
    language: List[str]
    keyphrases: List[str]
    locations: List[str]
    journal: List[str]
    authors: List[str]
    year: List[int]
    publication_types: List[str]
    user_labels: List[str]
    exclusion_labels: List[str]
    abstract_languages: List[str]
    fulltext_types: List[str]
    customized_by: List[str]
    decision_at_least: int
    decision_at_most: int
    dedup_result: int
    dedup_job_id: int
    dedup_result_cluster_id: int
    exact_matches: int
    pico_participants: List[str]
    pico_intervention: List[str]
    pico_control: List[str]
    pico_outcome: List[str]
    stages: List[str]


def build_query(filters: dict) -> list[tuple[str, str]]:
    query = []
    for key, value in filters.items():
        if isinstance(value, list):
            for v in value:
                query.append((f"{key}[]", str(v)))
        else:
            query.append((key, str(value)))
    return query


class Review:
    def __init__(self, rayyan: Rayyan):
        self.__rayyan__ = rayyan

    def get_all(self) -> Dict[str, str]:
        return self.__rayyan__.request.request_handler(method="GET", path=REVIEWS_ROUTE)

    def get(self, id: int) -> Dict[str, str]:
        return self.__rayyan__.request.request_handler(
            method="GET", path=f"{REVIEWS_ROUTE}/{id}"
        )

    def create(
        self,
        review={
            "title": str,
            "description": str,
            "metadata_attributes": {
                "research_question": str,
                "research_question_type": str,
                "research_field": str,
                "review_type": str,
                "review_domain": str,
            },
            "team_id": int,
        },
    ) -> Dict[str, str]:
        return self.__rayyan__.request.request_handler(
            method="POST",
            path=REVIEWS_ROUTE,
            payload={"review": review},
        )

    def export(
        self,
        review_id: int,
        export_format: Literal["csv", "ris", "bib", "enw"],
        filters: Optional[ExportFilters] = None
    ) -> Dict[str, Any]:
        """
        Export a review in one of the allowed formats: csv, ris, bib, enw.

        Args:
            review_id: The ID of the review to export.
            export_format: Must be one of "csv", "ris", "bib", "enw".
            filters: Optional dict of filters and flags for export.

        Returns:
            API response as dict.
        """

        # Default include_* values
        params: Dict[str, Any] = {
            "include_abstracts": 1,
            "include_decisions": 1,
            "include_labels": 1,
            "include_exclusion_reasons": 1,
            "include_user_notes": 1,
        }

        if filters:
            for key, value in filters.items():
                if isinstance(value, list):
                    params[key] = json.dumps(value)
                else:
                    params[key] = value

        params = build_query(params)
        return self.__rayyan__.request.request_handler(
            method="GET",
            path=f"{REVIEWS_ROUTE}/{review_id}/export.{export_format}",
            params=params,
        )



    def copy(
        self,
        id: int,
        review: Dict[str, int] = {
            "target_review": int,
            "start": int,
            "length": int,
            "order[0][column]": int,
            "order[0][dir]": str,
            "search[value]": None,
            "extra": {
                "article_ids": list,
                "mode": str,
                "searches": list,
                "highlights_1": list,
                "highlights_2": list,
                "language": list,
                "keyphrases": list,
                "locations": list,
                "journal": list,
                "authors": list,
                "year": list,
                "publication_types": list,
                "user_labels": list,
                "exclusion_labels": list,
                "abstract_languages": list,
                "fulltext_types": list,
                "customized_by": list,
                "decision_at_least": list,
                "decision_at_most": list,
                "dedup_result": list,
                "dedup_job_id": list,
                "dedup_result_cluster_id": list,
                "exact_matches": list,
                "pico_participants": list,
                "pico_intervention": list,
                "pico_control": list,
                "pico_outcome": list,
            },
        },
    ) -> Dict[str, str]:
        return self.__rayyan__.request.request_handler(
            method="POST",
            path=f"{REVIEWS_ROUTE}/{id}/copy",
            payload={"review": review},
        )

    def results(
        self,
        id: int,
        params: Dict[str, int] = {
            "start": int,
            "length": int,
            "order[0][column]": int,
            "order[0][dir]": str,
            "search[value]": str,
            "extra[article_ids][]": int,
            "extra[mode]": str,
            "extra[searches][]": int,
            "extra[highlights_1][]": str,
            "extra[highlights_2][]": str,
            "extra[language][]": str,
            "extra[keyphrases][]": str,
            "extra[locations][]": str,
            "extra[journal][]": int,
            "extra[authors][]": int,
            "extra[year][]": int,
            "extra[publication_types][]": str,
            "extra[user_labels][]": str,
            "extra[exclusion_labels][]": str,
            "extra[abstract_languages][]": str,
            "extra[fulltext_types][]": str,
            "extra[customized_by]": int,
            "extra[decision_at_least]": int,
            "extra[decision_at_most]": int,
            "extra[dedup_result]": int,
            "extra[dedup_job_id]": int,
            "extra[dedup_result_cluster_id]": int,
            "extra[exact_matches]": int,
            "extra[pico_participants][]": str,
            "extra[pico_intervention][]": str,
            "extra[pico_control][]": str,
            "extra[pico_outcome][]": str,
        },
    ) -> Dict[str, str]:
        return self.__rayyan__.request.request_handler(
            method="GET", path=f"{REVIEWS_ROUTE}/{id}/results", params=params
        )

    def customize(
        self,
        id: int,
        article_id: int,
        plan: dict,
    ) -> Dict[str, str]:
        return self.__rayyan__.request.request_handler(
            method="POST",
            path=f"{REVIEWS_ROUTE}/{id}/customize",
            payload={
                "article_id": article_id,
                "plan": plan,
            },
        )

    def articles(
        self, id: int, start: int = None, length: int = None
    ) -> Dict[str, str]:
        params = {}
        if start:
            params["start"] = start
        if length:
            params["length"] = length

        return self.__rayyan__.request.request_handler(
            method="GET", path=f"{REVIEWS_ROUTE}/{id}/articles", params=params
        )

    def bulk_customizations(
        self,
        id: int,
        key: str,
        value: int,
        article_ids: str,
    ) -> Dict[str, str]:
        params = {
            "key": key,
            "value": value,
            "article_ids": article_ids,
        }
        return self.__rayyan__.request.request_handler(
            method="POST",
            params=params,
            path=f"{REVIEWS_ROUTE}/{id}/customize",
        )

    def get_customizations(
        self,
        id: int,
        params: Dict[str, int] = {
            "start_id": int,
            "end_id": int,
            "types[]": list,
        },
    ) -> Dict[str, str]:
        return self.__rayyan__.request.request_handler(
            method="GET",
            params=params,
            path=f"{REVIEWS_ROUTE}/{id}/customizations",
        )

    def facets(
        self,
        id: int,
        params: Dict[str, int] = {
            "facets[inclusion_counts]": "1",
            "facets[decision_counts]": "1",
            "facets[user_labels]": "1",
            "facets[exclusion_labels]": "1",
            "facets[searches]": "1",
            "facets[exact_matches]": "1",
            "facets[dedup_result]": "1",
            "facets[highlights]": "1",
            "facets[locations]": "1",
            "facets[abstract_languages]": "1",
            "facets[language]": "1",
            "facets[journal]": "1",
            "facets[authors]": "1",
            "facets[year]": "1",
            "facets[publication_types]": "1",
            "facets[keyphrases]": "1",
            "facets[fulltext_types]": "1",
            "facets[pico_control]": "1",
            "facets[pico_intervention]": "1",
            "facets[pico_outcome]": "1",
            "facets[pico_participants]": "1",
        },
    ) -> Dict[str, str]:
        return self.__rayyan__.request.request_handler(
            method="GET",
            params=params,
            path=f"{REVIEWS_ROUTE}/{id}/facets",
        )

    def inclusion_counts(
        self,
        id: int,
        user_id: int = 0,
    ) -> Dict[str, str]:
        return self.__rayyan__.request.request_handler(
            method="GET",
            params={"user_id": user_id},
            path=f"{REVIEWS_ROUTE}/{id}/inclusion_counts",
        )

    def calculate_ratings(
        self,
        id: int,
    ) -> Dict[str, str]:
        return self.__rayyan__.request.request_handler(
            method="POST",
            path=f"{REVIEWS_ROUTE}/{id}/calculate_ratings",
        )

    def archive(
        self,
        id: int,
    ) -> Dict[str, str]:
        return self.__rayyan__.request.request_handler(
            method="POST",
            path=f"{REVIEWS_ROUTE}/{id}/archive",
        )

    def unarchive(
        self,
        id: int,
    ) -> Dict[str, str]:
        return self.__rayyan__.request.request_handler(
            method="POST",
            path=f"{REVIEWS_ROUTE}/{id}/unarchive",
        )

    def blind(
        self,
        id: int,
    ) -> Dict[str, str]:
        return self.__rayyan__.request.request_handler(
            method="POST", path=f"{REVIEWS_ROUTE}/{id}/blind"
        )
