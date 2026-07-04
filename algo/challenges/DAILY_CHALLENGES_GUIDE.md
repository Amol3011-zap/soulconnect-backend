# Daily Challenges Algorithm - Complete Guide

## 🎯 System Overview

**Goal:** Gamify user engagement with daily challenges that:
- ✅ Rotate every 2 weeks (14-day cycle)
- ✅ Auto-repeat after 2 weeks
- ✅ Award points for completion
- ✅ Track streaks for motivation
- ✅ Show progress daily

---

## 📊 How It Works

### 1. 2-Week Rotation System

```
CYCLE: Repeats every 14 days

Day 1  → [Challenge A, B, C]
Day 2  → [Challenge D, E, F]
Day 3  → [Challenge G, H, I]
...
Day 14 → [Challenge X, Y, Z]

After Day 14 → Repeats from Day 1 (same challenges)

Timeline:
Jan 1-14: Cycle 1
Jan 15-28: Cycle 2 (same challenges as Jan 1-14)
Jan 29-Feb 11: Cycle 3 (same challenges)
...continues forever
```

### 2. Daily Challenge Assignment

Each day has **exactly 3 challenges**:

```
Day 1 (Theme: Mindfulness Basics)
├── 3-Min Breathing       (+30 pts, easy)
├── Gratitude Journal     (+50 pts, easy)
└── 5-Min Meditation      (+70 pts, medium)

Day 2 (Theme: Inner Peace)
├── 5-Min Meditation      (+70 pts, medium)
├── Daily Reflection      (+40 pts, easy)
└── 3-Min Breathing       (+30 pts, easy)
```

### 3. Points System

```
BASE POINTS = Challenge difficulty
- Easy challenges: 30-50 pts
- Medium challenges: 60-100 pts
- Hard challenges: 100-150 pts

STREAK BONUS (extra points for completing daily)
- Day 1: 0 bonus
- Day 2: +5 pts
- Day 3: +10 pts
- Day 4+: +(5 × streak_day) pts

TIME BONUS (optional: if completed faster than expected)
- For each minute under the target: +5 pts

TOTAL = Base Points + Streak Bonus + Time Bonus
```

**Example Day 2:**
```
Completed: 3-Min Breathing
Base Points:     30
Streak Bonus:    10 (Day 3 streak)
Time Bonus:      0 (took exactly 3 min)
─────────────────────
Total:          40 pts
```

### 4. Streak Mechanics

```
STREAK = Number of consecutive days with ≥ 1 challenge completed

How it works:
Day 1: Complete any challenge → Streak = 1
Day 2: Complete any challenge → Streak = 2
Day 3: Complete any challenge → Streak = 3
Day 3: Miss challenges → Streak = 0 (BROKEN)
Day 4: Complete challenge → Streak = 1 (restart)

Motivation:
- Higher streak = higher bonus points
- Visual indicator to keep users engaged
- Leaderboard/social features possible
```

---

## 🔄 Challenge Rotation - 2 Week Schedule

### Week 1

| Day | Theme | Challenges |
|-----|-------|-----------|
| 1 | Mindfulness Basics | Breathing, Gratitude, Meditation |
| 2 | Inner Peace | Meditation, Reflection, Breathing |
| 3 | Body & Mind | Gratitude, Yoga, Breathing |
| 4 | Self Discovery | Deep Journal, Meditation, Affirmations |
| 5 | Deep Healing | Extended Breathing, Reflection, Guided Meditation |
| 6 | Balance & Flow | Yoga, Deep Journal, Breathing |
| 7 | Connection | Guided Meditation, Gratitude, Nature Walk |

### Week 2

| Day | Theme | Challenges |
|-----|-------|-----------|
| 8 | Reset Week | Breathing, Meditation, Deep Journal |
| 9 | Empowerment | Affirmations, Yoga, Reflection |
| 10 | Abundance | Guided Meditation, Extended Breathing, Gratitude |
| 11 | Connection | Peer Support Chat, Deep Journal, Breathing |
| 12 | Integration | Yoga, Meditation, Reflection |
| 13 | Renewal | Nature Walk, Extended Breathing, Guided Meditation |
| 14 | Gratitude & Release | Gratitude, Deep Journal, Breathing |

**Then repeats from Day 1**

---

## 💻 Core Functions

### 1. Get Current Cycle Day

```python
def get_current_cycle_day(reference_date) -> int:
    """
    Returns: 1-14 (which day of the 2-week cycle)
    
    Example:
    - Jan 1, 2024: Day 1
    - Jan 7, 2024: Day 7
    - Jan 15, 2024: Day 1 (cycle repeats)
    - Jan 21, 2024: Day 7
    """
```

### 2. Get Today's Challenges

```python
def get_todays_challenges(reference_date) -> List[Challenge]:
    """
    Returns: 3 challenges for today based on cycle day
    
    Example output:
    [
        {
            "id": "breathing_3min",
            "name": "3-Min Breathing",
            "points": 30,
            "completed": False,  # Not done yet
            "streak_bonus": 10
        },
        ...
    ]
    """
```

### 3. Complete Challenge

```python
def complete_challenge(challenge_id, actual_duration=None) -> Dict:
    """
    Mark challenge as done and calculate points
    
    Returns:
    {
        "challenge_name": "3-Min Breathing",
        "base_points": 30,
        "streak_bonus": 10,
        "time_bonus": 0,
        "total_points": 40,
        "current_streak": 3
    }
    """
```

### 4. Get Daily Progress

```python
def get_daily_progress() -> Dict:
    """
    Returns: Complete today's status
    
    {
        "cycle_day": 5,
        "challenges": [...],
        "completed": 1,  # Done 1/3
        "total": 3,
        "points_earned_today": 40,
        "points_remaining": 90,
        "current_streak": 3,
        "total_points": 1250
    }
    """
```

---

## 🎮 Challenge Types (Expandable)

```python
MEDITATION        # Guided meditation, various lengths
BREATHING         # Breathing exercises
JOURNAL           # Journaling prompts
GRATITUDE         # Gratitude exercises
YOGA              # Yoga routines
REFLECTION        # Self-reflection
CHAT              # Peer support chat
HEALER            # Professional healer session

Each type:
- Has fixed duration (3-30 min)
- Awards points based on difficulty
- Can be repeated/rotated
```

---

## 📈 Daily Progress Example

### Morning (No challenges done yet)

```
┌─────────────────────────────────┐
│ Complete 3 challenges for 150 pts│
├─────────────────────────────────┤
│ ○ 3-Min Breathing      +30 pts   │
│ ○ Gratitude Journal    +50 pts   │
│ ○ 5-Min Meditation     +70 pts   │
├─────────────────────────────────┤
│ 0 of 3 completed · 150 pts left  │
│ Streak: 3 days 🔥                │
└─────────────────────────────────┘
```

### Mid-day (1 challenge done)

```
┌─────────────────────────────────┐
│ Complete 3 challenges for 150 pts│
├─────────────────────────────────┤
│ ✓ 3-Min Breathing      +40 pts   │ (30 base + 10 streak)
│ ○ Gratitude Journal    +50 pts   │
│ ○ 5-Min Meditation     +70 pts   │
├─────────────────────────────────┤
│ 1 of 3 completed · 120 pts left  │
│ Streak: 3 days 🔥                │
└─────────────────────────────────┘
```

### Evening (All done!)

```
┌─────────────────────────────────┐
│ Complete 3 challenges for 150 pts│
├─────────────────────────────────┤
│ ✓ 3-Min Breathing      +40 pts   │
│ ✓ Gratitude Journal    +60 pts   │
│ ✓ 5-Min Meditation     +80 pts   │
├─────────────────────────────────┤
│ 3 of 3 completed · 0 pts left    │
│ Streak: 4 days 🔥                │
│ Total Earned: 1330 pts           │
└─────────────────────────────────┘
```

---

## 🏆 Gamification Features

### 1. Daily Missions
- 3 specific challenges each day
- Changes every day for 14 days
- Then repeats

### 2. Streak Tracking
- Visual fire emoji 🔥
- Increasing multiplier (2x, 3x, 4x+)
- Day count display

### 3. Points System
- Visual progress bar
- "Points Remaining" counter
- Bonus opportunities shown

### 4. Weekly Themes
- Each week has a theme (Mindfulness, Inner Peace, etc.)
- Creates narrative/journey
- Helps users feel progression

### 5. Leaderboard (Optional)
- Compare total points with friends
- Position on global leaderboard
- "Points to next rank" indicator

---

## 🔧 Integration with Soul Journey

**How they work together:**

```
Soul Journey Tracking:
- Logs activities (meditation, journaling, etc.)
- Calculates wellness score
- Tracks stage progression
- Long-term growth metric

Daily Challenges:
- Gamifies specific actions
- Encourages daily engagement
- Short-term motivation
- Quick wins

Combined:
User does meditation for Daily Challenge
↓
Logs as activity in Soul Journey
↓
Contributes to both challenge points AND wellness score
↓
Advances both gamified progress AND stage progress
```

---

## 📊 Database Schema

```python
@dataclass
class UserChallenge:
    user_id: str
    challenge_id: str
    challenge_date: datetime
    completed: bool
    completion_time: datetime = None
    actual_duration: int = None  # minutes taken
    points_earned: int = 0

# Tables needed:
- user_challenges (completed challenges)
- user_challenge_streaks (current/longest streaks)
- user_challenge_points (total points earned)

# Indexes:
- (user_id, challenge_date)  # Fast lookup for today's challenges
- (user_id, completion_date) # Fast streak calculation
```

---

## 🚀 How to Implement

### Backend (Python/FastAPI)

```python
from daily_challenges_algorithm import DailyChallengesTracker

@app.get("/api/v1/challenges/{user_id}/today")
async def get_today_challenges(user_id: str):
    tracker = DailyChallengesTracker(user_id)
    progress = tracker.get_daily_progress()
    return progress

@app.post("/api/v1/challenges/{user_id}/complete/{challenge_id}")
async def complete_challenge(user_id: str, challenge_id: str):
    tracker = DailyChallengesTracker(user_id)
    result = tracker.complete_challenge(challenge_id)
    return result

@app.get("/api/v1/challenges/{user_id}/weekly-summary")
async def get_weekly_summary(user_id: str):
    tracker = DailyChallengesTracker(user_id)
    summary = tracker.get_weekly_summary()
    return summary
```

### Frontend (React)

```jsx
import DailyChallengesWidget from './components/DailyChallenges';

export default function Dashboard() {
  return (
    <div>
      <DailyChallengesWidget userId={user.id} />
      <SoulJourneyDashboard userId={user.id} />
    </div>
  );
}
```

---

## 📈 Repeat Cycle Explanation

### Timeline

```
JANUARY 2024
├─ Jan 1-14  (Cycle 1, Day 1-14)
│  └─ Same challenges repeat daily on same cycle day
├─ Jan 15-28 (Cycle 2, Day 1-14)
│  └─ Same challenges as Jan 1-14, just repeated
└─ Jan 29-... (Cycle 3, etc.)
   └─ Continues indefinitely

User's perspective:
- "I've seen these challenges before!" (on cycle day repeat)
- But with accumulated points from previous cycles
- Streak continues across cycles
- Leaderboard adds competition
```

### Why 2 Weeks?

✅ **Benefits:**
- Long enough to be varied (14 different daily themes)
- Short enough to remember challenges
- 2 weeks = natural mental cycle
- Easy to explain to users
- Good balance of novelty and routine

---

## 🎯 Key Metrics to Track

For analytics/retention:

```
1. Daily Completion Rate
   - % of users completing ≥1 challenge
   - % completing all 3

2. Average Streak Length
   - How long users engage consecutively
   - When do they drop off?

3. Challenge Popularity
   - Which challenges completed most?
   - Which are skipped?

4. Points Distribution
   - Average points earned per user
   - Engagement progression

5. Repeat Cycle Retention
   - Do users stay when cycle repeats?
   - Do they get bored after 2 weeks?
```

---

## ✨ Future Enhancements

1. **Difficulty Scaling**
   - Increase difficulty as user completes more cycles
   
2. **Seasonal Themes**
   - Different challenges for different seasons
   
3. **Challenges Based on Weakness**
   - If user avoids meditation, feature more meditation
   
4. **Custom Challenges**
   - Let users create their own challenges
   
5. **Social Features**
   - Friends' challenges displayed
   - Cooperative challenges
   - Challenges against friends

6. **Achievements/Badges**
   - "7-Day Streak" badge
   - "100 Points in a Day" achievement
   - "Complete All 14 Days" medal

---

## 📋 Summary

| Feature | How It Works |
|---------|-------------|
| **Rotation** | 2-week cycle, 3 challenges/day, repeats |
| **Points** | Base + Streak Bonus + Time Bonus |
| **Streaks** | Days with ≥1 challenge completed |
| **Cycle Reset** | Automatic every 14 days, same challenges |
| **User Motivation** | Points, streaks, themes, progress bars |
| **Integration** | Works with Soul Journey tracking |

---

Ready to implement? The algorithm handles all the logic - just build the UI! 🚀
