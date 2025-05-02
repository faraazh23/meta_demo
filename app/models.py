# app/models.py

from pydantic import BaseModel


class TokenResponse(BaseModel):
    """
    Response model for the OAuth token endpoint.
    """

    access_token: str
    # how long (in seconds) the token is valid
    expires_in: int


class Insight(BaseModel):
    """
    Single insight record returned by the mock /insights endpoint.
    """

    name: str
    period: str
    value: int
