from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel

from app.database import get_db
from app.models import User, UserChallengeStreak, UserChallengeCompletion
from app.routes.users import get_current_user
from app.services import challenges_tracker as ct

router = APIRouter()


# ── Schemas ───────────────────────────────────────────────────────────────────

class CompleteRequest(BaseModel):
    actual_duration: Optional[int] = None


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_or_create_streak(user: User, db: Session) -> UserChallengeStreak:
    streak = db.query(UserChallengeStreak).filter(UserChallengeStreak.user_id == user.id).first()
    if not streak:
        streak = UserChallengeStreak(user_id=user.id)
        db.add(streak)
        db.commit()
        db.refresh(streak)
    return streak


def _completed_today_ids(user_id: int, db: Session) -> set:
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)
    rows = db.query(UserChallengeCompletion).filter(
        UserChallengeCompletion.user_id == user_id,
        UserChallengeCompletion.challenge_date >= today_start,
        UserChallengeCompletion.challenge_date < today_end,
    ).all()
    return {r.challenge_id for r in rows}


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/today")
async def get_today_challenges(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return today's 3 challenges with completion status."""
    streak = _get_or_create_streak(current_user, db)
    completed = _completed_today_ids(current_user.id, db)
    bonus = ct.calculate_streak_bonus(streak.current_streak)
    challenges = ct.get_todays_challenges(completed, bonus)

    completed_count = sum(1 for c in challenges if c["completed"])
    points_remaining = sum(
        c["points"] + bonus for c in challenges if not c["completed"]
    )

    return {
        "cycle_day": ct.get_current_cycle_day(),
        "theme": ct.TWO_WEEK_SCHEDULE[ct.get_current_cycle_day() - 1]["theme"],
        "challenges": challenges,
        "completed": completed_count,
        "total": len(challenges),
        "points_earned_today": sum(c["points"] + bonus for c in challenges if c["completed"]),
        "points_remaining": points_remaining,
        "current_streak": streak.current_streak,
        "longest_streak": streak.longest_streak,
        "total_points": streak.total_points,
    }


@router.post("/complete/{challenge_id}")
async def complete_challenge(
    challenge_id: str,
    payload: CompleteRequest = CompleteRequest(),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Mark a challenge as completed and award points."""
    if challenge_id not in ct.CHALLENGE_LIBRARY:
        raise HTTPException(status_code=404, detail="Challenge not found")

    # Check not already completed today
    completed = _completed_today_ids(current_user.id, db)
    if challenge_id in completed:
        raise HTTPException(status_code=400, detail="Challenge already completed today")

    streak = _get_or_create_streak(current_user, db)
    bonus = ct.calculate_streak_bonus(streak.current_streak)
    pts = ct.calculate_points(challenge_id, bonus, payload.actual_duration)

    # Save completion
    now = datetime.utcnow()
    completion = UserChallengeCompletion(
        user_id=current_user.id,
        challenge_id=challenge_id,
        challenge_date=now,
        completed_at=now,
        actual_duration=payload.actual_duration,
        points_earned=pts["total_points"],
    )
    db.add(completion)

    # Update streak
    if ct.should_increment_streak(streak.last_completion_date, now):
        if streak.last_completion_date is None or streak.last_completion_date.date() < now.date():
            streak.current_streak += 1
    else:
        streak.current_streak = 1

    if streak.current_streak > streak.longest_streak:
        streak.longest_streak = streak.current_streak

    streak.total_points += pts["total_points"]
    streak.last_completion_date = now
    db.commit()

    return {
        "challenge_id": challenge_id,
        "challenge_name": ct.CHALLENGE_LIBRARY[challenge_id]["name"],
        "base_points": pts["base_points"],
        "streak_bonus": pts["streak_bonus"],
        "time_bonus": pts["time_bonus"],
        "total_points": pts["total_points"],
        "current_streak": streak.current_streak,
        "longest_streak": streak.longest_streak,
        "total_earned": streak.total_points,
    }


@router.get("/weekly-summary")
async def get_weekly_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return progress for the current 2-week cycle."""
    cycle_day = ct.get_current_cycle_day()
    cycle_start_dt = datetime.utcnow() - timedelta(days=cycle_day - 1)

    # Fetch all completions in this cycle
    completions = db.query(UserChallengeCompletion).filter(
        UserChallengeCompletion.user_id == current_user.id,
        UserChallengeCompletion.challenge_date >= cycle_start_dt.replace(hour=0, minute=0, second=0, microsecond=0),
    ).all()

    # Build {date_str: set_of_challenge_ids}
    by_date: dict = {}
    for c in completions:
        ds = str(c.challenge_date.date())
        by_date.setdefault(ds, set()).add(c.challenge_id)

    return ct.get_weekly_summary(by_date)
