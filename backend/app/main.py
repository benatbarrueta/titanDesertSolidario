from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine
from app.api.v1.api import api_router
from app.api.v1.endpoints import health

app = FastAPI(title="Titan Desert Solidario API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://rumbomarruecos.es",
        "https://www.rumbomarruecos.es",
        "http://localhost:3000",
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include API router
app.include_router(api_router, prefix="/api/v1")
app.include_router(health.router, prefix="/api/v1/health", tags=["health"])