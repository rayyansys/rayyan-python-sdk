"""Behaviour added or changed in 1.0rc18. Existing callers must send the same requests as rc17."""
from urllib.parse import urlsplit

import pytest
import requests

from conftest import BASE, body
from rayyan.errors import ReviewNotLiveError
from rayyan.mylib import MyLib
from rayyan.review_access import ReviewAccess
from rayyan.reviews import Review

REVIEW = f"{BASE}/api/v1/reviews/7"


# --- create_ai_screener ----------------------------------------------------------

def test_ai_screener_without_model_sends_rc17_body(client, mocked):
    mocked.post(f"{REVIEW}/ai_screeners", json={})
    Review(client).create_ai_screener(7, {"mode": "undecided"})
    assert body(mocked.calls[0]) == {"extra": {"mode": "undecided"}}


def test_ai_screener_with_model(client, mocked):
    mocked.post(f"{REVIEW}/ai_screeners", json={})
    Review(client).create_ai_screener(7, {}, ai_model_name="gpt-4.1")
    assert body(mocked.calls[0]) == {"extra": {}, "ai_model_name": "gpt-4.1"}


def test_ai_screener_passes_empty_model_name_through(client, mocked):
    mocked.post(f"{REVIEW}/ai_screeners", json={})
    Review(client).create_ai_screener(7, {}, ai_model_name="")
    assert body(mocked.calls[0]) == {"extra": {}, "ai_model_name": ""}


# --- blind / set_blind ------------------------------------------------------------

def test_blind_is_still_a_single_toggle(client, mocked):
    mocked.post(f"{REVIEW}/blind", json={"is_blind": True})
    assert Review(client).blind(7) == {"is_blind": True}
    assert [(c.request.method, c.request.url) for c in mocked.calls] == [("POST", f"{REVIEW}/blind")]


def test_set_blind_does_nothing_when_state_matches(client, mocked):
    mocked.get(REVIEW, json={"is_blind": True})
    assert Review(client).set_blind(7, enabled=True) == {"is_blind": True, "changed": False}
    assert [c.request.method for c in mocked.calls] == ["GET"]


def test_set_blind_toggles_when_state_differs(client, mocked):
    mocked.get(REVIEW, json={"is_blind": True})
    mocked.post(f"{REVIEW}/blind", json={"is_blind": False})
    assert Review(client).set_blind(7, enabled=False) == {"is_blind": False, "changed": True}
    assert [c.request.method for c in mocked.calls] == ["GET", "POST"]


def test_set_blind_twice_only_toggles_once(client, mocked):
    mocked.get(REVIEW, json={"is_blind": True})
    mocked.get(REVIEW, json={"is_blind": False})
    mocked.post(f"{REVIEW}/blind", json={"is_blind": False})
    review = Review(client)
    assert review.set_blind(7, enabled=False)["changed"] is True
    assert review.set_blind(7, enabled=False)["changed"] is False
    assert [c.request.method for c in mocked.calls] == ["GET", "POST", "GET"]


def test_set_blind_on_archived_review_raises_clear_error(client, mocked):
    mocked.get(REVIEW, status=409, json={"error": "review archived"})
    with pytest.raises(ReviewNotLiveError, match="unarchive"):
        Review(client).set_blind(7, enabled=False)
    assert [c.request.method for c in mocked.calls] == ["GET"]


def test_set_blind_reraises_other_http_errors(client, mocked):
    mocked.get(REVIEW, status=500, body="boom")
    with pytest.raises(requests.HTTPError):
        Review(client).set_blind(7, enabled=False)


@pytest.mark.parametrize("value", ["false", "true", 0, 1, None])
def test_set_blind_rejects_non_bool_without_requests(client, mocked, value):
    with pytest.raises(TypeError):
        Review(client).set_blind(7, enabled=value)
    assert len(mocked.calls) == 0


def test_set_blind_after_401_refreshes_and_returns_a_dict(stateful_client, mocked):
    mocked.get(REVIEW, status=401)
    mocked.get(REVIEW, json={"is_blind": False})
    mocked.post(f"{BASE}/oauth/token", json={"access_token": "new", "refresh_token": "refresh2"})
    mocked.post(f"{REVIEW}/blind", json={"is_blind": True})

    assert Review(stateful_client).set_blind(7, enabled=True) == {"is_blind": True, "changed": True}
    retried_get = mocked.calls[2]
    assert retried_get.request.url == REVIEW
    assert retried_get.request.headers["Authorization"] == "Bearer new"


# --- 401 retry (shared by every method) -------------------------------------------

def test_retry_result_is_parsed_like_any_response(stateful_client, mocked):
    mocked.get(REVIEW, status=401)
    mocked.get(REVIEW, json={"id": 7})
    mocked.post(f"{BASE}/oauth/token", json={"access_token": "new", "refresh_token": "refresh2"})
    assert Review(stateful_client).get(7) == {"id": 7}


def test_second_401_raises_instead_of_looping(stateful_client, mocked):
    mocked.get(REVIEW, status=401)
    mocked.post(f"{BASE}/oauth/token", json={"access_token": "new", "refresh_token": "refresh2"})
    with pytest.raises(requests.HTTPError):
        Review(stateful_client).get(7)
    assert [c.request.method for c in mocked.calls] == ["GET", "POST", "GET"]


# --- ReviewAccess.invite ----------------------------------------------------------

@pytest.mark.parametrize("kwargs", [{}, {"user_reason": None}])
def test_invite_without_reason_omits_the_key(client, mocked, kwargs):
    mocked.post(f"{REVIEW}/invite", body="")
    ReviewAccess(client).invite(7, 6, ["a@b.c"], **kwargs)
    assert body(mocked.calls[0]) == {"role_id": 6, "user_emails": ["a@b.c"]}


def test_invite_with_reason_matches_rc17_body(client, mocked):
    mocked.post(f"{REVIEW}/invite", body="")
    ReviewAccess(client).invite(7, 6, ["a@b.c"], user_reason="why")
    assert body(mocked.calls[0]) == {"role_id": 6, "user_emails": ["a@b.c"], "user_reason": "why"}


def test_invite_old_positional_call_still_works(client, mocked):
    mocked.post(f"{BASE}/api/v1/reviews/1/invite", body="")
    assert ReviewAccess(client).invite(1, 6, ["a@b.c"], "why") == ""
    assert body(mocked.calls[0]) == {"role_id": 6, "user_emails": ["a@b.c"], "user_reason": "why"}


def test_invite_passes_empty_reason_through(client, mocked):
    mocked.post(f"{REVIEW}/invite", body="")
    ReviewAccess(client).invite(7, 6, ["a@b.c"], user_reason="")
    assert body(mocked.calls[0])["user_reason"] == ""


# --- MyLib ------------------------------------------------------------------------

@pytest.mark.parametrize("method", ["upload_file", "get_presigned_url"])
def test_mylib_has_no_local_file_upload(method):
    # Removed in 1.0rc18: reading local paths let the hosted MCP server leak its own files.
    assert not hasattr(MyLib, method)


# --- ExportFilters ----------------------------------------------------------------

def test_export_filters_build_the_expected_query(client, mocked):
    mocked.get(f"{REVIEW}/export.csv", json={"status": "OK"})
    result = Review(client).export(7, "csv", {"all_decisions": 1, "include_exclusion_reasons_col": 1})
    assert result == {"status": "OK"}
    assert urlsplit(mocked.calls[0].request.url).query == "all_decisions=1&include_exclusion_reasons_col=1"
