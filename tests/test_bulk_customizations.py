"""bulk_customizations sends its parameters in the JSON body, not the URL (1.0rc19)."""
from urllib.parse import urlsplit

from conftest import BASE, body
from rayyan.reviews import Review

CUSTOMIZE = f"{BASE}/api/v1/reviews/7/customize"


def test_large_id_list_goes_in_body_not_url(client, mocked):
    mocked.post(CUSTOMIZE, json={"customization_ids": []})
    ids = list(range(1, 5001))
    Review(client).bulk_customizations(7, "included", -1, ids)
    call = mocked.calls[0]
    assert call.request.method == "POST"
    assert urlsplit(call.request.url).query == ""
    assert body(call) == {"key": "included", "value": -1, "article_ids": ", ".join(map(str, ids))}


def test_stage_scope_in_body(client, mocked):
    mocked.post(CUSTOMIZE, json={})
    Review(client).bulk_customizations(7, "included", 1, [42], stage_id=3)
    assert body(mocked.calls[0]) == {"key": "included", "value": 1, "article_ids": "42", "scope": "__SYSTEM__STAGE__3"}


def test_string_ids_passed_through(client, mocked):
    mocked.post(CUSTOMIZE, json={})
    Review(client).bulk_customizations(7, "GT", 1, "1,2,3")
    assert body(mocked.calls[0]) == {"key": "GT", "value": 1, "article_ids": "1,2,3"}


def test_returns_api_response(client, mocked):
    mocked.post(CUSTOMIZE, json={"customization_ids": [10, 11], "missed_etags": {}, "new_etags": {}})
    assert Review(client).bulk_customizations(7, "included", 1, [1, 2]) == {
        "customization_ids": [10, 11], "missed_etags": {}, "new_etags": {}}


# --- answer_question -----------------------------------------------------------------

ANSWER_SCOPE = "__SYSTEM__STAGE__3__QUESTION__9"


def _answer_call(client, mocked, answer):
    import json
    mocked.post(CUSTOMIZE, json={})
    Review(client).answer_question(7, 42, 3, 9, answer)
    sent = body(mocked.calls[0])
    assert sent["article_id"] == 42 and sent["scope"] == ANSWER_SCOPE and sent["allow_string_value"] is True
    return json.loads(sent["plan"]["included"])


def test_answer_string_unchanged_from_rc18(client, mocked):
    assert _answer_call(client, mocked, "PD") == [{"text": "PD"}]


def test_answer_list_of_strings_unchanged_from_rc18(client, mocked):
    assert _answer_call(client, mocked, ["a", "b"]) == [{"text": "a"}, {"text": "b"}]


def test_answer_item_with_evidence(client, mocked):
    item = {"text": "RCT", "source_excerpt": "a randomised trial", "pages": [2, 3]}
    assert _answer_call(client, mocked, item) == [item]


def test_answer_mixed_list(client, mocked):
    item = {"id": "x1", "text": "n=42", "pages": [4]}
    assert _answer_call(client, mocked, ["USA", item]) == [{"text": "USA"}, item]


# --- label / reason removal (1.0rc19) ------------------------------------------------

def test_label_removal_is_one_bulk_request(client, mocked):
    mocked.post(CUSTOMIZE, json={"customization_ids": []})
    ids = list(range(1, 5001))
    Review(client).set_label(7, ids, "Pilot", -1)
    assert len(mocked.calls) == 1
    assert body(mocked.calls[0]) == {"key": "Pilot", "value": -1, "article_ids": ", ".join(map(str, ids))}


def test_reason_removal_is_one_bulk_request(client, mocked):
    mocked.post(CUSTOMIZE, json={"customization_ids": []})
    Review(client).set_reason(7, [1, 2], "wrong population", -1)
    assert len(mocked.calls) == 1
    assert body(mocked.calls[0]) == {"key": "__EXR__wrong population", "value": -1, "article_ids": "1, 2"}


# --- results (1.0rc19) ---------------------------------------------------------------

def test_results_uses_search_with_form_body(client, mocked):
    from urllib.parse import parse_qs
    mocked.add("SEARCH", f"{BASE}/api/v1/reviews/7/results", json={"data": []})
    ids = list(range(1, 3001))
    Review(client).results(7, {"start": 0, "length": 25, "extra[article_ids][]": ids})
    req = mocked.calls[0].request
    assert req.method == "SEARCH"
    assert urlsplit(req.url).query == ""
    assert req.headers["Content-Type"] == "application/x-www-form-urlencoded"
    form = parse_qs(req.body)
    assert form["start"] == ["0"] and form["length"] == ["25"]
    assert form["extra[article_ids][]"] == [str(i) for i in ids]
