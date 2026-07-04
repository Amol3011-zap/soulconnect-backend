# Daily Challenges - Quick Implementation Guide

## 📦 What You Got

### 3 Files:

1. **`daily_challenges_algorithm.py`** - Backend logic
2. **`DAILY_CHALLENGES_GUIDE.md`** - Complete documentation
3. **`DailyChallengesWidget.jsx`** - React UI component

---

## 🎯 How It Works (Simple Explanation)

```
CONCEPT:
- User gets 3 new challenges EVERY DAY
- Every 14 days, the challenges repeat (same order)
- Complete challenges = earn points
- Maintain streak = earn bonus points
- After 2 weeks, cycle restarts

TIMELINE:
Jan 1-14:   Cycle 1 (Days 1-14)
Jan 15-28:  Cycle 2 (Same days 1-14 repeat)
Jan 29+:    Cycle 3 (Same days 1-14 repeat)
...forever

USER EXPERIENCE:
Day 1: "3-Min Breathing, Gratitude Journal, 5-Min Meditation"
Day 2: "5-Min Meditation, Daily Reflection, 3-Min Breathing"
...
Day 14: "Gratitude, Deep Journal, Breathing"
Day 15: Back to Day 1 challenges (but with accumulated points)
```

---

## 🚀 Quick Start (5 Minutes)

### Backend Setup:

```bash
# 1. Copy algorithm file to your project
cp daily_challenges_algorithm.py your_project/

# 2. Import in your FastAPI app
from daily_challenges_algorithm import DailyChallengesTracker

# 3. Create endpoints
@app.get("/api/v1/challenges/{user_id}/today")
async def get_today_challenges(user_id: str):
    tracker = DailyChallengesTracker(user_id)
    return tracker.get_daily_progress()

@app.post("/api/v1/challenges/{user_id}/complete/{challenge_id}")
async def complete_challenge(user_id: str, challenge_id: str):
    tracker = DailyChallengesTracker(user_id)
    return tracker.complete_challenge(challenge_id)
```

### Frontend Setup:

```jsx
// 1. Copy component to your project
cp DailyChallengesWidget.jsx src/components/

// 2. Import and use
import DailyChallengesWidget from './components/DailyChallengesWidget';

export default function Dashboard() {
  return (
    <div>
      <DailyChallengesWidget userId={user.id} />
    </div>
  );
}

// 3. Done! ✅
```

---

## 📊 System at a Glance

### Points System:

```
BASE POINTS (challenge difficulty):
- Easy: 30-50 pts (Breathing, Gratitude)
- Medium: 60-100 pts (Meditation, Yoga)
- Hard: 100-150 pts (Chat, Healer Session)

+ STREAK BONUS (if completed yesterday too):
- Day 2: +5 pts
- Day 3: +10 pts
- Day 4: +20 pts
- Day 5: +25 pts (5 × 5)

+ TIME BONUS (optional):
- If completed faster than expected: +5 pts per minute

EXAMPLE:
User completes "3-Min Breathing" on Day 3 of streak:
Base:         30 pts
Streak Bonus: 10 pts (Day 3)
Time Bonus:   0 pts (took exactly 3 min)
─────────────────────
Total:        40 pts
```

### 2-Week Rotation:

```
WEEK 1
├─ Day 1: Mindfulness Basics
├─ Day 2: Inner Peace
├─ Day 3: Body & Mind
├─ Day 4: Self Discovery
├─ Day 5: Deep Healing
├─ Day 6: Balance & Flow
└─ Day 7: Connection

WEEK 2
├─ Day 8: Reset Week
├─ Day 9: Empowerment
├─ Day 10: Abundance
├─ Day 11: Connection
├─ Day 12: Integration
├─ Day 13: Renewal
└─ Day 14: Gratitude & Release

THEN REPEAT from Day 1
```

### Challenge Types (12 total):

```
Easy (30-50 pts):
- 3-Min Breathing
- Gratitude Journal
- Daily Affirmations
- Daily Reflection

Medium (60-100 pts):
- 5-Min Meditation
- 10-Min Yoga
- Deep Journal
- Extended Breathing
- Guided Meditation
- Nature Walk

Hard (100-150 pts):
- Peer Support Chat
- Healer Session
```

---

## 💾 Database Schema

```python
# Tables needed:

1. user_challenges
   - user_id (FK)
   - challenge_id (string)
   - challenge_date (date)
   - completed (boolean)
   - completion_time (datetime)
   - actual_duration (int)
   - points_earned (int)
   - INDEX: (user_id, challenge_date)

2. user_challenge_streaks
   - user_id (PK)
   - current_streak (int)
   - longest_streak (int)
   - last_completion_date (date)

3. user_challenge_points
   - user_id (PK)
   - total_points (int)
   - points_earned_today (int)
   - points_earned_week (int)
```

---

## 🔄 How Cycles Work

### Determining "Cycle Day":

```python
def get_current_cycle_day(date):
    """Calculate which day of 14-day cycle we're on"""
    
    CYCLE_START = Jan 1, 2024 (or your chosen date)
    days_elapsed = (date - CYCLE_START).days
    cycle_day = (days_elapsed % 14) + 1
    
    return cycle_day  # 1-14
```

### Example Timeline:

```
Jan 1, 2024 (Monday)   → Cycle Day 1
Jan 2, 2024 (Tuesday)  → Cycle Day 2
Jan 3, 2024 (Wednesday)→ Cycle Day 3
...
Jan 14, 2024 (Sunday)  → Cycle Day 14
Jan 15, 2024 (Monday)  → Cycle Day 1 (REPEATS!)
Jan 16, 2024 (Tuesday) → Cycle Day 2
...
Jan 28, 2024 (Sunday)  → Cycle Day 14
Jan 29, 2024 (Monday)  → Cycle Day 1 (REPEATS AGAIN!)
```

### What Happens When It Repeats?

✅ Same challenges appear
✅ User's points carry forward
✅ Streak continues across cycles
✅ Progress bar resets daily but cumulative total continues
✅ Leaderboard points accumulate

---

## 🎮 UI Flow

### Daily View:

```
┌─────────────────────────┐
│ ⚡ Daily Challenges     │
│ Complete 3 for 150 pts  │
├─────────────────────────┤
│ ✓ 3-Min Breathing  +30  │ (Day 7 streak 🔥)
│ ○ Gratitude Journal +50 │
│ ○ 5-Min Meditation +70  │
├─────────────────────────┤
│ 1 of 3 completed        │
│ 120 pts remaining       │
└─────────────────────────┘
```

### User Taps Challenge:

```
1. Challenge Card shows loading spinner
2. Backend processes completion
3. Points calculated (base + streak + time bonus)
4. UI updates:
   - Card shows checkmark ✓
   - Points updated
   - Streak may increase
   - Remaining points decrease
5. Toast notification shows "+40 pts earned!"
```

### After Completing All 3:

```
Celebration UI:
- Confetti animation (optional)
- "You earned 150 points! 🎉"
- Next day's challenges preview
- Leaderboard position update
```

---

## 🔌 API Endpoints

### GET /api/v1/challenges/{user_id}/today

Returns today's 3 challenges and progress:

```json
{
  "cycle_day": 5,
  "challenges": [
    {
      "id": "breathing_3min",
      "name": "3-Min Breathing",
      "points": 30,
      "icon": "🌬️",
      "completed": false,
      "streak_bonus": 10
    },
    // ... 2 more
  ],
  "completed": 1,
  "total": 3,
  "points_earned_today": 40,
  "points_remaining": 110,
  "current_streak": 3,
  "total_points": 1250
}
```

### POST /api/v1/challenges/{user_id}/complete/{challenge_id}

Mark challenge as complete:

```json
{
  "challenge_id": "breathing_3min",
  "challenge_name": "3-Min Breathing",
  "base_points": 30,
  "streak_bonus": 10,
  "time_bonus": 0,
  "total_points": 40,
  "current_streak": 3,
  "total_earned": 1250
}
```

### GET /api/v1/challenges/{user_id}/weekly-summary

Get 2-week cycle progress:

```json
{
  "cycle_day": 5,
  "theme": "Deep Healing",
  "days_completed": 4,
  "challenges_completed": 10,
  "total_points_cycle": 450,
  "daily_breakdown": [
    {"day": 1, "completed": 3, "total": 3, "points": 150},
    {"day": 2, "completed": 3, "total": 3, "points": 160},
    // ... more
  ]
}
```

---

## 🧪 Testing

### Backend Test:

```bash
python3 daily_challenges_algorithm.py
```

Output:
```
=== SIMULATING 3 DAYS OF CHALLENGES ===

--- Day 1: Thursday, June 18 ---
Cycle Day: 1/14
Challenges: 0/3 completed
Current Streak: 0 days
Total Points: 0

  ✓ 3-Min Breathing: +30 pts
  ✓ Gratitude Journal: +50 pts

--- Day 2: Friday, June 19 ---
...and so on
```

### Frontend Test:

```jsx
// In your React app
<DailyChallengesWidget userId="test_user" />

// Should display:
// - 3 challenges for today
// - Points for each
// - Complete/incomplete status
// - Streak indicator
// - "View All Challenges" button
```

---

## 🎯 Integration Checklist

- [ ] Copy `daily_challenges_algorithm.py` to backend
- [ ] Create API endpoints in FastAPI
- [ ] Set up database tables
- [ ] Copy `DailyChallengesWidget.jsx` to frontend
- [ ] Update React imports
- [ ] Test locally with `python3 daily_challenges_algorithm.py`
- [ ] Test API endpoints with curl/Postman
- [ ] Test React component loads and displays
- [ ] Test completing a challenge
- [ ] Verify points calculation
- [ ] Verify streak tracking
- [ ] Deploy to production

---

## 💡 Pro Tips

1. **Customize Challenges**
   Edit `CHALLENGE_LIBRARY` dict to add/remove challenges

2. **Adjust Points**
   Modify base points in challenge definitions

3. **Change Cycle Start Date**
   Edit `CYCLE_START` in `get_current_cycle_day()` function

4. **Add Leaderboard**
   Use `get_leaderboard_position()` method (already in algorithm!)

5. **Add Notifications**
   Show toast when challenge completed or streak milestone hit

6. **Add Persistence**
   Save completed challenges to database so streaks persist across sessions

---

## 🚀 Next Steps

1. **Integrate with Soul Journey**
   - When user completes Daily Challenge, auto-log to Soul Journey
   - Both systems track same activities

2. **Add Leaderboard**
   - Show top 10 users by points
   - Weekly/all-time leaderboards

3. **Add Badges**
   - "7-Day Streak" badge
   - "500 Points" achievement
   - "Perfect Week" (all 3/day for 7 days)

4. **Add Notifications**
   - Daily reminder at morning time
   - "Challenge available!" notification
   - "Streak milestone!" celebration

5. **Add Sharing**
   - Share achievement on social media
   - Challenge friends
   - Show progress in user profile

---

## 📝 Summary

| Aspect | Details |
|--------|---------|
| **Cycle Length** | 14 days (2 weeks) |
| **Challenges/Day** | 3 |
| **Points/Challenge** | 30-150 pts |
| **Repeat Schedule** | Every 14 days, same order |
| **Streak Bonus** | Day 2: +5, Day 3: +10, Day 4+: +5×day |
| **Challenge Types** | 12 different types |
| **Engagement** | Daily action, continuous engagement |

---

**Ready to build?** Start with the backend algorithm, then add the React component! 🚀
