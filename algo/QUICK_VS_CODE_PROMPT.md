# QUICK VS CODE AI PROMPT - Copy & Paste This

Paste this into GitHub Copilot Chat, Claude VS Code extension, or any AI assistant. It's a condensed version that gets straight to the point.

---

## SHORT VERSION (2 MIN READ)

```
PROJECT CONTEXT:
- Building: SoulConnect (peer-to-peer support platform)
- Adding: Soul Journey progress tracking module
- Tech: React frontend + FastAPI backend
- Database: PostgreSQL with SQLAlchemy

FILES I HAVE:
1. soul_journey_tracker.py - Core algorithm (progress, wellness, stages)
2. soul_journey_api.py - FastAPI endpoints 
3. SoulJourneyDashboard.jsx - React component

MY EXISTING SETUP:
- FastAPI structure: app/api/routes/*, app/models/*, app/schemas/*
- React structure: src/components/*, src/services/*, src/pages/*
- Database: PostgreSQL with SQLAlchemy ORM
- Auth: [JWT / Session-based - choose one]
- State: [Redux / Context API / Zustand - choose one]

TASK:
Integrate Soul Journey into my SoulConnect codebase. Generate:

1. DATABASE LAYER:
   - Create models/journey.py with Activity & UserJourney models
   - Link to existing User table
   - Include (user_id, activity_type, intensity, date, notes) fields
   - Add indexes on (user_id, date)

2. BACKEND LAYER:
   - Create routes/journey.py with endpoints:
     POST /api/v1/journey/{user_id}/activity
     GET /api/v1/journey/{user_id}/progress
     GET /api/v1/journey/{user_id}/activities
     GET /api/v1/journey/{user_id}/stats
   - Add @require_auth middleware
   - Integrate soul_journey_tracker.py algorithm
   - Use existing database session (app.db)

3. FRONTEND LAYER:
   - Create components/SoulJourneyDashboard/index.jsx
   - Create services/journeyApi.js (with auth headers)
   - Add route /dashboard/journey to App.jsx
   - Update Header to show wellness score
   - Add "Log Activity" button to chat UI

4. INTEGRATION:
   - Use existing axios instance (not hardcoded API URLs)
   - Use existing auth token from [your auth store]
   - Match existing color scheme/Tailwind theme
   - Use existing toast/notification library
   - Follow existing error handling patterns

CONSTRAINTS:
- No new database connections
- No duplicate state management
- Reuse existing auth mechanism
- Match existing code style
- Include error handling for all API calls
- Add loading states in UI components

DELIVERABLES:
- Migrations (alembic/)
- Python files (models, routes, services)
- React files (components, services, updated routing)
- Test examples for both backend and frontend
```

---

## EVEN SHORTER (30 SEC VERSION)

If the AI assistant asks "What do you want me to do?" paste this:

```
I need to integrate Soul Journey tracking into my SoulConnect platform. 
I have the algorithm (Python) and React component ready.

Generate integration code for:
1. PostgreSQL tables (Activity, UserJourney) - link to Users
2. FastAPI endpoints (/api/v1/journey/*) with auth
3. React components/services for the dashboard
4. Database migration file (Alembic)

Use my existing:
- Database session: app.db
- Auth: [existing auth method]
- Axios: [existing axios config]
- Tailwind: [your Tailwind setup]

Return one file at a time, following my codebase patterns.
```

---

## TARGETED PROMPTS FOR DIFFERENT SCENARIOS

### If using GitHub Copilot:
```
@workspace

I'm integrating a progress tracking system into /src and /backend.

Files available:
- soul_journey_tracker.py (algorithm)
- soul_journey_api.py (FastAPI routes)
- SoulJourneyDashboard.jsx (React UI)

Generate /backend/app/models/journey.py following my existing model patterns.
Then generate /backend/app/routes/journey.py with 4 endpoints.
Then generate /src/components/SoulJourneyDashboard/index.jsx adapted to my app.

Use existing:
- Database session
- Auth patterns
- Error handling
- Styling (Tailwind from package.json)
```

### If using Claude VS Code Extension:
```
I'm adding a Soul Journey tracking module to my SoulConnect app.

My stack:
- Backend: FastAPI + PostgreSQL + SQLAlchemy
- Frontend: React + Tailwind + [Redux/Context]
- Auth: [JWT tokens / Sessions]

I have complete algorithm & component code ready.

Help me:
1. Create database models (Activity, UserJourney)
2. Create 4 API endpoints with auth
3. Create React service + component
4. Add route to existing App.jsx
5. Update existing Header component
6. Create Alembic migration

Follow my existing code patterns. One file at a time.
```

### If using Cursor or other AI IDE:
```
/integrate

Project: SoulConnect emotional support platform
Feature: Soul Journey progress tracking

Available code:
- Backend algorithm: soul_journey_tracker.py
- API template: soul_journey_api.py  
- React component: SoulJourneyDashboard.jsx

Integration checklist:
- [ ] Add to models/ (link Activity to User)
- [ ] Add to routes/ (4 endpoints + auth)
- [ ] Add services/journeyApi.js
- [ ] Add components/SoulJourneyDashboard
- [ ] Update src/App.jsx routing
- [ ] Update src/components/Header.jsx
- [ ] Create Alembic migration
- [ ] Add error handling & loading states
- [ ] Test with existing auth

Start with models/journey.py using my SQLAlchemy patterns.
```

---

## FOLLOW-UP PROMPTS (Ask After Initial Integration)

```
1. "Add auto-logging: when a user completes a chat session, 
   automatically log a CHAT_SESSION activity with intensity modal"

2. "Create a migration file (Alembic) for the journey tables"

3. "Add unit tests for journey_tracker.py core algorithm"

4. "Integrate wellness score into existing user nav header"

5. "Add 'Log Activity' quick-action button to chat completion flow"

6. "Create journeySlice.js for Redux to sync progress with app state"

7. "Add performance optimization: cache progress data with 30s TTL"

8. "Create API response/error standardization matching existing patterns"

9. "Generate example curl commands for testing all endpoints"

10. "Add data export: generate PDF report of journey progress"
```

---

## CONTEXT YOU MIGHT NEED TO PROVIDE

Before pasting the prompt, answer these in your head:

- **Database**: PostgreSQL? MySQL? 
- **Auth type**: JWT? Session? OAuth?
- **State management**: Redux? Context API? Zustand?
- **HTTP client**: axios? fetch? Apollo?
- **Styling**: Tailwind v3? v4? Custom config?
- **Toast library**: React-Toastify? Notistack? Custom?
- **Project structure**: Monorepo? Separate repos?

---

## WHAT THE AI WILL GENERATE

✅ Database models with relationships
✅ FastAPI routes with dependency injection
✅ React hooks and service files
✅ Error handling and validation
✅ Loading and error states
✅ Auth header integration
✅ Type hints (Python) and PropTypes (React)
✅ Comments and docstrings
✅ Database migration file

---

## RECOMMENDED WORKFLOW

1. **Paste prompt** → AI generates database models
2. **Review & ask** → "Does this match my SQLAlchemy patterns?"
3. **Iterate** → Ask for routes, then services, then components
4. **Test** → Ask for "curl commands to test endpoints"
5. **Deploy** → Ask for "Alembic migration for these tables"

This is faster than pasting huge context at once!

---

## ONE-LINER QUICK START

If you just want to get started NOW:

```
Help me integrate soul_journey_tracker.py (algorithm), soul_journey_api.py 
(FastAPI routes), and SoulJourneyDashboard.jsx (React component) into my 
SoulConnect app using existing PostgreSQL, auth, and Redux. One file at a time.
```

That's it! The AI will ask clarifying questions. Answer them and you're golden.

---

## VS CODE KEYBOARD SHORTCUTS

- **macOS**: `Cmd + Shift + P` → search "Copilot Chat" or "Claude"
- **Windows/Linux**: `Ctrl + Shift + P` → search "Copilot Chat" or "Claude"
- **Alternative**: Install extension, then `Cmd/Ctrl + L` to open chat

---

Ready? Open VS Code and let's go! 🚀
