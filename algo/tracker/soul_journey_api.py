from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import Column, String, Float, Integer, DateTime, Enum as SQLEnum, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta
import uuid
from typing import Optional
from soul_journey_tracker import (
    SoulJourneyTracker, Activity, ActivityType, 
    JourneyStage, ActivityRequest, ProgressResponse
)

# Database setup (using SQLite for simplicity, use PostgreSQL in production)
DATABASE_URL = "sqlite:///./soul_journey.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class UserJourneyDB(Base):
    __tablename__ = "user_journeys"
    
    user_id = Column(String, primary_key=True, index=True)
    current_stage = Column(String, default=JourneyStage.BEGINNING.value)
    joined_date = Column(DateTime, default=datetime.now)
    total_activities = Column(Integer, default=0)

class ActivityDB(Base):
    __tablename__ = "activities"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    activity_type = Column(String)
    duration_minutes = Column(Integer, default=0)
    intensity = Column(Integer)
    date = Column(DateTime, default=datetime.now)
    notes = Column(String, default="")

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Soul Journey Tracker")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints
@app.post("/api/v1/journey/{user_id}/activity")
async def log_activity(
    user_id: str,
    activity: ActivityRequest,
    db: Session = Depends(get_db)
):
    """Log a new activity for the user"""
    
    # Ensure user exists
    user_journey = db.query(UserJourneyDB).filter(
        UserJourneyDB.user_id == user_id
    ).first()
    
    if not user_journey:
        user_journey = UserJourneyDB(user_id=user_id)
        db.add(user_journey)
        db.commit()
    
    # Create activity record
    activity_id = str(uuid.uuid4())
    activity_db = ActivityDB(
        id=activity_id,
        user_id=user_id,
        activity_type=activity.activity_type,
        duration_minutes=activity.duration_minutes,
        intensity=activity.intensity,
        notes=activity.notes,
        date=datetime.now()
    )
    
    db.add(activity_db)
    
    # Update user journey
    user_journey.total_activities += 1
    
    db.commit()
    
    return {
        "message": "Activity logged successfully",
        "activity_id": activity_id,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/journey/{user_id}/progress")
async def get_progress(user_id: str, db: Session = Depends(get_db)):
    """Get user's current progress report"""
    
    # Fetch all activities from database
    activities_db = db.query(ActivityDB).filter(
        ActivityDB.user_id == user_id
    ).all()
    
    if not activities_db:
        return {
            "user_id": user_id,
            "current_stage": JourneyStage.BEGINNING.value,
            "stage_progress": 0,
            "overall_wellness_score": 0.0,
            "weekly_growth_percentage": 0.0,
            "total_activities": 0,
            "stage_metrics": {}
        }
    
    # Initialize tracker
    tracker = SoulJourneyTracker(user_id)
    
    # Load activities into tracker
    for activity_db in activities_db:
        activity = Activity(
            id=activity_db.id,
            user_id=activity_db.user_id,
            activity_type=ActivityType[activity_db.activity_type.upper()],
            duration_minutes=activity_db.duration_minutes,
            intensity=activity_db.intensity,
            date=activity_db.date,
            notes=activity_db.notes
        )
        tracker.add_activity(activity)
    
    # Calculate metrics
    current_stage = tracker.get_current_stage()
    stage_progress = tracker.calculate_stage_progress(current_stage)
    stage_metrics = tracker.get_stage_metrics()
    
    # Format response
    formatted_stage_metrics = {}
    for stage_key, metrics in stage_metrics.items():
        formatted_stage_metrics[stage_key] = {
            "completion_percentage": metrics.completion_percentage,
            "activities_completed": metrics.activities_completed,
            "total_expected_activities": metrics.total_expected_activities,
            "days_in_stage": metrics.days_in_stage,
            "wellness_contribution": round(metrics.wellness_contribution, 1)
        }
    
    return {
        "user_id": user_id,
        "current_stage": current_stage.value,
        "stage_progress": round(stage_progress, 1),
        "overall_wellness_score": tracker.calculate_wellness_score(),
        "weekly_growth_percentage": tracker.calculate_weekly_growth(),
        "total_activities": len(activities_db),
        "stage_metrics": formatted_stage_metrics,
        "last_updated": datetime.now().isoformat()
    }

@app.get("/api/v1/journey/{user_id}/activities")
async def get_activities(
    user_id: str,
    days: int = 30,
    activity_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get user's activity history"""
    
    start_date = datetime.now() - timedelta(days=days)
    
    query = db.query(ActivityDB).filter(
        ActivityDB.user_id == user_id,
        ActivityDB.date >= start_date
    )
    
    if activity_type:
        query = query.filter(ActivityDB.activity_type == activity_type)
    
    activities = query.order_by(ActivityDB.date.desc()).all()
    
    return {
        "user_id": user_id,
        "activities": [
            {
                "id": a.id,
                "activity_type": a.activity_type,
                "duration_minutes": a.duration_minutes,
                "intensity": a.intensity,
                "date": a.date.isoformat(),
                "notes": a.notes
            }
            for a in activities
        ],
        "count": len(activities)
    }

@app.get("/api/v1/journey/{user_id}/stats")
async def get_stats(user_id: str, db: Session = Depends(get_db)):
    """Get aggregated statistics"""
    
    activities_db = db.query(ActivityDB).filter(
        ActivityDB.user_id == user_id
    ).all()
    
    if not activities_db:
        return {
            "user_id": user_id,
            "total_sessions": 0,
            "total_meditation_minutes": 0,
            "average_intensity": 0,
            "activity_breakdown": {},
            "weekly_trend": []
        }
    
    tracker = SoulJourneyTracker(user_id)
    for activity_db in activities_db:
        activity = Activity(
            id=activity_db.id,
            user_id=activity_db.user_id,
            activity_type=ActivityType[activity_db.activity_type.upper()],
            duration_minutes=activity_db.duration_minutes,
            intensity=activity_db.intensity,
            date=activity_db.date,
            notes=activity_db.notes
        )
        tracker.add_activity(activity)
    
    # Calculate stats
    total_meditation = sum(
        a.duration_minutes for a in activities_db 
        if a.activity_type == "MEDITATION"
    )
    
    avg_intensity = sum(a.intensity for a in activities_db) / len(activities_db) if activities_db else 0
    
    # Activity breakdown
    activity_breakdown = {}
    for activity in activities_db:
        activity_breakdown[activity.activity_type] = \
            activity_breakdown.get(activity.activity_type, 0) + 1
    
    # Weekly trend (last 4 weeks)
    weekly_trend = []
    for week in range(4):
        week_start = datetime.now() - timedelta(days=7 * (week + 1))
        week_end = datetime.now() - timedelta(days=7 * week)
        week_count = len([
            a for a in activities_db
            if week_start <= a.date <= week_end
        ])
        weekly_trend.append({
            "week": f"Week {4 - week}",
            "activities": week_count
        })
    
    weekly_trend.reverse()
    
    return {
        "user_id": user_id,
        "total_sessions": len(activities_db),
        "total_meditation_minutes": total_meditation,
        "average_intensity": round(avg_intensity, 1),
        "activity_breakdown": activity_breakdown,
        "weekly_trend": weekly_trend
    }

@app.post("/api/v1/journey/{user_id}/reset")
async def reset_journey(user_id: str, db: Session = Depends(get_db)):
    """Reset user's journey (for testing)"""
    
    db.query(ActivityDB).filter(ActivityDB.user_id == user_id).delete()
    db.query(UserJourneyDB).filter(UserJourneyDB.user_id == user_id).delete()
    db.commit()
    
    return {"message": f"Journey reset for user {user_id}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
