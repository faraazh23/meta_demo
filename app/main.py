from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routes.mock_api import router as mock_router
from app.routes.client import router as client_router

# 1) Create the FastAPI “app” instance
app = FastAPI(title="Meta Graph Mock Demo")

# 2) allow your browser or frontend to call these endpoints
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3) Include your routers
app.include_router(mock_router, prefix="", tags=["mock"])
app.include_router(client_router, prefix="", tags=["client"])
