from datetime import datetime, timedelta
from enum import Enum
from typing import List, Dict
from dataclasses import dataclass, asdict
import json
from pydantic import BaseModel

class JourneyStage(str, Enum):
    BEGINNING = "beginning"
    HEALING = "healing"
    GROWTH = "growth"
    TRANSFORMATION = "transformation"
    INNER_HARMONY = "inner_harmony"

class ActivityType(str, Enum):
    MEDITATION = "meditation"
    JOURNAL = "journal"
    CHAT_SESSION = "chat_session"
    HEALER_BOOKING = "healer_booking"
    CHECK_IN = "check_in"
    REFLECTION = "reflection"

@dataclass
class Activity:
    """User activity tracking"""
    id: str
    user_id: str
    activity_type: ActivityType
    duration_minutes: int  # for meditation
    intensity: int  # 1-10 scale
    date: datetime
    notes: str = ""

@dataclass
class StageMetrics:
    """Metrics for each journey stage"""
    stage: JourneyStage
    completion_percentage: float  # 0-100
    activities_completed: int
    total_expected_activities: int
    days_in_stage: int
    wellness_contribution: float  # 0-10 scale

@dataclass
class UserProgress:
    """Overall user progress"""
    user_id: str
    current_stage: JourneyStage
    overall_wellness_score: float  # 0-10
    weekly_growth_percentage: float  # 0-100
    total_activities: int
    stage_metrics: Dict[str, StageMetrics]
    last_updated: datetime

class SoulJourneyTracker:
    """Main tracking algorithm"""
    
    STAGE_ORDER = [
        JourneyStage.BEGINNING,
        JourneyStage.HEALING,
        JourneyStage.GROWTH,
        JourneyStage.TRANSFORMATION,
        JourneyStage.INNER_HARMONY
    ]
    
    STAGE_THRESHOLDS = {
        JourneyStage.BEGINNING: 15,
        JourneyStage.HEALING: 40,
        JourneyStage.GROWTH: 70,
        JourneyStage.TRANSFORMATION: 85,
        JourneyStage.INNER_HARMONY: 100
    }
    
    ACTIVITY_WEIGHTS = {
        ActivityType.MEDITATION: 2.0,
        ActivityType.CHAT_SESSION: 1.5,
        ActivityType.HEALER_BOOKING: 3.0,
        ActivityType.JOURNAL: 1.0,
        ActivityType.CHECK_IN: 0.5,
        ActivityType.REFLECTION: 1.2
    }
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.activities: List[Activity] = []
        self.stage_start_dates: Dict[JourneyStage, datetime] = {}
    
    def add_activity(self, activity: Activity) -> None:
        """Log a new user activity"""
        self.activities.append(activity)
    
    def calculate_stage_progress(self, stage: JourneyStage) -> float:
        """
        Calculate progress percentage for a specific stage (0-100)
        Based on activities completed in that stage
        """
        stage_activities = [
            a for a in self.activities 
            if self._get_activity_stage(a) == stage
        ]
        
        if not stage_activities:
            return 0.0
        
        # Calculate weighted score
        total_weight = 0.0
        for activity in stage_activities:
            weight = self.ACTIVITY_WEIGHTS[activity.activity_type]
            intensity_multiplier = activity.intensity / 10.0
            total_weight += weight * intensity_multiplier
        
        # Normalize to 0-100 (adjust divisor based on expected activities per stage)
        max_weight_per_stage = 20.0
        progress = min((total_weight / max_weight_per_stage) * 100, 100.0)
        
        return progress
    
    def get_current_stage(self) -> JourneyStage:
        """Determine current stage based on overall progress"""
        overall_progress = self.calculate_overall_progress()
        
        for stage in reversed(self.STAGE_ORDER):
            if overall_progress >= self.STAGE_THRESHOLDS[stage]:
                return stage
        
        return JourneyStage.BEGINNING
    
    def calculate_overall_progress(self) -> float:
        """
        Calculate overall journey progress (0-100)
        Weighted average of all stage completions
        """
        if not self.activities:
            return 0.0
        
        stage_progresses = {}
        for stage in self.STAGE_ORDER:
            stage_progresses[stage] = self.calculate_stage_progress(stage)
        
        # Weight each stage equally or by time spent
        weighted_progress = sum(stage_progresses.values()) / len(self.STAGE_ORDER)
        return weighted_progress
    
    def calculate_wellness_score(self) -> float:
        """
        Calculate wellness score (0-10)
        Based on activity frequency, intensity, and types
        """
        if not self.activities:
            return 0.0
        
        # Calculate weekly activity metrics
        last_week = datetime.now() - timedelta(days=7)
        week_activities = [a for a in self.activities if a.date >= last_week]
        
        if not week_activities:
            return 0.0
        
        # Score components
        activity_count_score = min(len(week_activities) / 7, 1.0)  # Max 7/week
        
        avg_intensity = sum(a.intensity for a in week_activities) / len(week_activities) / 10.0
        
        # Variety bonus (different activity types)
        activity_types = set(a.activity_type for a in week_activities)
        variety_bonus = min(len(activity_types) / 4, 1.0)  # Max 4 types
        
        wellness_score = (
            (activity_count_score * 0.4) +
            (avg_intensity * 0.4) +
            (variety_bonus * 0.2)
        ) * 10
        
        return round(wellness_score, 1)
    
    def calculate_weekly_growth(self) -> float:
        """
        Calculate weekly growth percentage
        Comparing this week vs previous week activity
        """
        today = datetime.now()
        this_week_start = today - timedelta(days=7)
        last_week_start = today - timedelta(days=14)
        
        this_week_activities = [
            a for a in self.activities 
            if this_week_start <= a.date <= today
        ]
        
        last_week_activities = [
            a for a in self.activities 
            if last_week_start <= a.date < this_week_start
        ]
        
        if len(last_week_activities) == 0:
            return 0.0 if len(this_week_activities) == 0 else 100.0
        
        growth = ((len(this_week_activities) - len(last_week_activities)) 
                  / len(last_week_activities)) * 100
        
        return round(max(growth, -100), 1)
    
    def _get_activity_stage(self, activity: Activity) -> JourneyStage:
        """
        Determine which stage an activity belongs to
        Can be overridden based on custom logic
        """
        # Default: map activity type to stage
        if activity.activity_type == ActivityType.MEDITATION:
            return JourneyStage.HEALING
        elif activity.activity_type == ActivityType.JOURNAL:
            return JourneyStage.HEALING
        elif activity.activity_type == ActivityType.CHAT_SESSION:
            return JourneyStage.GROWTH
        elif activity.activity_type == ActivityType.HEALER_BOOKING:
            return JourneyStage.TRANSFORMATION
        else:
            return self.get_current_stage()
    
    def get_stage_metrics(self) -> Dict[str, StageMetrics]:
        """Get detailed metrics for each stage"""
        metrics = {}
        
        for stage in self.STAGE_ORDER:
            stage_activities = [
                a for a in self.activities 
                if self._get_activity_stage(a) == stage
            ]
            
            # Calculate days in stage
            if stage in self.stage_start_dates:
                days_in_stage = (datetime.now() - self.stage_start_dates[stage]).days
            else:
                days_in_stage = 0
            
            stage_progress = self.calculate_stage_progress(stage)
            wellness_contribution = stage_progress / 100 * 10  # Convert to 0-10
            
            metrics[stage.value] = StageMetrics(
                stage=stage,
                completion_percentage=stage_progress,
                activities_completed=len(stage_activities),
                total_expected_activities=5,  # Adjust based on your requirements
                days_in_stage=days_in_stage,
                wellness_contribution=wellness_contribution
            )
        
        return metrics
    
    def get_progress_report(self) -> UserProgress:
        """Generate complete progress report"""
        return UserProgress(
            user_id=self.user_id,
            current_stage=self.get_current_stage(),
            overall_wellness_score=self.calculate_wellness_score(),
            weekly_growth_percentage=self.calculate_weekly_growth(),
            total_activities=len(self.activities),
            stage_metrics=self.get_stage_metrics(),
            last_updated=datetime.now()
        )


# Example usage with data models
class ActivityRequest(BaseModel):
    activity_type: ActivityType
    duration_minutes: int = 0
    intensity: int  # 1-10
    notes: str = ""

class ProgressResponse(BaseModel):
    current_stage: str
    stage_progress: float  # 0-100 for current stage
    overall_wellness_score: float
    weekly_growth_percentage: float
    total_activities: int
    stage_metrics: Dict[str, Dict]
