# SoulConnect Email - Quick Start Guide

Everything you need to get the premium welcome email running in minutes.

## ⚡ 60-Second Setup

### 1. Install Dependencies

```bash
npm install react-email resend
```

### 2. Get Your Resend API Key

1. Go to https://resend.com
2. Create account (free tier: 100 emails/day)
3. Add domain: `soulconnect.health`
4. Copy API key

### 3. Add Environment Variable

```bash
# .env.production
RESEND_API_KEY=re_xxxxx
```

### 4. Copy Email Components

```bash
cp -r emails/ your-project/
```

### 5. Send Your First Email

```typescript
import { Resend } from 'resend';
import { WelcomeEmail } from '@/emails/WelcomeEmail';

const resend = new Resend(process.env.RESEND_API_KEY);

await resend.emails.send({
  from: 'SoulConnect <community@soulconnect.health>',
  to: 'user@example.com',
  subject: '💜 Welcome to SoulConnect, Amol',
  react: <WelcomeEmail userEmail="user@example.com" userName="Amol Londhe" />,
});
```

**Done!** 🎉

---

## 📁 File Structure

```
emails/
├── WelcomeEmail.tsx              # Main component ⭐
├── components/
│   ├── EmailHeader.tsx           # Logo + tagline
│   ├── EmailFooter.tsx           # Links + disclaimer
│   ├── FeatureCard.tsx           # Feature cards
│   ├── MomentOfCalm.tsx          # Breathing exercise
│   └── Divider.tsx               # Divider component
├── helpers/
│   └── getFirstName.ts           # Name parser
├── types.ts                      # TypeScript types
├── index.ts                      # Exports
├── package.json.example          # Dependencies
├── README.md                     # Full docs
├── SETUP.md                      # Installation
├── INTEGRATION_GUIDE.md          # Backend integration
├── QUICK_START.md                # This file
└── example-usage.tsx             # Code examples
```

---

## 🎨 What It Includes

✅ Premium, minimal design matching Apple/Notion/Stripe
✅ Deep purple header with gold divider
✅ Personalized greeting with user's first name
✅ 4 feature cards (Connect, Heal, Professional Support, Grow)
✅ "We're building for you" checklist section
✅ Large purple CTA button
✅ "Moment of Calm" breathing exercise
✅ Warm, genuine closing message
✅ Professional footer with links
✅ Fully responsive (mobile + desktop)
✅ Dark mode support
✅ Outlook compatible (VML fallback)
✅ All major email clients supported

---

## 🚀 Common Tasks

### Send Welcome Email

```typescript
import { Resend } from 'resend';
import { WelcomeEmail } from '@/emails/WelcomeEmail';

const resend = new Resend(process.env.RESEND_API_KEY);

await resend.emails.send({
  from: 'SoulConnect <community@soulconnect.health>',
  to: 'user@example.com',
  subject: '💜 Welcome to SoulConnect, Amol',
  react: <WelcomeEmail userEmail="user@example.com" userName="Amol Londhe" />,
});
```

### Preview Locally

```bash
npx react-email preview emails/WelcomeEmail.tsx
```

Opens http://localhost:3000 with live preview and dark mode toggle.

### Extract Name from Full Name

```typescript
import { getFirstName } from '@/emails/helpers/getFirstName';

getFirstName('Amol Londhe')        // 'Amol'
getFirstName(' John Smith ')       // 'John'
getFirstName(undefined)            // 'there'
```

### Render as HTML String

```typescript
import { render } from '@react-email/render';
import { WelcomeEmail } from '@/emails/WelcomeEmail';

const html = render(<WelcomeEmail userEmail="user@example.com" userName="Amol Londhe" />);
```

### Send via Python Backend

```python
from resend import Resend

client = Resend(api_key="your-resend-key")

response = client.emails.send({
    "from": "SoulConnect <community@soulconnect.health>",
    "to": "user@example.com",
    "subject": "💜 Welcome to SoulConnect",
    "html": "<html>...</html>"  # Pre-rendered HTML
})
```

### Customize Colors

Edit these values in component files:

```typescript
// Purple accent
color: '#7C3AED'

// Gold accent  
color: '#EAB308'

// Dark background
backgroundColor: '#3e1c52'
```

---

## 🧪 Testing Checklist

- [ ] Email sends successfully
- [ ] Gmail receives and renders correctly
- [ ] Outlook receives and renders correctly
- [ ] Apple Mail looks good
- [ ] Mobile view is responsive
- [ ] Dark mode renders correctly
- [ ] Button is clickable
- [ ] Links work
- [ ] Name personalization works
- [ ] Emoji render correctly
- [ ] Typography is readable
- [ ] No images fail to load (no external images used)

---

## 🔧 Troubleshooting

### Email not sending?

1. Check API key is set: `console.log(process.env.RESEND_API_KEY)`
2. Verify domain is configured in Resend dashboard
3. Check email address is valid
4. Check Resend quota (free: 100/day)

### Styling looks wrong?

1. Check email client (some strip CSS)
2. Test in Litmus or Email on Acid
3. Try Gmail or Apple Mail
4. Check dark mode setting

### Component import error?

1. Verify file paths are correct
2. Check tsconfig allows `.tsx`
3. Install `react-email` package
4. Clear node_modules: `rm -rf node_modules && npm install`

### Mobile view broken?

1. Test at actual width (393px for iPhone 15 Pro)
2. Check container max-width is 640px
3. Verify responsive table widths
4. Test in actual mobile email app

---

## 📊 Email Specifications

| Aspect | Value |
|--------|-------|
| **Max Width** | 640px |
| **Mobile Width** | 375-393px |
| **Design** | Mobile-first responsive |
| **Fonts** | System fonts (no web fonts) |
| **Colors** | Purple (#7C3AED) + Gold (#EAB308) |
| **Images** | None (all emojis) |
| **Size (uncompressed)** | ~25KB |
| **Size (gzip)** | ~8KB |
| **Support** | 99%+ email clients |

---

## 📧 Integration Points

### 1. User Signs Up

```
Frontend Form Submission
  ↓
API Call (POST /api/early-access)
  ↓
Backend Saves to Database
  ↓
Backend Sends Welcome Email
  ↓
User Receives in Inbox
```

### 2. Email Service Options

**Option A: Use Resend Directly** (Simplest)
- Send from Next.js API route
- Resend handles rendering

**Option B: Render in Python**
- Render component to HTML in Node.js
- Send HTML via Resend from Python

**Option C: Next.js API Route**
- FastAPI calls Next.js API
- Next.js renders and sends
- Separation of concerns

---

## 🎯 Next Steps

1. **Install dependencies**
   ```bash
   npm install react-email resend
   ```

2. **Copy email components**
   ```bash
   cp -r emails/ your-project/
   ```

3. **Add API key**
   - Create `.env.local`
   - Add `RESEND_API_KEY=...`

4. **Test locally**
   ```bash
   npx react-email preview emails/WelcomeEmail.tsx
   ```

5. **Send test email**
   ```bash
   npm run test
   ```

6. **Deploy**
   - Push to main branch
   - Railway auto-deploys
   - Verify in production

7. **Monitor**
   - Check Resend dashboard
   - Monitor email delivery
   - Track open rates

---

## 📚 Full Documentation

- **README.md** — Complete component documentation
- **SETUP.md** — Detailed installation guide
- **INTEGRATION_GUIDE.md** — Backend integration options
- **types.ts** — TypeScript type definitions
- **example-usage.tsx** — Code examples

---

## 💬 Need Help?

### React Email Issues
- https://react.email/docs
- https://github.com/resendlabs/react-email

### Resend Issues
- https://resend.com/docs
- https://resend.com/support

### SoulConnect Questions
- Contact engineering team

---

## ✨ Features Highlight

### Design Excellence

- Premium, minimal aesthetic
- Warm purple + gold palette
- Excellent spacing and typography
- Professional hierarchy
- No clutter or distractions

### User Experience

- Personalized greeting
- Warm, hopeful tone
- Clear call-to-action
- Breathing exercise for calm
- Trust-building messaging

### Technical Excellence

- Fully responsive
- Dark mode support
- Email-safe HTML
- Outlook compatible
- Production-ready code

### Developer Experience

- Type-safe TypeScript
- Reusable components
- Clean file organization
- Comprehensive documentation
- Easy integration

---

**Ready to get started?** Follow the 60-second setup above! 🚀