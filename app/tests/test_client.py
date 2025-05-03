# app/tests/test_client.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_client_insights_happy_path(monkeypatch):
    """
    Monkeypatch the mock API endpoints so we can simulate responses
    and isolate the client logic.
    """

    # 1) Patch the OAuth endpoint to return a custom token payload
    async def fake_oauth(url, params=None, **kwargs):
        class FakeResp:
            status_code = 200

            def json(self):
                return {"access_token": "patched_token", "expires_in": 1234}

            def raise_for_status(self):
                pass

        return FakeResp()

    # 2) Patch the insights endpoint to return a custom insight
    async def fake_insights(url, params=None, **kwargs):
        class FakeResp:
            status_code = 200

            def json(self):
                return [
                    {
                        "name": params["metric"],
                        "period": "hour",
                        "value": 7,
                    }
                ]

            def raise_for_status(self):
                pass

        return FakeResp()

    # Apply the monkeypatch to httpx.AsyncClient methods
    import httpx

    monkeypatch.setattr(
        httpx.AsyncClient,
        "post",
        fake_oauth,
    )
    monkeypatch.setattr(
        httpx.AsyncClient,
        "get",
        fake_insights,
    )

    # 3) Call the client endpoint
    resp = client.get(
        "/client/insights/xyz?metric=test_metric"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert data[0]["name"] == "test_metric"
    assert data[0]["period"] == "hour"
    assert data[0]["value"] == 7


def test_client_insights_auth_fail(monkeypatch):
    """
    Simulate the token fetch failing (non-200), so client returns 502.
    """

    async def bad_oauth(url, params=None, **kwargs):
        import httpx

        class FakeResp:
            status_code = 400

            def raise_for_status(self):
                raise httpx.HTTPStatusError(
                    "err", request=None, response=None
                )

        return FakeResp()

    import httpx

    monkeypatch.setattr(
        httpx.AsyncClient,
        "post",
        bad_oauth,
    )

    resp = client.get("/client/insights/123?metric=foo")
    assert resp.status_code == 502
    assert resp.json()["detail"] == "Auth service error"
