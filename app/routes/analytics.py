"""
Anonymous Visitor Analytics — privacy-first, no PII collected.
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta

from app.database import get_db
from app.models import VisitorAnalytics, SecurityLog

router = APIRouter()


class VisitorSessionCreate(BaseModel):
    session_id: str
    device_type: Optional[str] = None
    browser: Optional[str] = None
    os: Optional[str] = None
    screen_resolution: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    referral_source: Optional[str] = None
    landing_page: Optional[str] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    utm_content: Optional[str] = None
    utm_term: Optional[str] = None


class VisitorSessionUpdate(BaseModel):
    session_id: str
    pages_viewed: Optional[List[str]] = None
    session_duration_seconds: Optional[int] = None
    click_events: Optional[List[dict]] = None


@router.post("/session/start")
def start_visitor_session(data: VisitorSessionCreate, db: Session = Depends(get_db)):
    """Record the start of an anonymous visitor session."""
    existing = db.query(VisitorAnalytics).filter(
        VisitorAnalytics.session_id == data.session_id
    ).first()
    if existing:
        return {"status": "exists", "session_id": data.session_id}

    session = VisitorAnalytics(
        session_id=data.session_id,
        device_type=data.device_type,
        browser=data.browser,
        os=data.os,
        screen_resolution=data.screen_resolution,
        country=data.country,
        city=data.city,
        referral_source=data.referral_source,
        landing_page=data.landing_page,
        utm_source=data.utm_source,
        utm_medium=data.utm_medium,
        utm_campaign=data.utm_campaign,
        utm_content=data.utm_content,
        utm_term=data.utm_term,
    )
    db.add(session)
    db.commit()
    return {"status": "created", "session_id": data.session_id}


@router.post("/session/update")
def update_visitor_session(data: VisitorSessionUpdate, db: Session = Depends(get_db)):
    """Update session with page views and duration."""
    session = db.query(VisitorAnalytics).filter(
        VisitorAnalytics.session_id == data.session_id
    ).first()
    if not session:
        return {"status": "not_found"}

    if data.pages_viewed is not None:
        session.pages_viewed = data.pages_viewed
    if data.session_duration_seconds is not None:
        session.session_duration_seconds = data.session_duration_seconds
    if data.click_events is not None:
        session.click_events = data.click_events
    session.last_seen_at = datetime.utcnow()

    db.commit()
    return {"status": "updated"}


@router.get("/summary")
def get_analytics_summary(db: Session = Depends(get_db)):
    """Public summary stats — no PII returned."""
    now = datetime.utcnow()
    last_30 = now - timedelta(days=30)
    last_7 = now - timedelta(days=7)

    total_sessions = db.query(VisitorAnalytics).count()
    sessions_30d = db.query(VisitorAnalytics).filter(
        VisitorAnalytics.created_at >= last_30
    ).count()
    sessions_7d = db.query(VisitorAnalytics).filter(
        VisitorAnalytics.created_at >= last_7
    ).count()

    return {
        "total_sessions": total_sessions,
        "sessions_last_30_days": sessions_30d,
        "sessions_last_7_days": sessions_7d,
    }
