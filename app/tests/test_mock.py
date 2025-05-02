# app/tests/test_mock.py

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_oauth_success():
    resp = client.post(
        "/oauth/access_token",
        params={"client_id": "demo", "client_secret": "secret"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert isinstance(data["access_token"], str)
    assert data["expires_in"] == 3600


def test_oauth_invalid_credentials():
    resp = client.post(
        "/oauth/access_token",
        params={"client_id": "bad", "client_secret": "nope"},
    )
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Unauthorized"


def test_insights_success():
    # first get a valid token
    tok = client.post(
        "/oauth/access_token",
        params={"client_id": "demo", "client_secret": "secret"},
    ).json()["access_token"]

    # call insights
    resp = client.get(
        "/v14.0/123/insights",
        params={"metric": "page_impressions", "access_token": tok},
    )
    assert resp.status_code == 200
    data = resp.json()
    # should be a list of one insight
    assert isinstance(data, list)
    assert data[0]["name"] == "page_impressions"
    assert data[0]["period"] == "day"
    assert data[0]["value"] == 42


def test_insights_invalid_token():
    resp = client.get(
        "/v14.0/123/insights",
        params={"metric": "page_impressions", "access_token": "wrong_token"},
    )
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Invalid token"
