# app/config.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings, loaded from environment variables
    (e.g. via a .env file at the project root).
    """

    # OAuth client credentials (for the mock API)
    client_id: str
    client_secret: str
    api_url: str = "http://localhost:8000"

    class Config:
        # tell Pydantic to read a file named “.env” in the CWD
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instantiate a single Settings() object for the whole app
settings = Settings()
