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
