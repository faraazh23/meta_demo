# app/routes/client.py

from fastapi import APIRouter, HTTPException
import httpx

from app.config import settings
from app.models import TokenResponse, Insight

router = APIRouter(prefix="/client", tags=["client"])


@router.get("/insights/{object_id}", response_model=list[Insight])
async def fetch_insights(object_id: str, metric: str):
    """
    Client endpoint that:
      1) Obtains an access token from /oauth/access_token.
      2) Uses that token to call /v14.0/{object_id}/insights.
    """
    async with httpx.AsyncClient(base_url=settings.api_url) as client:
        # 1) Get token
        try:
            token_resp = await client.post(
                "/oauth/access_token",
                params={
                    "client_id": settings.client_id,
                    "client_secret": settings.client_secret,
                },
            )
            token_resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=502, detail="Auth service error") from exc

        token = TokenResponse(**token_resp.json())

        # 2) Call insights endpoint
        try:
            insights_resp = await client.get(
                f"/v14.0/{object_id}/insights",
                params={
                    "metric": metric,
                    "access_token": token.access_token,
                },
            )
            insights_resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=502, detail="Insights service error"
            ) from exc

        data = insights_resp.json()
        return [Insight(**item) for item in data]
