from fastapi import APIRouter
from app.api.v1.endpoints import warriors, challenges, participations, stats

api_router = APIRouter()

api_router.include_router(warriors.router, prefix="/warriors", tags=["warriors"])
api_router.include_router(challenges.router, prefix="/challenges", tags=["challenges"])
api_router.include_router(participations.router, prefix="/participations", tags=["participations"])
api_router.include_router(stats.router, prefix="/stats", tags=["stats"])