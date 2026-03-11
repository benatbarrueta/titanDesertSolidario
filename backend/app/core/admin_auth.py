from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, Header
from jose import jwt, JWTError


ADMIN_JWT_SECRET = os.getenv("ADMIN_JWT_SECRET", "change-me")
ADMIN_JWT_ALGORITHM = "HS256"
ADMIN_JWT_EXPIRE_HOURS = 24


def get_allowed_admin_emails() -> set[str]:
    raw = os.getenv("ADMIN_ALLOWED_EMAILS", "")
    return {
        email.strip().lower()
        for email in raw.split(",")
        if email.strip()
    }


def create_admin_token(email: str, name: str | None = None) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": email.lower(),
        "name": name or "",
        "role": "admin",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=ADMIN_JWT_EXPIRE_HOURS)).timestamp()),
    }
    return jwt.encode(payload, ADMIN_JWT_SECRET, algorithm=ADMIN_JWT_ALGORITHM)


def decode_admin_token(token: str) -> dict:
    try:
        return jwt.decode(token, ADMIN_JWT_SECRET, algorithms=[ADMIN_JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired admin token")


def require_admin_auth(authorization: str | None = Header(default=None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing admin authorization token")

    token = authorization.removeprefix("Bearer ").strip()
    payload = decode_admin_token(token)

    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not an admin token")

    allowed = get_allowed_admin_emails()
    email = str(payload.get("sub", "")).lower()

    if allowed and email not in allowed:
        raise HTTPException(status_code=403, detail="Admin email not allowed")

    return payload