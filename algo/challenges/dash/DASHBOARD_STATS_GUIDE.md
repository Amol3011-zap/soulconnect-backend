# Dashboard Stats - Implementation Guide

## 🎯 What You're Building

A dashboard with 4 stat cards that show real-time metrics:

```
┌──────────────┬──────────────────┬──────────────┬────────────────┐
│   🧘 7       │  🌍 1,247        │   ⚡ 847     │   🔔 3         │
│ Day Healing  │ Souls healing    │ Soul Points  │ Healing        │
│ Streak       │ right now        │              │ Sessions       │
│ Best: 14     │ ● LIVE           │ Level 3→4    │ This week:+2   │
│              │                  │ 153 pts left │                │
└──────────────┴──────────────────┴──────────────┴────────────────┘
```

---

## 📦 Files You Got

### Backend (3 files):

1. **`dashboard_stats_algorithm.py`** (~450 lines)
   - Core algorithm for all 4 metrics
   - Pure Python, no dependencies
   - Classes: HealingStreakTracker, LevelSystem, HealingSessionsTracker, DashboardStats

2. **`dashboard_routes.py`** (~200 lines)
   - FastAPI routes for all endpoints
   - 10+ endpoints ready to use
   - Sync methods for Soul Journey + Daily Challenges

### Frontend (1 file):

3. **`DashboardStats.jsx`** (~180 lines)
   - React component matching your design
   - Shows 4 stat cards
   - Real-time updates every 30 seconds

---

## 🚀 Quick Setup (10 Minutes)

### Backend:

```bash
# 1. Copy files
cp dashboard_stats_algorithm.py your_project/
cp dashboard_routes.py your_project/

# 2. Add to your FastAPI app (main.py)
from dashboard_routes import router as dashboard_router
app.include_router(dashboard_router)

# 3. Test it
curl http://localhost:8000/api/v1/dashboard/user_123/stats
```

### Frontend:

```bash
# 1. Copy component
cp DashboardStats.jsx src/components/

# 2. Use it
import DashboardStats from './components/DashboardStats';

export default function Dashboard() {
  return <DashboardStats userId={user.id} />;
}

# 3. Done!
```

---

## 📊 Metric 1: Day Healing Streak

**What it tracks:** Consecutive days of healing activities

**Activities that count:**
- Meditation
- Yoga
- Breathing exercises
- Journaling
- Chat sessions
- Healer bookings

**How it works:**

```python
Day 1: User meditates          → Streak = 1
Day 2: User does yoga          → Streak = 2
Day 3: User journals           → Streak = 3
Day 4: User does nothing       → Streak = 0 (BROKEN)
Day 5: User breathes           → Streak = 1 (restart)
```

**Backend endpoint:**

```python
POST /api/v1/dashboard/{user_id}/streak/log

# Any of these count:
- Challenge completed
- Soul Journey activity logged
- Healing session started
- etc.
```

**Display:**

```
🧘 7
Day Healing Streak
Best: 14 days
```

---

## 🌍 Metric 2: Souls Healing Right Now (LIVE)

**What it tracks:** Number of users currently in healing sessions

**Updates in real-time** (every 30 seconds)

**How it works:**

```python
# When user starts meditation/yoga/chat
POST /api/v1/dashboard/{user_id}/session/start/meditation
→ Count increases by 1

# When user finishes
POST /api/v1/dashboard/{user_id}/session/end
→ Count decreases by 1
```

**Auto-cleanup:**
- Sessions older than 2 hours assumed inactive
- Automatically removed from count

**Backend endpoint:**

```python
GET /api/v1/dashboard/live/count
Returns: { "souls_healing_now": 1247 }

GET /api/v1/dashboard/{user_id}/stats
Returns: { "souls_healing": { "count": 1247, "live": true, ... } }
```

**Display:**

```
🌍 1,247
Souls healing right now
● LIVE (green dot)
```

---

## ⚡ Metric 3: Soul Points & Level System

**What it tracks:** Total points earned, current level, progress to next level

**Points sources:**

```
Daily Challenges:     30-150 pts per challenge
Soul Journey:         Varies by activity
Healing Sessions:     50-100 pts per session
Streak Bonus:         5-50 pts for maintaining streak
```

**Level progression:**

```
Level 1:  0 pts
Level 2:  100 pts
Level 3:  300 pts
Level 4:  600 pts      ← 300 pts to reach this
Level 5:  1000 pts
Level 6:  1500 pts
Level 7:  2100 pts
Level 8:  2800 pts
Level 9:  3600 pts
Level 10: 4500 pts
...continues
```

**How it works:**

```python
# User completes challenge
POST /api/v1/dashboard/{user_id}/points/add
{
  "amount": 50,
  "source": "challenge",
  "description": "Gratitude Journal"
}

# Response shows:
{
  "total_points": 847,
  "current_level": 3,
  "points_to_next": 153,
  "leveled_up": false
}
```

**Display:**

```
⚡ 847
Soul Points
Level 3 · 153 pts to Level 4

[████████░░░░░░] 51% progress
```

---

## 🔔 Metric 4: Healing Sessions

**What it tracks:** Number of healing sessions completed

**Session types:**
- Professional healer (30-60 min)
- Peer chat session (15-30 min)
- Self-guided meditation (5-30 min)
- Yoga session (15-45 min)

**Time period tracked:**
- This week: Last 7 days
- Change from last week
- Total hours invested
- Average session length

**How it works:**

```python
# Log completed session
POST /api/v1/dashboard/{user_id}/session/log
{
  "session_type": "healer",
  "duration_minutes": 30,
  "notes": "Great session with healer"
}

# Response shows:
{
  "this_week": 3,
  "change_from_last_week": 2,
  "total_hours": 12.5,
  "average_session_minutes": 25
}
```

**Display:**

```
🔔 3
Healing Sessions
This week: +2 from last
```

---

## 🔗 Integration with Other Systems

### With Soul Journey:

```python
# When activity is logged to Soul Journey:
1. Send to dashboard_streak/log         → Updates streak
2. Send to dashboard_points/add         → Awards points
3. Counts towards wellness score AND level

# Endpoint provided:
POST /api/v1/dashboard/{user_id}/sync-with-journey
```

### With Daily Challenges:

```python
# When challenge is completed:
1. Send to dashboard_points/add         → Awards points
2. Send to dashboard_streak/log         → Updates streak
3. Counts towards both challenge AND dashboard progress

# Endpoint provided:
POST /api/v1/dashboard/{user_id}/sync-with-challenges
```

### Combined Flow:

```
User completes "5-Min Meditation" challenge
   ↓
Dashboard:    +70 challenge points
              Streak = +1 day
              Level progress
   ↓
Soul Journey: +1 meditation activity
              Wellness score increase
              Stage progress
   ↓
Both systems updated!
```

---

## 📈 API Endpoints Reference

### Get All Stats

```
GET /api/v1/dashboard/{user_id}/stats

Response:
{
  "healing_streak": {
    "current": 7,
    "best": 14,
    "icon": "🧘",
    "label": "Day Healing Streak"
  },
  "souls_healing": {
    "count": 1247,
    "live": true,
    "icon": "🌍",
    "label": "Souls healing right now"
  },
  "soul_points": {
    "current": 847,
    "level": 3,
    "next_level": 4,
    "progress": 51,
    "to_next": 153,
    "icon": "⚡"
  },
  "healing_sessions": {
    "total": 3,
    "change": 2,
    "change_display": "+2",
    "icon": "🔔"
  }
}
```

### Log Healing Activity (Streak)

```
POST /api/v1/dashboard/{user_id}/streak/log

Response:
{
  "current_streak": 8,
  "longest_streak": 14
}
```

### Add Soul Points

```
POST /api/v1/dashboard/{user_id}/points/add

Body:
{
  "amount": 50,
  "source": "challenge",  // or "journey", "session", "streak"
  "description": "Gratitude Journal"
}

Response:
{
  "total_points": 897,
  "current_level": 3,
  "leveled_up": false,
  "points_to_next": 103
}
```

### Get Level Info

```
GET /api/v1/dashboard/{user_id}/points/level

Response:
{
  "current_level": 3,
  "total_points": 847,
  "points_to_next": 153,
  "progress_percentage": 51,
  "next_level_start": 1000
}
```

### Start/End Session

```
POST /api/v1/dashboard/{user_id}/session/start/meditation
POST /api/v1/dashboard/{user_id}/session/start/yoga
POST /api/v1/dashboard/{user_id}/session/start/chat
POST /api/v1/dashboard/{user_id}/session/start/healer

POST /api/v1/dashboard/{user_id}/session/end
```

### Log Completed Session

```
POST /api/v1/dashboard/{user_id}/session/log

Body:
{
  "session_type": "healer",
  "duration_minutes": 30,
  "notes": "Great session"
}

Response:
{
  "total_sessions": 15,
  "this_week": 3
}
```

### Get Weekly Sessions

```
GET /api/v1/dashboard/{user_id}/session/weekly

Response:
{
  "this_week": 3,
  "change_from_last_week": 2,
  "total_hours": 12.5,
  "average_session_minutes": 25
}
```

### Get Live Count (Global)

```
GET /api/v1/dashboard/live/count

Response:
{
  "souls_healing_now": 1247
}
```

---

## 🧪 Testing

### Python Testing:

```bash
# Run the algorithm
python3 dashboard_stats_algorithm.py

# Output:
=== DASHBOARD STATS SIMULATION ===

1️⃣ Logging healing activities...
   Streak: 7 days

2️⃣ Adding Soul Points...
   Level: 3
   Points: 440
   To next level: 160
...
```

### API Testing with curl:

```bash
# Get stats
curl http://localhost:8000/api/v1/dashboard/user_amol/stats | jq

# Log activity
curl -X POST http://localhost:8000/api/v1/dashboard/user_amol/streak/log

# Add points
curl -X POST http://localhost:8000/api/v1/dashboard/user_amol/points/add \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 50,
    "source": "challenge",
    "description": "Gratitude Journal"
  }'

# Log session
curl -X POST http://localhost:8000/api/v1/dashboard/user_amol/session/log \
  -H "Content-Type: application/json" \
  -d '{
    "session_type": "meditation",
    "duration_minutes": 15,
    "notes": "Morning meditation"
  }'

# Get live count
curl http://localhost:8000/api/v1/dashboard/live/count | jq
```

---

## 🎯 Implementation Checklist

### Backend:
- [ ] Copy `dashboard_stats_algorithm.py`
- [ ] Copy `dashboard_routes.py`
- [ ] Add routes to your FastAPI app
- [ ] Test endpoints with curl
- [ ] Set up database models (optional, using in-memory for now)
- [ ] Add auth checks to endpoints

### Frontend:
- [ ] Copy `DashboardStats.jsx`
- [ ] Import in your dashboard page
- [ ] Configure API_BASE_URL
- [ ] Test component renders
- [ ] Verify real-time updates (30-sec refresh)
- [ ] Test all 4 cards display correctly

### Integration:
- [ ] Connect with Soul Journey activities
- [ ] Connect with Daily Challenges
- [ ] Sync points between systems
- [ ] Test complete user flow

### Deployment:
- [ ] Move from in-memory to database storage
- [ ] Add proper authentication
- [ ] Deploy backend
- [ ] Deploy frontend
- [ ] Monitor live count updates

---

## 💡 Pro Tips

1. **Real-time Updates**
   - Component refreshes every 30 seconds
   - Adjust interval in `DashboardStats.jsx` useEffect

2. **Database Integration**
   - Currently uses in-memory storage
   - Create `UserStats` SQLAlchemy model for persistence

3. **Level Design**
   - Adjust `LEVEL_THRESHOLDS` to make levels easier/harder
   - Current: ~300 pts per level (adjust as needed)

4. **Streak Reset**
   - Currently resets after 1 day of inactivity
   - Change logic in `HealingStreakTracker.update_streak()` if needed

5. **Live Count Cleanup**
   - Sessions inactive >2 hours auto-removed
   - Adjust the 2-hour threshold if needed

6. **Points Distribution**
   - Challenge: 30-150 pts
   - Journey: varies
   - Session: 50-100 pts
   - Streak: 10-50 pts (increase with longer streaks)

---

## 🎓 Architecture

```
DashboardStats (Main class)
├── HealingStreakTracker
│   ├── Tracks consecutive days
│   ├── Calculates current/longest streak
│   └── Updates on any healing activity
│
├── LevelSystem
│   ├── Manages total points
│   ├── Calculates current level
│   ├── Tracks progress to next level
│   └── Histories all point transactions
│
├── HealingSessionsTracker
│   ├── Logs completed sessions
│   ├── Calculates weekly stats
│   ├── Tracks total hours
│   └── Shows change from last week
│
└── LiveHealingTracker (Global)
    ├── Tracks active sessions
    ├── Auto-cleanup old sessions
    ├── Returns live count
    └── Updates every request
```

---

## 🚀 Next Steps

1. **Copy files** to your project
2. **Add routes** to FastAPI app
3. **Import component** in React
4. **Test endpoints** with curl
5. **Test component** in browser
6. **Deploy**!

Total time: 30-60 minutes for full integration

---

**Ready to make your dashboard functional?** Start with the quick setup above! 🚀
