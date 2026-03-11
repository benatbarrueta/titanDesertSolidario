from fastapi import APIRouter, Depends
from app.core.admin_auth import require_admin_auth

from app.api.v1.endpoints import (
    warriors,
    challenges,
    participations,
    stats,
    stages,
    admin_auth,
    admin_stages,
    admin_challenges,
    admin_participation,
    admin_challenge_options,
    admin_warriors,
    admin_stage_results,
)

api_router = APIRouter()

# PUBLIC API
api_router.include_router(warriors.router, prefix="/warriors", tags=["warriors"])
api_router.include_router(challenges.router, prefix="/challenges", tags=["challenges"])
api_router.include_router(participations.router, prefix="/participations", tags=["participations"])
api_router.include_router(stats.router, prefix="/stats", tags=["stats"])
api_router.include_router(stages.router, prefix="/stages", tags=["stages"])

# ADMIN AUTH (sin protección)
api_router.include_router(admin_auth.router, prefix="/admin/auth", tags=["admin-auth"])

# ADMIN API (protegida dentro de cada router)
api_router.include_router(admin_stages.router, prefix="/admin/stages", tags=["admin-stages"], dependencies=[Depends(require_admin_auth)])
api_router.include_router(admin_challenges.router, prefix="/admin/challenges", tags=["admin-challenges"], dependencies=[Depends(require_admin_auth)])
api_router.include_router(admin_participation.router, prefix="/admin/participations", tags=["admin-participations"], dependencies=[Depends(require_admin_auth)])
api_router.include_router(admin_challenge_options.router, prefix="/admin/challenge-options", tags=["admin-challenge-options"], dependencies=[Depends(require_admin_auth)])
api_router.include_router(admin_warriors.router, prefix="/admin/warriors", tags=["admin-warriors"], dependencies=[Depends(require_admin_auth)])
api_router.include_router(admin_stage_results.router, prefix="/admin/stage-results", tags=["admin-stage-results"], dependencies=[Depends(require_admin_auth)])