# 🎨 SOULCONNECT FRONTEND - COMPLETE SETUP GUIDE

## STEP 1: Local Development Setup

### Create React Project

```bash
# Using Vite (faster than Create React App)
npm create vite@latest soulconnect-frontend -- --template react

cd soulconnect-frontend
npm install
```

### Install Dependencies

```bash
npm install \
  react-router-dom \
  axios \
  zustand \
  @tanstack/react-query \
  tailwindcss \
  postcss \
  autoprefixer

# Dev dependencies
npm install -D tailwindcss postcss autoprefixer

# Initialize Tailwind
npx tailwindcss init -p
```

### Directory Structure

```
soulconnect-frontend/
├── src/
│   ├── pages/
│   │   ├── Landing.jsx
│   │   ├── Signup.jsx
│   │   ├── Matches.jsx
│   │   ├── Chat.jsx
│   │   ├── Healers.jsx
│   │   ├── Meetups.jsx
│   │   ├── Premium.jsx
│   │   └── Account.jsx
│   ├── components/
│   │   ├── Navbar.jsx
│   │   ├── CrisisResources.jsx
│   │   └── (reusable components)
│   ├── services/
│   │   └── api.ts
│   ├── store/
│   │   └── auth.ts
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── public/
│   ├── manifest.json (for PWA)
│   └── service-worker.js
├── .env.example
├── vite.config.js
└── package.json
```

### Tailwind Configuration

```javascript
// tailwind.config.js
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### Create .env.example

```
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=SoulConnect
```

### Create .env (Local Development)

```
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=SoulConnect
```

### Vite Configuration

```javascript
// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '/api'),
      }
    }
  }
})
```

### Test Local Setup

```bash
# Terminal 1: Backend (if not using Railway)
cd soulconnect-backend
python -m uvicorn app.main:app --reload

# Terminal 2: Frontend
cd soulconnect-frontend
npm run dev

# Visit http://localhost:5173
```

---

## STEP 2: PWA Setup (Mobile-Like Experience)

### Create manifest.json

```json
// public/manifest.json
{
  "name": "SoulConnect - Problem-Solver Peer Support",
  "short_name": "SoulConnect",
  "description": "Find someone with your problem. Talk. Heal.",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#7c3aed",
  "orientation": "portrait-primary",
  "scope": "/",
  "icons": [
    {
      "src": "/icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/icon-maskable.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "maskable"
    }
  ]
}
```

### Create Service Worker

```javascript
// public/service-worker.js
const CACHE_NAME = 'soulconnect-v1';

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll([
        '/',
        '/index.html',
        '/manifest.json',
      ]);
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  // Cache-first strategy for static assets
  if (event.request.method === 'GET') {
    event.respondWith(
      caches.match(event.request).then((response) => {
        return response || fetch(event.request).then((response) => {
          const clonedResponse = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, clonedResponse);
          });
          return response;
        });
      })
    );
  }
});

// Handle push notifications
self.addEventListener('push', (event) => {
  const data = event.data.json();
  self.registration.showNotification(data.title, {
    body: data.body,
    icon: '/icon-192.png',
  });
});
```

### Register Service Worker

```javascript
// src/main.jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

// Register service worker
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/service-worker.js').then((reg) => {
    console.log('Service Worker registered');
  }).catch((err) => {
    console.log('Service Worker registration failed:', err);
  });
}

// Request notification permission
if ('Notification' in window && Notification.permission === 'default') {
  Notification.requestPermission();
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

### Add Meta Tags to index.html

```html
<!-- index.html -->
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    
    <!-- PWA Meta Tags -->
    <meta name="theme-color" content="#7c3aed">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <meta name="apple-mobile-web-app-title" content="SoulConnect">
    
    <!-- Manifest -->
    <link rel="manifest" href="/manifest.json">
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    
    <title>SoulConnect - Find Your People</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

---

## STEP 3: Build for Production

```bash
npm run build

# This creates a 'dist' folder ready to deploy
```

---

## STEP 4: Vercel Deployment

### Connect to GitHub

1. Push frontend code to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/soulconnect-frontend.git
   git push -u origin main
   ```

2. Go to https://vercel.com
3. Sign up / Login with GitHub
4. Click "New Project"
5. Select your GitHub repo
6. Click "Import"

### Configure Environment Variables

In Vercel Dashboard:
1. Go to Settings → Environment Variables
2. Add:
   ```
   VITE_API_URL=https://your-api.railway.app/api
   VITE_APP_NAME=SoulConnect
   ```

3. Click "Deploy"

### Custom Domain (Optional)

1. In Vercel → Settings → Domains
2. Add custom domain (e.g., soulconnect.com)
3. Follow DNS setup instructions
4. Wait 15-30 minutes for propagation

---

## STEP 5: Configuration Files

### package.json Scripts

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint src"
  }
}
```

### Vite Build Optimization

```javascript
// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor': ['react', 'react-dom'],
        }
      }
    },
    // Minify
    minify: 'terser',
    // Source maps (disable in production for security)
    sourcemap: false,
  }
})
```

---

## STEP 6: Performance Optimization

### Image Optimization

```jsx
// Use optimized images
import { lazy, Suspense } from 'react';

// Lazy load images
const LazyImage = ({ src, alt }) => (
  <img src={src} alt={alt} loading="lazy" />
);
```

### Code Splitting

```jsx
// Split routes for faster loading
import { lazy, Suspense } from 'react';

const Landing = lazy(() => import('./pages/Landing'));
const Signup = lazy(() => import('./pages/Signup'));
const Matches = lazy(() => import('./pages/Matches'));

// In routes
<Suspense fallback={<Loading />}>
  <Route path="/" element={<Landing />} />
</Suspense>
```

---

## STEP 7: Testing

### Setup Vitest

```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom
```

### Create test file

```javascript
// src/__tests__/App.test.jsx
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from '../App';

describe('App', () => {
  it('renders landing page', () => {
    render(<App />);
    expect(screen.getByText(/SoulConnect/i)).toBeInTheDocument();
  });
});
```

### Run tests

```bash
npm run test
```

---

## STEP 8: Monitoring & Analytics

### Add Sentry for Error Tracking

```bash
npm install @sentry/react @sentry/tracing
```

```javascript
// src/main.jsx
import * as Sentry from "@sentry/react";
import { BrowserTracing } from "@sentry/tracing";

Sentry.init({
  dsn: "your-sentry-dsn",
  integrations: [
    new BrowserTracing(),
  ],
  tracesSampleRate: 1.0,
});

// Wrap App
const SentryApp = Sentry.withProfiler(App);
```

### Add Analytics (Plausible or Simple Events)

```javascript
// services/analytics.js
export const trackEvent = (event, properties) => {
  if (window.plausible) {
    window.plausible(event, { props: properties });
  }
};
```

---

## Production Checklist

- [ ] All API URLs use production backend
- [ ] Environment variables configured in Vercel
- [ ] Remove console.logs from code
- [ ] Test all pages on mobile
- [ ] Test all buttons/forms
- [ ] Check performance (Lighthouse score >80)
- [ ] Test PWA (add to home screen on mobile)
- [ ] Test offline functionality
- [ ] Enable HTTPS (auto on Vercel)
- [ ] Monitor errors via Sentry

---

## Troubleshooting

### CORS Error

**Error:** `Access to XMLHttpRequest blocked by CORS policy`

**Solution:** Ensure VITE_API_URL in Vercel environment variables matches backend ALLOWED_ORIGINS

### Blank Page

**Error:** Frontend loads but shows nothing

**Solution:**
1. Check browser console for errors
2. Verify API_URL is correct
3. Check if backend is running
4. Clear browser cache

### Slow Load

**Error:** App takes >3 seconds to load

**Solution:**
1. Check network tab in DevTools
2. Enable code splitting
3. Optimize images
4. Use CDN for assets

---

## Next Steps

1. ✅ Frontend deployed
2. ✅ Backend deployed (from BACKEND_SETUP_GUIDE.md)
3. 🔄 Set up healer onboarding
4. 🔄 Launch to beta users
