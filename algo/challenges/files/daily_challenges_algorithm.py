"""
Daily Challenges System for SoulConnect
- 2-week rotating challenge schedule
- Point system and streak tracking
- Gamification & engagement mechanics
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import json

# ============================================================================
# CHALLENGE DEFINITIONS
# ============================================================================

class ChallengeType(str, Enum):
    MEDITATION = "meditation"
    BREATHING = "breathing"
    JOURNAL = "journal"
    GRATITUDE = "gratitude"
    YOGA = "yoga"
    REFLECTION = "reflection"
    CHAT = "chat_support"
    HEALER = "healer_session"

@dataclass
class Challenge:
    """Individual challenge definition"""
    id: str
    name: str
    description: str
    challenge_type: ChallengeType
    duration_minutes: int
    points: int  # Base points
    icon: str
    difficulty: str  # easy, medium, hard
    instructions: str = ""

# Pre-defined challenges
CHALLENGE_LIBRARY = {
    "breathing_3min": Challenge(
        id="breathing_3min",
        name="3-Min Breathing",
        description="Deep breathing exercise to calm your mind",
        challenge_type=ChallengeType.BREATHING,
        duration_minutes=3,
        points=30,
        icon="🌬️",
        difficulty="easy",
        instructions="Breathe in for 4 counts, hold for 4, exhale for 4. Repeat 15 times."
    ),
    "gratitude_journal": Challenge(
        id="gratitude_journal",
        name="Gratitude Journal",
        description="Write 3 things you're grateful for today",
        challenge_type=ChallengeType.GRATITUDE,
        duration_minutes=5,
        points=50,
        icon="📔",
        difficulty="easy",
        instructions="Reflect and write about what you're thankful for."
    ),
    "meditation_5min": Challenge(
        id="meditation_5min",
        name="5-Min Meditation",
        description="Guided meditation for peace and clarity",
        challenge_type=ChallengeType.MEDITATION,
        duration_minutes=5,
        points=70,
        icon="🧘",
        difficulty="medium",
        instructions="Find a quiet space and follow the meditation guide."
    ),
    "yoga_10min": Challenge(
        id="yoga_10min",
        name="10-Min Yoga",
        description="Gentle yoga flow for body and mind",
        challenge_type=ChallengeType.YOGA,
        duration_minutes=10,
        points=80,
        icon="🧘‍♀️",
        difficulty="medium",
        instructions="Follow the yoga sequence at your own pace."
    ),
    "reflection": Challenge(
        id="reflection",
        name="Daily Reflection",
        description="Reflect on today's experiences and learnings",
        challenge_type=ChallengeType.REFLECTION,
        duration_minutes=5,
        points=40,
        icon="💭",
        difficulty="easy",
        instructions="Think about what you learned and how you grew today."
    ),
    "journal_deep": Challenge(
        id="journal_deep",
        name="Deep Journal",
        description="Write freely about your feelings and thoughts",
        challenge_type=ChallengeType.JOURNAL,
        duration_minutes=10,
        points=60,
        icon="✍️",
        difficulty="medium",
        instructions="Write without judgment about what's on your mind."
    ),
    "chat_support": Challenge(
        id="chat_support",
        name="Peer Support Chat",
        description="Connect with someone for emotional support",
        challenge_type=ChallengeType.CHAT,
        duration_minutes=15,
        points=100,
        icon="💬",
        difficulty="hard",
        instructions="Join a peer support session."
    ),
    "healer_session": Challenge(
        id="healer_session",
        name="Healer Session",
        description="Book a session with a professional healer",
        challenge_type=ChallengeType.HEALER,
        duration_minutes=30,
        points=150,
        icon="✨",
        difficulty="hard",
        instructions="Schedule and complete a healer session."
    ),
    "breathing_extended": Challenge(
        id="breathing_extended",
        name="Extended Breathing",
        description="Advanced breathing techniques (10 min)",
        challenge_type=ChallengeType.BREATHING,
        duration_minutes=10,
        points=60,
        icon="🌬️",
        difficulty="medium",
        instructions="Practice box breathing: 4-4-4-4 for 10 minutes."
    ),
    "meditation_guided": Challenge(
        id="meditation_guided",
        name="Guided Meditation",
        description="10-minute guided meditation",
        challenge_type=ChallengeType.MEDITATION,
        duration_minutes=10,
        points=100,
        icon="🧘",
        difficulty="medium",
        instructions="Follow the guided meditation audio."
    ),
    "affirmations": Challenge(
        id="affirmations",
        name="Daily Affirmations",
        description="Speak positive affirmations for yourself",
        challenge_type=ChallengeType.REFLECTION,
        duration_minutes=3,
        points=25,
        icon="💫",
        difficulty="easy",
        instructions="Repeat 5 positive affirmations out loud."
    ),
    "nature_walk": Challenge(
        id="nature_walk",
        name="Nature Walk",
        description="Take a mindful walk in nature (15 min)",
        challenge_type=ChallengeType.REFLECTION,
        duration_minutes=15,
        points=75,
        icon="🌿",
        difficulty="medium",
        instructions="Walk mindfully and observe your surroundings."
    ),
}

# ============================================================================
# 2-WEEK CHALLENGE ROTATION SCHEDULE
# ============================================================================

TWO_WEEK_SCHEDULE = [
    # WEEK 1
    {
        "day": 1,
        "challenges": ["breathing_3min", "gratitude_journal", "meditation_5min"],
        "theme": "Mindfulness Basics"
    },
    {
        "day": 2,
        "challenges": ["meditation_5min", "reflection", "breathing_3min"],
        "theme": "Inner Peace"
    },
    {
        "day": 3,
        "challenges": ["gratitude_journal", "yoga_10min", "breathing_3min"],
        "theme": "Body & Mind"
    },
    {
        "day": 4,
        "challenges": ["journal_deep", "meditation_5min", "affirmations"],
        "theme": "Self Discovery"
    },
    {
        "day": 5,
        "challenges": ["breathing_extended", "reflection", "meditation_guided"],
        "theme": "Deep Healing"
    },
    {
        "day": 6,
        "challenges": ["yoga_10min", "journal_deep", "breathing_3min"],
        "theme": "Balance & Flow"
    },
    {
        "day": 7,
        "challenges": ["meditation_guided", "gratitude_journal", "nature_walk"],
        "theme": "Connection"
    },
    # WEEK 2
    {
        "day": 8,
        "challenges": ["breathing_3min", "meditation_5min", "journal_deep"],
        "theme": "Reset Week"
    },
    {
        "day": 9,
        "challenges": ["affirmations", "yoga_10min", "reflection"],
        "theme": "Empowerment"
    },
    {
        "day": 10,
        "challenges": ["meditation_guided", "breathing_extended", "gratitude_journal"],
        "theme": "Abundance"
    },
    {
        "day": 11,
        "challenges": ["chat_support", "journal_deep", "breathing_3min"],
        "theme": "Connection"
    },
    {
        "day": 12,
        "challenges": ["yoga_10min", "meditation_5min", "reflection"],
        "theme": "Integration"
    },
    {
        "day": 13,
        "challenges": ["nature_walk", "breathing_extended", "meditation_guided"],
        "theme": "Renewal"
    },
    {
        "day": 14,
        "challenges": ["gratitude_journal", "journal_deep", "breathing_3min"],
        "theme": "Gratitude & Release"
    },
]

# ============================================================================
# CORE ALGORITHM
# ============================================================================

class DailyChallengesTracker:
    """Main algorithm for daily challenges"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.challenges_completed: Dict[str, bool] = {}
        self.completion_dates: Dict[str, datetime] = {}
        self.current_streak: int = 0
        self.longest_streak: int = 0
        self.total_points: int = 0
        self.last_completion_date: Optional[datetime] = None
    
    def get_current_cycle_day(self, reference_date: datetime = None) -> int:
        """
        Get which day of the 2-week cycle we're on.
        
        Cycle repeats every 14 days starting from a reference date.
        """
        if reference_date is None:
            reference_date = datetime.now()
        
        # You can set a "cycle start date" for your app
        # For now, we'll use the epoch (Jan 1, 2024)
        cycle_start = datetime(2024, 1, 1)
        
        days_since_cycle_start = (reference_date - cycle_start).days
        cycle_day = (days_since_cycle_start % 14) + 1
        
        return cycle_day
    
    def get_todays_challenges(self, reference_date: datetime = None) -> List[Dict]:
        """Get the 3 challenges for today based on 2-week rotation"""
        
        cycle_day = self.get_current_cycle_day(reference_date)
        
        # Get schedule for this day
        day_schedule = TWO_WEEK_SCHEDULE[cycle_day - 1]
        
        # Fetch challenge objects
        challenges = []
        for challenge_id in day_schedule["challenges"]:
            challenge = CHALLENGE_LIBRARY[challenge_id]
            challenges.append({
                "id": challenge.id,
                "name": challenge.name,
                "description": challenge.description,
                "type": challenge.challenge_type.value,
                "duration": challenge.duration_minutes,
                "points": challenge.points,
                "icon": challenge.icon,
                "difficulty": challenge.difficulty,
                "instructions": challenge.instructions,
                "completed": self.is_challenge_completed(challenge.id),
                "streak_bonus": self.calculate_streak_bonus()
            })
        
        return challenges
    
    def is_challenge_completed(self, challenge_id: str, date: datetime = None) -> bool:
        """Check if a specific challenge is completed today"""
        
        if date is None:
            date = datetime.now()
        
        today = date.date()
        key = f"{challenge_id}_{today}"
        
        return key in self.challenges_completed and self.challenges_completed[key]
    
    def complete_challenge(
        self, 
        challenge_id: str, 
        completion_date: datetime = None,
        actual_duration: int = None
    ) -> Dict:
        """
        Mark a challenge as completed and calculate points.
        
        Args:
            challenge_id: ID of the challenge
            completion_date: When it was completed (default: now)
            actual_duration: How long it actually took (for bonus calculation)
        """
        
        if completion_date is None:
            completion_date = datetime.now()
        
        today = completion_date.date()
        key = f"{challenge_id}_{today}"
        
        # Get challenge details
        challenge = CHALLENGE_LIBRARY[challenge_id]
        
        # Calculate points
        base_points = challenge.points
        streak_bonus = self.calculate_streak_bonus()
        time_bonus = 0
        
        # Bonus if completed faster than expected
        if actual_duration and actual_duration < challenge.duration_minutes:
            time_bonus = int((challenge.duration_minutes - actual_duration) * 5)
        
        total_points = base_points + streak_bonus + time_bonus
        
        # Mark as completed
        self.challenges_completed[key] = True
        self.completion_dates[key] = completion_date
        
        # Update streak
        self.update_streak(completion_date)
        
        # Add points
        self.total_points += total_points
        
        return {
            "challenge_id": challenge_id,
            "challenge_name": challenge.name,
            "base_points": base_points,
            "streak_bonus": streak_bonus,
            "time_bonus": time_bonus,
            "total_points": total_points,
            "current_streak": self.current_streak,
            "total_earned": self.total_points
        }
    
    def calculate_streak_bonus(self) -> int:
        """
        Calculate bonus points based on current streak.
        
        Streak formula:
        - Day 1: 0 bonus
        - Day 2: 5 pts
        - Day 3: 10 pts
        - Day 4+: 5 * day
        """
        if self.current_streak <= 1:
            return 0
        elif self.current_streak == 2:
            return 5
        elif self.current_streak == 3:
            return 10
        else:
            return 5 * self.current_streak
    
    def update_streak(self, completion_date: datetime) -> None:
        """
        Update streak tracking.
        
        Streak increments if:
        - Challenge completed today AND
        - Previous day had a completion OR it's day 1
        """
        
        today = completion_date.date()
        yesterday = today - timedelta(days=1)
        
        # Check if completed yesterday
        yesterday_completed = any(
            key.endswith(str(yesterday)) 
            for key in self.challenges_completed 
            if self.challenges_completed[key]
        )
        
        # Check if completed today
        today_completed = any(
            key.endswith(str(today)) 
            for key in self.challenges_completed 
            if self.challenges_completed[key]
        )
        
        if today_completed:
            if yesterday_completed or self.current_streak == 0:
                self.current_streak += 1
                
                # Update longest streak
                if self.current_streak > self.longest_streak:
                    self.longest_streak = self.current_streak
            else:
                # Streak broken, reset
                self.current_streak = 1
        
        self.last_completion_date = completion_date
    
    def get_daily_progress(self, reference_date: datetime = None) -> Dict:
        """Get progress for today"""
        
        if reference_date is None:
            reference_date = datetime.now()
        
        challenges = self.get_todays_challenges(reference_date)
        completed_count = sum(1 for c in challenges if c["completed"])
        total_count = len(challenges)
        total_points = sum(c["points"] for c in challenges)
        
        # Calculate points earned today
        today_points = 0
        for challenge in challenges:
            if challenge["completed"]:
                today_points += challenge["points"] + challenge["streak_bonus"]
        
        # Points remaining
        remaining_points = total_points - today_points + (total_count - completed_count) * self.calculate_streak_bonus()
        
        return {
            "cycle_day": self.get_current_cycle_day(reference_date),
            "challenges": challenges,
            "completed": completed_count,
            "total": total_count,
            "points_earned_today": today_points,
            "points_remaining": max(0, remaining_points),
            "current_streak": self.current_streak,
            "longest_streak": self.longest_streak,
            "total_points": self.total_points
        }
    
    def get_weekly_summary(self, reference_date: datetime = None) -> Dict:
        """Get summary for the current 2-week cycle"""
        
        if reference_date is None:
            reference_date = datetime.now()
        
        cycle_day = self.get_current_cycle_day(reference_date)
        
        summary = {
            "cycle_day": cycle_day,
            "theme": TWO_WEEK_SCHEDULE[cycle_day - 1]["theme"],
            "days_completed": 0,
            "challenges_completed": 0,
            "total_points_cycle": 0,
            "daily_breakdown": []
        }
        
        # Calculate for each day so far in this cycle
        cycle_start = reference_date - timedelta(days=cycle_day - 1)
        
        for day in range(1, cycle_day + 1):
            day_date = cycle_start + timedelta(days=day - 1)
            day_challenges = self.get_todays_challenges(day_date)
            
            completed = sum(1 for c in day_challenges if c["completed"])
            total = len(day_challenges)
            day_points = sum(c["points"] for c in day_challenges if c["completed"])
            
            summary["daily_breakdown"].append({
                "day": day,
                "completed": completed,
                "total": total,
                "points": day_points
            })
            
            summary["days_completed"] += (1 if completed == total else 0)
            summary["challenges_completed"] += completed
            summary["total_points_cycle"] += day_points
        
        return summary
    
    def get_leaderboard_position(self, all_users_points: Dict[str, int]) -> Dict:
        """
        Get user's position on leaderboard.
        
        Args:
            all_users_points: Dict of {user_id: total_points}
        """
        
        sorted_users = sorted(all_users_points.items(), key=lambda x: x[1], reverse=True)
        
        position = next(
            (i + 1 for i, (uid, _) in enumerate(sorted_users) if uid == self.user_id),
            len(sorted_users) + 1
        )
        
        return {
            "user_id": self.user_id,
            "position": position,
            "total_users": len(all_users_points),
            "user_points": self.total_points,
            "points_to_next": (
                sorted_users[position - 2][1] - self.total_points 
                if position > 1 else 0
            )
        }


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Initialize tracker for a user
    tracker = DailyChallengesTracker("user_amol")
    
    # Simulate 3 days of activity
    print("=== SIMULATING 3 DAYS OF CHALLENGES ===\n")
    
    for day in range(3):
        date = datetime.now() - timedelta(days=2-day)
        
        print(f"--- Day {day + 1}: {date.strftime('%A, %B %d')} ---")
        
        progress = tracker.get_daily_progress(date)
        
        print(f"Cycle Day: {progress['cycle_day']}/14")
        print(f"Challenges: {progress['completed']}/{progress['total']} completed")
        print(f"Current Streak: {progress['current_streak']} days")
        print(f"Total Points: {progress['total_points']}\n")
        
        # Simulate completing challenges
        challenges = tracker.get_todays_challenges(date)
        for i, challenge in enumerate(challenges[:2]):  # Complete first 2
            result = tracker.complete_challenge(challenge["id"], date)
            print(f"  ✓ {result['challenge_name']}: +{result['total_points']} pts "
                  f"(base: {result['base_points']}, streak bonus: {result['streak_bonus']})")
        
        print()
    
    # Final report
    print("\n=== FINAL REPORT ===")
    final_progress = tracker.get_daily_progress()
    print(f"Total Points Earned: {final_progress['total_points']}")
    print(f"Current Streak: {final_progress['current_streak']} days")
    print(f"Longest Streak: {tracker.longest_streak} days")
    
    print("\n=== CYCLE SUMMARY ===")
    weekly = tracker.get_weekly_summary()
    print(f"Theme: {weekly['theme']}")
    print(f"Days Completed: {weekly['days_completed']}/3")
    print(f"Challenges Completed: {weekly['challenges_completed']}")
    print(f"Points This Cycle: {weekly['total_points_cycle']}")
