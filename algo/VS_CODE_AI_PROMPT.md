# Soul Journey Tracking System - Integration Prompt for VS Code

You can copy this entire prompt into GitHub Copilot, Claude VS Code extension, or any AI coding assistant in VS Code to integrate the Soul Journey tracking system into your SoulConnect website.

---

## CONTEXT & REQUIREMENTS

**Project**: SoulConnect - Peer-to-peer emotional support platform
**Task**: Integrate Soul Journey progress tracking module into existing website
**Tech Stack**: 
- Frontend: React + Tailwind CSS
- Backend: FastAPI + SQLAlchemy
- Database: PostgreSQL (production)
- Current Status: Full-stack tracker code exists, needs integration

**Files You're Working With**:
1. `soul_journey_tracker.py` - Core algorithm for progress calculation
2. `soul_journey_api.py` - FastAPI backend endpoints
3. `SoulJourneyDashboard.jsx` - React component for UI
4. Existing SoulConnect codebase (FastAPI backend + React frontend)

---

## INTEGRATION REQUIREMENTS

### Backend Integration (FastAPI):

1. **Merge soul_journey_api.py endpoints into existing FastAPI app**
   - Keep database models separate but linkable to Users table
   - Add authentication checks using existing SoulConnect auth
   - Link activities to ChatSessions (when user logs activity after chat, auto-create record)
   - Use existing database connection (don't create new SQLite)

2. **Database Schema Changes**:
   - Add `soul_journey_activities` table with foreign key to `users.id`
   - Optional: Add `soul_journey_checkpoint` table to track stage transitions
   - Ensure all timestamps use timezone-aware UTC

3. **Environment Variables**:
   - DATABASE_URL should use existing connection
   - Add WELLNESS_CALCULATION_WEIGHTS config (for easy tuning)
   - Add STAGE_PROGRESSION_THRESHOLDS config

### Frontend Integration (React):

1. **Add SoulJourneyDashboard component to existing app**
   - Import into main user dashboard
   - Make API_URL use existing axios/fetch instance with auth headers
   - Use existing Tailwind config (match site colors)
   - Add route `/dashboard/journey` or similar

2. **State Management**:
   - Use existing Redux/Context (don't create new store)
   - Dispatch progress updates to existing user state
   - Keep activity logging in sync with chat history

3. **UI Integration Points**:
   - Add "Log Activity" button after chat sessions
   - Display mini wellness score in user header/nav
   - Add journey progress to user profile page
   - Optional: Show wellness score in chat list (visual indicator)

4. **Responsive Design**:
   - Component already uses Tailwind - just verify colors match site
   - Test on mobile (dashboard is sticky form-heavy)
   - Ensure progress bars render correctly on all breakpoints

---

## STEP-BY-STEP IMPLEMENTATION PLAN

**Backend (Backend Dev):**
1. Create migration file: `alembic/versions/xxx_add_soul_journey_tables.py`
2. Extract tracker logic from `soul_journey_api.py` into `app/services/journey_tracker.py`
3. Add endpoints to existing router: `app/api/routes/journey.py`
4. Add database models to `app/models/journey.py`
5. Update `app/schemas/journey.py` with Pydantic models
6. Add middleware to auto-log activities after chat sessions (optional)
7. Add tests in `tests/test_journey_api.py`

**Frontend (Frontend Dev):**
1. Add component: `src/components/SoulJourneyDashboard/index.jsx`
2. Add route to React Router config
3. Create API client: `src/services/journeyApi.js` (using existing axios instance)
4. Add Redux actions (if using Redux): `src/redux/slices/journeySlice.js`
5. Update user header component to show wellness score
6. Add "Log Activity" quick-action button to chat UI
7. Add journey page to sidebar navigation
8. Test integration with existing auth

---

## SPECIFIC IMPLEMENTATION TASKS

### Task 1: Backend Routes
```
Need to create: /api/journey/v1/{user_id}/activity (POST)
Need to create: /api/journey/v1/{user_id}/progress (GET)
Need to create: /api/journey/v1/{user_id}/activities (GET)
Need to create: /api/journey/v1/{user_id}/stats (GET)

Requirements:
- Use existing @router decorator pattern
- Add @require_auth dependency
- Validate user_id matches current user
- Use app.db (existing session)
- Return existing response format/status codes
```

### Task 2: Database Models
```
Need to create:
- ActivityDB model (link to User, ChatSession)
- UserJourneyDB model (stages, milestones)
- Optional: JourneyCheckpointDB (track transitions)

Requirements:
- Use existing base model/mixins
- Add timestamp columns (created_at, updated_at)
- Index on (user_id, date) for fast queries
- Soft delete support if using elsewhere
```

### Task 3: React Component Integration
```
Need to:
- Replace hardcoded API_URL with existing config
- Use existing axios instance with auth headers
- Integrate with Redux/Context (show user wellness in nav)
- Add component to dashboard route
- Handle loading/error states with existing patterns

Requirements:
- Use existing color theme (not hardcoded colors)
- Match existing form/input styling
- Use existing spinner component
- Toast notifications on success/error (existing library)
```

### Task 4: Activity Auto-Logging (Optional but Recommended)
```
When user:
- Completes a chat session → Auto-log CHAT_SESSION activity
- Schedules healer booking → Auto-log HEALER_BOOKING activity
- Journals in app → Auto-log JOURNAL activity

Implementation:
- Create middleware/hook in chat completion flow
- Show "Log intensity" modal (quick 2-step form)
- Default intensity to 5 if skipped
```

---

## CODE SNIPPETS TO INTEGRATE

### Existing Tracker Algorithm (KEEP AS-IS):
```python
# soul_journey_tracker.py - Don't modify core logic
# Just import into: app/services/journey_tracker.py
from app.utils.journey_tracker import SoulJourneyTracker, Activity, ActivityType
```

### Existing React Component (MINIMAL CHANGES):
```jsx
// SoulJourneyDashboard.jsx
// Only changes needed:
// 1. Import useAuth() from your auth context
// 2. Replace API_BASE_URL with: process.env.REACT_APP_API_URL || '/api'
// 3. Add auth headers: headers: { Authorization: `Bearer ${token}` }
// 4. Use existing UI components (spinners, toasts)
```

---

## QUESTIONS TO ANSWER BEFORE STARTING

1. **Database**: PostgreSQL? MySQL? Already set up?
2. **Authentication**: JWT tokens? Session-based? Where's the token stored?
3. **Existing Redux/Context**: Using Redux, Zustand, Context API, or plain state?
4. **User Model**: Does User table have `id`, `email`, etc.? Foreign key names?
5. **Axios Setup**: Is there existing `axiosInstance` with auth headers?
6. **UI Theme**: What color palette? (Component uses purple/blue)
7. **Styling**: Tailwind CSS already configured? Version?
8. **Auto-logging**: Want to auto-log activities after chats or manual-only?
9. **Deployment**: Docker? Vercel? Self-hosted?
10. **Notifications**: Toast library? Snackbar? Alert?

---

## EXPECTED OUTPUT STRUCTURE

After integration, your project structure should look like:

```
backend/
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── journey.py          (NEW - endpoints)
│   ├── models/
│   │   └── journey.py              (NEW - database models)
│   ├── schemas/
│   │   └── journey.py              (NEW - Pydantic models)
│   ├── services/
│   │   └── journey_tracker.py      (NEW - core algorithm)
│   └── main.py                     (MODIFY - add journey routes)
├── alembic/
│   └── versions/
│       └── xxx_add_soul_journey.py (NEW - migration)
└── tests/
    └── test_journey_api.py         (NEW - tests)

frontend/
├── src/
│   ├── components/
│   │   ├── SoulJourneyDashboard/   (NEW)
│   │   │   ├── index.jsx
│   │   │   ├── ActivityForm.jsx
│   │   │   └── ProgressDisplay.jsx
│   │   └── ... (existing)
│   ├── pages/
│   │   └── JourneyPage.jsx         (NEW)
│   ├── services/
│   │   └── journeyApi.js           (NEW - API client)
│   ├── redux/ or context/
│   │   └── journeySlice.js         (NEW - if using Redux)
│   ├── App.jsx                     (MODIFY - add route)
│   └── ... (existing)
└── ... (existing)
```

---

## COMMON PITFALLS TO AVOID

1. ❌ Don't create separate database - use existing connection
2. ❌ Don't hardcode API URLs - use config/env vars
3. ❌ Don't skip auth checks on endpoints
4. ❌ Don't duplicate state management - integrate with existing store
5. ❌ Don't use hardcoded colors - use Tailwind theme config
6. ❌ Don't forget timezone conversion (use UTC)
7. ❌ Don't skip error handling for API calls
8. ❌ Don't ignore loading states in UI
9. ❌ Don't make database queries without indexes
10. ❌ Don't expose user_id in URLs without auth check

---

## TESTING CHECKLIST

Before deployment:
- [ ] Create test user and log 5+ activities
- [ ] Verify progress calculates correctly
- [ ] Check wellness score is 0-10
- [ ] Verify weekly growth shows positive/negative
- [ ] Test stage progression with high-weight activities
- [ ] Check activity history filters (by type, date)
- [ ] Test API auth (reject requests without token)
- [ ] Test database migrations on fresh database
- [ ] Verify UI renders on mobile (< 768px)
- [ ] Check progress updates in real-time
- [ ] Test with production database size (1000+ users)

---

## PROMPT VARIATIONS FOR DIFFERENT TASKS

### For Backend Integration:
```
I'm integrating a Soul Journey progress tracking system into my SoulConnect FastAPI backend. 
[Paste the code blocks from soul_journey_api.py and soul_journey_tracker.py]

My existing FastAPI structure is:
- Database: {PostgreSQL/MySQL/SQLite} with SQLAlchemy
- Auth: {JWT/Session-based} 
- Users table: {describe schema}
- Existing routes in: app/api/routes/

Generate:
1. Migration file for new tables
2. models/journey.py with database models
3. services/journey_tracker.py with algorithm
4. routes/journey.py with endpoints
5. schemas/journey.py with request/response models

Use existing patterns for:
- Database sessions
- Auth dependency injection
- Error handling
- Response models
```

### For Frontend Integration:
```
I'm integrating a Soul Journey React dashboard into my SoulConnect frontend.
[Paste the SoulJourneyDashboard.jsx code]

My existing React setup:
- State management: {Redux/Context/Zustand}
- HTTP client: {axios/fetch} at {path to setup}
- Tailwind: {version and config location}
- Auth: {how tokens stored and accessed}
- UI components: {list any shared components used}

Generate:
1. journeyApi.js service file (with auth headers)
2. journeySlice.js or context (state management)
3. Updated App.jsx with new route
4. Updated Header component to show wellness score
5. ActivityForm component (quick-log modal)

Use existing patterns for:
- API calls with auth
- Loading/error states
- Toast notifications
- Tailwind styling
- Icons/assets
```

### For Database Migration:
```
I need a Alembic migration for these new tables:

Tables to add:
- soul_journey_activities (user_id, activity_type, intensity, date, notes)
- user_journeys (user_id, current_stage, total_activities)

Constraints:
- Foreign key to users.id
- Indexes on (user_id, date)
- Timestamps (created_at, updated_at)
- Use {existing UUID/int} for IDs

Generate Alembic migration file with:
- upgrade() function
- downgrade() function
- Proper constraints and indexes
```

---

## AI CODING ASSISTANT TIPS

**For GitHub Copilot:**
- Use `/explain` to understand generated code
- Use `Ctrl+Shift+A` to trigger inline suggestions
- Use comments to guide code generation

**For Claude VS Code Extension:**
- Paste this entire prompt in Claude chat
- Ask follow-up questions about your specific setup
- Request code review/refactoring suggestions

**For Any AI Assistant:**
1. Ask for one file at a time (easier to review)
2. Ask it to follow your existing code patterns
3. Request error handling for each function
4. Ask for tests alongside implementation code
5. Request docstrings/comments for complex logic

---

## FOLLOW-UP PROMPTS

After initial integration, you might ask:

- "How do I add notifications when user reaches a new stage?"
- "Can we add a leaderboard comparing wellness scores?"
- "How to export journey progress as PDF?"
- "How to add gamification (badges/achievements)?"
- "How to integrate with existing chat history?"
- "Performance optimization for 10k+ users?"
- "How to add social sharing of progress?"
- "How to implement streak tracking?"

---

## QUICK COPY-PASTE COMMANDS

For testing in terminal:
```bash
# Test backend API
python -m pytest tests/test_journey_api.py -v

# Start dev server with journey endpoints
python -m uvicorn app.main:app --reload

# Frontend integration test
npm test -- src/services/journeyApi.test.js

# Check database migrations
alembic current
alembic upgrade head
```

---

**Ready to integrate?** Copy this prompt into your AI coding assistant and start with answering the "Questions to Answer Before Starting" section for best results!
