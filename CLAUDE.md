# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

SoulConnect is a peer-support / mental-wellness web app for India — users pick a specific life struggle (breakup, anxiety, grief, one of ~25 categories) and get matched with peers, guided-healing journeys, support circles, and verified healers.

The **actual application lives in `frontend/`** (its own git repo, remote `Amol3011-zap/soulconnect-frontend`). The repo root is a working area holding brand assets, marketing images, SEO audit reports (`*.html`, `SEO_*.md`), and scratch folders (`algo/`, `files/`, `src/`, `post login/`) that are NOT part of the shipped app. When doing app work, treat `frontend/` as the project root.

## Commands (run from `frontend/`)

```bash
npm run dev       # Vite dev server on :5173, proxies /api -> http://localhost:8000
npm run build     # vite build THEN node scripts/inject-static.js (see below)
npm run preview   # serve the production build locally
```

There is **no test runner, linter, or typecheck configured** — do not invent `npm test`/`npm run lint`. Verify changes by running `npm run dev` and checking in-browser.

The build is two steps: `scripts/inject-static.js` runs after `vite build` and replaces the empty `<div id="root">` in `dist/index.html` with a hand-written static HTML landing page so crawlers/link-preview bots see real content without JS. **If you change landing-page copy, stats, or the 25 problem categories, update `scripts/inject-static.js` too** or the crawler view drifts from the app.

## Deployment

- **Frontend → Vercel.** `frontend/.env.production` points `VITE_API_URL` at the Railway backend. `vercel.json` owns SPA rewrites, cache headers, a strict CSP, and security headers.
- **Backend → Railway** (`soulconnect-backend-production.up.railway.app`), separate repo, not in this tree. The frontend only talks to it through `src/services/api.js`.
- **Maintenance mode is currently ON via `vercel.json`**: `/login`, `/signup`, `/register`, `/dashboard*` are redirected to `/maintenance`. Auth is gated in-app by `VITE_LAUNCH_READY`. Be aware the live site does not expose login even though the code paths exist.
- Git flow uses two branches: `dev` (working) and `main`. Capacitor (`capacitor.config.ts`, appId `com.soulconnect.app`) wraps `dist/` for iOS/Android — web is the source of truth.

## Architecture

**Stack:** React 18 + Vite 5, React Router v6, Zustand (state), axios (HTTP), `motion/react` (animation), Lucide (icons), Tailwind is installed but see styling rule below.

**Routing & app shell — all in `src/App.jsx`.** Three concepts gate what renders:
- `VITE_LAUNCH_READY` (`LAUNCH_READY`): when false, only public/marketing + auth routes exist; everything else redirects home. This is the master "is the product live" switch.
- **Role split:** `role === 'healer'` users get only `HealerDashboard`; everyone else gets the member app.
- **Three layout tiers:** (1) marketing/legal pages render bare, (2) `DASHBOARD_PATHS` render inside `<DashboardLayout>` (persistent sidebar + bottom nav), (3) full-screen experiences (`/chat`, `/chat/:id`, `/groups`, `/tiny-wins`) render with no chrome. `App.jsx` computes `isDashboard`/`isFullScreen` from the pathname to decide nav visibility. When adding a route, put it in the correct tier and update `DASHBOARD_PATHS` if it needs the sidebar.
- Most pages are `lazy()`-loaded; only Landing, Login, HealerDashboard, SafetyOnboarding are eager (critical path).

**State — `src/store/*` (Zustand + `persist` middleware).** Each domain is its own store (`auth`, `theme`, `weather`, `dashboard`, `stories`, `challenges`, `tinyWins`). `auth` persists to localStorage key `auth-store` and holds `{ user, token, role }`; it is the single source of truth for login. Read it outside React with `useAuthStore.getState()`.

**API layer — `src/services/api.js`.** One axios instance, base URL from `VITE_API_URL` (`/api` in dev via Vite proxy). A request interceptor injects `Authorization: Bearer <token>` from the auth store. Endpoints are grouped into exported objects (`authAPI`, `userAPI`, `matchAPI`, `chatAPI`, `challengesAPI`, `onboardingAPI`, etc.). Newer endpoints (`challengesAPI`, `dashboardAPI`) catch errors and re-throw a normalized `{ type, message }` — follow that pattern for new calls rather than leaking raw axios errors. Auth uses **phone + password**, not email.

**Feature flags — `src/config/FEATURE_FLAGS.js`.** MVP features are on; v2 features (Reflection/journaling, voice journal, letters) are `false` and must NOT be surfaced in the UI. To enable one: flip the flag, add the route in `App.jsx`, add the nav item in `DashboardLayout.jsx`.

**Content data — `src/data/*`** holds large static datasets (`storiesDB.js`, `tinyWinsDatabase.js`, `articles.js`). `vite.config.js` manually chunks `storiesDB.js` and heavy legacy pages so they don't bloat the auth bundle. If you add a large data file, consider a manualChunk entry.

**SEO is first-class.** `src/lib/metadata.js` maps every public route to title/description/canonical/OG/keywords; `<MetaHead>` applies it per route. Combined with the static-shell injection, SEO changes usually touch `metadata.js` + `MetaHead.jsx` + possibly `inject-static.js`.

## Styling rules (strict — see `frontend/docs/DESIGN_SYSTEM.md`)

This is the most important convention in the codebase. The product must feel like a premium native wellness app (Calm/Headspace tier), never a dashboard.

- **Do NOT style with Tailwind utility classes** even though Tailwind is installed. UI is built with **inline styles + CSS variables** (`var(--bg)`, `var(--text)`) using the design tokens. Tailwind is effectively limited to a few layout helpers.
- **Animation: import from `motion/react` only. Never `framer-motion`.**
- **Icons: Lucide React only**, stroke width 2.
- Cards use glassmorphism (`rgba(34,18,73,0.72)` + `backdrop-filter: blur(24px)`), colored ambient shadows (never black box-shadows), layered gradient backgrounds (never flat), border-radius ≥ 12px on cards. Purple accent palette (`#7C3AED`/`#8B5CF6`/`#A855F7`).
- Mobile-first, target iPhone 15 Pro (393×852), 48px min touch targets, `padding-bottom` for bottom nav.

Read `frontend/docs/DESIGN_SYSTEM.md` before building or restyling any screen — it has the full token list, the "Forbidden" list, and the pre-ship checklist.

## Conventions

- New Zustand store: `create(persist((set) => ({...}), { name: '<key>-store' }))`, one file per domain in `src/store/`.
- New API call: add to the relevant `*API` object in `services/api.js`; for user-facing calls, catch and re-throw `{ type, message }`.
- New page: create in `src/pages/`, `lazy()`-import in `App.jsx`, place in the correct layout tier.
- Pure display components should be `React.memo`; list handlers `useCallback` (perf targets 60fps).
