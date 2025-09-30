from typing import Dict, Any, List, Literal, TypedDict
import json

class ExportFilters(TypedDict, total=False):
    author_format: Literal["lf", "fl"]
    include_abstracts: int
    include_decisions: int
    include_labels: int
    include_exclusion_reasons: int
    include_user_notes: int
    include_fulltexts: int
    include_questions: int
    all_decisions: int
    all_labels: int
    all_notes: int
    include_fields: List[str]


def build_query(filters: Dict[str, Any]) -> List[tuple[str, str]]:
    """Convert a dict of parameters into a list of (key, value) query tuples.

    Lists are expanded into repeated `key[]` entries and non-list values are
    stringified.
    """
    query: List[tuple[str, str]] = []
    for key, value in filters.items():
        if isinstance(value, list):
            for v in value:
                query.append((f"{key}[]", str(v)))
        else:
            # JSON-encode non-primitive lists/dicts to keep parameter intent
            if isinstance(value, (dict, list)):
                query.append((key, json.dumps(value)))
            else:
                query.append((key, str(value)))
    return query
