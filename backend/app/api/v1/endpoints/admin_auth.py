from __future__ import annotations

import os

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse

from app.core.admin_auth import (
    create_admin_token,
    get_allowed_admin_emails,
    require_admin_auth,
)

router = APIRouter()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
ADMIN_FRONTEND_CALLBACK_URL = os.getenv(
    "ADMIN_FRONTEND_CALLBACK_URL",
    "http://localhost:3000/admin/auth/callback",
)

oauth = OAuth()

oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@router.get("/google")
async def admin_google_login(request: Request):
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        raise HTTPException(status_code=500, detail="Google OAuth is not configured")

    redirect_uri = str(request.url_for("admin_google_callback"))
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/callback", name="admin_google_callback")
async def admin_google_callback(request: Request):
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        raise HTTPException(status_code=500, detail="Google OAuth is not configured")

    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")

    if not user_info:
        raise HTTPException(status_code=400, detail="Google user info not available")

    email = str(user_info.get("email", "")).lower().strip()
    name = user_info.get("name", "")

    if not email:
        raise HTTPException(status_code=400, detail="Google account email not found")

    allowed = get_allowed_admin_emails()
    if allowed and email not in allowed:
        raise HTTPException(status_code=403, detail="This Google account is not allowed")

    admin_jwt = create_admin_token(email=email, name=name)

    return RedirectResponse(
        url=f"{ADMIN_FRONTEND_CALLBACK_URL}?token={admin_jwt}"
    )


@router.get("/me")
def admin_me(admin_payload: dict = Depends(require_admin_auth)):
    return {
        "email": admin_payload.get("sub"),
        "name": admin_payload.get("name"),
        "role": admin_payload.get("role"),
    }