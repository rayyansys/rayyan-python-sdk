"""Shared fixtures. All HTTP is mocked with `responses`; no network is used."""
import json

import pytest
import responses

from rayyan import Rayyan, StatelessRayyan

BASE = "https://rayyan.test"


@pytest.fixture
def mocked():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        yield rsps


@pytest.fixture
def client():
    return StatelessRayyan(bearer_token="token", url=BASE)


@pytest.fixture
def stateful_client(tmp_path):
    creds = tmp_path / "creds.json"
    creds.write_text(json.dumps({"access_token": "old", "refresh_token": "refresh"}))
    return Rayyan(credentials_file_path=str(creds), url=BASE)


def body(call):
    """Decoded JSON body of a recorded call."""
    return json.loads(call.request.body) if call.request.body else None
