# Email Service Deployment Guide

## ✅ What's Been Implemented

Your waitlist email service is now ready for production. This includes:

### 1. **Email Service** (`app/services/email.py`)
- Resend API integration with `httpx`
- Two email templates:
  - **Welcome Email**: Premium design with purple/gold branding, benefits list, CTA to visit soulconnect.health
  - **Admin Notification**: Professional format with signup details (email, name, struggle, date, time, IP, user-agent)
- Graceful error handling (email failures logged but never break signup)
- Singleton pattern for reusable service instance

### 2. **Waitlist Endpoint** (`app/routes/early_access.py` - POST `/api/early-access/`)
- **Duplicate Handling**: Returns success message "You're already on the SoulConnect waitlist 💜" instead of error
- **Email Sending**: After successful database insert, sends:
  - Welcome email to user
  - Admin notification to community@soulconnect.health
- **Failure Safety**: If emails fail, they're logged but don't break the signup process
- **Rate Limiting**: Existing 5 attempts per IP per 10 minutes still enforced
- **Input Validation**: Email normalization, name truncation, struggle validation

### 3. **Environment Configuration**
Updated `.env` template with new variables:
```
RESEND_API_KEY=your_resend_api_key_here
FROM_EMAIL=community@soulconnect.health
ADMIN_EMAIL=community@soulconnect.health
```

### 4. **Code Committed**
- Commit: `2227f61` — "Add Resend email service for waitlist signup notifications"
- Files: `app/services/email.py`, `app/routes/early_access.py`
- Branch: `main` ✅ Pushed to GitHub

---

## 🚀 Production Deployment Steps

### Step 1: Revoke the Exposed API Key
**CRITICAL SECURITY ISSUE**: The Resend API key was shared in plain text during development.

1. Go to [Resend Dashboard](https://resend.com/dashboard)
2. Navigate to **API Keys** section
3. Find and **revoke** any exposed API keys
4. Generate a **new API key**

### Step 2: Update Railway Environment Variables

1. Log in to [Railway Dashboard](https://railway.app)
2. Open your **soulconnect-backend-production** project
3. Go to **Variables** tab
4. Add/update these variables:
   ```
   RESEND_API_KEY=<your_new_api_key_from_step_1>
   FROM_EMAIL=community@soulconnect.health
   ADMIN_EMAIL=community@soulconnect.health
   ```

5. **Save changes** — Railway will automatically redeploy with new environment variables

### Step 3: Verify Deployment

Once Railway redeploys (~2-3 minutes), test the endpoint:

**Test Sign-up with Welcome Email:**
```bash
curl -X POST http://localhost:8000/api/early-access/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "name": "Test User",
    "struggle": "Anxiety"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "You're on the list! 💜"
}
```

**Check Logs:**
- Go to Railway → **Logs** tab
- Look for: `"Welcome email sent to test@example.com"`
- If errors, you'll see: `"Failed to send welcome email..."`

### Step 4: Verify Email Reception

1. **Welcome email** should arrive in the test inbox within 30 seconds
2. **Admin notification** should arrive in `community@soulconnect.health` inbox
3. Check both for:
   - Purple gradient header
   - Gold accent colors
   - Properly formatted content
   - "Visit SoulConnect" CTA button

---

## 📊 Testing Checklist

### ✅ Happy Path (New User)
- [ ] Fill out waitlist form with email, name, struggle
- [ ] Receive "You're on the list! 💜" message
- [ ] Welcome email arrives with premium design
- [ ] Admin notification includes all details
- [ ] Database has new row in `early_access_submissions`

### ✅ Duplicate Handling
- [ ] Submit same email twice
- [ ] Second attempt returns "You're already on the SoulConnect waitlist 💜"
- [ ] No duplicate DB row created
- [ ] No duplicate emails sent

### ✅ Rate Limiting
- [ ] Submit 5 requests from same IP in 10 minutes
- [ ] 6th request returns 429 Too Many Requests
- [ ] After 10 minutes, can submit again

### ✅ Email Resilience
- [ ] Temporarily disable `RESEND_API_KEY` in Railway
- [ ] Submit waitlist form
- [ ] Still get "You're on the list! 💜" (signup succeeds)
- [ ] Check logs: `"Failed to send welcome email..."` (logged, not fatal)
- [ ] Re-enable `RESEND_API_KEY`

### ✅ Data Validation
- [ ] Invalid email rejected
- [ ] Empty name defaults gracefully
- [ ] Invalid struggle category → "Other"
- [ ] Name > 200 chars truncated
- [ ] Email normalized (lowercase, trimmed)

---

## 📧 Email Template Details

### Welcome Email
- **From**: `SoulConnect <community@soulconnect.health>`
- **Subject**: `💜 Welcome to the SoulConnect Waitlist`
- **Design Elements**:
  - Purple gradient header (#7C3AED → #8B5CF6)
  - Personalized greeting with user's name
  - Mission statement: "No one should have to go through life's challenges alone"
  - 3 key benefits with checkmarks
  - Gold accent color (#EAB308)
  - "Visit SoulConnect" CTA button
  - Footer with privacy/terms links
  - Responsive for mobile (600px max-width)

### Admin Notification
- **From**: `SoulConnect <community@soulconnect.health>`
- **To**: `community@soulconnect.health`
- **Subject**: `🎉 New Waitlist Signup`
- **Content**:
  - Email address
  - User name (if provided)
  - Primary struggle category
  - Signup date & time (UTC)
  - IP address (with Cloudflare Email Routing support)
  - User-Agent string

---

## 🔧 Troubleshooting

### Emails Not Sending

**Check 1: API Key Configured**
```bash
# On Railway, in Logs:
# Should see: "Welcome email sent to..."
# If not: "RESEND_API_KEY not configured - emails will not be sent"
```

**Check 2: Resend Account Status**
- Verify key is active in [Resend Dashboard](https://resend.com/dashboard)
- Check Resend usage limits
- Verify domain verification (if using custom domain)

**Check 3: Error Logs**
- Go to Railway → **Logs**
- Search for "Failed to send" or "Exception sending"
- Common errors:
  - `status_code 401` → Invalid/expired API key
  - `status_code 422` → Invalid email address format
  - `timeout` → Network connectivity issue

### Database Insert Succeeds But No Email

This is **expected behavior** — emails fail gracefully. Check logs:
```
Failed to send welcome email to test@example.com: ...
```

Signup still succeeds, just without email notification. Fix the email issue and manually resend via:
```bash
# (Implement manual resend endpoint if needed)
```

### Duplicate Detection Not Working

Ensure database index on `email` column exists:
```sql
SELECT * FROM information_schema.statistics 
WHERE table_name = 'early_access_submissions';
```

Should show index on `email` column.

---

## 📝 Production Checklist

- [ ] Revoked old Resend API key
- [ ] Generated new Resend API key
- [ ] Updated `RESEND_API_KEY` in Railway
- [ ] Set `FROM_EMAIL` to `community@soulconnect.health`
- [ ] Set `ADMIN_EMAIL` to `community@soulconnect.health`
- [ ] Railway redeployed successfully
- [ ] Tested signup flow end-to-end
- [ ] Verified welcome email arrives
- [ ] Verified admin notification arrives
- [ ] Tested duplicate handling
- [ ] Tested rate limiting
- [ ] Checked logs for any errors
- [ ] Verified mobile email rendering
- [ ] Documented in team wiki/Slack

---

## 🔐 Security Reminders

1. **Never commit `.env` files** — API keys stay local only ✅
2. **Revoke exposed keys immediately** — Done via Railway UI
3. **Use environment variables** — All secrets in Railway, not code
4. **Monitor Resend API usage** — Check dashboard for suspicious activity
5. **Log email failures** — For debugging but don't expose keys in logs ✅

---

## 📈 Monitoring

### Key Metrics to Track
- Waitlist signups per day (via `/api/early-access/count`)
- Email send success rate (via Railway logs)
- Email delivery failures (via Resend dashboard)
- Rate limit hits (via Railway logs)

### Admin Endpoints
```bash
# Get total waitlist count
curl https://soulconnect-backend-production.up.railway.app/api/early-access/count

# Get all signups (requires X-Admin-Key header)
curl -H "X-Admin-Key: $ADMIN_SECRET" \
  https://soulconnect-backend-production.up.railway.app/api/early-access/admin

# Debug endpoint (public, for testing)
curl https://soulconnect-backend-production.up.railway.app/api/early-access/debug
```

---

## 🎯 Next Steps (Optional Enhancements)

1. **Email Preferences**: Add opt-out/unsubscribe links
2. **Send Logs**: Store email send events in database for retry capability
3. **A/B Testing**: Create alternate welcome email templates
4. **Scheduled Emails**: Send email sequence (day 1, day 7, day 30)
5. **Analytics**: Track email open rates via Resend webhooks

---

## 📞 Support

If emails aren't working after deployment:

1. Check Railway logs for errors
2. Verify API key in Resend dashboard
3. Test with `curl` locally against `/api/early-access/`
4. Review email service code: `app/services/email.py`
5. Check Resend dashboard for bounced emails

---

**Status**: ✅ Ready for Production  
**Last Updated**: 2026-07-04  
**Commit**: 2227f61  
**Branch**: main
