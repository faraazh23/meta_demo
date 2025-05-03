# app/tests/conftest.py

import os

# Ensure our mock credentials are available at import time
os.environ.setdefault("CLIENT_ID", "demo")
os.environ.setdefault("CLIENT_SECRET", "secret")
# If you use api_url in Settings, set it too:
os.environ.setdefault("API_URL", "http://localhost:8000")
