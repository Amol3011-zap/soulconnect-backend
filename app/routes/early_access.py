import re
import logging
from collections import defaultdict
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

from app.database import get_db

router = APIRouter()
logger = logging.getLogger("waitlist")

# ─── In-memory rate limiter ───────────────────────────────────────────────────
# 5 attempts per IP per 10 minutes
_rate_store: dict = defaultdict(list)
RATE_LIMIT  = 5
RATE_WINDOW = timedelta(minutes=10)


def _check_rate_limit(ip: str):
    now = datetime.utcnow()
    cutoff = now - RATE_WINDOW
    _rate_store[ip] = [t for t in _rate_store[ip] if t > cutoff]
    if len(_rate_store[ip]) >= RATE_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please wait a few minutes and try again.",
        )
    _rate_store[ip].append(now)


def _get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


# ─── Schemas ─────────────────────────────────────────────────────────────────

VALID_STRUGGLES = {
    "Anxiety", "Breakup", "Burnout", "Loneliness",
    "Grief", "Stress", "Self Growth", "Other",
}


class WaitlistRequest(BaseModel):
    name:          Optional[str] = None
    email:         str
    struggle:      Optional[str] = None
    source:        Optional[str] = "Landing Page"
    referral_code: Optional[str] = None

    @field_validator("email", mode="before")
    @classmethod
    def normalise_email(cls, v):
        if not v or not isinstance(v, str):
            raise ValueError("Email is required")
        v = v.strip().lower()
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", v):
            raise ValueError("Invalid email address")
        return v

    @field_validator("name", mode="before")
    @classmethod
    def clean_name(cls, v):
        if v is None:
            return v
        v = str(v).strip()
        if len(v) > 200:
            return v[:200]
        return v or None

    @field_validator("struggle", mode="before")
    @classmethod
    def validate_struggle(cls, v):
        if v is None:
            return v
        v = str(v).strip()
        if v and v not in VALID_STRUGGLES:
            return "Other"
        return v or None

    @field_validator("referral_code", mode="before")
    @classmethod
    def clean_referral(cls, v):
        if v is None:
            return v
        return str(v).strip()[:100]


class WaitlistResponse(BaseModel):
    success: bool
    message: str


# ─── POST /api/early-access/ ──────────────────────────────────────────────────

@router.post("/", response_model=WaitlistResponse)
async def join_waitlist(
    data: WaitlistRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    # Rate limit
    ip = _get_client_ip(request)
    _check_rate_limit(ip)

    # Extra server-side email validation
    if not data.email or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", data.email):
        return WaitlistResponse(success=False, message="Invalid email address")

    try:
        from app.models import EarlyAccessSubmission

        existing = db.query(EarlyAccessSubmission).filter(
            EarlyAccessSubmission.email == data.email
        ).first()

        if existing:
            logger.info("Duplicate waitlist: %s", data.email)
            return WaitlistResponse(
                success=False,
                message="Email already registered",
            )

        submission = EarlyAccessSubmission(
            name          = data.name,
            email         = data.email,
            struggle      = data.struggle,
            challenge     = data.struggle,       # backward compat column
            source        = (data.source or "Landing Page")[:100],
            referral_code = data.referral_code,
            created_at    = datetime.utcnow(),
        )
        db.add(submission)
        db.commit()

        logger.info(
            "Waitlist signup: email=%s struggle=%s source=%s ip=%s",
            data.email, data.struggle, data.source, ip,
        )

        return WaitlistResponse(
            success=True,
            message="You're on the list! 💜",
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error("Waitlist DB error for %s: %s", data.email, str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong. Please try again.",
        )


# ─── GET /api/early-access/count ─────────────────────────────────────────────

@router.get("/count")
async def get_waitlist_count(db: Session = Depends(get_db)):
    from app.models import EarlyAccessSubmission
    count = db.query(EarlyAccessSubmission).count()
    return {"count": count}


# ─── GET /api/early-access/admin ─────────────────────────────────────────────
# Requires header:  X-Admin-Key: <value of ADMIN_SECRET in .env>

@router.get("/admin")
async def get_waitlist_admin(
    request: Request,
    db: Session = Depends(get_db),
):
    import os
    admin_secret = os.getenv("ADMIN_SECRET", "")
    provided     = request.headers.get("x-admin-key", "")

    if not admin_secret or provided != admin_secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    from app.models import EarlyAccessSubmission
    rows = (
        db.query(EarlyAccessSubmission)
        .order_by(EarlyAccessSubmission.created_at.desc())
        .all()
    )

    return [
        {
            "id":            r.id,
            "name":          r.name,
            "email":         r.email,
            "struggle":      r.struggle,
            "source":        r.source,
            "referral_code": getattr(r, "referral_code", None),
            "created_at":    r.created_at.isoformat() if r.created_at else None,
        }
        for r in rows
    ]
