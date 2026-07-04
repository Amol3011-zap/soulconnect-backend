"""
FastAPI routes for dashboard statistics
Endpoints for: Healing streak, Live souls, Soul points, Healing sessions
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from dashboard_stats_algorithm import (
    DashboardStats, 
    HealingStreakTracker,
    LevelSystem,
    HealingSessionsTracker,
    LiveHealingTracker
)

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])

# In-memory storage (replace with database for production)
user_stats = {}
live_tracker = LiveHealingTracker()

def get_or_create_stats(user_id: str) -> DashboardStats:
    """Get or create dashboard stats for user"""
    if user_id not in user_stats:
        user_stats[user_id] = DashboardStats(user_id)
    return user_stats[user_id]


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("/{user_id}/stats")
async def get_dashboard_stats(user_id: str):
    """
    Get all 4 dashboard metrics for user
    
    Returns:
    {
        "healing_streak": {...},
        "souls_healing": {...},
        "soul_points": {...},
        "healing_sessions": {...}
    }
    """
    stats = get_or_create_stats(user_id)
    return stats.get_dashboard_stats()


@router.post("/{user_id}/streak/log")
async def log_healing_activity(user_id: str):
    """
    Log a healing activity (meditation, yoga, breathing, etc)
    Increments the healing streak
    """
    stats = get_or_create_stats(user_id)
    stats.streak_tracker.log_healing_activity()
    
    return {
        "message": "Healing activity logged",
        "current_streak": stats.streak_tracker.current_streak,
        "longest_streak": stats.streak_tracker.longest_streak
    }


@router.post("/{user_id}/points/add")
async def add_soul_points(
    user_id: str,
    amount: int,
    source: str,  # "challenge", "journey", "session", "streak"
    description: str = ""
):
    """
    Add soul points to user
    
    Sources:
    - challenge: Daily challenge completion (30-150 pts)
    - journey: Soul Journey activity (varies)
    - session: Healing session (50-100 pts)
    - streak: Streak bonus (10-50 pts)
    """
    
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Points must be positive")
    
    if source not in ["challenge", "journey", "session", "streak"]:
        raise HTTPException(status_code=400, detail="Invalid source")
    
    stats = get_or_create_stats(user_id)
    result = stats.points_system.add_points(amount, source, description)
    
    return result


@router.get("/{user_id}/points/level")
async def get_level_info(user_id: str):
    """
    Get detailed level and points information
    """
    stats = get_or_create_stats(user_id)
    level_progress = stats.points_system.get_level_progress()
    
    return {
        "current_level": level_progress["current_level"],
        "total_points": level_progress["total_points"],
        "points_to_next": level_progress["points_to_next"],
        "progress_percentage": level_progress["progress_percentage"],
        "current_level_start": level_progress["current_level_start"],
        "next_level_start": level_progress["next_level_start"]
    }


@router.post("/{user_id}/session/start/{session_type}")
async def start_healing_session(user_id: str, session_type: str):
    """
    Mark user as starting a healing session
    
    Session types: meditation, yoga, chat, healer
    Updates live count
    """
    
    valid_types = ["meditation", "yoga", "chat", "healer"]
    if session_type not in valid_types:
        raise HTTPException(status_code=400, detail=f"Invalid session type. Must be one of: {valid_types}")
    
    live_tracker.start_session(user_id, session_type)
    
    return {
        "message": f"Session started: {session_type}",
        "user_id": user_id,
        "souls_healing_now": live_tracker.get_active_count()
    }


@router.post("/{user_id}/session/end")
async def end_healing_session(user_id: str):
    """
    Mark user as ending a healing session
    """
    
    live_tracker.end_session(user_id)
    
    return {
        "message": "Session ended",
        "user_id": user_id,
        "souls_healing_now": live_tracker.get_active_count()
    }


@router.post("/{user_id}/session/log")
async def log_healing_session(
    user_id: str,
    session_type: str,  # meditation, yoga, chat, healer
    duration_minutes: int,
    notes: str = ""
):
    """
    Log a completed healing session
    Adds to session count and history
    """
    
    valid_types = ["meditation", "yoga", "chat", "healer"]
    if session_type not in valid_types:
        raise HTTPException(status_code=400, detail=f"Invalid session type")
    
    if duration_minutes <= 0:
        raise HTTPException(status_code=400, detail="Duration must be positive")
    
    stats = get_or_create_stats(user_id)
    stats.sessions_tracker.log_session(session_type, duration_minutes, notes=notes)
    
    sessions_data = stats.sessions_tracker.get_sessions_data()
    
    return {
        "message": "Session logged",
        "session_type": session_type,
        "duration_minutes": duration_minutes,
        "total_sessions": sessions_data["total_sessions"],
        "this_week": sessions_data["this_week"]
    }


@router.get("/{user_id}/session/weekly")
async def get_weekly_sessions(user_id: str):
    """
    Get this week's session statistics
    """
    stats = get_or_create_stats(user_id)
    sessions_data = stats.sessions_tracker.get_sessions_data()
    
    return {
        "this_week": sessions_data["this_week"],
        "change_from_last_week": sessions_data["weekly_change"],
        "total_hours": sessions_data["total_hours"],
        "average_session_minutes": sessions_data["average_session_minutes"]
    }


@router.get("/live/count")
async def get_live_souls_count():
    """
    Get number of souls healing right now
    Global statistic (all users)
    """
    return {
        "souls_healing_now": live_tracker.get_active_count(),
        "timestamp": datetime.now().isoformat()
    }


@router.post("/{user_id}/reset")
async def reset_user_stats(user_id: str):
    """
    Reset all stats for a user (for testing)
    """
    if user_id in user_stats:
        del user_stats[user_id]
    
    return {
        "message": f"Stats reset for user {user_id}"
    }


# ============================================================================
# INTEGRATION WITH EXISTING SYSTEMS
# ============================================================================

@router.post("/{user_id}/sync-with-journey")
async def sync_with_soul_journey(user_id: str):
    """
    Sync dashboard stats with Soul Journey data
    
    This endpoint:
    1. Fetches activities from Soul Journey
    2. Logs them as healing activities (for streak)
    3. Adds corresponding points
    4. Updates session count
    """
    
    stats = get_or_create_stats(user_id)
    
    # TODO: Fetch from soul_journey API
    # journey_activities = await get_soul_journey_activities(user_id)
    # 
    # for activity in journey_activities:
    #     stats.streak_tracker.log_healing_activity(activity.date)
    #     points_value = calculate_points(activity.type)
    #     stats.points_system.add_points(points_value, "journey", activity.type)
    
    return {
        "message": "Synced with Soul Journey",
        "stats": stats.get_dashboard_stats()
    }


@router.post("/{user_id}/sync-with-challenges")
async def sync_with_daily_challenges(user_id: str):
    """
    Sync dashboard stats with Daily Challenges data
    
    This endpoint:
    1. Fetches completed challenges from Daily Challenges
    2. Adds points for each completed challenge
    3. Updates streak if challenge completed today
    """
    
    stats = get_or_create_stats(user_id)
    
    # TODO: Fetch from daily_challenges API
    # challenges = await get_completed_challenges(user_id)
    # 
    # for challenge in challenges:
    #     stats.points_system.add_points(challenge.points, "challenge", challenge.name)
    #     if challenge.date == today:
    #         stats.streak_tracker.log_healing_activity(challenge.date)
    
    return {
        "message": "Synced with Daily Challenges",
        "stats": stats.get_dashboard_stats()
    }


# ============================================================================
# EXAMPLE: Add to your main FastAPI app
# ============================================================================

"""
In your main.py:

from fastapi import FastAPI
from dashboard_routes import router as dashboard_router

app = FastAPI()
app.include_router(dashboard_router)

# This makes all dashboard routes available:
# GET  /api/v1/dashboard/{user_id}/stats
# POST /api/v1/dashboard/{user_id}/streak/log
# POST /api/v1/dashboard/{user_id}/points/add
# GET  /api/v1/dashboard/{user_id}/points/level
# POST /api/v1/dashboard/{user_id}/session/start/{session_type}
# POST /api/v1/dashboard/{user_id}/session/end
# POST /api/v1/dashboard/{user_id}/session/log
# GET  /api/v1/dashboard/{user_id}/session/weekly
# GET  /api/v1/dashboard/live/count
"""
