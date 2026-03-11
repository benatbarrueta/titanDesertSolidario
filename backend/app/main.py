import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.api.v1.api import api_router
from app.api.v1.endpoints import health

app = FastAPI(title="Titan Desert Solidario API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://rumbomarruecos2026.es",
        "https://www.rumbomarruecos2026.es",
        "http://localhost:8080",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "dev-secret"),
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(api_router, prefix="/api/v1")
app.include_router(health.router, prefix="/api/v1/health", tags=["health"])