"""
Dashboard Statistics System
Calculates: Healing Streak, Active Souls, Soul Points, Sessions Count
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

# ============================================================================
# METRIC 1: HEALING STREAK
# ============================================================================

class HealingStreakTracker:
    """
    Tracks consecutive days of healing activities.
    Includes: meditation, yoga, breathing, journaling, chat sessions
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.activity_dates: List[datetime] = []
        self.current_streak: int = 0
        self.longest_streak: int = 0
        self.best_streak_date_range: tuple = None
    
    def log_healing_activity(self, activity_date: datetime = None) -> None:
        """
        Log that user did a healing activity today
        Any of: meditation, yoga, breathing, journal, chat, healer session
        """
        if activity_date is None:
            activity_date = datetime.now()
        
        # Only count once per day
        today = activity_date.date()
        if any(a.date() == today for a in self.activity_dates):
            return
        
        self.activity_dates.append(activity_date)
        self.update_streak()
    
    def update_streak(self) -> None:
        """Calculate current streak based on activity dates"""
        
        if not self.activity_dates:
            self.current_streak = 0
            return
        
        # Sort by date
        sorted_dates = sorted(set(a.date() for a in self.activity_dates))
        
        # Calculate current streak (from today backwards)
        today = datetime.now().date()
        current_streak = 0
        check_date = today
        
        for _ in range(365):  # Max 365 days
            if check_date in sorted_dates:
                current_streak += 1
                check_date -= timedelta(days=1)
            elif check_date == today:
                # Haven't done activity today, so streak is yesterday's count
                check_date -= timedelta(days=1)
            else:
                break
        
        self.current_streak = current_streak
        
        # Calculate longest streak (ever)
        max_streak = 0
        current_temp = 0
        
        for i, date in enumerate(sorted_dates):
            if i == 0:
                current_temp = 1
            else:
                if (date - sorted_dates[i-1]).days == 1:
                    current_temp += 1
                else:
                    if current_temp > max_streak:
                        max_streak = current_temp
                    current_temp = 1
        
        if current_temp > max_streak:
            max_streak = current_temp
        
        self.longest_streak = max_streak
    
    def get_streak_data(self) -> Dict:
        """Return streak information"""
        return {
            "current_streak": self.current_streak,
            "longest_streak": self.longest_streak,
            "days_active": len(set(a.date() for a in self.activity_dates))
        }


# ============================================================================
# METRIC 2: SOULS HEALING RIGHT NOW (Live Users Count)
# ============================================================================

class LiveHealingTracker:
    """
    Tracks users currently in healing sessions.
    Counts: Active meditations, yoga sessions, chat sessions, healer bookings
    Updates in real-time
    """
    
    def __init__(self):
        self.active_sessions: Dict[str, Dict] = {}  # {user_id: session_info}
    
    def start_session(
        self, 
        user_id: str, 
        session_type: str,  # meditation, yoga, chat, healer
        start_time: datetime = None
    ) -> None:
        """
        Mark user as starting a healing session
        Example: User opens meditation app or joins chat
        """
        if start_time is None:
            start_time = datetime.now()
        
        self.active_sessions[user_id] = {
            "type": session_type,
            "start_time": start_time,
            "user_id": user_id
        }
    
    def end_session(self, user_id: str) -> None:
        """
        Mark user as ending a healing session
        Example: User closes meditation app or leaves chat
        """
        if user_id in self.active_sessions:
            del self.active_sessions[user_id]
    
    def get_active_count(self) -> int:
        """Return number of people healing right now"""
        # Clean up old sessions (older than 2 hours = probably inactive)
        cutoff_time = datetime.now() - timedelta(hours=2)
        
        active = {
            uid: session for uid, session in self.active_sessions.items()
            if session["start_time"] > cutoff_time
        }
        
        return len(active)
    
    def get_live_data(self) -> Dict:
        """Return live healing data"""
        return {
            "souls_healing_now": self.get_active_count(),
            "active_sessions": list(self.active_sessions.keys()),
            "last_updated": datetime.now().isoformat()
        }


# ============================================================================
# METRIC 3: SOUL POINTS & LEVEL SYSTEM
# ============================================================================

class LevelSystem:
    """
    Points system with levels.
    Points come from: Daily challenges, Soul Journey activities, Sessions
    Levels: 1-10+ (each level requires more points)
    """
    
    # Points required for each level
    LEVEL_THRESHOLDS = {
        1: 0,
        2: 100,
        3: 300,
        4: 600,      # Level 3->4 = 300 pts
        5: 1000,
        6: 1500,
        7: 2100,
        8: 2800,
        9: 3600,
        10: 4500,
        11: 5500,
        # Continue pattern for higher levels
    }
    
    def __init__(self, user_id: str, total_points: int = 0):
        self.user_id = user_id
        self.total_points = total_points
        self.points_history: List[Dict] = []
    
    def add_points(
        self, 
        amount: int, 
        source: str,  # "challenge", "journey", "session"
        description: str = ""
    ) -> Dict:
        """
        Add points to user and return new level info
        
        Sources:
        - challenge: Daily challenge completion (+30-150)
        - journey: Soul Journey activity (+varies)
        - session: Healing session (+50-100)
        - streak: Streak bonus (+10-50)
        """
        
        old_level = self.get_current_level()
        self.total_points += amount
        new_level = self.get_current_level()
        
        # Record transaction
        self.points_history.append({
            "timestamp": datetime.now(),
            "amount": amount,
            "source": source,
            "description": description,
            "total_after": self.total_points
        })
        
        return {
            "points_added": amount,
            "total_points": self.total_points,
            "old_level": old_level,
            "new_level": new_level,
            "leveled_up": new_level > old_level,
            "points_to_next_level": self.get_points_to_next_level()
        }
    
    def get_current_level(self) -> int:
        """Calculate current level based on total points"""
        current_level = 1
        
        for level, threshold in sorted(self.LEVEL_THRESHOLDS.items()):
            if self.total_points >= threshold:
                current_level = level
            else:
                break
        
        return current_level
    
    def get_points_to_next_level(self) -> int:
        """How many points until next level"""
        current_level = self.get_current_level()
        next_level = current_level + 1
        
        if next_level not in self.LEVEL_THRESHOLDS:
            return 0  # Already at max
        
        points_needed = self.LEVEL_THRESHOLDS[next_level]
        return points_needed - self.total_points
    
    def get_level_progress(self) -> Dict:
        """Get detailed level progress"""
        current_level = self.get_current_level()
        next_level = current_level + 1
        
        current_threshold = self.LEVEL_THRESHOLDS[current_level]
        next_threshold = self.LEVEL_THRESHOLDS.get(next_level, current_threshold)
        
        progress_in_level = self.total_points - current_threshold
        points_for_level = next_threshold - current_threshold
        progress_percentage = (progress_in_level / points_for_level * 100) if points_for_level > 0 else 0
        
        return {
            "current_level": current_level,
            "total_points": self.total_points,
            "points_to_next": self.get_points_to_next_level(),
            "progress_percentage": progress_percentage,
            "current_level_start": current_threshold,
            "next_level_start": next_threshold
        }


# ============================================================================
# METRIC 4: HEALING SESSIONS COUNT
# ============================================================================

class HealingSessionsTracker:
    """
    Tracks completed healing sessions.
    Types: Professional healer, peer chat, self-guided meditation, yoga
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.sessions: List[Dict] = []
    
    def log_session(
        self,
        session_type: str,  # healer, chat, meditation, yoga
        duration_minutes: int,
        date: datetime = None,
        notes: str = ""
    ) -> None:
        """
        Log a completed healing session
        """
        if date is None:
            date = datetime.now()
        
        self.sessions.append({
            "type": session_type,
            "duration": duration_minutes,
            "date": date,
            "notes": notes
        })
    
    def get_this_week_count(self) -> int:
        """Count sessions from last 7 days"""
        week_ago = datetime.now() - timedelta(days=7)
        return len([s for s in self.sessions if s["date"] >= week_ago])
    
    def get_this_week_change(self) -> int:
        """
        Change from previous week
        Example: This week 3, last week 1 = +2
        """
        now = datetime.now()
        
        # This week: last 7 days
        this_week_start = now - timedelta(days=7)
        this_week = len([s for s in self.sessions if s["date"] >= this_week_start])
        
        # Last week: 14 days ago to 7 days ago
        last_week_start = now - timedelta(days=14)
        last_week = len([s for s in self.sessions 
                        if last_week_start <= s["date"] < this_week_start])
        
        return this_week - last_week
    
    def get_total_hours(self) -> float:
        """Total healing hours invested"""
        return sum(s["duration"] for s in self.sessions) / 60
    
    def get_sessions_data(self) -> Dict:
        """Return all session metrics"""
        this_week = self.get_this_week_count()
        change = self.get_this_week_change()
        
        return {
            "total_sessions": len(self.sessions),
            "this_week": this_week,
            "weekly_change": change,
            "weekly_change_display": f"+{change}" if change > 0 else str(change),
            "total_hours": round(self.get_total_hours(), 1),
            "average_session_minutes": (
                sum(s["duration"] for s in self.sessions) / len(self.sessions)
                if self.sessions else 0
            )
        }


# ============================================================================
# COMPLETE DASHBOARD STATS
# ============================================================================

class DashboardStats:
    """
    Combines all 4 metrics into one dashboard view
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.streak_tracker = HealingStreakTracker(user_id)
        self.points_system = LevelSystem(user_id)
        self.sessions_tracker = HealingSessionsTracker(user_id)
        self.live_tracker = LiveHealingTracker()
    
    def get_dashboard_stats(self) -> Dict:
        """
        Return all 4 dashboard metrics
        
        Returns:
        {
            "healing_streak": {
                "current": 7,
                "best": 14,
                "icon": "🧘"
            },
            "souls_healing": {
                "count": 1247,
                "icon": "🌍",
                "live": true
            },
            "soul_points": {
                "current": 847,
                "level": 3,
                "progress": 153,
                "to_next": 153,
                "icon": "⚡"
            },
            "healing_sessions": {
                "total": 3,
                "this_week": 2,
                "change": "+2",
                "icon": "🔔"
            }
        }
        """
        
        streak_data = self.streak_tracker.get_streak_data()
        level_progress = self.points_system.get_level_progress()
        sessions_data = self.sessions_tracker.get_sessions_data()
        live_data = self.live_tracker.get_live_data()
        
        return {
            "healing_streak": {
                "current": streak_data["current_streak"],
                "best": streak_data["longest_streak"],
                "icon": "🧘",
                "label": "Day Healing Streak"
            },
            "souls_healing": {
                "count": live_data["souls_healing_now"],
                "icon": "🌍",
                "label": "Souls healing right now",
                "live": True,
                "dot_color": "green"
            },
            "soul_points": {
                "current": level_progress["total_points"],
                "level": level_progress["current_level"],
                "next_level": level_progress["current_level"] + 1,
                "progress": level_progress["progress_percentage"],
                "to_next": level_progress["points_to_next"],
                "icon": "⚡",
                "label": "Soul Points"
            },
            "healing_sessions": {
                "total": sessions_data["this_week"],
                "all_time": sessions_data["total_sessions"],
                "change": sessions_data["weekly_change"],
                "change_display": sessions_data["weekly_change_display"],
                "icon": "🔔",
                "label": "Healing Sessions"
            }
        }


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("=== DASHBOARD STATS SIMULATION ===\n")
    
    # Create dashboard
    dashboard = DashboardStats("user_amol")
    
    # Simulate user activities
    print("1️⃣ Logging healing activities...")
    
    # Log activities for last 7 days
    for day in range(7):
        date = datetime.now() - timedelta(days=day)
        dashboard.streak_tracker.log_healing_activity(date)
    
    print(f"   Streak: {dashboard.streak_tracker.current_streak} days\n")
    
    print("2️⃣ Adding Soul Points...")
    
    # Challenge points
    dashboard.points_system.add_points(30, "challenge", "3-Min Breathing")
    dashboard.points_system.add_points(50, "challenge", "Gratitude Journal")
    dashboard.points_system.add_points(70, "challenge", "5-Min Meditation")
    
    # Activity points
    dashboard.points_system.add_points(100, "journey", "Completed meditation session")
    dashboard.points_system.add_points(150, "journey", "Healer booking")
    
    # Streak bonus
    dashboard.points_system.add_points(40, "streak", "7-day streak bonus")
    
    level_info = dashboard.points_system.get_level_progress()
    print(f"   Level: {level_info['current_level']}")
    print(f"   Points: {level_info['total_points']}")
    print(f"   To next level: {level_info['points_to_next']}\n")
    
    print("3️⃣ Logging healing sessions...")
    
    dashboard.sessions_tracker.log_session("healer", 30)
    dashboard.sessions_tracker.log_session("meditation", 15)
    dashboard.sessions_tracker.log_session("chat", 20)
    
    sessions_info = dashboard.sessions_tracker.get_sessions_data()
    print(f"   This week: {sessions_info['this_week']}")
    print(f"   Change from last week: {sessions_info['weekly_change_display']}\n")
    
    print("4️⃣ Getting final dashboard stats...\n")
    
    stats = dashboard.get_dashboard_stats()
    
    print("📊 DASHBOARD DISPLAY:")
    print(f"""
    {stats['healing_streak']['icon']} {stats['healing_streak']['current']}
    Day Healing Streak
    Best: {stats['healing_streak']['best']} days
    
    {stats['souls_healing']['icon']} {stats['souls_healing']['count']:,}
    Souls healing right now
    
    {stats['soul_points']['icon']} {stats['soul_points']['current']}
    Soul Points
    Level {stats['soul_points']['level']} → {stats['soul_points']['next_level']}
    {stats['soul_points']['to_next']} pts remaining
    
    {stats['healing_sessions']['icon']} {stats['healing_sessions']['total']}
    Healing Sessions
    This week: {stats['healing_sessions']['change_display']} from last
    """)
