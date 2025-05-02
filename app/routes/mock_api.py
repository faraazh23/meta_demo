# app/routes/mock_api.py

from fastapi import APIRouter, HTTPException
from typing import List

from app.config import settings
from app.models import TokenResponse, Insight

router = APIRouter(tags=["mock"])


@router.post("/oauth/access_token", response_model=TokenResponse)
def oauth_token(client_id: str, client_secret: str):
    """
    Mock OAuth2 token endpoint.
    Expects client_id & client_secret as query params.
    """
    if (
        client_id != settings.client_id
        or client_secret != settings.client_secret
    ):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
        )
    return TokenResponse(access_token="mock_token_123", expires_in=3600)


@router.get(
    "/v14.0/{object_id}/insights",
    response_model=List[Insight],
)
def get_insights(
    object_id: str,
    metric: str,
    access_token: str,
):
    """
    Mock insights endpoint.
    Expects:
      - path param: object_id (e.g. page or ad ID)
      - query params: metric, access_token
    """
    if access_token != "mock_token_123":
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )
    return [
        Insight(
            name=metric,
            period="day",
            value=42,
        )
    ]
