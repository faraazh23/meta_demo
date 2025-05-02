Meta Graph Mock Demo

A minimal FastAPI-based demo showcasing:
  • A mock implementation of the Meta (Facebook) Graph API  
  • A simple client that fetches a token and reads “insights”  
  • Production-style patterns: env-based config, Pydantic validation, separate routers, tests, Docker, CI

What’s in this README
1. Project Overview
2. Project Structure
3. Prerequisites
4. Setup & Installation
5. Running the Server
6. API Usage Examples
7. Testing
8. Docker
9. CI/CD
10. Next Steps
11. Contributing

---

1. Project Overview
   This repo provides:
     • /oauth/access_token (mock OAuth2 token endpoint)
     • /v14.0/{object_id}/insights (mock insights)
     • /client/insights/{object_id} (client that chains those two calls)

2. Project Structure
   meta_demo/
   ├── Dockerfile
   ├── requirements.txt
   ├── .env.example
   ├── README.txt
   ├── app/
   │   ├── main.py
   │   ├── config.py
   │   ├── models.py
   │   ├── routes/
   │   │   ├── mock_api.py
   │   │   └── client.py
   │   └── tests/
   │       ├── test_mock.py
   │       └── test_client.py
   └── .github/
       └── workflows/
           └── ci.yml

3. Prerequisites
   • Python 3.10+  
   • virtualenv or built-in venv  
   • Docker (optional)  
   • GitHub account (for CI)

4. Setup & Installation
   ```bash
   git clone <repo-url> meta_demo
   cd meta_demo

   # Copy .env template
   cp .env.example .env        # Unix
   # or
   copy .env.example .env      # Windows CMD

   # Create venv & install
   python3 -m venv venv
   source venv/bin/activate    # Windows: venv\Scripts\activate
   pip install --upgrade pip
   pip install -r requirements.txt